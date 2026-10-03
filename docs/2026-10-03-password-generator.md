# 2026-10-03 (Password Generator)

Projeto finalizado hoje: **Password Generator**.

## Password Generator

Arquivo: `password-generator/password_generator.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `ask_int(prompt, low, high)` | Lê um inteiro do usuário garantindo que esteja em `[low, high]`, repetindo a pergunta em caso de valor inválido. |
| `ask_yes_no(prompt, default=True)` | Pergunta sim/não; Enter vazio usa o valor padrão. Aceita variações (`s`, `sim`, `y`, `yes`, `n`, `nao`, `não`, `no`). |
| `choose_character_sets()` | Pergunta, um a um, se cada tipo de caractere (`CHARACTER_SETS`) deve entrar na senha; retorna a lista dos tipos escolhidos. Se nada for escolhido, cai no padrão (letras minúsculas). |
| `generate_password(length, chosen_sets)` | Monta a senha final: garante 1 caractere de cada tipo escolhido e completa o restante do tamanho sorteando do conjunto combinado; embaralha tudo no final. |
| `main()` | Loop principal: pergunta os tipos de caractere, pergunta o tamanho (respeitando um mínimo que depende de quantos tipos foram escolhidos), gera e mostra a senha, e pergunta se quer gerar outra. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `CHARACTER_SETS` (dicionário tipo → (nome exibido, string de caracteres), usando as constantes do módulo `string`: `ascii_lowercase`, `ascii_uppercase`, `digits`, `punctuation`), `MIN_LENGTH_FLOOR`/`MAX_LENGTH` (limites de tamanho da senha) e `_rng` (instância de `random.SystemRandom()`).

### Por que foi feito assim

- **`random.SystemRandom()` em vez de `random.random()`/`random.choice()` do módulo padrão.** O gerador padrão do Python (Mersenne Twister) é determinístico e, com informação suficiente sobre as saídas, previsível — ótimo para jogos e simulações, ruim para senhas. `SystemRandom` lê de `os.urandom()`, a fonte de aleatoriedade do próprio sistema operacional, a mesma classe de fonte usada em contextos criptográficos. Mesmo sendo um "mini-projeto de estudo", a senha gerada é usável de verdade, então vale a pena fazer esse detalhe certo.
- **Garantir 1 caractere de cada tipo escolhido, em vez de sortear tudo do pool combinado.** Se a senha fosse gerada só com `"".join(rng.choice(pool) for _ in range(length))`, nada impediria que, por azar estatístico (mais comum em senhas curtas), ela saísse só com letras minúsculas mesmo o usuário tendo pedido números e símbolos também. Sortear 1 de cada tipo primeiro e só depois completar o restante garante que a "complexidade" pedida realmente apareça na senha — e embaralhar no final evita o padrão óbvio de "sempre começa com minúscula, depois maiúscula, depois número...".
- **`min_length` depende da quantidade de tipos escolhidos (`max(MIN_LENGTH_FLOOR, len(chosen_sets))`).** Como a lógica acima exige 1 caractere garantido por tipo, uma senha de tamanho 2 com os 4 tipos marcados seria impossível de cumprir a garantia. Em vez de deixar isso quebrar o programa, o tamanho mínimo pedido ao usuário já reflete essa restrição.
- **`choose_character_sets()` cai para "letras minúsculas" se nada for escolhido**, em vez de gerar uma senha vazia ou travar o programa — evita um estado inválido sem precisar de tratamento de erro extra em `generate_password`.
- **List comprehensions em `generate_password` e `choose_character_sets`** (em vez de loops `for` com `.append()`) seguem o conceito-chave do projeto listado no README e deixam explícito que cada linha produz uma lista nova a partir de uma coleção existente (os tipos escolhidos, ou as posições restantes da senha).
