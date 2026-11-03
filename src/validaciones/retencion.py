from config import TASA_RETENCION, TOLERANCIA_PESOS


def formatear_pesos(monto):
    return "$" + f"{monto:,}".replace(",", ".")


def retencion_esperada(boleta):
    if boleta["retiene_receptor"] == "NO":
        return 0
    return round(boleta["monto_bruto"] * TASA_RETENCION)


def validar_retencion(boleta):
    esperada = retencion_esperada(boleta)
    informada = boleta["retencion"]

    if abs(informada - esperada) > TOLERANCIA_PESOS:
        mensaje = (
            f"Retención no cuadra (esperada {formatear_pesos(esperada)}, "
            f"informada {formatear_pesos(informada)})"
        )
        return [mensaje]
    return []
