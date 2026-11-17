
from io import BytesIO

import pandas as pd


COLUMNAS = [
    "numero",
    "fecha",
    "rut_emisor",
    "nombre_emisor",
    "rut_receptor",
    "nombre_receptor",
    "monto_bruto",
    "retencion",
    "monto_liquido",
    "estado",
    "observaciones",
]


def generar_resumen_receptores(resultados):
    df = pd.DataFrame(resultados)

    columnas_resumen = [
        "rut_receptor",
        "nombre_receptor",
        "total_retenido",
    ]

    if df.empty:
        return pd.DataFrame(columns=columnas_resumen)

    df["retencion"] = pd.to_numeric(
        df["retencion"], errors="coerce"
    ).fillna(0)

    resumen = (
        df.groupby("rut_receptor", as_index=False, dropna=False)
        .agg(
            nombre_receptor=("nombre_receptor", "first"),
            total_retenido=("retencion", "sum"),
        )
    )

    return resumen[columnas_resumen]


def generar_excel(resultados, ruta):
    df = pd.DataFrame(resultados).reindex(columns=COLUMNAS)
    resumen = generar_resumen_receptores(resultados)

    ruta.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Boletas")
        resumen.to_excel(
            writer,
            index=False,
            sheet_name="Resumen por receptor",
        )

    return df


def generar_excel_en_memoria(resultados):
    df = pd.DataFrame(resultados).reindex(columns=COLUMNAS)
    resumen = generar_resumen_receptores(resultados)

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Boletas")
        resumen.to_excel(
            writer,
            index=False,
            sheet_name="Resumen por receptor",
        )

    return buffer.getvalue()
