"""Pomodoro Timer (GUI).

Ferramenta de gestão de tempo usando a Técnica Pomodoro: alterna entre
sessões de foco e pausas (curtas e, periodicamente, uma pausa longa),
com as durações configuráveis na própria janela.

Conceitos: módulo time, threading, loops e GUI com Tkinter.

A contagem regressiva roda numa thread separada, pra não travar a
interface enquanto espera. Só a thread principal pode tocar nos widgets
do Tkinter, então a thread de contagem nunca atualiza a tela diretamente:
ela só manda mensagens por uma `queue.Queue`, que a própria janela
consome periodicamente via `self.after(...)`.
"""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

try:
    import winsound
except ImportError:  # não-Windows: beep vira um no-op.
    winsound = None

DEFAULT_DURATIONS = {"Foco": 25, "Pausa curta": 5, "Pausa longa": 15}
DEFAULT_CYCLES_BEFORE_LONG_BREAK = 4
MIN_MINUTES, MAX_MINUTES = 1, 120

PHASE_COLORS = {
    "Foco": "#e74c3c",
    "Pausa curta": "#2ecc71",
    "Pausa longa": "#3498db",
}

POLL_INTERVAL_MS = 100


def format_time(seconds):
    """Formata segundos como string 'MM:SS' com zero-padding."""
    minutes, secs = divmod(seconds, 60)
    return f"{minutes:02d}:{secs:02d}"


def next_phase(current_phase, completed_focus_sessions, cycles_before_long_break):
    """Retorna (próxima_fase, completed_focus_sessions_atualizado).

    Depois de "Foco", a próxima fase é "Pausa longa" a cada
    `cycles_before_long_break` sessões de foco completadas, e "Pausa
    curta" nas demais. Depois de qualquer pausa, a próxima é sempre
    "Foco".
    """
    if current_phase == "Foco":
        completed_focus_sessions += 1
        if completed_focus_sessions % cycles_before_long_break == 0:
            return "Pausa longa", completed_focus_sessions
        return "Pausa curta", completed_focus_sessions
    return "Foco", completed_focus_sessions


def phase_duration_seconds(phase, durations):
    """Converte a duração (em minutos) da fase para segundos."""
    return durations[phase] * 60


def parse_minutes(raw, field_name):
    """Valida e converte o texto de um campo em inteiro dentro de [MIN_MINUTES, MAX_MINUTES]."""
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"{field_name}: digite um número inteiro de minutos.")
    if not MIN_MINUTES <= value <= MAX_MINUTES:
        raise ValueError(f"{field_name}: deve estar entre {MIN_MINUTES} e {MAX_MINUTES}.")
    return value


def play_beep():
    """Toca um beep curto ao fim de uma fase. Sem efeito se `winsound` não existir."""
    if winsound is not None:
        winsound.Beep(880, 300)


class PomodoroApp(tk.Tk):
    """Janela principal do Pomodoro Timer."""

    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.resizable(False, False)

        self._stop_event = threading.Event()
        self._running_event = threading.Event()  # set = contando, clear = pausado
        self._queue = queue.Queue()
        self._timer_thread = None
        self._running = False

        self._build_widgets()

    def _build_widgets(self):
        padding = {"padx": 10, "pady": 6}

        settings = ttk.Frame(self)
        settings.grid(row=0, column=0, **padding)

        self._duration_vars = {}
        for row, phase in enumerate(("Foco", "Pausa curta", "Pausa longa")):
            ttk.Label(settings, text=f"{phase} (min):").grid(row=row, column=0, sticky="w")
            var = tk.StringVar(value=str(DEFAULT_DURATIONS[phase]))
            entry = ttk.Entry(settings, textvariable=var, width=6)
            entry.grid(row=row, column=1)
            self._duration_vars[phase] = var

        ttk.Label(settings, text="Ciclos até pausa longa:").grid(row=3, column=0, sticky="w")
        self._cycles_var = tk.StringVar(value=str(DEFAULT_CYCLES_BEFORE_LONG_BREAK))
        ttk.Entry(settings, textvariable=self._cycles_var, width=6).grid(row=3, column=1)
        self._setting_entries = settings

        self._error_label = ttk.Label(self, text="", foreground="#c0392b")
        self._error_label.grid(row=1, column=0, **padding)

        self._phase_label = ttk.Label(self, text="Pronto para começar", font=("Segoe UI", 12, "bold"))
        self._phase_label.grid(row=2, column=0, **padding)

        self._time_label = tk.Label(self, text="00:00", font=("Segoe UI", 40, "bold"), width=6)
        self._time_label.grid(row=3, column=0, **padding)

        buttons = ttk.Frame(self)
        buttons.grid(row=4, column=0, **padding)

        self._start_pause_button = ttk.Button(buttons, text="Iniciar", command=self._on_start_pause)
        self._start_pause_button.grid(row=0, column=0, padx=5)

        self._reset_button = ttk.Button(buttons, text="Resetar", command=self._on_reset, state="disabled")
        self._reset_button.grid(row=0, column=1, padx=5)

    def _read_settings(self):
        """Lê e valida os campos de configuração. Levanta ValueError se algo for inválido."""
        durations = {
            phase: parse_minutes(var.get(), phase)
            for phase, var in self._duration_vars.items()
        }
        cycles = parse_minutes(self._cycles_var.get(), "Ciclos até pausa longa")
        return durations, cycles

    def _set_settings_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        for child in self._setting_entries.winfo_children():
            child.configure(state=state)

    def _on_start_pause(self):
        if not self._running:
            self._start()
        else:
            self._toggle_pause()

    def _start(self):
        try:
            durations, cycles = self._read_settings()
        except ValueError as exc:
            self._error_label.configure(text=str(exc))
            return

        self._error_label.configure(text="")
        self._set_settings_enabled(False)
        self._reset_button.configure(state="normal")
        self._start_pause_button.configure(text="Pausar")

        self._stop_event.clear()
        self._running_event.set()
        self._running = True

        self._timer_thread = threading.Thread(
            target=self._run_timer, args=(durations, cycles), daemon=True
        )
        self._timer_thread.start()
        self.after(POLL_INTERVAL_MS, self._process_queue)

    def _toggle_pause(self):
        if self._running_event.is_set():
            self._running_event.clear()
            self._start_pause_button.configure(text="Continuar")
        else:
            self._running_event.set()
            self._start_pause_button.configure(text="Pausar")

    def _on_reset(self):
        self._stop_event.set()
        self._running_event.set()  # acorda a thread se ela estiver pausada, pra poder sair do loop
        self._running = False
        self._queue = queue.Queue()  # descarta mensagens pendentes da thread anterior
        self._set_settings_enabled(True)
        self._reset_button.configure(state="disabled")
        self._start_pause_button.configure(text="Iniciar")
        self._phase_label.configure(text="Pronto para começar")
        self._time_label.configure(text="00:00", background=self["background"])

    def _run_timer(self, durations, cycles_before_long_break):
        """Roda na thread de contagem: só lê/decrementa segundos e manda mensagens pela fila."""
        phase = "Foco"
        completed_focus_sessions = 0
        remaining = phase_duration_seconds(phase, durations)
        self._queue.put(("phase_start", phase, completed_focus_sessions, cycles_before_long_break))

        while not self._stop_event.is_set():
            self._running_event.wait()  # bloqueia aqui enquanto pausado, sem busy-loop
            if self._stop_event.is_set():
                break

            self._queue.put(("tick", remaining))
            time.sleep(1)
            remaining -= 1

            if remaining < 0:
                phase, completed_focus_sessions = next_phase(
                    phase, completed_focus_sessions, cycles_before_long_break
                )
                remaining = phase_duration_seconds(phase, durations)
                self._queue.put(
                    ("phase_complete", phase, completed_focus_sessions, cycles_before_long_break)
                )

    def _process_queue(self):
        try:
            while True:
                message = self._queue.get_nowait()
                self._handle_message(message)
        except queue.Empty:
            pass

        if self._running:
            self.after(POLL_INTERVAL_MS, self._process_queue)

    def _handle_message(self, message):
        kind = message[0]
        if kind == "tick":
            remaining = message[1]
            self._time_label.configure(text=format_time(max(remaining, 0)))
        elif kind in ("phase_start", "phase_complete"):
            _, phase, completed_focus_sessions, cycles = message
            if phase == "Foco":
                # completed_focus_sessions ainda não inclui a sessão que está começando agora.
                cycle_display = (completed_focus_sessions % cycles) + 1
            else:
                # a pausa pertence ao ciclo da sessão de foco que ela acabou de completar.
                cycle_display = (completed_focus_sessions % cycles) or cycles
            self._phase_label.configure(text=f"{phase} — Ciclo {cycle_display}/{cycles}")
            self._time_label.configure(background=PHASE_COLORS[phase])
            if kind == "phase_complete":
                play_beep()

    def destroy(self):
        self._stop_event.set()
        self._running_event.set()  # acorda a thread caso esteja pausada, pra ela poder sair
        super().destroy()


if __name__ == "__main__":
    app = PomodoroApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.destroy()
