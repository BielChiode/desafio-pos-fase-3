# Plano — Desafio Final ClearBank (Fase 3)

## Context

Desafio final do módulo de Python para análise de dados (fintech ClearBank).
Entrega obrigatória: um repositório público no GitHub `clearbank-analise`
contendo um notebook `.ipynb` que lê um CSV de transações (com sujeira),
valida/limpa os dados, calcula métricas mensais, sinaliza transações
suspeitas, exibe relatório formatado no terminal e exporta `relatorio.json`.

O diretório `/home/chiode/Projetos/personal-projects/desafio-pos-fase-3/`
está vazio — todo o projeto será criado do zero. O usuário optou por:
- Incluir **ambos** os opcionais (pandas + matplotlib).
- Estrutura com **células temáticas + célula principal** no notebook.
- Gerar o `transacoes.csv` **manualmente** com dados fixos.

Objetivo: um notebook executável de ponta a ponta no Colab/Jupyter, com
saídas salvas, atendendo a 100% dos requisitos obrigatórios + RO1 + RO2.

---

## Estrutura final do repositório

```
desafio-pos-fase-3/
├── desafio-final.ipynb     # notebook principal (obrigatório)
├── transacoes.csv          # dataset de entrada (criado manualmente)
├── relatorio.json          # gerado pelo notebook ao executar
├── analise_pandas.py       # RO1 — versão alternativa com pandas
├── grafico.png             # RO2 — gerado pelo notebook
└── README.md               # descrição do projeto
```

---

## Etapa 1 — Criar `transacoes.csv` manualmente

Arquivo com **20 linhas** (15 válidas + 5 inválidas), cobrindo:

- ≥ 3 meses distintos (jan/2026, fev/2026, mar/2026, abr/2026).
- ≥ 2 transações com valor acima de R$ 10.000,00 (suspeitas).
- 5 linhas inválidas cobrindo **cada caso de validação**:
  1. `id` não numérico (`"abc"`).
  2. `cliente_id` vazio.
  3. `data` mal formatada (ex.: `2026/02/30` ou `14-02-2026`).
  4. `tipo` inválido (ex.: `transferencia` no campo tipo).
  5. `valor` não numérico ou ≤ 0 (ex.: `abc`, `-50`, `0`).

Colunas exatas: `id,data,cliente_id,tipo,valor,descricao,categoria`.

---

## Etapa 2 — Estrutura do notebook `desafio-final.ipynb`

Sequência de células (markdown + código), uma por requisito, cada uma
seguida de um pequeno bloco de teste rápido. Célula final orquestra tudo.

### Célula 1 — Markdown: Cabeçalho e instruções
Título, descrição do desafio, como executar, requisitos atendidos.

### Célula 2 — Imports e constantes globais
```python
import csv
import json
from datetime import datetime, date
from collections import defaultdict

ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"
LIMITE_SUSPEITO = 10000.00
FORMATO_DATA = "%Y-%m-%d"
```

### Célula 3 — Função `ler_transacoes(caminho)`
- Abre o CSV via `with open(...)` + `csv.DictReader`.
- `try/except FileNotFoundError` → retorna lista vazia e avisa.
- Retorna lista de dicts crus (sem validação ainda).

### Célula 4 — Funções de validação
- `validar_data(texto)` → usa `datetime.strptime` com `try/except ValueError`.
- `validar_valor(texto)` → `float()` com `try/except ValueError`; rejeita ≤ 0.
- `validar_transacao(linha)` → aplica todas as regras (`id` int, `cliente_id`
  não vazio, `data`, `tipo` ∈ {`credito`,`debito`}, `valor` > 0).
  Retorna dict limpo + objeto `datetime` para a data, ou `None` se inválida.

Teste rápido: invocar com 3 linhas (1 válida + 2 inválidas) e imprimir o
resultado.

### Célula 5 — Função `processar_transacoes(linhas_brutas)`
- Itera, chama `validar_transacao`, separa em `validas` e `invalidas`.
- Retorna `(validas, total_lidas, total_invalidas)`.

### Célula 6 — Função `gerar_relatorio(validas)`
- Calcula período (data mais antiga e mais recente, `(max - min).days`).
- Agrupa por mês (`data.strftime("%Y-%m")`) usando `defaultdict`.
- Para cada mês calcula: quantidade, total_credito, total_debito, saldo,
  media, maior_valor (dict), menor_valor (dict).
- Filtra suspeitas: `valor > LIMITE_SUSPEITO`.
- Retorna dict com: `gerado_em`, `periodo`, `total_validas`,
  `total_invalidas`, `dias_periodo`, `resumo_mensal`, `suspeitas`.

### Célula 7 — Funções utilitárias de formato
- `formatar_brl(valor)` → padrão brasileiro com a técnica das dicas
  (`replace` triplo).

### Célula 8 — Função `salvar_json(relatorio, caminho)`
- `json.dump(..., ensure_ascii=False, indent=2, default=str)` para
  serializar `date`/`datetime` sem erro.

### Célula 9 — Função `exibir_relatorio(relatorio)`
- Imprime cabeçalho com separadores `=====`.
- Mostra período (mais antiga → mais recente) e contagem válidas/inválidas.
- Para cada mês: bloco formatado conforme exemplo do enunciado.
- Lista transações suspeitas ou `"Nenhuma transação suspeita encontrada."`.

### Célula 10 — **Célula de Execução Principal**
Orquestra:
```python
brutas = ler_transacoes(ARQUIVO_CSV)
validas, total_lidas, total_invalidas = processar_transacoes(brutas)
print(f"Total de linhas lidas: {total_lidas}")
print(f"Linhas válidas: {len(validas)}")
print(f"Linhas inválidas: {total_invalidas}")
relatorio = gerar_relatorio(validas)
relatorio["total_transacoes_invalidas"] = total_invalidas
salvar_json(relatorio, ARQUIVO_JSON)
exibir_relatorio(relatorio)
```

### Célula 11 — Markdown: RO1 — pandas
Explicação curta + execução de `analise_pandas.py` para comparar.

### Célula 12 — Código RO1
- `import pandas as pd`.
- `pd.read_csv` + limpeza equivalente (dropna, conversões com `errors="coerce"`).
- `groupby` mensal calculando as mesmas métricas.
- Imprime o DataFrame agrupado e confirma igualdade dos saldos com a solução
  nativa (mesmo opcional, é interessante manter no notebook).

### Célula 13 — Markdown: RO2 — matplotlib
### Célula 14 — Código RO2
- Gráfico de **barras empilhadas crédito vs débito por mês** (opção C).
- Título, rótulos nos eixos, legenda.
- `plt.savefig("grafico.png", bbox_inches="tight")`.
- `plt.show()`.

---

## Etapa 3 — `analise_pandas.py` (RO1)

Script independente que reproduz a análise mensal com pandas. Executável
via `python analise_pandas.py`. Importado/exibido pela Célula 12 do
notebook, mas funcional como CLI.

Conteúdo:
- `pd.read_csv("transacoes.csv")`.
- Conversões com `pd.to_numeric(..., errors="coerce")` e
  `pd.to_datetime(..., format="%Y-%m-%d", errors="coerce")`.
- Filtro de validade equivalente ao do notebook.
- `df.groupby(df["data"].dt.strftime("%Y-%m"))` para métricas.
- `print` do DataFrame agrupado.

---

## Etapa 4 — `README.md`

Conteúdo mínimo:
- Título e descrição (analista jr na fintech ClearBank).
- Stack: Python 3.10+, módulos nativos (`csv`, `json`, `datetime`), pandas
  e matplotlib (opcionais).
- Como executar (Colab ou Jupyter local; comando `pip install pandas
  matplotlib`).
- Saídas geradas: `relatorio.json` e `grafico.png`.
- Estrutura do repositório.
- Checklist de requisitos obrigatórios + opcionais cobertos.

---

## Tratamento de erros (`try/except`) — onde aparece

Cobre os 3 pontos exigidos pelo enunciado:
1. **`ler_transacoes`** → `FileNotFoundError` ao abrir o CSV.
2. **`validar_valor`** → `ValueError` ao converter `float(linha["valor"])`.
3. **`validar_data`** → `ValueError` ao `datetime.strptime(...)`.

Sempre captura exceção específica (não `except:` genérico).

---

## Verificação end-to-end

Após implementar:

1. `cd /home/chiode/Projetos/personal-projects/desafio-pos-fase-3`.
2. Abrir o notebook no Jupyter local (ou Colab) e executar **Run All**.
3. Conferir saída da célula principal:
   - "Total de linhas lidas: 20", "Linhas válidas: 15", "Linhas inválidas: 5".
   - Relatório mensal com pelo menos 3 meses.
   - Pelo menos 2 transações listadas em "TRANSAÇÕES SUSPEITAS".
4. Conferir que `relatorio.json` foi criado com a estrutura esperada
   (`gerado_em`, `total_transacoes_validas`, `total_transacoes_invalidas`,
   `resumo_mensal`, `suspeitas`).
5. Rodar `python analise_pandas.py` separadamente e comparar os saldos
   mensais com o relatório nativo — devem ser idênticos.
6. Conferir que `grafico.png` foi gerado (mesma execução do notebook).
7. Salvar notebook com as saídas (`File → Save` no Colab / `Ctrl+S` no
   Jupyter).

Critérios de aceitação (checklist do enunciado):
- [x] ≥ 4 funções com responsabilidades separadas
  (`ler_transacoes`, `validar_transacao`, `processar_transacoes`,
  `gerar_relatorio`, `salvar_json`, `exibir_relatorio`, + utilitárias).
- [x] ≥ 3 usos distintos de `try/except`.
- [x] CSV lido com `csv.DictReader` nativo.
- [x] Datas via `datetime.strptime` / `strftime`.
- [x] Métricas mensais completas (qtd, crédito, débito, saldo, média,
  maior, menor).
- [x] `LIMITE_SUSPEITO = 10000.00` + lista de suspeitas.
- [x] `relatorio.json` com `ensure_ascii=False, indent=2`.
- [x] Relatório formatado no terminal com separadores e R$ no padrão BR.
- [x] RO1 (pandas) e RO2 (matplotlib) ambos implementados.

---

## Critical files a serem criados

| Arquivo | Propósito |
|---|---|
| `transacoes.csv` | Dataset de entrada (manual, 20 linhas) |
| `desafio-final.ipynb` | Notebook principal com todas as células |
| `analise_pandas.py` | RO1 — versão pandas executável |
| `README.md` | Documentação do repositório |
| `relatorio.json` | Gerado pela execução do notebook |
| `grafico.png` | Gerado pela execução do notebook (RO2) |

Nada a reutilizar: o diretório está vazio. Toda a implementação é nova.
