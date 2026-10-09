"""Unit Converter (CLI).

Converte valores entre unidades de categorias diferentes: temperatura
(Celsius/Fahrenheit/Kelvin), distância (metros/pés, quilômetros/milhas)
e peso (quilogramas/libras).

Conceitos: operações matemáticas e fórmulas de conversão de unidades.
"""

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def meters_to_feet(meters):
    return meters * 3.28084


def feet_to_meters(feet):
    return feet / 3.28084


def km_to_miles(km):
    return km * 0.621371


def miles_to_km(miles):
    return miles / 0.621371


def kg_to_lb(kg):
    return kg * 2.20462


def lb_to_kg(lb):
    return lb / 2.20462


# Categorias disponíveis: chave -> (rótulo, conversões daquela categoria).
# Cada conversão: chave -> (unidade de origem, unidade de destino, função).
CATEGORIES = {
    "1": (
        "Temperatura",
        {
            "1": ("Celsius", "Fahrenheit", celsius_to_fahrenheit),
            "2": ("Fahrenheit", "Celsius", fahrenheit_to_celsius),
            "3": ("Celsius", "Kelvin", celsius_to_kelvin),
            "4": ("Kelvin", "Celsius", kelvin_to_celsius),
        },
    ),
    "2": (
        "Distância",
        {
            "1": ("Metros", "Pés", meters_to_feet),
            "2": ("Pés", "Metros", feet_to_meters),
            "3": ("Quilômetros", "Milhas", km_to_miles),
            "4": ("Milhas", "Quilômetros", miles_to_km),
        },
    ),
    "3": (
        "Peso",
        {
            "1": ("Quilogramas", "Libras", kg_to_lb),
            "2": ("Libras", "Quilogramas", lb_to_kg),
        },
    ),
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


def choose_from_menu(prompt, options):
    """Mostra um menu numerado genérico e retorna a entrada escolhida de `options`.

    `options` é um dict chave -> item; o rótulo exibido é o primeiro
    elemento do item (tupla) ou o próprio item (se for string).
    """
    print(f"\n{BOLD}{prompt}{RESET}")
    for key, item in options.items():
        label = item[0] if isinstance(item, tuple) else item
        print(f"  {CYAN}{key}{RESET} - {label}")

    while True:
        choice = input("Opção: ").strip()
        if choice in options:
            return options[choice]
        print(f"{RED}Opção inválida.{RESET}")


def choose_conversion(conversions):
    """Mostra o menu de conversões de uma categoria e retorna (origem, destino, função)."""
    print(f"\n{BOLD}Escolha a conversão:{RESET}")
    for key, (from_unit, to_unit, _) in conversions.items():
        print(f"  {CYAN}{key}{RESET} - {from_unit} → {to_unit}")

    while True:
        choice = input("Opção: ").strip()
        if choice in conversions:
            return conversions[choice]
        print(f"{RED}Opção inválida.{RESET}")


def play_round():
    """Escolhe categoria e conversão, pede o valor e mostra o resultado."""
    _, conversions = choose_from_menu("Escolha a categoria:", CATEGORIES)
    from_unit, to_unit, convert = choose_conversion(conversions)

    value = ask_float(f"\nValor em {from_unit}: ")
    result = convert(value)

    print(f"{BOLD}{value} {from_unit} = {GREEN}{result:.2f}{RESET} {to_unit}")


def main():
    print(f"{BOLD}{CYAN}=== Conversor de Unidades ==={RESET}")

    while True:
        play_round()
        again = input("\nFazer outra conversão? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
