"""Contact Book (CLI).

Sistema simples de gerenciamento de contatos: adicionar, listar, buscar,
atualizar e remover, com os dados persistidos num arquivo JSON ao lado
do script.

Conceitos: dicionários, listas e leitura/escrita de arquivos (JSON).
"""

import json
import os

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Arquivo de dados ao lado do script, não importando de onde o programa é chamado.
CONTACTS_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")

MENU = {
    "1": "Adicionar contato",
    "2": "Listar contatos",
    "3": "Buscar contato",
    "4": "Atualizar contato",
    "5": "Remover contato",
    "6": "Sair",
}


def load_contacts():
    """Carrega a lista de contatos do arquivo JSON. Retorna lista vazia se não existir."""
    if not os.path.isfile(CONTACTS_FILE):
        return []
    try:
        with open(CONTACTS_FILE, encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"{RED}Arquivo de contatos corrompido; começando do zero.{RESET}")
        return []


def save_contacts(contacts):
    """Salva a lista de contatos no arquivo JSON, formatada e legível."""
    with open(CONTACTS_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=2, ensure_ascii=False)


def ask_text(prompt):
    """Lê um texto do usuário, repetindo a pergunta se vier em branco."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print(f"{RED}Digite alguma coisa — não pode ficar em branco.{RESET}")


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


def find_contact(contacts, name):
    """Procura um contato pelo nome (sem diferenciar maiúsculas/minúsculas). Retorna o dict ou None."""
    for contact in contacts:
        if contact["nome"].lower() == name.lower():
            return contact
    return None


def print_contact(contact):
    """Imprime os dados de um único contato formatados."""
    print(
        f"{BOLD}{contact['nome']}{RESET} — "
        f"Tel: {CYAN}{contact['telefone']}{RESET} — "
        f"E-mail: {CYAN}{contact['email']}{RESET}"
    )


def add_contact(contacts):
    """Pergunta nome, telefone e e-mail e adiciona um novo contato à lista."""
    nome = ask_text("\nNome: ")
    if find_contact(contacts, nome):
        print(f"{RED}Já existe um contato com esse nome.{RESET}")
        return False

    telefone = ask_text("Telefone: ")
    email = ask_text("E-mail: ")
    contacts.append({"nome": nome, "telefone": telefone, "email": email})
    print(f"{GREEN}Contato adicionado.{RESET}")
    return True


def list_contacts(contacts):
    """Imprime todos os contatos cadastrados, em ordem alfabética pelo nome."""
    if not contacts:
        print(f"\n{YELLOW}Nenhum contato cadastrado.{RESET}")
        return

    print(f"\n{BOLD}Contatos ({len(contacts)}):{RESET}")
    for contact in sorted(contacts, key=lambda c: c["nome"].lower()):
        print_contact(contact)


def search_contact(contacts):
    """Pergunta um nome e mostra o contato correspondente, se existir."""
    nome = ask_text("\nNome a buscar: ")
    contact = find_contact(contacts, nome)
    if contact:
        print_contact(contact)
    else:
        print(f"{RED}Nenhum contato encontrado com esse nome.{RESET}")


def update_contact(contacts):
    """Pergunta um nome e permite atualizar telefone/e-mail. Retorna True se algo mudou."""
    nome = ask_text("\nNome do contato a atualizar: ")
    contact = find_contact(contacts, nome)
    if not contact:
        print(f"{RED}Nenhum contato encontrado com esse nome.{RESET}")
        return False

    print("Deixe em branco e aperte Enter pra manter o valor atual.")
    novo_telefone = input(f"Telefone atual ({contact['telefone']}). Novo: ").strip()
    novo_email = input(f"E-mail atual ({contact['email']}). Novo: ").strip()

    if novo_telefone:
        contact["telefone"] = novo_telefone
    if novo_email:
        contact["email"] = novo_email

    print(f"{GREEN}Contato atualizado.{RESET}")
    return True


def delete_contact(contacts):
    """Pergunta um nome, confirma e remove o contato correspondente. Retorna True se removeu."""
    nome = ask_text("\nNome do contato a remover: ")
    contact = find_contact(contacts, nome)
    if not contact:
        print(f"{RED}Nenhum contato encontrado com esse nome.{RESET}")
        return False

    if ask_yes_no(f"Remover {contact['nome']} de verdade?", default=False):
        contacts.remove(contact)
        print(f"{GREEN}Contato removido.{RESET}")
        return True

    print(f"{YELLOW}Remoção cancelada.{RESET}")
    return False


def show_menu():
    """Imprime o menu principal."""
    print(f"\n{BOLD}O que você quer fazer?{RESET}")
    for key, label in MENU.items():
        print(f"  {CYAN}{key}{RESET} - {label}")


def main():
    print(f"{BOLD}{CYAN}=== Contact Book ==={RESET}")
    contacts = load_contacts()

    while True:
        show_menu()
        choice = input("Opção: ").strip()

        if choice == "1":
            if add_contact(contacts):
                save_contacts(contacts)
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            if update_contact(contacts):
                save_contacts(contacts)
        elif choice == "5":
            if delete_contact(contacts):
                save_contacts(contacts)
        elif choice == "6":
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break
        else:
            print(f"{RED}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
