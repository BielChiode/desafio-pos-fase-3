# ClearBank — Análise de Transações (Desafio Final · Fase 3)

Projeto do desafio final do módulo de Python para análise de dados. No papel
de **analista de dados júnior** da fintech fictícia **ClearBank**, o objetivo
é processar um arquivo de transações com dados "sujos": ler o CSV, **validar e
limpar** os registros, calcular **métricas mensais**, sinalizar **transações
suspeitas** (acima de R$ 10.000,00), exibir um relatório formatado no terminal
e exportar o resultado em `relatorio.json`.

## Stack

- **Python 3.10+** (testado em 3.12).
- Módulos **nativos**: `csv`, `json`, `datetime`, `collections`.
- **Opcionais**: `pandas` (RO1) e `matplotlib` (RO2).

```bash
pip install pandas matplotlib
```

## Como executar

### No Google Colab (recomendado)

1. Faça upload de `desafio-final.ipynb` **e** de `transacoes.csv`.
2. Menu **Ambiente de execução → Executar tudo**.
3. `pandas` e `matplotlib` já vêm instalados no Colab.

### No Jupyter local

```bash
cd desafio-pos-fase-3
pip install pandas matplotlib jupyter
jupyter notebook desafio-final.ipynb   # depois: Run → Run All Cells
```

### Análise com pandas via linha de comando (RO1)

```bash
python analise_pandas.py
```

## Saídas geradas

| Arquivo | Origem |
|---|---|
| `relatorio.json` | Gerado pela célula de execução principal do notebook |
| `grafico.png` | Gerado pela célula RO2 (matplotlib) |

> Esses dois arquivos **não** ficam versionados de antemão — são produzidos ao
> executar o notebook de ponta a ponta.

## Estrutura do repositório

```
desafio-pos-fase-3/
├── desafio-final.ipynb   # notebook principal (obrigatório)
├── transacoes.csv        # dataset de entrada (20 linhas: 15 válidas + 5 inválidas)
├── analise_pandas.py     # RO1 — análise alternativa com pandas (executável)
├── relatorio.json        # gerado pelo notebook
├── grafico.png           # gerado pelo notebook (RO2)
└── README.md             # este arquivo
```

## Regras de validação

Uma transação é considerada **válida** somente se passar em todas as regras:

| Campo | Regra |
|---|---|
| `id` | inteiro (apenas dígitos) |
| `cliente_id` | não vazio |
| `data` | formato `AAAA-MM-DD` (`datetime.strptime`) |
| `tipo` | `credito` ou `debito` |
| `valor` | número **positivo** (`> 0`) |

O dataset de exemplo inclui propositalmente 5 linhas inválidas — uma para cada
regra acima — para exercitar o tratamento de erros.

## Checklist de requisitos

**Obrigatórios**

- [x] Leitura de CSV com `csv.DictReader` (stdlib).
- [x] 6+ funções com responsabilidades separadas (`ler_transacoes`,
      `validar_data`, `validar_valor`, `validar_transacao`,
      `processar_transacoes`, `gerar_relatorio`, `salvar_json`,
      `exibir_relatorio`, `formatar_brl`).
- [x] 3 usos distintos de `try/except` específicos: `FileNotFoundError` na
      leitura, `ValueError` na conversão de data e na de valor.
- [x] Datas tratadas com `datetime.strptime` / `strftime`.
- [x] Métricas mensais: quantidade, total de crédito, total de débito, saldo,
      média, maior e menor transação.
- [x] Detecção de transações suspeitas (`LIMITE_SUSPEITO = 10000.00`).
- [x] Exportação para `relatorio.json` (`ensure_ascii=False, indent=2`).
- [x] Relatório formatado no terminal com separadores e valores em R$ (padrão BR).

**Opcionais**

- [x] **RO1** — análise mensal alternativa com `pandas` (notebook + `analise_pandas.py`).
- [x] **RO2** — gráfico de crédito vs débito por mês com `matplotlib` (`grafico.png`).
