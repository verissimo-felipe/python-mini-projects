"""Tic-Tac-Toe (CLI).

Dois jogadores (X e O) se revezam marcando um tabuleiro 3x3 até que um deles
alinhe três marcas (linha, coluna ou diagonal) ou o tabuleiro se esgote,
resultando em empate.

Conceitos: funções, listas, loops, lógica condicional e gerenciamento básico
de estado de jogo.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Combinações de índices (0-8) que configuram vitória.
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
]


def create_board():
    """Retorna um tabuleiro novo: lista de 9 posições vazias."""
    return [" "] * 9


def print_board(board):
    """Imprime o tabuleiro atual, mostrando o número da posição nas células vazias."""
    cells = [
        cell if cell != " " else f"{CYAN}{i + 1}{RESET}"
        for i, cell in enumerate(board)
    ]
    print()
    print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]} ")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]} ")
    print()


def check_winner(board):
    """Retorna 'X' ou 'O' se houver um vencedor, ou None caso contrário."""
    for a, b, c in WINNING_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def check_draw(board):
    """Retorna True se o tabuleiro estiver cheio (sem espaços vazios)."""
    return " " not in board


def ask_move(board, player):
    """Pergunta a posição (1-9) do próximo movimento, validando que está livre."""
    color = GREEN if player == "X" else YELLOW
    while True:
        raw = input(f"{color}{BOLD}Vez de {player}{RESET} — escolha uma posição (1-9): ").strip()
        try:
            position = int(raw)
        except ValueError:
            print(f"{RED}Digite um número inteiro entre 1 e 9.{RESET}")
            continue
        if not 1 <= position <= 9:
            print(f"{RED}Escolha uma posição entre 1 e 9.{RESET}")
            continue
        index = position - 1
        if board[index] != " ":
            print(f"{RED}Essa posição já está ocupada.{RESET}")
            continue
        return index


def play_round():
    """Executa uma partida completa. Retorna 'X', 'O' (vencedor) ou None (empate)."""
    board = create_board()
    player = "X"

    print_board(board)
    while True:
        index = ask_move(board, player)
        board[index] = player

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"{GREEN}{BOLD}🎉 {winner} venceu o jogo!{RESET}")
            return winner

        if check_draw(board):
            print_board(board)
            print(f"{YELLOW}{BOLD}🤝 Empate! O tabuleiro encheu sem vencedor.{RESET}")
            return None

        print_board(board)
        player = "O" if player == "X" else "X"


def main():
    print(f"{BOLD}{CYAN}=== Jogo da Velha (Tic-Tac-Toe) ==={RESET}")

    score = {"X": 0, "O": 0, "Empates": 0}
    while True:
        result = play_round()
        if result is None:
            score["Empates"] += 1
        else:
            score[result] += 1

        print(
            f"\nPlacar: {GREEN}X {score['X']}{RESET} | "
            f"{YELLOW}O {score['O']}{RESET} | "
            f"Empates {score['Empates']}"
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
