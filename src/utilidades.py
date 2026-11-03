def normalizar_rut(rut):
    if rut is None:
        return ""
    return str(rut).replace(".", "").replace(" ", "").strip().upper()


def a_entero(valor):
    if valor is None or str(valor).strip() == "":
        return None
    limpio = str(valor).replace("$", "").replace(".", "").replace(" ", "")
    return int(limpio)
