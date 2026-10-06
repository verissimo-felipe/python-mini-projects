# 2026-10-06 (BMI Calculator)

Projeto finalizado hoje: **BMI Calculator**.

## BMI Calculator

Arquivo: `bmi-calculator/bmi_calculator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `ask_float(prompt, low, high)` | Lê um número decimal do usuário garantindo que esteja em `[low, high]`. Aceita vírgula ou ponto como separador decimal. |
| `calculate_bmi(weight_kg, height_cm)` | Calcula o IMC: converte a altura de cm para metros e retorna `peso / altura²`. |
| `classify_bmi(bmi)` | Percorre `BMI_CATEGORIES` e retorna `(rótulo, insight)` da primeira faixa cujo limite superior é maior que o IMC calculado. |
| `print_result(weight_kg, height_cm, bmi, label, insight)` | Imprime peso, altura, IMC calculado, a categoria e o insight de saúde correspondente. |
| `play_round()` | Pergunta peso e altura, calcula o IMC e mostra o resultado classificado. |
| `main()` | Loop principal: mostra o aviso de que o IMC não substitui avaliação médica, chama `play_round()` repetidamente e pergunta se quer calcular outro. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `MIN_WEIGHT_KG`/`MAX_WEIGHT_KG`, `MIN_HEIGHT_CM`/`MAX_HEIGHT_CM` (limites de input) e `BMI_CATEGORIES` (lista de tuplas `(limite_superior, rótulo, insight)`, na ordem das faixas da OMS).

### Por que foi feito assim

- **`BMI_CATEGORIES` como lista ordenada de tuplas `(limite_superior, rótulo, insight)`, percorrida num loop, em vez de uma cadeia de `if/elif`.** As faixas de IMC da OMS têm a mesma estrutura (um limite superior, um rótulo, um texto) e são checadas sempre do mesmo jeito ("é menor que esse limite?"); representar isso como dados e iterar é mais fácil de ajustar (mudar um limite ou adicionar uma faixa não exige tocar na lógica) do que uma sequência de condicionais repetidas.
- **Altura pedida em centímetros, não em metros.** "175" é uma entrada mais natural e menos propensa a erro de digitação do que "1.75" — e a conversão (`/100`) fica isolada dentro de `calculate_bmi`, então quem usa a função não precisa se preocupar com a unidade.
- **Aviso explícito de que o IMC não substitui avaliação médica**, impresso uma vez no início do programa. IMC é uma métrica de triagem simples (só peso e altura) que não considera massa muscular, densidade óssea, idade ou sexo — é importante que a ferramenta não dê a entender que é um diagnóstico.
- **`classify_bmi` sempre retorna algo, mesmo em IMCs extremos**, porque a última faixa usa `float("inf")` como limite superior — não existe caminho onde o loop termina sem encontrar uma categoria, então não precisa de tratamento de erro extra pra esse caso.
