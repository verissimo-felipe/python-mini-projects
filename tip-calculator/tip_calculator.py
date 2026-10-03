"""Tip Calculator (CLI).

Calcula a gorjeta e o total a pagar a partir do valor da conta e da
qualidade do atendimento, podendo também dividir o total entre várias
pessoas.

Conceitos: aritmética de ponto flutuante, validação de input do usuário
e formatação de valores monetários.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Qualidade do atendimento -> (rótulo, percentual de gorjeta sugerido).
# "Personalizado" usa `None` como marcador para pedir o percentual ao usuário.
SERVICE_QUALITY = {
    "1": ("Ruim", 0.10),
    "2": ("Razoável", 0.15),
    "3": ("Bom", 0.20),
    "4": ("Excelente", 0.25),
    "5": ("Personalizado", None),
}

MIN_BILL, MAX_BILL = 0.01, 1_000_000.0
MIN_PERCENTAGE, MAX_PERCENTAGE = 0.0, 100.0
MIN_PEOPLE, MAX_PEOPLE = 1, 50


def ask_float(prompt, low, high):
    """Lê um número decimal do usuário garantindo que esteja em [low, high].

    Aceita tanto ponto quanto vírgula como separador decimal.
    """
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print(f"{RED}Digite um número válido (ex.: 49.90).{RESET}")
            continue
        if not low <= value <= high:
            print(f"{RED}O valor deve estar entre {low} e {high}.{RESET}")
            continue
        return value


def ask_int(prompt, low, high):
    """Lê um inteiro do usuário garantindo que esteja em [low, high]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"{RED}Digite um número inteiro válido.{RESET}")
            continue
        if not low <= value <= high:
            print(f"{RED}O número deve estar entre {low} e {high}.{RESET}")
            continue
        return value


def choose_tip_percentage():
    """Mostra o menu de qualidade do atendimento e retorna (rótulo, percentual 0-1)."""
    print(f"\n{BOLD}Como foi o atendimento?{RESET}")
    for key, (label, percentage) in SERVICE_QUALITY.items():
        suffix = f" ({percentage:.0%})" if percentage is not None else ""
        print(f"  {CYAN}{key}{RESET} - {label}{suffix}")

    while True:
        choice = input("Opção: ").strip()
        if choice in SERVICE_QUALITY:
            label, percentage = SERVICE_QUALITY[choice]
            if percentage is None:
                percentage = ask_float(
                    f"Qual percentual de gorjeta ({MIN_PERCENTAGE:.0f}-{MAX_PERCENTAGE:.0f})? ",
                    MIN_PERCENTAGE,
                    MAX_PERCENTAGE,
                ) / 100
                label = f"Personalizado ({percentage:.0%})"
            return label, percentage
        print(f"{RED}Opção inválida.{RESET}")


def calculate_tip(bill, percentage):
    """Retorna o valor da gorjeta: `bill * percentage`."""
    return bill * percentage


def format_currency(value):
    """Formata um valor float como moeda, com 2 casas decimais."""
    return f"R$ {value:.2f}"


def print_summary(bill, quality_label, percentage, tip, people):
    """Imprime o resumo formatado: conta, gorjeta, total e valor por pessoa."""
    total = bill + tip
    share = total / people

    print(f"\n{BOLD}Resumo:{RESET}")
    print(f"Conta: {format_currency(bill)}")
    print(f"Atendimento: {quality_label} ({percentage:.0%})")
    print(f"Gorjeta: {YELLOW}{format_currency(tip)}{RESET}")
    print(f"{BOLD}Total: {GREEN}{format_currency(total)}{RESET}")
    if people > 1:
        print(f"Dividido entre {people} pessoas: {CYAN}{format_currency(share)}{RESET} cada")


def play_round():
    """Pergunta conta, qualidade do atendimento e nº de pessoas, e mostra o resumo."""
    bill = ask_float("\nValor da conta (R$): ", MIN_BILL, MAX_BILL)
    quality_label, percentage = choose_tip_percentage()
    people = ask_int(
        f"\nDividir entre quantas pessoas ({MIN_PEOPLE}-{MAX_PEOPLE})? ", MIN_PEOPLE, MAX_PEOPLE
    )

    tip = calculate_tip(bill, percentage)
    print_summary(bill, quality_label, percentage, tip, people)


def main():
    print(f"{BOLD}{CYAN}=== Calculadora de Gorjeta ==={RESET}")

    while True:
        play_round()
        again = input("\nCalcular outra conta? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
