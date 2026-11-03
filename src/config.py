from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
ARCHIVO_BOLETAS = CARPETA_PROYECTO / "data" / "boletas.csv"
ARCHIVO_REPORTE = CARPETA_PROYECTO / "output" / "reporte_auditoria.xlsx"

TASA_RETENCION = 0.1375

TOLERANCIA_PESOS = 1

PERIODO = (2026, 9)
