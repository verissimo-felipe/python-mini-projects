# 2026-10-10 (Contact Book)

Projeto finalizado hoje: **Contact Book**.

## Contact Book

Arquivo: `contact-book/contact_book.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `load_contacts()` | Carrega a lista de contatos do `contacts.json`. Retorna lista vazia se o arquivo não existir, e também se ele estiver corrompido (JSON inválido). |
| `save_contacts(contacts)` | Salva a lista inteira no `contacts.json`, formatada (`indent=2`) e legível. |
| `find_contact(contacts, name)` | Procura um contato pelo nome, sem diferenciar maiúsculas/minúsculas. Retorna o dict ou `None`. |
| `print_contact(contact)` | Imprime os dados de um único contato formatados. |
| `add_contact(contacts)` | Pergunta nome/telefone/e-mail e adiciona um novo contato, recusando nomes duplicados. |
| `list_contacts(contacts)` | Imprime todos os contatos, ordenados alfabeticamente pelo nome. |
| `search_contact(contacts)` | Pergunta um nome e mostra o contato correspondente, se existir. |
| `update_contact(contacts)` | Pergunta um nome e permite atualizar telefone/e-mail (Enter mantém o valor atual). |
| `delete_contact(contacts)` | Pergunta um nome, confirma e remove o contato correspondente. |
| `show_menu()` | Imprime o menu principal (`MENU`). |
| `main()` | Carrega os contatos uma vez no início, mostra o menu em loop e despacha pra cada função, salvando no JSON depois de qualquer operação que mude os dados. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `CONTACTS_FILE` (caminho do JSON, montado a partir da pasta do próprio script — funciona independente de onde o programa é chamado) e `MENU` (dicionário opção → rótulo).

### Por que foi feito assim

- **`CONTACTS_FILE` é montado com `os.path.dirname(__file__)`, não um caminho relativo simples (`"contacts.json"`).** Um caminho relativo dependeria de onde o programa foi chamado (`cd` até a pasta certa antes de rodar); montar o caminho a partir da localização do próprio script garante que o arquivo de dados sempre fica ao lado dele, não importa de onde o `python contact_book.py` foi disparado.
- **`load_contacts()` trata `json.JSONDecodeError` e devolve lista vazia, em vez de deixar o programa quebrar.** Um arquivo `.json` pode ficar corrompido por várias razões (um `Ctrl+C` no meio de uma escrita, edição manual malfeita); já que é um arquivo de dados "descartável" do ponto de vista do programa, recomeçar do zero é uma recuperação razoável, em vez de travar o app inteiro.
- **`find_contact` faz a busca sem diferenciar maiúsculas/minúsculas.** Pra um humano, "Ana" e "ana" são claramente a mesma pessoa; exigir que o usuário digite o nome com a capitalização exata seria uma fonte boba de "contato não encontrado".
- **`add_contact` recusa nomes duplicados**, usando o próprio `find_contact` pra checar antes de inserir. Sem essa checagem, seria possível ter dois contatos "João" na lista e `find_contact`/`update_contact`/`delete_contact` sempre acertariam só o primeiro, ignorando o segundo silenciosamente — a duplicata ficaria "invisível" pro resto do programa.
- **`save_contacts` só é chamado depois de operações que de fato mudaram algo** (`add_contact`, `update_contact` e `delete_contact` retornam `True`/`False` pra indicar isso) — listar ou buscar não precisa reescrever o arquivo em disco.
- **`contact-book/contacts.json` foi adicionado ao `.gitignore`.** É dado gerado pelo próprio programa em tempo de execução, não código-fonte — análogo ao motivo de `__pycache__/` já estar ignorado.
