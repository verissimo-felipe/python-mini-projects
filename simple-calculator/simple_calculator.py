"""Simple Calculator (CLI).

Calculadora de quatro operações básicas (soma, subtração, multiplicação
e divisão) com interface de linha de comando.

Conceitos: funções, interação com o usuário e tratamento de exceções.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b  # levanta ZeroDivisionError se b for 0; quem chama trata isso.


# Operações disponíveis: chave digitada -> (rótulo, símbolo, função).
OPERATIONS = {
    "1": ("Soma", "+", add),
    "2": ("Subtração", "-", subtract),
    "3": ("Multiplicação", "*", multiply),
    "4": ("Divisão", "/", divide),
}


def ask_float(prompt):
    """Lê um número decimal do usuário, repetindo a pergunta se a conversão falhar.

    Aceita tanto ponto quanto vírgula como separador decimal.
    """
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print(f"{RED}Digite um número válido (ex.: 3.5).{RESET}")


def choose_operation():
    """Mostra o menu de operações e retorna (rótulo, símbolo, função) escolhida."""
    print(f"\n{BOLD}Escolha a operação:{RESET}")
    for key, (label, symbol, _) in OPERATIONS.items():
        print(f"  {CYAN}{key}{RESET} - {label} ({symbol})")

    while True:
        choice = input("Opção: ").strip()
        if choice in OPERATIONS:
            return OPERATIONS[choice]
        print(f"{RED}Opção inválida. Escolha de 1 a 4.{RESET}")


def calculate(a, b, operation_func):
    """Aplica `operation_func` em (a, b). Retorna o resultado, ou None se der erro.

    Trata ZeroDivisionError (divisão por zero), já que essa é a única
    operação das quatro que pode falhar com entradas válidas.
    """
    try:
        return operation_func(a, b)
    except ZeroDivisionError:
        print(f"{RED}Não é possível dividir por zero.{RESET}")
        return None


def play_round():
    """Pergunta os dois números e a operação, calcula e mostra o resultado."""
    a = ask_float("\nPrimeiro número: ")
    b = ask_float("Segundo número: ")
    label, symbol, operation_func = choose_operation()

    result = calculate(a, b, operation_func)
    if result is not None:
        print(f"{BOLD}{a} {symbol} {b} = {GREEN}{result}{RESET} ({label})")


def main():
    print(f"{BOLD}{CYAN}=== Calculadora Simples ==={RESET}")

    while True:
        play_round()
        again = input("\nFazer outro cálculo? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
