# 2026-10-05 (Pomodoro Timer)

Projeto finalizado hoje: **Pomodoro Timer**.

## Pomodoro Timer

Arquivo: `pomodoro-timer/pomodoro_timer.py`

Primeiro projeto do repositório com interface gráfica (Tkinter) — todos os anteriores eram CLI reaproveitando cores ANSI.

### O que o código faz

**Funções puras** (sem depender da janela, testáveis isoladamente):

| Função | O que faz |
|---|---|
| `format_time(seconds)` | Formata segundos como string `"MM:SS"` com zero-padding. |
| `next_phase(current_phase, completed_focus_sessions, cycles_before_long_break)` | Decide a próxima fase: depois de "Foco" vai para "Pausa longa" quando o nº de sessões de foco completadas é múltiplo de `cycles_before_long_break`, senão para "Pausa curta"; depois de qualquer pausa, sempre volta para "Foco". |
| `phase_duration_seconds(phase, durations)` | Converte a duração (minutos) de uma fase para segundos. |
| `parse_minutes(raw, field_name)` | Valida e converte o texto de um campo em inteiro dentro de `[MIN_MINUTES, MAX_MINUTES]`, levantando `ValueError` com mensagem clara se inválido. |
| `play_beep()` | Toca um beep (`winsound.Beep`) ao fim de cada fase; não faz nada se `winsound` não existir (ex.: fora do Windows). |

**Classe `PomodoroApp` (Tkinter)**:

| Método | O que faz |
|---|---|
| `_build_widgets()` | Monta os campos de configuração (minutos de cada fase + ciclos até a pausa longa), o label do contador, o label de fase/ciclo e os botões Iniciar/Pausar/Resetar. |
| `_read_settings()` / `_set_settings_enabled()` | Lê e valida os campos de configuração; habilita/desabilita os campos enquanto o timer está rodando. |
| `_on_start_pause()` / `_start()` / `_toggle_pause()` | Lógica dos botões: inicia a thread de contagem, ou alterna entre pausado/rodando via `_running_event`. |
| `_on_reset()` | Sinaliza parada pra thread, descarta a fila e devolve a janela ao estado inicial. |
| `_run_timer(durations, cycles_before_long_break)` | Roda **na thread separada**: conta os segundos (`time.sleep(1)`), nunca toca em widgets — só manda mensagens (`"tick"`, `"phase_start"`, `"phase_complete"`) pela `queue.Queue`. |
| `_process_queue()` / `_handle_message(message)` | Rodam na thread principal via `self.after(...)`: consomem a fila e são o único ponto que de fato atualiza os widgets (contador, cor de fundo, label de fase, beep). |

Constantes de suporte: `DEFAULT_DURATIONS`, `DEFAULT_CYCLES_BEFORE_LONG_BREAK`, `MIN_MINUTES`/`MAX_MINUTES`, `PHASE_COLORS` (cor de fundo por fase — a versão GUI do feedback por cor ANSI dos projetos de terminal) e `POLL_INTERVAL_MS`.

### Por que foi feito assim

- **`queue.Queue` + `self.after(...)` em vez de atualizar widgets direto da thread de contagem.** Tkinter não é thread-safe: só a thread principal (a que roda `mainloop()`) deve tocar nos widgets. A thread de contagem só sabe contar segundos e empilhar mensagens; é a própria janela, rodando no laço principal, que periodicamente esvazia a fila e atualiza a tela. Esse é o padrão recomendado para combinar `threading` com Tkinter sem corromper o estado da UI.
- **`threading.Event` (`_running_event`) em vez de uma flag booleana simples para pausar.** Uma flag comum exigiria um laço de verificação constante (busy-loop) gastando CPU à toa enquanto pausado. Com `Event.wait()`, a thread simplesmente dorme até alguém chamar `.set()` — pausar/continuar vira dar unset/set no evento, sem polling.
- **Funções puras separadas da classe Tkinter.** `format_time`, `next_phase`, `phase_duration_seconds` e `parse_minutes` não dependem de nenhum widget, então podem ser testadas diretamente num `python -c`, sem precisar abrir a janela — igual ao padrão de smoke test já usado nos outros mini-projetos do repositório.
- **`winsound` importado dentro de `try/except ImportError`.** O resto do projeto não depende de Windows especificamente; encapsular o beep assim evita que o programa quebre só por rodar num SO sem esse módulo (o beep simplesmente não toca).
- **Cálculo do "Ciclo X/N" exibido depende se a fase é "Foco" ou uma pausa**, porque `completed_focus_sessions` representa sessões de foco já **concluídas**, não a que está em andamento. Ao iniciar uma sessão de foco ela ainda não foi contada, então o ciclo exibido é `completed % cycles + 1`; já uma pausa se refere à sessão que *acabou de terminar*, então usa `completed % cycles` (ou `cycles`, se for múltiplo exato — a pausa longa).
