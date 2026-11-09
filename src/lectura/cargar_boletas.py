import pandas as pd

from utilidades import a_entero

COLUMNAS_USADAS = [
    "numero",
    "fecha",
    "rut_emisor",
    "nombre_emisor",
    "rut_receptor",
    "nombre_receptor",
    "monto_bruto",
    "retencion",
    "retiene_receptor",
]


def cargar_boletas(ruta):
    df = pd.read_csv(ruta, dtype=str, encoding="utf-8")
    df = df[COLUMNAS_USADAS].copy()

    df["monto_bruto"] = df["monto_bruto"].apply(a_entero)
    df["retencion"] = df["retencion"].apply(a_entero)
    df["retiene_receptor"] = (
        df["retiene_receptor"].str.strip().str.upper()
    )

    return df.to_dict("records")
