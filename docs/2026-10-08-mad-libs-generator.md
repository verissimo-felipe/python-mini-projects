# 2026-10-08 (Mad Libs Generator)

Projeto finalizado hoje: **Mad Libs Generator**.

## Mad Libs Generator

Arquivo: `mad-libs-generator/mad_libs_generator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `build_space_story(...)` / `build_school_story(...)` / `build_party_story(...)` | Cada uma recebe as palavras já coletadas como parâmetros nomeados e retorna o texto final da história montado com f-strings. |
| `ask_text(prompt)` | Lê uma palavra do usuário, repetindo a pergunta se vier em branco. |
| `choose_story()` | Mostra o menu de histórias (`STORIES`) e retorna `(título, campos, função de montagem)` escolhida. |
| `collect_words(fields)` | Pergunta uma palavra pra cada campo da história escolhida e retorna um dict `nome_do_parâmetro -> palavra`. |
| `play_round()` | Escolhe a história, coleta as palavras e monta/imprime o resultado final. |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer criar outra história. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores) e `STORIES` (dicionário opção → `(título, lista de campos, função que monta a história)`).

### Por que foi feito assim

- **Cada história é uma função que retorna uma f-string literal, em vez de um texto genérico com `.format(**words)`.** O conceito-chave do projeto no README é especificamente "f-strings" — escrever `build_space_story(adjetivo1, substantivo1, ...)` com os parâmetros nomeados deixa o encaixe das palavras explícito no próprio código da história, e não só num dicionário genérico.
- **`STORIES` guarda, junto do título, a lista de campos a perguntar *e* a função que monta o texto.** Isso mantém cada história autocontida: `collect_words` não precisa saber nada sobre o conteúdo da história, só a lista de `(nome_do_parâmetro, pergunta)` — e `play_round()` só repassa o dict coletado direto pra função via `**words`, que bate com os parâmetros nomeados de cada `build_*_story`.
- **`ask_text` rejeita entrada em branco.** Num Mad Libs, uma palavra vazia faria a história sair com buracos ("o(a) " sem nada depois); validar isso na hora da pergunta evita um resultado final estranho sem precisar tratar strings vazias depois.
