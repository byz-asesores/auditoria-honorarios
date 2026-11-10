import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lectura.cargar_boletas import cargar_boletas
from main import auditar
from reportes.excel import COLUMNAS, generar_excel_en_memoria

st.set_page_config(page_title="Auditoría de Honorarios", layout="wide")
st.title("Auditoría de Honorarios")

archivo = st.file_uploader("Archivo de boletas (CSV)", type="csv")

if archivo:
    boletas = cargar_boletas(archivo)
    resultados = auditar(boletas)
    df = pd.DataFrame(resultados).reindex(columns=COLUMNAS)

    a_revisar = int((df["estado"] == "REVISAR").sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Boletas leídas", len(df))
    col2.metric("Boletas OK", len(df) - a_revisar)
    col3.metric("Boletas a revisar", a_revisar)

    st.dataframe(df, hide_index=True)

    st.download_button(
        "Descargar reporte",
        data=generar_excel_en_memoria(resultados),
        file_name="reporte_auditoria.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
