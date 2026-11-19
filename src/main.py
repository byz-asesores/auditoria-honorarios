from config import ARCHIVO_BOLETAS, ARCHIVO_REPORTE
from lectura.cargar_boletas import cargar_boletas
from reportes.excel import generar_excel
from validaciones.duplicados import buscar_duplicados
from validaciones.retencion import validar_retencion, validar_monto_liquido
from validaciones.rut import validar_ruts



def auditar(boletas):
    duplicadas = buscar_duplicados(boletas)

    resultados = []

    campos_monetarios = [
        "monto_bruto",
        "retencion",
        "monto_liquido",
    ]

    for i, boleta in enumerate(boletas):
        observaciones = []

        # Incorporar errores encontrados al leer los montos
        observaciones += boleta.get("_errores_monto", [])

        # Validar RUT
        observaciones += validar_ruts(boleta)

        # Comprobar que los montos sean válidos
        montos_validos = True

        for campo in campos_monetarios:
            if boleta.get(campo) is None:
                montos_validos = False

                if not any(
                    campo in error
                    for error in observaciones
                ):
                    observaciones.append(
                        f"Dato inválido o faltante en {campo}"
                    )

        # Validar montos solamente cuando sean válidos
        if montos_validos:
            observaciones += validar_retencion(boleta)
            observaciones += validar_monto_liquido(boleta)

        # Incorporar duplicados
        if i in duplicadas:
            observaciones.append(duplicadas[i])

        fila = dict(boleta)
        fila["estado"] = "OK" if not observaciones else "REVISAR"
        fila["observaciones"] = "; ".join(observaciones)

        resultados.append(fila)

    return resultados



def main():
    print("Auditor de honorarios")

    boletas = cargar_boletas(ARCHIVO_BOLETAS)
    print(f"Boletas leídas: {len(boletas)}")

    resultados = auditar(boletas)
    df = generar_excel(resultados, ARCHIVO_REPORTE)

    a_revisar = (df["estado"] == "REVISAR").sum()
    print(f"Boletas OK: {len(df) - a_revisar}")
    print(f"Boletas a revisar: {a_revisar}")
    print(f"Reporte: {ARCHIVO_REPORTE}")


if __name__ == "__main__":
    main()