# 2026-10-10 (Markdown Previewer)

Projeto finalizado hoje: **Markdown Previewer**.

Primeiro projeto do repositório com uma dependência de terceiros (biblioteca `markdown`, instalada via `requirements.txt` — ver `markdown-previewer/requirements.txt`).

## Markdown Previewer

Arquivo: `markdown-previewer/markdown_previewer.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `read_markdown_file(path)` | Lê e retorna o conteúdo de um arquivo `.md` como texto. |
| `convert_to_html(markdown_text)` | Converte o texto Markdown em HTML usando `markdown.markdown(...)`, com as extensões `extra` e `sane_lists` (tabelas, blocos de código com ```` ``` ````, listas, etc.). |
| `build_html_document(title, body_html)` | Encaixa o fragmento HTML convertido dentro de um documento completo (`HTML_TEMPLATE`), com um CSS simples pra ficar legível no navegador. |
| `write_html_file(path, html)` | Escreve a string HTML final num arquivo. |
| `derive_output_path(input_path)` | Deriva o caminho do `.html` de saída a partir do caminho do `.md` de entrada (troca a extensão). |
| `ask_markdown_path()` | Pergunta o caminho de um arquivo Markdown, repetindo até o arquivo existir de fato. |
| `ask_yes_no(prompt, default=True)` | Pergunta sim/não; Enter vazio usa o valor padrão. |
| `play_round()` | Encadeia os passos: pede o `.md`, lê, converte, monta o documento, salva o `.html` e pergunta se quer abrir no navegador (`webbrowser.open`). |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer converter outro arquivo. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `MARKDOWN_EXTENSIONS` (lista de extensões do python-markdown habilitadas) e `HTML_TEMPLATE` (template do documento HTML final).

### Por que foi feito assim

- **`convert_to_html` retorna só o fragmento do corpo, e `build_html_document` é quem monta o documento completo.** Separar as duas responsabilidades (conversão Markdown→HTML vs. montagem do HTML final) deixa `convert_to_html` testável isoladamente (só compara o fragmento contra o que se espera) sem precisar comparar documentos HTML inteiros no teste.
- **Extensões `extra` e `sane_lists` habilitadas**, em vez de usar `markdown.markdown()` sem argumentos. O Markdown "puro" (sem extensões) do python-markdown não entende tabelas nem listas numeradas fora de ordem do jeito que a maioria das pessoas escreve — como o objetivo é ser um previewer de verdade, faz sentido já habilitar o que cobre o Markdown mais comum do dia a dia.
- **`derive_output_path` troca só a extensão (`.md` → `.html`), salvando ao lado do arquivo de entrada**, em vez de perguntar um caminho de saída separado. Reduz uma pergunta a mais pro usuário no caso comum (quem tem `nota.md` normalmente quer `nota.html` do lado), sem impedir nada — quem quiser mover o arquivo depois, move.
- **`ask_markdown_path()` já valida que o arquivo existe antes de seguir**, em vez de deixar `read_markdown_file` estourar um `FileNotFoundError` sem tratamento. Como ler um arquivo que não existe é um erro bem comum de digitação de caminho, vale a pena resolver isso na validação do input em vez de precisar de try/except na leitura.
- **`requirements.txt` próprio do projeto, não um arquivo na raiz do repositório.** Como cada mini-projeto é autocontido (sem imports entre pastas), só este aqui precisa de uma dependência externa — colocar o `requirements.txt` dentro de `markdown-previewer/` deixa claro que é uma dependência só desse projeto, sem implicar que o repositório inteiro precisa dela.
