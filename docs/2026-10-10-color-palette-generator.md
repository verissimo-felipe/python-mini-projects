# 2026-10-10 (Color Palette Generator)

Projeto finalizado hoje: **Color Palette Generator**. Com ele, todos os projetos da tabela do README estão ✅.

## Color Palette Generator

Arquivo: `color-palette-generator/color_palette_generator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `random_base_color()` | Sorteia uma cor base aleatória como tupla `(r, g, b)`. |
| `rgb_to_hex(rgb)` | Formata uma tupla `(r, g, b)` como string hexadecimal `"#RRGGBB"`. |
| `shift_hue(rgb, degrees)` | Retorna uma cor com o mesmo tom/luminosidade, mas o matiz girado em `degrees` graus na roda de cores (via `colorsys`). |
| `adjust_lightness(rgb, lightness)` | Retorna uma cor com o mesmo matiz/saturação, mas luminosidade ajustada pra um valor absoluto (0-1). |
| `monochromatic_scheme` / `complementary_scheme` / `analogous_scheme` / `triadic_scheme` | Os quatro esquemas de cor: mesmo matiz em luminosidades diferentes, matiz oposto (180°), matizes vizinhos (±30°) e matizes equidistantes (120° cada). |
| `choose_scheme()` | Mostra o menu de esquemas (`SCHEMES`) e retorna `(rótulo, função)` escolhida. |
| `print_palette(colors)` | Imprime cada cor da paleta com uma amostra visual (bloco colorido via ANSI 24-bit, `\033[48;2;r;g;bm`) e o código hex. |
| `play_round()` | Sorteia a cor base, escolhe o esquema e mostra a paleta gerada. |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer gerar outra paleta. |

Constantes de suporte: `RESET/BOLD/CYAN/RED` (cores ANSI pro texto) e `SCHEMES` (dicionário opção → `(rótulo, função geradora)`).

### Por que foi feito assim

- **`colorsys` (biblioteca padrão) pra girar matiz/ajustar luminosidade, em vez de manipular os canais R/G/B diretamente.** Teoria das cores (complementar, análoga, tríade) é definida em termos de matiz na roda de cores — um conceito de HSL/HLS, não de RGB. Trabalhar em RGB diretamente pra, por exemplo, "girar 180°" exigiria reimplementar a conversão por conta própria; `colorsys.rgb_to_hls`/`hls_to_rgb` já faz isso, então `shift_hue` só soma graus ao matiz e converte de volta.
- **Cada esquema é uma função pura `scheme(base_rgb) -> lista de cores`, independente de quantas cores ela retorna.** Monocromático sempre faz sentido com vários tons (5, nesse caso); complementar é literalmente só 2 cores (a base e a oposta) — forçar os dois esquemas a sempre devolverem a mesma quantidade de cores seria artificial. Deixar cada função decidir seu próprio tamanho de paleta é mais fiel à definição de cada esquema.
- **Teste de sanidade conferindo a tríade do vermelho puro contra verde e azul puros.** Rotações de matiz de 120° e 240° a partir do vermelho (`#FF0000`) devem cair exatamente em verde (`#00FF00`) e azul (`#0000FF`) — é um jeito direto de confirmar que a matemática de `shift_hue` está certa, sem precisar confiar só na leitura visual da paleta.
- **Amostra visual com ANSI 24-bit (`\033[48;2;r;g;bm`), não só o texto do código hex.** Esse projeto é sobre *ver* cores — imprimir só `#FF0000` como texto não transmite a cor de verdade. É uma extensão natural do mesmo princípio do primeiro projeto do repositório (`ansi-color-chart-generator`), só que usando o modo 24-bit do terminal em vez da paleta de 16 cores, já que aqui as cores são arbitrárias (não um dos 8/16 códigos ANSI fixos).
