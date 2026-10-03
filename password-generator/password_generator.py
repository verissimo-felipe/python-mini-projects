"""Password Generator (CLI).

Gera senhas aleatórias, permitindo customizar o tamanho e a complexidade
(quais tipos de caractere entram na senha: minúsculas, maiúsculas, números
e símbolos). A senha gerada garante pelo menos um caractere de cada tipo
escolhido, para não depender só da sorte do sorteio.

Conceitos: módulo random (via random.SystemRandom, mais adequado para
senhas do que o gerador padrão), constantes do módulo string e list
comprehensions.
"""

import random
import string

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Tipos de caractere disponíveis: chave -> (nome exibido, conjunto de caracteres).
CHARACTER_SETS = {
    "lower": ("Letras minúsculas (a-z)", string.ascii_lowercase),
    "upper": ("Letras maiúsculas (A-Z)", string.ascii_uppercase),
    "digits": ("Números (0-9)", string.digits),
    "symbols": ("Símbolos (!@#...)", string.punctuation),
}

MIN_LENGTH_FLOOR = 4
MAX_LENGTH = 128

# random.random() usa o gerador Mersenne Twister, previsível demais para senhas.
# random.SystemRandom() lê de os.urandom(), a fonte de aleatoriedade do sistema
# operacional — a mesma classe de fonte usada por bibliotecas criptográficas.
_rng = random.SystemRandom()


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


def choose_character_sets():
    """Pergunta quais tipos de caractere incluir. Retorna a lista de (nome, charset) escolhidos."""
    print(f"\n{BOLD}Quais tipos de caractere a senha deve conter?{RESET}")
    chosen = [
        (name, chars)
        for name, chars in CHARACTER_SETS.values()
        if ask_yes_no(f"  Incluir {name}?")
    ]
    if not chosen:
        print(f"{YELLOW}Nenhum tipo selecionado — usando letras minúsculas por padrão.{RESET}")
        chosen = [CHARACTER_SETS["lower"]]
    return chosen


def generate_password(length, chosen_sets):
    """Gera uma senha de `length` caracteres com pelo menos 1 de cada tipo em `chosen_sets`."""
    pool = "".join(chars for _, chars in chosen_sets)

    # Garante representação de cada tipo escolhido (senão uma senha longa
    # poderia, por sorte, sair só com um dos tipos selecionados).
    guaranteed = [_rng.choice(chars) for _, chars in chosen_sets]
    filler = [_rng.choice(pool) for _ in range(length - len(guaranteed))]

    password_chars = guaranteed + filler
    _rng.shuffle(password_chars)
    return "".join(password_chars)


def main():
    print(f"{BOLD}{CYAN}=== Gerador de Senhas ==={RESET}")

    while True:
        chosen_sets = choose_character_sets()
        min_length = max(MIN_LENGTH_FLOOR, len(chosen_sets))
        length = ask_int(
            f"\nTamanho da senha ({min_length}-{MAX_LENGTH}): ", min_length, MAX_LENGTH
        )

        password = generate_password(length, chosen_sets)
        print(f"\n{GREEN}{BOLD}🔐 Senha gerada:{RESET} {CYAN}{password}{RESET}")

        again = input("\nGerar outra senha? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
