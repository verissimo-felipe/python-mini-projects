"""Color Palette Generator (CLI).

Sorteia uma cor base aleatória e gera uma paleta a partir dela, seguindo
um esquema de cores clássico da teoria das cores: monocromático,
complementar, análogo ou triádico. Cada cor é mostrada com seu código
hexadecimal e uma amostra visual (usando cores ANSI 24-bit no terminal).

Conceitos: módulo random, formatação hexadecimal e noções básicas de
teoria das cores (matiz, saturação, luminosidade).
"""

import colorsys
import random

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
RED = "\033[91m"


def random_base_color():
    """Sorteia uma cor base aleatória como tupla (r, g, b), cada um em 0-255."""
    return tuple(random.randint(0, 255) for _ in range(3))


def rgb_to_hex(rgb):
    """Formata uma tupla (r, g, b) como string hexadecimal '#RRGGBB'."""
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def shift_hue(rgb, degrees):
    """Retorna uma cor com o mesmo tom/luminosidade, mas o matiz girado em `degrees`."""
    r, g, b = (channel / 255 for channel in rgb)
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    hue = (hue + degrees / 360) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(hue, lightness, saturation)
    return tuple(round(channel * 255) for channel in (r2, g2, b2))


def adjust_lightness(rgb, lightness):
    """Retorna uma cor com o mesmo matiz/saturação, mas luminosidade ajustada para `lightness` (0-1)."""
    r, g, b = (channel / 255 for channel in rgb)
    hue, _, saturation = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(hue, lightness, saturation)
    return tuple(round(channel * 255) for channel in (r2, g2, b2))


def monochromatic_scheme(base_rgb):
    """Mesmo matiz da cor base, em 5 níveis de luminosidade (claro ao escuro)."""
    return [adjust_lightness(base_rgb, lightness) for lightness in (0.85, 0.65, 0.5, 0.35, 0.15)]


def complementary_scheme(base_rgb):
    """A cor base e sua complementar (matiz oposto, 180° na roda de cores)."""
    return [base_rgb, shift_hue(base_rgb, 180)]


def analogous_scheme(base_rgb):
    """A cor base e suas vizinhas na roda de cores (±30°)."""
    return [shift_hue(base_rgb, -30), base_rgb, shift_hue(base_rgb, 30)]


def triadic_scheme(base_rgb):
    """A cor base e outras duas espaçadas igualmente na roda de cores (120° cada)."""
    return [base_rgb, shift_hue(base_rgb, 120), shift_hue(base_rgb, 240)]


# Esquemas disponíveis: chave -> (rótulo, função que gera a lista de cores).
SCHEMES = {
    "1": ("Monocromática", monochromatic_scheme),
    "2": ("Complementar", complementary_scheme),
    "3": ("Análoga", analogous_scheme),
    "4": ("Triádica", triadic_scheme),
}


def choose_scheme():
    """Mostra o menu de esquemas de cor e retorna (rótulo, função) escolhida."""
    print(f"\n{BOLD}Escolha o esquema de cores:{RESET}")
    for key, (label, _) in SCHEMES.items():
        print(f"  {CYAN}{key}{RESET} - {label}")

    while True:
        choice = input("Opção: ").strip()
        if choice in SCHEMES:
            return SCHEMES[choice]
        print(f"{RED}Opção inválida.{RESET}")


def print_palette(colors):
    """Imprime cada cor da paleta com uma amostra visual (ANSI 24-bit) e o código hex."""
    for rgb in colors:
        r, g, b = rgb
        swatch = f"\033[48;2;{r};{g};{b}m        {RESET}"
        print(f"{swatch} {rgb_to_hex(rgb)}")


def play_round():
    """Sorteia uma cor base, escolhe um esquema e mostra a paleta gerada."""
    base_rgb = random_base_color()
    print(f"\n{BOLD}Cor base sorteada:{RESET} {rgb_to_hex(base_rgb)}")

    label, scheme_func = choose_scheme()
    colors = scheme_func(base_rgb)

    print(f"\n{BOLD}Paleta {label}:{RESET}")
    print_palette(colors)


def main():
    print(f"{BOLD}{CYAN}=== Color Palette Generator ==={RESET}")

    while True:
        play_round()
        again = input("\nGerar outra paleta? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
