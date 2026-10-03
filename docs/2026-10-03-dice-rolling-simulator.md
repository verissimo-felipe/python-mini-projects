# 2026-10-03 (Dice Rolling Simulator)

Projeto finalizado hoje: **Dice Rolling Simulator**.

## Dice Rolling Simulator

Arquivo: `dice-rolling-simulator/dice_rolling_simulator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `ask_int(prompt, low, high)` | Lê um inteiro do usuário garantindo que esteja em `[low, high]`. |
| `ask_yes_no(prompt, default=True)` | Pergunta sim/não; Enter vazio usa o valor padrão. |
| `choose_dice_type()` | Mostra o menu de tipos de dado (`DICE_TYPES`: d4/d6/d8/d10/d12/d20/Personalizado) e retorna `(rótulo, lados)` escolhido. Se for "Personalizado", pede o número de lados. |
| `roll_dice(num_dice, sides)` | Rola `num_dice` dados de `sides` lados e retorna a lista de resultados. |
| `print_rolls(rolls)` | Imprime cada resultado da rolagem e a soma total. |
| `run_single_roll(num_dice, sides)` | Roda uma única rolagem e mostra o resultado. |
| `simulate_many_rolls(num_dice, sides, trials)` | Roda `trials` rolagens repetidas e retorna a lista das somas de cada uma. |
| `summarize_statistics(totals)` | Retorna a média, o mínimo e o máximo observados numa lista de somas. |
| `build_histogram(totals, num_dice, sides)` | Conta quantas vezes cada soma possível apareceu, cobrindo todo o intervalo `[num_dice, num_dice * sides]`. |
| `print_histogram(histogram, trials)` | Imprime um histograma ASCII (barras de `#`) da distribuição das somas, escalado à maior contagem, com percentual de cada soma. |
| `run_simulation(num_dice, sides)` | Pede o número de tentativas, roda a simulação completa e mostra estatísticas + histograma. |
| `play_round()` | Pergunta nº de dados e tipo de dado, pergunta se o jogador quer rodar uma rolagem simples ou uma simulação estatística, e despacha para a função correspondente. |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer rolar de novo. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `DICE_TYPES` (dicionário tipo → (rótulo, lados)), `MIN_DICE`/`MAX_DICE`, `MIN_SIDES`/`MAX_SIDES`, `MIN_TRIALS`/`MAX_TRIALS` (limites de input) e `HISTOGRAM_WIDTH` (largura máxima, em caracteres, da barra do histograma).

### Por que o modo estatístico foi feito assim

- **Comparar a média observada com a média teórica (`num_dice * (sides + 1) / 2`).** Isso é a Lei dos Grandes Números na prática: com poucas rolagens o resultado pode variar bastante, mas conforme `trials` cresce, a média observada converge pra média teórica. Mostrar os dois números lado a lado deixa esse conceito visível sem precisar explicar estatística — o próprio número confirma.
- **Histograma com contagem por soma, não por resultado individual de cada dado.** A soma de múltiplos dados não é uniforme (ex.: em 2d6, somar 7 é muito mais provável que somar 2 ou 12, porque há mais combinações de dados que resultam em 7). Construir o histograma sobre as somas, e não sobre cada dado isolado, é o que deixa essa distribuição em formato de "sino" visível no terminal.
- **`build_histogram` cobre todo o intervalo `range(num_dice, num_dice * sides + 1)`, mesmo somas com contagem 0.** Garante que o histograma sempre tenha o mesmo formato/eixo, não só os valores que por acaso saíram na simulação — importante pra comparar simulações diferentes de forma consistente.
- **Sem importar o módulo `statistics`.** O README lista as bibliotecas usadas no repositório (`random`, `time`, `datetime`, `math`, `json`, `os`) e `statistics` não está entre elas; `sum()/len()`, `min()` e `max()` já são suficientes pra média/mínimo/máximo, então usá-los mantém o projeto dentro do escopo de bibliotecas já estabelecido.
