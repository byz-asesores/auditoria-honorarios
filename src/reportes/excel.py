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
    "estado",
    "observaciones",
]


def generar_excel(resultados, ruta):
    df = pd.DataFrame(resultados).reindex(columns=COLUMNAS)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(ruta, index=False, sheet_name="Boletas")
    return df
