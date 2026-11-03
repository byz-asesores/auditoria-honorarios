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
    if not cuerpo.isdigit():
        return False

    return calcular_dv(cuerpo) == dv


def validar_ruts(boleta):
    observaciones = []
    if not rut_valido(boleta["rut_emisor"]):
        observaciones.append("RUT emisor inválido")
    if not rut_valido(boleta["rut_receptor"]):
        observaciones.append("RUT receptor inválido")
    return observaciones
