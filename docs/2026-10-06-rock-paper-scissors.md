# 2026-10-06 (Rock, Paper, Scissors)

Projeto finalizado hoje: **Rock, Paper, Scissors**.

## Rock, Paper, Scissors

Arquivo: `rock-paper-scissors/rock_paper_scissors.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `ask_choice()` | Mostra o menu de opções (`CHOICES`: Pedra/Papel/Tesoura) e retorna a escolha do jogador. |
| `computer_choice()` | Sorteia a escolha do computador entre as mesmas opções. |
| `decide_winner(player, computer)` | Retorna `"player"`, `"computer"` ou `"draw"` com base na regra `BEATS`. |
| `print_round_result(player, computer, outcome)` | Imprime as escolhas de cada lado e o resultado da rodada. |
| `play_round()` | Executa uma rodada completa (pergunta, sorteia, decide e imprime) e retorna o resultado. |
| `main()` | Loop principal: chama `play_round()` repetidamente, mantém o placar de vitórias/derrotas/empates e pergunta se quer jogar de novo. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores), `CHOICES` (dicionário opção digitada → rótulo) e `BEATS` (dicionário rótulo → o que ele vence).

### Por que foi feito assim

- **`BEATS` como dicionário (`"Pedra": "Tesoura"`, etc.) em vez de uma cadeia de `if/elif` com as 9 combinações.** A regra do jogo é só "cada opção vence exatamente uma outra"; representar isso como dado permite que `decide_winner` seja só 3 linhas (empate, `BEATS[player] == computer`, senão computador venceu) em vez de testar as 9 combinações possíveis uma por uma.
- **`CHOICES` compartilhado entre `ask_choice()` e `computer_choice()`.** Tanto o menu mostrado ao jogador quanto o sorteio do computador usam a mesma fonte de opções — evita o risco de um dia alguém adicionar uma opção só de um lado e o jogo ficar com regras inconsistentes entre os dois.
