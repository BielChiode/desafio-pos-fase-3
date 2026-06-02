"""RO1 — Análise mensal de transações com pandas.

Reproduz a análise feita com Python nativo no notebook `desafio-final.ipynb`,
usando pandas. Os saldos mensais resultantes devem ser idênticos aos da
solução nativa.

Uso:
    python analise_pandas.py
"""

import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
LIMITE_SUSPEITO = 10000.00
FORMATO_DATA = "%Y-%m-%d"
TIPOS_VALIDOS = {"credito", "debito"}


def carregar_e_limpar(caminho=ARQUIVO_CSV):
    """Lê o CSV e aplica as mesmas regras de validação do notebook.

    Retorna um DataFrame apenas com as transações válidas e com as colunas
    `id`, `data` (datetime), `cliente_id`, `tipo`, `valor` (float),
    `descricao` e `categoria` já convertidas.
    """
    df = pd.read_csv(caminho, dtype=str)

    # Conversões com coerção: valores inválidos viram NaN/NaT.
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data"] = pd.to_datetime(df["data"], format=FORMATO_DATA, errors="coerce")

    # cliente_id vazio (string vazia ou só espaços) vira NaN.
    df["cliente_id"] = df["cliente_id"].str.strip()
    df.loc[df["cliente_id"] == "", "cliente_id"] = pd.NA

    # tipo normalizado.
    df["tipo"] = df["tipo"].str.strip().str.lower()

    # Regras de validade equivalentes às de validar_transacao():
    valido = (
        df["id"].notna()
        & df["data"].notna()
        & df["cliente_id"].notna()
        & df["valor"].notna()
        & (df["valor"] > 0)
        & df["tipo"].isin(TIPOS_VALIDOS)
    )

    return df[valido].copy()


def resumo_mensal(df):
    """Calcula as métricas mensais (qtd, crédito, débito, saldo, média)."""
    df = df.copy()
    df["mes"] = df["data"].dt.strftime("%Y-%m")

    creditos = (
        df[df["tipo"] == "credito"]
        .groupby("mes")["valor"]
        .sum()
        .rename("total_credito")
    )
    debitos = (
        df[df["tipo"] == "debito"]
        .groupby("mes")["valor"]
        .sum()
        .rename("total_debito")
    )

    resumo = df.groupby("mes").agg(
        quantidade=("valor", "size"),
        media=("valor", "mean"),
    )
    resumo = resumo.join(creditos).join(debitos).fillna(0.0)
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]

    colunas = ["quantidade", "total_credito", "total_debito", "saldo", "media"]
    return resumo[colunas].sort_index()


def transacoes_suspeitas(df):
    """Retorna as transações com valor acima do limite suspeito."""
    return df[df["valor"] > LIMITE_SUSPEITO].copy()


def main():
    df = carregar_e_limpar()
    print(f"Transações válidas: {len(df)}\n")

    resumo = resumo_mensal(df)
    print("=== RESUMO MENSAL (pandas) ===")
    print(resumo.to_string(float_format=lambda x: f"{x:,.2f}"))

    suspeitas = transacoes_suspeitas(df)
    print(f"\n=== TRANSAÇÕES SUSPEITAS (> R$ {LIMITE_SUSPEITO:,.2f}) ===")
    if suspeitas.empty:
        print("Nenhuma transação suspeita encontrada.")
    else:
        print(
            suspeitas[["id", "data", "cliente_id", "tipo", "valor", "descricao"]]
            .to_string(index=False, float_format=lambda x: f"{x:,.2f}")
        )


if __name__ == "__main__":
    main()
