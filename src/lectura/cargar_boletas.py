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
    "monto_liquido",
    "retiene_receptor",
]


def cargar_boletas(ruta):
    df = pd.read_csv(ruta, dtype=str, encoding="utf-8")
    df = df[COLUMNAS_USADAS].copy()

    df["retiene_receptor"] = (
        df["retiene_receptor"].fillna("").str.strip().str.upper()
    )

    boletas = []

    for registro in df.to_dict("records"):
        errores_monto = []

        for campo in ["monto_bruto", "retencion", "monto_liquido"]:
            valor = registro[campo]

            if pd.isna(valor) or str(valor).strip() == "":
                registro[campo] = None
                continue

            try:
                registro[campo] = a_entero(valor)
            except ValueError:
                registro[campo] = None
                errores_monto.append(
                    f"Dato invalido en {campo}: {valor}"
                )

        registro["_errores_monto"] = errores_monto
        boletas.append(registro)

    return boletas
