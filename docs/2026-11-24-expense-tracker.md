# 2026-11-24 (Expense Tracker)

Projeto finalizado hoje: **Expense Tracker**.

## Expense Tracker

Arquivo: `expense-tracker/expense_tracker.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `load_expenses()` | Carrega os gastos do `expenses.csv` via `csv.DictReader`, convertendo `valor` pra `float`. Retorna lista vazia se o arquivo não existir ou estiver corrompido (incluindo um `valor` não numérico). |
| `save_expenses(expenses)` | Salva a lista inteira no `expenses.csv` via `csv.DictWriter`, com cabeçalho. |
| `ask_text` / `ask_positive_float` / `ask_date_with_default_today` / `ask_yes_no` / `ask_expense_number` | Helpers de validação de input, nos mesmos padrões já usados nos projetos anteriores (vírgula como separador decimal, Enter pra usar um padrão, etc.). |
| `choose_category()` | Mostra o menu de categorias (`CATEGORIES`) e retorna a escolhida. |
| `format_expense(index, expense)` | Formata a linha de exibição de um gasto. |
| `add_expense(expenses)` | Pergunta data (padrão hoje), categoria, valor e descrição, e adiciona o gasto. |
| `list_expenses(expenses)` | Imprime todos os gastos, ordenados por data. |
| `group_by_category(expenses)` / `group_by_month(expenses)` | Retornam, respectivamente, um dict categoria → soma e um dict `"AAAA-MM"` → soma. |
| `show_summary(expenses)` | Mostra as estatísticas: total gasto, média por lançamento, maior gasto individual, e os totais por categoria (com %) e por mês. |
| `delete_expense(expenses)` | Lista os gastos, pergunta qual remover (por número) e confirma antes de remover. |
| `show_menu()` | Imprime o menu principal (`MENU`). |
| `main()` | Carrega os gastos uma vez no início, mostra o menu em loop e despacha pra cada função, salvando no CSV depois de qualquer operação que mude os dados. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI), `EXPENSES_FILE`/`FIELDNAMES` (caminho e colunas do CSV), `CATEGORIES` (lista fixa de categorias) e `MENU` (dicionário opção → rótulo).

### Por que foi feito assim

- **CSV em vez de JSON, diferente do Contact Book e do To-Do List.** O conceito-chave deste projeto no README é especificamente "File I/O (CSV)" — gastos são, por natureza, dados tabulares (mesmas colunas em toda linha: data, categoria, valor, descrição), que é exatamente o formato que CSV representa bem e que também abre direto numa planilha, caso a pessoa queira analisar os dados fora do programa.
- **`group_by_category`/`group_by_month` usam `dict.get(chave, 0.0)` pra acumular, em vez de checar `if chave in dict` antes.** É o padrão mais direto pra "somar valores agrupados por chave" em Python: não precisa de um `if/else` a mais só pra inicializar a primeira ocorrência de cada categoria/mês.
- **`show_summary` calcula total, média e maior gasto com as próprias funções nativas do Python (`sum`, `len`, `max` com `key=`), sem importar um módulo de estatística.** Pelo mesmo motivo do `dice-rolling-simulator`: o README não lista nenhuma biblioteca de estatística entre as usadas no repositório, e essas três contas não precisam de nada além do que já vem embutido na linguagem.
- **`group_by_month` agrupa pelo prefixo `"AAAA-MM"` da data (`data[:7]`), não por um campo de mês separado.** Guardar a data inteira em formato ISO já é suficiente pra derivar o mês quando precisar — duplicar essa informação em dois campos só criaria a possibilidade de ficarem inconsistentes entre si.
- **`expense-tracker/expenses.csv` foi adicionado ao `.gitignore`**, pela mesma razão do `contacts.json` e do `tasks.json`: é dado gerado pelo programa em tempo de execução, não código-fonte.
