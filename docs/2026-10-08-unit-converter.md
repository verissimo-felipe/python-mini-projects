# 2026-10-08 (Unit Converter)

Projeto finalizado hoje: **Unit Converter**.

## Unit Converter

Arquivo: `unit-converter/unit_converter.py`

### O que o código faz

| Função | O que faz |
|---|---|
| `celsius_to_fahrenheit` / `fahrenheit_to_celsius` / `celsius_to_kelvin` / `kelvin_to_celsius` | Fórmulas de conversão de temperatura. |
| `meters_to_feet` / `feet_to_meters` / `km_to_miles` / `miles_to_km` | Fórmulas de conversão de distância. |
| `kg_to_lb` / `lb_to_kg` | Fórmulas de conversão de peso. |
| `ask_float(prompt)` | Lê um número decimal do usuário, repetindo a pergunta se a conversão falhar. Aceita vírgula ou ponto como separador decimal. |
| `choose_from_menu(prompt, options)` | Menu numerado genérico: mostra as opções de um dict e retorna o item escolhido. Usado para escolher a categoria (Temperatura/Distância/Peso). |
| `choose_conversion(conversions)` | Mostra o menu de conversões de uma categoria (`"Origem → Destino"`) e retorna `(unidade_origem, unidade_destino, função)`. |
| `play_round()` | Encadeia os três passos: escolhe categoria, escolhe conversão, pede o valor e mostra o resultado. |
| `main()` | Loop principal: chama `play_round()` repetidamente e pergunta se quer converter de novo. |

Constantes de suporte: `RESET/GREEN/RED/YELLOW/CYAN/BOLD` (cores ANSI, mesmo padrão dos projetos anteriores) e `CATEGORIES` (dicionário categoria → `(rótulo, dict de conversões)`, cada conversão sendo `(unidade_origem, unidade_destino, função)`).

### Por que foi feito assim

- **Cada fórmula de conversão é uma função própria e pura (só recebe o valor, só retorna o resultado), sem nenhuma lógica de menu/input dentro.** Isso deixa as fórmulas em si triviais de testar isoladamente (como foi feito no smoke test, comparando com valores de referência conhecidos: 0°C = 32°F, 1 m ≈ 3.28084 ft, etc.) e completamente desacopladas de como o usuário chega até elas.
- **`CATEGORIES` é um dicionário de dicionários** (categoria → conversões → `(origem, destino, função)`), em vez de um menu só e achatado com todas as conversões juntas. Isso evita uma lista enorme e confusa de opções (temperatura, distância e peso misturados) e deixa claro que escolher a categoria primeiro restringe as opções da segunda pergunta.
- **`choose_from_menu` é genérico (funciona com qualquer dict cujo item seja uma tupla com rótulo na posição 0, ou uma string)**, reaproveitado só para escolher a categoria — enquanto `choose_conversion` tem seu próprio formato de exibição (`"Origem → Destino"`) porque o rótulo de cada conversão não é um texto solto, é montado a partir dos dois nomes de unidade.
- **Testes de ida-e-volta** (ex.: Celsius → Fahrenheit → Celsius) no smoke test, além dos valores de referência isolados — confirma que as duas fórmulas de cada par são realmente inversas uma da outra, não só que cada uma bate com um valor conhecido isoladamente.
