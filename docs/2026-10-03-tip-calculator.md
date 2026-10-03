# 2026-10-03 (Tip Calculator)

Projeto finalizado hoje: **Tip Calculator**.

## Tip Calculator

Arquivo: `tip-calculator/tip_calculator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `ask_float(prompt, low, high)` | Lê um número decimal do usuário garantindo que esteja em `[low, high]`. Aceita vírgula ou ponto como separador decimal. |
| `ask_int(prompt, low, high)` | Lê um inteiro do usuário garantindo que esteja em `[low, high]`. |
| `choose_tip_percentage()` | Mostra o menu de qualidade do atendimento (`SERVICE_QUALITY`: Ruim/Razoável/Bom/Excelente/Personalizado) e retorna `(rótulo, percentual)` escolhido. Se for "Personalizado", pede o percentual ao usuário. |
| `calculate_tip(bill, percentage)` | Retorna o valor da gorjeta (`bill * percentage`). |
| `format_currency(value)` | Formata um valor float como moeda, com 2 casas decimais (`R$ 49.90`). |
| `print_summary(bill, quality_label, percentage, tip, people)` | Imprime o resumo: valor da conta, atendimento escolhido, gorjeta, total e, se mais de 1 pessoa, o valor dividido por pessoa. |
| `play_round()` | Pergunta valor da conta, qualidade do atendimento e número de pessoas, calcula a gorjeta e mostra o resumo. |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer calcular outra conta. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `SERVICE_QUALITY` (dicionário qualidade → (rótulo, percentual sugerido)) e `MIN_BILL`/`MAX_BILL`, `MIN_PERCENTAGE`/`MAX_PERCENTAGE`, `MIN_PEOPLE`/`MAX_PEOPLE` (limites de input).

### Por que foi feito assim

- **`ask_float` aceita vírgula como separador decimal (`raw.replace(",", ".")`).** No teclado brasileiro é natural digitar "49,90", mas `float()` do Python só entende ponto. Normalizar a entrada antes de converter evita que todo mundo que testar o programa caia num erro bobo de formatação logo na primeira pergunta.
- **Menu de qualidade do atendimento com percentuais sugeridos + opção "Personalizado",** em vez de só pedir "digite o percentual de gorjeta" direto. Segue o mesmo padrão já usado em `number-guessing-game` (dificuldade) e `dice-rolling-simulator` (tipo de dado): dá uma sugestão sensata pra quem não sabe quanto dar de gorjeta, mas ainda permite controle total.
- **`format_currency` isolada numa função própria**, mesmo sendo só um f-string com `:.2f`, porque é usada em três lugares diferentes dentro de `print_summary` (conta, gorjeta, total) e potencialmente no valor por pessoa — centraliza o formato caso ele precise mudar (por exemplo, pra exibir o símbolo da moeda de outro jeito).
- **Divisão por pessoa só aparece no resumo se `people > 1`.** Dividir uma conta sozinho por "1 pessoa" é um resultado óbvio e repetitivo (seria o mesmo valor do total); escondê-lo nesse caso deixa a saída mais limpa sem perder a funcionalidade pra quem realmente for dividir a conta.
