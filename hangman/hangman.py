"""Hangman (CLI).

O computador sorteia uma palavra secreta de uma categoria aleatória e o
jogador tenta descobri-la letra por letra antes que o boneco seja
"enforcado" (número de erros esgotado).

Conceitos: dicionários, módulo random, manipulação de strings e
validação de input.
"""

import random

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Categoria -> lista de palavras possíveis.
WORDS_BY_CATEGORY = {
    "Frutas": ["abacaxi", "banana", "laranja", "manga", "morango"],
    "Animais": ["elefante", "girafa", "tartaruga", "jacare", "cavalo"],
    "Linguagens de Programação": ["python", "javascript", "java", "ruby", "golang"],
    "Países": ["brasil", "portugal", "argentina", "japao", "canada"],
}

# Desenhos do boneco, do menos (0 erros) ao mais enforcado (erros máximos).
HANGMAN_STAGES = [
    r"""
       +---+
           |
           |
           |
          ===""",
    r"""
       +---+
       O   |
           |
           |
          ===""",
    r"""
       +---+
       O   |
       |   |
           |
          ===""",
    r"""
       +---+
       O   |
      /|   |
           |
          ===""",
    r"""
       +---+
       O   |
      /|\  |
           |
          ===""",
    r"""
       +---+
       O   |
      /|\  |
      /    |
          ===""",
    r"""
       +---+
       O   |
      /|\  |
      / \  |
          ===""",
]

MAX_ATTEMPTS = len(HANGMAN_STAGES) - 1


def choose_word():
    """Sorteia uma categoria e uma palavra dentro dela. Retorna (categoria, palavra)."""
    category = random.choice(list(WORDS_BY_CATEGORY.keys()))
    word = random.choice(WORDS_BY_CATEGORY[category])
    return category, word


def display_word(word, guessed_letters):
    """Retorna a palavra mascarada, mostrando só as letras já acertadas."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def draw_hangman(wrong_count):
    """Imprime o desenho do boneco correspondente ao número de erros atual."""
    print(f"{RED}{HANGMAN_STAGES[wrong_count]}{RESET}")


def ask_letter(guessed_letters):
    """Pede uma letra ao jogador, validando que é uma letra única ainda não tentada."""
    while True:
        raw = input(f"{CYAN}Digite uma letra: {RESET}").strip().lower()
        if len(raw) != 1 or not raw.isalpha():
            print(f"{RED}Digite apenas uma letra do alfabeto.{RESET}")
            continue
        if raw in guessed_letters:
            print(f"{RED}Você já tentou a letra '{raw}'.{RESET}")
            continue
        return raw


def play_round():
    """Executa uma partida completa. Retorna True se o jogador descobriu a palavra."""
    category, word = choose_word()
    guessed_letters = set()
    wrong_count = 0

    print(f"\n{BOLD}Categoria: {CYAN}{category}{RESET}")

    while wrong_count < MAX_ATTEMPTS:
        draw_hangman(wrong_count)
        print(f"{BOLD}Palavra:{RESET} {display_word(word, guessed_letters)}")
        print(f"Erros: {wrong_count}/{MAX_ATTEMPTS}")

        letter = ask_letter(guessed_letters)
        guessed_letters.add(letter)

        if letter in word:
            print(f"{GREEN}Boa! A letra '{letter}' está na palavra.{RESET}")
            if all(char in guessed_letters for char in word):
                draw_hangman(wrong_count)
                print(f"\n{GREEN}{BOLD}🎉 Você venceu! A palavra era '{word}'.{RESET}")
                return True
        else:
            wrong_count += 1
            print(f"{YELLOW}Que pena, a letra '{letter}' não está na palavra.{RESET}")

    draw_hangman(wrong_count)
    print(f"\n{RED}{BOLD}💀 Fim de jogo! A palavra era '{word}'.{RESET}")
    return False


def main():
    print(f"{BOLD}{CYAN}=== Jogo da Forca (Hangman) ==={RESET}")

    wins = 0
    losses = 0
    while True:
        if play_round():
            wins += 1
        else:
            losses += 1

        print(f"\nPlacar: {GREEN}{wins} vitória(s){RESET} | {RED}{losses} derrota(s){RESET}")
        again = input("Jogar de novo? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Obrigado por jogar! Até a próxima. 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Jogo encerrado. Até mais!{RESET}")
