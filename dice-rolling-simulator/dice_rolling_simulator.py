"""Dice Rolling Simulator (CLI).

Simula a rolagem de um ou mais dados, com quantidade de lados customizável
(d4, d6, d8, d10, d12, d20 ou um valor personalizado). Além da rolagem
simples, tem um modo de simulação estatística: roda muitas rolagens
repetidas e mostra a média/mínimo/máximo observados e um histograma da
distribuição das somas.

Conceitos: módulo random, validação de input do usuário e simulação
estatística (lei dos grandes números: a média observada se aproxima da
média teórica conforme o número de tentativas cresce).
"""

import random

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Tipos de dado disponíveis: chave -> (rótulo, nº de lados). "Personalizado"
# usa `None` como marcador para pedir o número de lados ao jogador.
DICE_TYPES = {
    "1": ("d4", 4),
    "2": ("d6", 6),
    "3": ("d8", 8),
    "4": ("d10", 10),
    "5": ("d12", 12),
    "6": ("d20", 20),
    "7": ("Personalizado", None),
}

MIN_DICE, MAX_DICE = 1, 10
MIN_SIDES, MAX_SIDES = 2, 100
MIN_TRIALS, MAX_TRIALS = 100, 100_000

HISTOGRAM_WIDTH = 50


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


def choose_dice_type():
    """Mostra o menu de tipos de dado e retorna (rótulo, lados) escolhido."""
    print(f"\n{BOLD}Escolha o tipo de dado:{RESET}")
    for key, (label, sides) in DICE_TYPES.items():
        suffix = f" ({sides} lados)" if sides else ""
        print(f"  {CYAN}{key}{RESET} - {label}{suffix}")

    while True:
        choice = input("Opção: ").strip()
        if choice in DICE_TYPES:
            label, sides = DICE_TYPES[choice]
            if sides is None:
                sides = ask_int(f"Quantos lados tem o dado ({MIN_SIDES}-{MAX_SIDES})? ", MIN_SIDES, MAX_SIDES)
                label = f"d{sides}"
            return label, sides
        print(f"{RED}Opção inválida.{RESET}")


def roll_dice(num_dice, sides):
    """Rola `num_dice` dados de `sides` lados e retorna a lista de resultados."""
    return [random.randint(1, sides) for _ in range(num_dice)]


def print_rolls(rolls):
    """Imprime cada resultado da rolagem e a soma total."""
    formatted = ", ".join(f"{CYAN}{roll}{RESET}" for roll in rolls)
    print(f"\nResultados: {formatted}")
    print(f"{BOLD}Soma: {GREEN}{sum(rolls)}{RESET}")


def run_single_roll(num_dice, sides):
    """Roda uma única rolagem de `num_dice` dados de `sides` lados."""
    rolls = roll_dice(num_dice, sides)
    print_rolls(rolls)


def simulate_many_rolls(num_dice, sides, trials):
    """Roda `trials` rolagens de `num_dice` dados e retorna a lista das somas."""
    return [sum(roll_dice(num_dice, sides)) for _ in range(trials)]


def summarize_statistics(totals):
    """Retorna (média, mínimo, máximo) observados na lista de somas `totals`."""
    average = sum(totals) / len(totals)
    return average, min(totals), max(totals)


def build_histogram(totals, num_dice, sides):
    """Retorna um dict soma -> contagem, cobrindo todas as somas possíveis."""
    possible_totals = range(num_dice, num_dice * sides + 1)
    return {total: totals.count(total) for total in possible_totals}


def print_histogram(histogram, trials):
    """Imprime um histograma ASCII da distribuição de somas, escalado à maior contagem."""
    max_count = max(histogram.values())
    print(f"\n{BOLD}Distribuição das somas:{RESET}")
    for total, count in histogram.items():
        if count == 0:
            continue
        bar_length = round((count / max_count) * HISTOGRAM_WIDTH)
        bar = "#" * bar_length
        percentage = (count / trials) * 100
        print(f"{total:>4} | {YELLOW}{bar}{RESET} {count} ({percentage:.1f}%)")


def run_simulation(num_dice, sides):
    """Pede o nº de tentativas, roda a simulação e mostra estatísticas + histograma."""
    trials = ask_int(
        f"\nQuantas rolagens simular ({MIN_TRIALS}-{MAX_TRIALS})? ", MIN_TRIALS, MAX_TRIALS
    )
    totals = simulate_many_rolls(num_dice, sides, trials)
    average, minimum, maximum = summarize_statistics(totals)
    theoretical_average = num_dice * (sides + 1) / 2

    print(f"\n{BOLD}Resultado de {trials} rolagens:{RESET}")
    print(f"Mínimo observado: {CYAN}{minimum}{RESET} | Máximo observado: {CYAN}{maximum}{RESET}")
    print(
        f"Média observada: {GREEN}{average:.2f}{RESET} "
        f"(média teórica: {theoretical_average:.2f})"
    )

    histogram = build_histogram(totals, num_dice, sides)
    print_histogram(histogram, trials)


def play_round():
    """Pergunta a configuração do jogador e roda uma rolagem simples ou uma simulação."""
    num_dice = ask_int(f"\nQuantos dados rolar ({MIN_DICE}-{MAX_DICE})? ", MIN_DICE, MAX_DICE)
    label, sides = choose_dice_type()
    print(f"{BOLD}Rolando {num_dice}x {label}.{RESET}")

    run_stats = ask_yes_no(
        "Rodar uma simulação estatística (muitas rolagens) em vez de uma rolagem única?",
        default=False,
    )
    if run_stats:
        run_simulation(num_dice, sides)
    else:
        run_single_roll(num_dice, sides)


def main():
    print(f"{BOLD}{CYAN}=== Dice Rolling Simulator ==={RESET}")

    while True:
        play_round()
        again = input("\nRolar de novo? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
