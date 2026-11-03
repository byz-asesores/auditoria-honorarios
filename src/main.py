from config import ARCHIVO_BOLETAS, ARCHIVO_REPORTE
from lectura.cargar_boletas import cargar_boletas
from reportes.excel import generar_excel
from validaciones.duplicados import buscar_duplicados
from validaciones.retencion import validar_retencion
from validaciones.rut import validar_ruts


def auditar(boletas):
    duplicadas = buscar_duplicados(boletas)

    resultados = []
    for i, boleta in enumerate(boletas):
        observaciones = []
        observaciones += validar_ruts(boleta)
        observaciones += validar_retencion(boleta)
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
