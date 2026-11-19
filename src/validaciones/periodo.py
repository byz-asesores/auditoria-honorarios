from datetime import datetime

from config import PERIODO


FORMATOS_FECHA = [
    "%d/%m/%Y",
    "%Y-%m-%d",
]


def validar_periodo(boleta):
    observaciones = []
    fecha = boleta.get("fecha")

    if not fecha:
        return ["Fecha faltante"]

    fecha_convertida = None

    for formato in FORMATOS_FECHA:
        try:
            fecha_convertida = datetime.strptime(
                fecha.strip(), formato
            )
            break
        except ValueError:
            continue

    if fecha_convertida is None:
        return [f"Fecha inválida o con formato no permitido: {fecha}"]

    if (fecha_convertida.year, fecha_convertida.month) != PERIODO:
        observaciones.append(
            f"Fecha fuera del período configurado: {fecha}"
        )

    return observaciones