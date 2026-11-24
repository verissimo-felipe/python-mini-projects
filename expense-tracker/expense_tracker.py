"""Expense Tracker (CLI).

Registra gastos (data, categoria, valor e descrição), lista os
lançamentos e mostra um resumo com estatísticas básicas: total gasto,
média por lançamento, maior gasto, e o total por categoria e por mês.
Os dados persistem num arquivo CSV ao lado do script.

Conceitos: leitura/escrita de arquivos (CSV), dicionários e estatísticas
básicas (soma, média, máximo, agrupamento).
"""

import csv
import datetime
import os

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Arquivo de dados ao lado do script, não importando de onde o programa é chamado.
EXPENSES_FILE = os.path.join(os.path.dirname(__file__), "expenses.csv")
FIELDNAMES = ["data", "categoria", "valor", "descricao"]

CATEGORIES = ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"]

MENU = {
    "1": "Adicionar gasto",
    "2": "Listar gastos",
    "3": "Ver resumo (por categoria e por mês)",
    "4": "Remover gasto",
    "5": "Sair",
}


def load_expenses():
    """Carrega os gastos do arquivo CSV. Retorna lista vazia se não existir ou estiver corrompido."""
    if not os.path.isfile(EXPENSES_FILE):
        return []
    try:
        with open(EXPENSES_FILE, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return [
                {
                    "data": row["data"],
                    "categoria": row["categoria"],
                    "valor": float(row["valor"]),
                    "descricao": row["descricao"],
                }
                for row in reader
            ]
    except (csv.Error, ValueError, KeyError):
        print(f"{RED}Arquivo de gastos corrompido; começando do zero.{RESET}")
        return []


def save_expenses(expenses):
    """Salva a lista de gastos no arquivo CSV."""
    with open(EXPENSES_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


def ask_text(prompt):
    """Lê um texto do usuário, repetindo a pergunta se vier em branco."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print(f"{RED}Digite alguma coisa — não pode ficar em branco.{RESET}")


def ask_positive_float(prompt):
    """Lê um número decimal maior que zero. Aceita vírgula ou ponto como separador decimal."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print(f"{RED}Digite um número válido (ex.: 25.90).{RESET}")
            continue
        if value <= 0:
            print(f"{RED}O valor deve ser maior que zero.{RESET}")
            continue
        return value


def ask_date_with_default_today(prompt):
    """Pergunta uma data no formato AAAA-MM-DD. Enter em branco usa a data de hoje."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return datetime.date.today()
        try:
            return datetime.date.fromisoformat(raw)
        except ValueError:
            print(f"{RED}Use o formato AAAA-MM-DD (ex.: 2026-11-24).{RESET}")


def ask_yes_no(prompt, default=True):
    """Pergunta sim/não. Enter vazio usa o valor padrão (`default`)."""
    suffix = "S/n" if default else "s/N"
    while True:
        raw = input(f"{prompt} ({suffix}): ").strip().lower()
        if raw == "":
            return default
        if raw in ("s", "sim", "y", "yes"):
            return True
        if raw in ("n", "nao", "não", "no"):
            return False
        print(f"{RED}Responda com 's' ou 'n'.{RESET}")


def ask_expense_number(expenses, prompt):
    """Pede o número de um gasto (1-based) e retorna o índice (0-based) correspondente."""
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
        except ValueError:
            print(f"{RED}Digite um número inteiro.{RESET}")
            continue
        if not 1 <= number <= len(expenses):
            print(f"{RED}Escolha um número entre 1 e {len(expenses)}.{RESET}")
            continue
        return number - 1


def choose_category():
    """Mostra o menu de categorias e retorna a categoria escolhida."""
    print(f"\n{BOLD}Categoria:{RESET}")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"  {CYAN}{index}{RESET} - {category}")

    while True:
        raw = input("Opção: ").strip()
        try:
            index = int(raw)
        except ValueError:
            print(f"{RED}Digite um número inteiro.{RESET}")
            continue
        if 1 <= index <= len(CATEGORIES):
            return CATEGORIES[index - 1]
        print(f"{RED}Escolha um número entre 1 e {len(CATEGORIES)}.{RESET}")


def format_expense(index, expense):
    """Formata uma linha de exibição pra um gasto."""
    return (
        f"{CYAN}{index}{RESET}. {expense['data']} — {BOLD}{expense['categoria']}{RESET} — "
        f"{YELLOW}R$ {expense['valor']:.2f}{RESET} — {expense['descricao']}"
    )


def add_expense(expenses):
    """Pergunta data, categoria, valor e descrição e adiciona um novo gasto."""
    data = ask_date_with_default_today("\nData (AAAA-MM-DD, Enter = hoje): ")
    categoria = choose_category()
    valor = ask_positive_float("Valor (R$): ")
    descricao = ask_text("Descrição: ")

    expenses.append({"data": data.isoformat(), "categoria": categoria, "valor": valor, "descricao": descricao})
    print(f"{GREEN}Gasto adicionado.{RESET}")


def list_expenses(expenses):
    """Imprime todos os gastos, ordenados por data."""
    if not expenses:
        print(f"\n{YELLOW}Nenhum gasto cadastrado.{RESET}")
        return

    ordered = sorted(expenses, key=lambda e: e["data"])
    print(f"\n{BOLD}Gastos ({len(ordered)}):{RESET}")
    for index, expense in enumerate(ordered, start=1):
        print(format_expense(index, expense))


def group_by_category(expenses):
    """Retorna um dict categoria -> soma dos valores daquela categoria."""
    totals = {}
    for expense in expenses:
        totals[expense["categoria"]] = totals.get(expense["categoria"], 0.0) + expense["valor"]
    return totals


def group_by_month(expenses):
    """Retorna um dict 'AAAA-MM' -> soma dos valores daquele mês."""
    totals = {}
    for expense in expenses:
        month = expense["data"][:7]
        totals[month] = totals.get(month, 0.0) + expense["valor"]
    return totals


def show_summary(expenses):
    """Mostra estatísticas básicas: total, média, maior gasto, e totais por categoria e por mês."""
    if not expenses:
        print(f"\n{YELLOW}Nenhum gasto cadastrado.{RESET}")
        return

    total = sum(expense["valor"] for expense in expenses)
    average = total / len(expenses)
    biggest = max(expenses, key=lambda e: e["valor"])

    print(f"\n{BOLD}Total gasto: {RED}R$ {total:.2f}{RESET} em {len(expenses)} lançamento(s)")
    print(f"Média por lançamento: {YELLOW}R$ {average:.2f}{RESET}")
    print(
        f"Maior gasto individual: {YELLOW}R$ {biggest['valor']:.2f}{RESET} "
        f"({biggest['categoria']} — {biggest['descricao']}, {biggest['data']})"
    )

    print(f"\n{BOLD}Por categoria:{RESET}")
    by_category = group_by_category(expenses)
    for category, subtotal in sorted(by_category.items(), key=lambda item: item[1], reverse=True):
        percentage = (subtotal / total) * 100
        print(f"  {category}: {CYAN}R$ {subtotal:.2f}{RESET} ({percentage:.1f}%)")

    print(f"\n{BOLD}Por mês:{RESET}")
    by_month = group_by_month(expenses)
    for month, subtotal in sorted(by_month.items()):
        print(f"  {month}: {CYAN}R$ {subtotal:.2f}{RESET}")


def delete_expense(expenses):
    """Pergunta qual gasto, confirma e remove. Retorna True se removeu."""
    if not expenses:
        print(f"\n{YELLOW}Nenhum gasto cadastrado.{RESET}")
        return False

    list_expenses(expenses)
    ordered = sorted(expenses, key=lambda e: e["data"])
    index = ask_expense_number(ordered, "\nNúmero do gasto a remover: ")
    expense = ordered[index]

    if ask_yes_no(f"Remover o gasto '{expense['descricao']}' ({expense['data']}) de verdade?", default=False):
        expenses.remove(expense)
        print(f"{GREEN}Gasto removido.{RESET}")
        return True

    print(f"{YELLOW}Remoção cancelada.{RESET}")
    return False


def show_menu():
    """Imprime o menu principal."""
    print(f"\n{BOLD}O que você quer fazer?{RESET}")
    for key, label in MENU.items():
        print(f"  {CYAN}{key}{RESET} - {label}")


def main():
    print(f"{BOLD}{CYAN}=== Expense Tracker ==={RESET}")
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Opção: ").strip()

        if choice == "1":
            add_expense(expenses)
            save_expenses(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            if delete_expense(expenses):
                save_expenses(expenses)
        elif choice == "5":
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break
        else:
            print(f"{RED}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
