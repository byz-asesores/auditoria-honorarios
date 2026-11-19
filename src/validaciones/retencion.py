from datetime import datetime

from config import TASAS_RETENCION, TOLERANCIA_PESOS


def formatear_pesos(monto):
    return "$" + f"{monto:,}".replace(",", ".")


def retencion_esperada(boleta):
    if boleta["retiene_receptor"] == "NO":
        return 0

    fecha_texto = boleta["fecha"]
    fecha = None

    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            fecha = datetime.strptime(fecha_texto, formato)
            break
        except (TypeError, ValueError):
            continue

    if fecha is None:
        raise ValueError(
            f"Fecha de boleta inválida: {fecha_texto}. "
            "Se esperaba DD/MM/AAAA o AAAA-MM-DD."
        )

    tasa = TASAS_RETENCION.get(fecha.year)

    if tasa is None:
        raise ValueError(
            f"No existe una tasa de retención definida "
            f"para el año {fecha.year}."
        )

    return round(boleta["monto_bruto"] * tasa)


def validar_retencion(boleta):
    try:
        esperada = retencion_esperada(boleta)
    except ValueError as error:
        return [str(error)]

    informada = boleta["retencion"]

    if abs(informada - esperada) > TOLERANCIA_PESOS:
        mensaje = (
            f"Retención no cuadra (esperada {formatear_pesos(esperada)}, "
            f"informada {formatear_pesos(informada)})"
        )
        return [mensaje]

    return []


def validar_monto_liquido(boleta):
    esperado = boleta["monto_bruto"] - boleta["retencion"]
    informado = boleta["monto_liquido"]

    if abs(informado - esperado) > TOLERANCIA_PESOS:
        mensaje = (
            f"Líquido no cuadra (esperado {formatear_pesos(esperado)}, "
            f"informado {formatear_pesos(informado)})"
        )
        return [mensaje]

    return []
