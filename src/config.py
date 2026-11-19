from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
ARCHIVO_BOLETAS = CARPETA_PROYECTO / "data" / "boletas.csv"
ARCHIVO_REPORTE = CARPETA_PROYECTO / "output" / "reporte_auditoria.xlsx"

TASAS_RETENCION = {
    2019: 0.10,
    2020: 0.1075,
    2021: 0.115,
    2022: 0.1225,
    2023: 0.13,
    2024: 0.1375,
    2025: 0.145,
    2026: 0.1525,
    2027: 0.16,
    2028: 0.17,
}

TOLERANCIA_PESOS = 1

PERIODO = (2026, 9)
