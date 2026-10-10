"""Markdown Previewer (CLI).

Lê um arquivo Markdown (.md), converte o conteúdo para HTML e salva o
resultado num arquivo .html pronto pra abrir no navegador.

Conceitos: biblioteca `markdown` (terceiros — requer `pip install markdown`,
ver requirements.txt), leitura/escrita de arquivos e geração de HTML.
"""

import os
import webbrowser

import markdown

# --- Cores ANSI (reaproveitando o conceito do projeto ansi-color-chart-generator) ---
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"

# Extensões do python-markdown que cobrem o Markdown mais usado no dia a dia
# (tabelas, blocos de código com ```, listas de tarefas, etc.).
MARKDOWN_EXTENSIONS = ["extra", "sane_lists"]

# Template do documento HTML final, com um CSS simples pra ficar legível
# direto no navegador, sem depender de nenhum arquivo externo.
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
    body {{
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
        font-family: -apple-system, Segoe UI, Arial, sans-serif;
        line-height: 1.6;
        color: #1a1a1a;
    }}
    code, pre {{
        background: #f2f2f2;
        border-radius: 4px;
        padding: 2px 6px;
    }}
    pre code {{
        display: block;
        padding: 12px;
        overflow-x: auto;
    }}
    table {{
        border-collapse: collapse;
    }}
    th, td {{
        border: 1px solid #ccc;
        padding: 6px 10px;
    }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def read_markdown_file(path):
    """Lê e retorna o conteúdo de um arquivo Markdown como texto."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def convert_to_html(markdown_text):
    """Converte texto Markdown em HTML (só o fragmento do corpo, sem <html>/<head>)."""
    return markdown.markdown(markdown_text, extensions=MARKDOWN_EXTENSIONS)


def build_html_document(title, body_html):
    """Monta o documento HTML completo a partir do fragmento convertido."""
    return HTML_TEMPLATE.format(title=title, body=body_html)


def write_html_file(path, html):
    """Escreve a string HTML num arquivo."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)


def derive_output_path(input_path):
    """Deriva o caminho do .html de saída a partir do caminho do .md de entrada."""
    base, _ = os.path.splitext(input_path)
    return f"{base}.html"


def ask_markdown_path():
    """Pergunta o caminho de um arquivo Markdown, repetindo até ele existir."""
    while True:
        raw = input("\nCaminho do arquivo Markdown (.md): ").strip()
        if os.path.isfile(raw):
            return raw
        print(f"{RED}Arquivo não encontrado: {raw}{RESET}")


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


def play_round():
    """Pede um arquivo .md, converte para HTML e salva (abrindo no navegador se o usuário quiser)."""
    input_path = ask_markdown_path()
    markdown_text = read_markdown_file(input_path)
    body_html = convert_to_html(markdown_text)

    title = os.path.basename(input_path)
    html_document = build_html_document(title, body_html)

    output_path = derive_output_path(input_path)
    write_html_file(output_path, html_document)
    print(f"{GREEN}Preview gerado:{RESET} {output_path}")

    if ask_yes_no("Abrir no navegador agora?"):
        webbrowser.open(f"file://{os.path.abspath(output_path)}")


def main():
    print(f"{BOLD}{CYAN}=== Markdown Previewer ==={RESET}")

    while True:
        play_round()
        again = input("\nConverter outro arquivo? (s/n): ").strip().lower()
        if again not in ("s", "sim", "y", "yes"):
            print(f"\n{CYAN}Até a próxima! 👋{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CYAN}Encerrado. Até mais!{RESET}")
