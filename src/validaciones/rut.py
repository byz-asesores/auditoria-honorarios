
from utilidades import normalizar_rut


def calcular_dv(cuerpo):
    suma = 0
    factor = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * factor
        factor = 2 if factor == 7 else factor + 1

    resto = 11 - (suma % 11)

    if resto == 11:
        return "0"
    if resto == 10:
        return "K"

    return str(resto)


def rut_valido(rut):
    rut = normalizar_rut(rut)

    if "-" not in rut:
        return False

    cuerpo, dv = rut.split("-")

    if not cuerpo.isdigit() or not dv:
        return False

    return calcular_dv(cuerpo) == dv


def validar_ruts(boleta):
    observaciones = []

    for campo, nombre in [
        ("rut_emisor", "emisor"),
        ("rut_receptor", "receptor"),
    ]:
        rut = normalizar_rut(boleta[campo])

        if not rut_valido(rut):
            observaciones.append(
                f"RUT {nombre} inválido: {rut}. "
                "El dígito verificador informado no coincide "
                "con el calculado mediante el algoritmo módulo 11."
            )

    return observaciones

