"""Rock, Paper, Scissors (CLI).

Clássico jogo de Pedra, Papel e Tesoura contra o computador: cada um
escolhe uma opção, e quem escolheu a opção que vence a do outro ganha a
rodada (ou é empate, se escolherem a mesma).

Conceitos: módulo random, lógica condicional e interação com o usuário.
"""

import random

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Opções disponíveis: chave digitada -> rótulo.
CHOICES = {"1": "Pedra", "2": "Papel", "3": "Tesoura"}

# O que cada opção vence (regra clássica: Pedra vence Tesoura, Tesoura
# vence Papel, Papel vence Pedra).
BEATS = {"Pedra": "Tesoura", "Tesoura": "Papel", "Papel": "Pedra"}


def ask_choice():
    """Mostra o menu de opções e retorna a escolha do jogador (rótulo)."""
    print(f"\n{BOLD}Escolha:{RESET}")
    for key, label in CHOICES.items():
        print(f"  {CYAN}{key}{RESET} - {label}")

    while True:
        choice = input("Opção: ").strip()
        if choice in CHOICES:
            return CHOICES[choice]
        print(f"{RED}Opção inválida. Escolha 1, 2 ou 3.{RESET}")


def computer_choice():
    """Sorteia a escolha do computador entre as opções disponíveis."""
    return random.choice(list(CHOICES.values()))


def decide_winner(player, computer):
    """Retorna 'player', 'computer' ou 'draw' com base nas escolhas das duas partes."""
    if player == computer:
        return "draw"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def print_round_result(player, computer, outcome):
    """Imprime as escolhas de cada lado e o resultado da rodada."""
    print(f"\nVocê escolheu: {CYAN}{player}{RESET} | Computador escolheu: {CYAN}{computer}{RESET}")
    if outcome == "draw":
        print(f"{YELLOW}{BOLD}Empate!{RESET}")
    elif outcome == "player":
        print(f"{GREEN}{BOLD}Você venceu esta rodada!{RESET}")
    else:
        print(f"{RED}{BOLD}O computador venceu esta rodada!{RESET}")


def play_round():
    """Executa uma rodada completa e retorna o resultado ('player'/'computer'/'draw')."""
    player = ask_choice()
    computer = computer_choice()
    outcome = decide_winner(player, computer)
    print_round_result(player, computer, outcome)
    return outcome


def main():
    print(f"{BOLD}{CYAN}=== Pedra, Papel e Tesoura ==={RESET}")

    wins = losses = draws = 0
    while True:
        outcome = play_round()
        if outcome == "player":
            wins += 1
        elif outcome == "computer":
            losses += 1
        else:
            draws += 1

        print(
            f"\nPlacar: {GREEN}{wins} vitória(s){RESET} | "
            f"{RED}{losses} derrota(s){RESET} | {YELLOW}{draws} empate(s){RESET}"
        )
        again = input("Jogar de novo? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Obrigado por jogar! Até a próxima. 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Jogo encerrado. Até mais!{RESET}")
