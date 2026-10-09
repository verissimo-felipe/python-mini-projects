"""Mad Libs Generator (CLI).

Jogo de palavras onde o jogador escolhe uma história e preenche uma lista
de palavras (substantivo, adjetivo, verbo, etc.) sem saber onde elas vão
entrar. No final, as palavras são encaixadas na história através de
f-strings, geralmente formando um resultado bem bobo.

Conceitos: formatação de strings (f-strings) e interação com o usuário.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def build_space_story(adjetivo1, substantivo1, verbo1, animal, numero, lugar):
    return (
        f"Era uma vez um(a) astronauta {adjetivo1} chamado(a) {substantivo1}, "
        f"que decidiu {verbo1} rumo a {lugar}. No caminho, encontrou "
        f"{numero} {animal}s flutuando no espaço, cantando uma música "
        f"completamente desafinada."
    )


def build_school_story(nome, adjetivo1, materia, verbo1, comida, numero):
    return (
        f"Hoje {nome} chegou à escola se sentindo muito {adjetivo1}. "
        f"Na aula de {materia}, o professor pediu pra turma {verbo1} em "
        f"grupos de {numero} pessoas. No intervalo, todo mundo só queria "
        f"saber de uma coisa: quem é que ia dividir o(a) {comida}?"
    )


def build_party_story(adjetivo1, animal, verbo1, lugar, numero, substantivo1):
    return (
        f"A festa surpresa era pra ser {adjetivo1}, mas ninguém esperava "
        f"que um(a) {animal} fosse {verbo1} direto pra {lugar}. No fim, "
        f"{numero} pessoas passaram a noite inteira rindo do(a) "
        f"{substantivo1} que sobrou em cima da mesa."
    )


# Histórias disponíveis: chave -> (título, campos a preguntar, função que monta o texto).
# Cada campo é (nome_do_parâmetro, pergunta mostrada ao jogador).
STORIES = {
    "1": (
        "Aventura no espaço",
        [
            ("adjetivo1", "Um adjetivo"),
            ("substantivo1", "Um substantivo"),
            ("verbo1", "Um verbo (no infinitivo)"),
            ("animal", "Um animal"),
            ("numero", "Um número"),
            ("lugar", "Um lugar"),
        ],
        build_space_story,
    ),
    "2": (
        "Um dia na escola",
        [
            ("nome", "Um nome de pessoa"),
            ("adjetivo1", "Um adjetivo"),
            ("materia", "Uma matéria escolar"),
            ("verbo1", "Um verbo (no infinitivo)"),
            ("comida", "Uma comida"),
            ("numero", "Um número"),
        ],
        build_school_story,
    ),
    "3": (
        "Festa surpresa",
        [
            ("adjetivo1", "Um adjetivo"),
            ("animal", "Um animal"),
            ("verbo1", "Um verbo (no infinitivo)"),
            ("lugar", "Um lugar"),
            ("numero", "Um número"),
            ("substantivo1", "Um substantivo"),
        ],
        build_party_story,
    ),
}


def ask_text(prompt):
    """Lê uma palavra/texto do usuário, repetindo a pergunta se vier em branco."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print(f"{RED}Digite alguma coisa — não pode ficar em branco.{RESET}")


def choose_story():
    """Mostra o menu de histórias e retorna (título, campos, função de montagem) escolhida."""
    print(f"\n{BOLD}Escolha uma história:{RESET}")
    for key, (title, _, _) in STORIES.items():
        print(f"  {CYAN}{key}{RESET} - {title}")

    while True:
        choice = input("Opção: ").strip()
        if choice in STORIES:
            return STORIES[choice]
        print(f"{RED}Opção inválida.{RESET}")


def collect_words(fields):
    """Pergunta uma palavra pra cada campo e retorna um dict nome_do_parâmetro -> palavra."""
    print(f"\n{BOLD}Agora me dê as palavras, sem saber onde elas vão entrar:{RESET}")
    return {name: ask_text(f"{label}: ") for name, label in fields}


def play_round():
    """Escolhe uma história, coleta as palavras e mostra o resultado final."""
    title, fields, build_story = choose_story()
    words = collect_words(fields)
    story_text = build_story(**words)

    print(f"\n{BOLD}{YELLOW}=== {title} ==={RESET}")
    print(f"{GREEN}{story_text}{RESET}")


def main():
    print(f"{BOLD}{CYAN}=== Mad Libs Generator ==={RESET}")

    while True:
        play_round()
        again = input("\nCriar outra história? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
