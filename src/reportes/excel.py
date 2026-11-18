
from io import BytesIO

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment


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
        preparar_excel(writer)

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
        preparar_excel(writer)

    return buffer.getvalue()

def aplicar_formato(hoja, anchos):
    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions
    hoja.sheet_view.showGridLines = False

    encabezado = PatternFill(fill_type="solid", fgColor="1F4E78")

    for celda in hoja[1]:
        celda.fill = encabezado
        celda.font = Font(bold=True, color="FFFFFF")
        celda.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

    hoja.row_dimensions[1].height = 30

    for columna, ancho in anchos.items():
        hoja.column_dimensions[columna].width = ancho


def formatear_boletas(hoja):
    anchos = {
        "A": 10, "B": 14, "C": 16, "D": 25,
        "E": 16, "F": 25, "G": 16, "H": 16,
        "I": 16, "J": 14, "K": 60,
    }

    aplicar_formato(hoja, anchos)

    for fila in hoja.iter_rows(min_row=2):
        numero_fila = fila[0].row

        for celda in fila:
            celda.alignment = Alignment(vertical="top", wrap_text=True)

        hoja.row_dimensions[numero_fila].height = 30

        for columna in ("G", "H", "I"):
            hoja[f"{columna}{numero_fila}"].number_format = '"$"#,##0'

        estado = hoja[f"J{numero_fila}"]

        if estado.value == "OK":
            estado.fill = PatternFill(fill_type="solid", fgColor="E2F0D9")
            estado.font = Font(bold=True, color="375623")

        elif estado.value == "REVISAR":
            estado.fill = PatternFill(fill_type="solid", fgColor="FCE4D6")
            estado.font = Font(bold=True, color="C00000")


def formatear_resumen(hoja):
    anchos = {"A": 20, "B": 30, "C": 22}

    aplicar_formato(hoja, anchos)

    for fila in range(2, hoja.max_row + 1):
        hoja[f"C{fila}"].number_format = '"$"#,##0'


def preparar_excel(writer):
    formatear_boletas(writer.sheets["Boletas"])
    formatear_resumen(writer.sheets["Resumen por receptor"])
