
from utilidades import normalizar_rut


def buscar_duplicados(boletas):
    grupos = {}

    for i, boleta in enumerate(boletas):
        numero = str(boleta["numero"]).strip()
        rut_emisor = normalizar_rut(boleta["rut_emisor"])

        clave = (numero, rut_emisor)
        grupos.setdefault(clave, []).append(i)

    duplicadas = {}

    for posiciones in grupos.values():
        if len(posiciones) > 1:
            for i in posiciones:
                otras = [str(j + 2) for j in posiciones if j != i]

                duplicadas[i] = (
                    f"Posible duplicada (ver fila {', '.join(otras)} del CSV)"
                )

    return duplicadas