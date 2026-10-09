# 2026-10-08 (Simple Calculator)

Projeto finalizado hoje: **Simple Calculator**.

## Simple Calculator

Arquivo: `simple-calculator/simple_calculator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `add(a, b)` / `subtract(a, b)` / `multiply(a, b)` / `divide(a, b)` | Cada uma implementa uma das quatro operações básicas. `divide` não trata nada sozinha — deixa o `ZeroDivisionError` subir pra quem chamar. |
| `ask_float(prompt)` | Lê um número decimal do usuário, repetindo a pergunta se a conversão falhar. Aceita vírgula ou ponto como separador decimal. |
| `choose_operation()` | Mostra o menu de operações (`OPERATIONS`) e retorna `(rótulo, símbolo, função)` escolhida. |
| `calculate(a, b, operation_func)` | Chama `operation_func(a, b)` dentro de um `try/except ZeroDivisionError`, retornando `None` (e avisando o usuário) se a divisão por zero acontecer. |
| `play_round()` | Pergunta os dois números e a operação, calcula e mostra o resultado (ou nada, se `calculate` retornou `None`). |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer fazer outro cálculo. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores) e `OPERATIONS` (dicionário opção → `(rótulo, símbolo, função)`).

### Por que foi feito assim

- **`divide` não tem `try/except` dentro dela — quem trata o erro é `calculate`.** Cada uma das quatro funções de operação faz só a conta, sem se preocupar com validação; isso é o que o conceito-chave "funções" pede: unidades pequenas e previsíveis. O tratamento de exceção fica centralizado em um único lugar (`calculate`), que funciona pra qualquer operação passada a ele, não só pra divisão — mesmo sendo a única que de fato pode lançar erro com números válidos.
- **`OPERATIONS` guarda a função de cada operação junto do rótulo e do símbolo.** Isso deixa `choose_operation()` e `calculate()` genéricos: nenhum dos dois precisa saber qual operação foi escolhida, só executam o que veio no dicionário — adicionar uma quinta operação no futuro seria só adicionar uma entrada nova, sem tocar na lógica de `calculate`.
- **`ask_float` aceita vírgula como separador decimal**, reaproveitando a mesma validação já usada no `tip-calculator` e no `bmi-calculator`, pela mesma razão: no teclado brasileiro "3,5" é mais natural de digitar que "3.5".
