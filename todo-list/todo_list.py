"""To-Do List (CLI).

Gerenciador de tarefas por linha de comando: adicionar, listar, marcar
como concluída (ou reabrir) e remover tarefas, cada uma com um prazo
opcional. Os dados persistem num arquivo JSON ao lado do script.

Conceitos: listas, dicionários, leitura/escrita de arquivos (JSON) e
módulo datetime (prazos e detecção de tarefas atrasadas).
"""

import datetime
import json
import os

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Arquivo de dados ao lado do script, não importando de onde o programa é chamado.
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

MENU = {
    "1": "Adicionar tarefa",
    "2": "Listar tarefas",
    "3": "Concluir/reabrir tarefa",
    "4": "Remover tarefa",
    "5": "Sair",
}


def load_tasks():
    """Carrega a lista de tarefas do arquivo JSON. Retorna lista vazia se não existir."""
    if not os.path.isfile(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"{RED}Arquivo de tarefas corrompido; começando do zero.{RESET}")
        return []


def save_tasks(tasks):
    """Salva a lista de tarefas no arquivo JSON, formatada e legível."""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)


def ask_text(prompt):
    """Lê um texto do usuário, repetindo a pergunta se vier em branco."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print(f"{RED}Digite alguma coisa — não pode ficar em branco.{RESET}")


def ask_date(prompt):
    """Pergunta uma data no formato AAAA-MM-DD. Enter em branco retorna None (sem prazo)."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return datetime.date.fromisoformat(raw)
        except ValueError:
            print(f"{RED}Use o formato AAAA-MM-DD (ex.: 2026-12-31).{RESET}")


def ask_yes_no(prompt, default=True):
    """Pergunta sim/não. Enter vazio usa o valor padrão (`default`)."""
    suffix = "S/n" if default else "s/N"
    while True:
        raw = input(f"{prompt} ({suffix}): ").strip().lower()
        if raw == "":
            return default
        if raw in ("s", "sim", "y", "yes"):
            return True
        if raw in ("n", "nao", "não", "no"):
            return False
        print(f"{RED}Responda com 's' ou 'n'.{RESET}")


def ask_task_number(tasks, prompt):
    """Pede o número de uma tarefa (1-based) e retorna o índice (0-based) correspondente."""
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
        except ValueError:
            print(f"{RED}Digite um número inteiro.{RESET}")
            continue
        if not 1 <= number <= len(tasks):
            print(f"{RED}Escolha um número entre 1 e {len(tasks)}.{RESET}")
            continue
        return number - 1


def is_overdue(task):
    """Retorna True se a tarefa tem prazo, não está concluída e o prazo já passou."""
    if task["concluida"] or task["prazo"] is None:
        return False
    return datetime.date.fromisoformat(task["prazo"]) < datetime.date.today()


def format_task(index, task):
    """Formata uma linha de exibição pra uma tarefa, com cores de acordo com o status."""
    checkbox = f"{GREEN}[x]{RESET}" if task["concluida"] else "[ ]"
    prazo_text = f" (prazo: {task['prazo']})" if task["prazo"] else ""

    if task["concluida"]:
        texto = f"{GREEN}{task['tarefa']}{RESET}"
    elif is_overdue(task):
        texto = f"{RED}{task['tarefa']}{RESET}{RED} — atrasada!{RESET}"
    else:
        texto = task["tarefa"]

    return f"{CYAN}{index}{RESET}. {checkbox} {texto}{prazo_text}"


def add_task(tasks):
    """Pergunta a descrição e o prazo (opcional) e adiciona uma nova tarefa."""
    tarefa = ask_text("\nTarefa: ")
    prazo = ask_date("Prazo (AAAA-MM-DD, Enter pra deixar sem prazo): ")
    tasks.append({"tarefa": tarefa, "prazo": prazo.isoformat() if prazo else None, "concluida": False})
    print(f"{GREEN}Tarefa adicionada.{RESET}")


def list_tasks(tasks):
    """Imprime todas as tarefas, na ordem em que foram adicionadas."""
    if not tasks:
        print(f"\n{YELLOW}Nenhuma tarefa cadastrada.{RESET}")
        return

    print(f"\n{BOLD}Tarefas ({len(tasks)}):{RESET}")
    for index, task in enumerate(tasks, start=1):
        print(format_task(index, task))


def toggle_task(tasks):
    """Pergunta qual tarefa e alterna seu status entre concluída/pendente. Retorna True se mudou algo."""
    if not tasks:
        print(f"\n{YELLOW}Nenhuma tarefa cadastrada.{RESET}")
        return False

    list_tasks(tasks)
    index = ask_task_number(tasks, "\nNúmero da tarefa a concluir/reabrir: ")
    tasks[index]["concluida"] = not tasks[index]["concluida"]
    status = "concluída" if tasks[index]["concluida"] else "reaberta"
    print(f"{GREEN}Tarefa marcada como {status}.{RESET}")
    return True


def delete_task(tasks):
    """Pergunta qual tarefa, confirma e remove. Retorna True se removeu."""
    if not tasks:
        print(f"\n{YELLOW}Nenhuma tarefa cadastrada.{RESET}")
        return False

    list_tasks(tasks)
    index = ask_task_number(tasks, "\nNúmero da tarefa a remover: ")
    tarefa = tasks[index]["tarefa"]

    if ask_yes_no(f"Remover '{tarefa}' de verdade?", default=False):
        tasks.pop(index)
        print(f"{GREEN}Tarefa removida.{RESET}")
        return True

    print(f"{YELLOW}Remoção cancelada.{RESET}")
    return False


def show_menu():
    """Imprime o menu principal."""
    print(f"\n{BOLD}O que você quer fazer?{RESET}")
    for key, label in MENU.items():
        print(f"  {CYAN}{key}{RESET} - {label}")


def main():
    print(f"{BOLD}{CYAN}=== To-Do List ==={RESET}")
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Opção: ").strip()

        if choice == "1":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            if toggle_task(tasks):
                save_tasks(tasks)
        elif choice == "4":
            if delete_task(tasks):
                save_tasks(tasks)
        elif choice == "5":
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break
        else:
            print(f"{RED}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
