"""BMI Calculator (CLI).

Calcula o Índice de Massa Corporal (IMC) a partir do peso e da altura
informados, classifica o resultado segundo as faixas da OMS e mostra um
comentário de saúde (health insight) correspondente.

O IMC é só uma triagem simples (peso / altura²) — não leva em conta massa
muscular, densidade óssea, idade ou sexo, então não substitui avaliação
de um profissional de saúde.

Conceitos: operações matemáticas, lógica condicional e métricas de saúde.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

MIN_WEIGHT_KG, MAX_WEIGHT_KG = 1.0, 500.0
MIN_HEIGHT_CM, MAX_HEIGHT_CM = 50.0, 250.0

# Faixas de IMC (limite superior, rótulo, insight de saúde), na ordem da OMS.
# A última faixa usa infinito como limite, pra sempre ter uma categoria pro bmi.
BMI_CATEGORIES = [
    (18.5, "Abaixo do peso", "Um IMC baixo pode indicar desnutrição. Vale considerar uma avaliação nutricional."),
    (25.0, "Peso normal", "Seu IMC está na faixa considerada saudável pela OMS. Manter a alimentação equilibrada e a atividade física ajuda a continuar assim."),
    (30.0, "Sobrepeso", "Pequenos ajustes na alimentação e no nível de atividade física podem ajudar a trazer o IMC de volta à faixa considerada saudável."),
    (35.0, "Obesidade grau I", "Vale buscar orientação de um profissional de saúde para montar um plano de alimentação e exercícios."),
    (40.0, "Obesidade grau II", "É recomendável acompanhamento médico e nutricional para reduzir riscos à saúde associados a esse IMC."),
    (float("inf"), "Obesidade grau III", "Esse nível de IMC está associado a riscos sérios à saúde; acompanhamento médico é fortemente recomendado."),
]


def ask_float(prompt, low, high):
    """Lê um número decimal do usuário garantindo que esteja em [low, high].

    Aceita tanto ponto quanto vírgula como separador decimal.
    """
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print(f"{RED}Digite um número válido (ex.: 70.5).{RESET}")
            continue
        if not low <= value <= high:
            print(f"{RED}O valor deve estar entre {low} e {high}.{RESET}")
            continue
        return value


def calculate_bmi(weight_kg, height_cm):
    """Calcula o IMC: peso (kg) / altura (m) ao quadrado."""
    height_m = height_cm / 100
    return weight_kg / height_m ** 2


def classify_bmi(bmi):
    """Retorna (rótulo, insight) da faixa de IMC correspondente, segundo a OMS."""
    for upper_bound, label, insight in BMI_CATEGORIES:
        if bmi < upper_bound:
            return label, insight
    return BMI_CATEGORIES[-1][1], BMI_CATEGORIES[-1][2]


def print_result(weight_kg, height_cm, bmi, label, insight):
    """Imprime o IMC calculado, a categoria e o insight de saúde correspondente."""
    print(f"\n{BOLD}Peso:{RESET} {weight_kg:.1f} kg | {BOLD}Altura:{RESET} {height_cm:.0f} cm")
    print(f"{BOLD}IMC: {CYAN}{bmi:.1f}{RESET} — {YELLOW}{label}{RESET}")
    print(f"{insight}")


def play_round():
    """Pergunta peso e altura, calcula o IMC e mostra o resultado classificado."""
    weight_kg = ask_float("\nPeso (kg): ", MIN_WEIGHT_KG, MAX_WEIGHT_KG)
    height_cm = ask_float("Altura (cm): ", MIN_HEIGHT_CM, MAX_HEIGHT_CM)

    bmi = calculate_bmi(weight_kg, height_cm)
    label, insight = classify_bmi(bmi)
    print_result(weight_kg, height_cm, bmi, label, insight)


def main():
    print(f"{BOLD}{CYAN}=== Calculadora de IMC ==={RESET}")
    print("(O IMC é uma triagem simples; não substitui avaliação médica.)")

    while True:
        play_round()
        again = input("\nCalcular outro IMC? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
