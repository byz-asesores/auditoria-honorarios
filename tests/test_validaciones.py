import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import auditar
from validaciones.rut import rut_valido, validar_ruts
from validaciones.duplicados import buscar_duplicados
from validaciones.retencion import (
    retencion_esperada,
    validar_retencion,
    validar_monto_liquido,
)
from reportes.excel import (
    generar_resumen_receptores,
    generar_resumen_anual,
)


def crear_boleta(**cambios):
    boleta = {
        "numero": "100",
        "fecha": "15/09/2026",
        "rut_emisor": "11.111.111-1",
        "rut_receptor": "22.222.222-2",
        "monto_bruto": 1000000,
        "retencion": 152500,
        "monto_liquido": 847500,
        "retiene_receptor": "SI",
    }
    boleta.update(cambios)
    return boleta


class TestRut(unittest.TestCase):

    def test_rut_valido(self):
        self.assertTrue(rut_valido("11.111.111-1"))

    def test_rut_invalido(self):
        self.assertFalse(rut_valido("11.111.111-2"))

    def test_detecta_rut_emisor_invalido(self):
        boleta = crear_boleta(rut_emisor="11.111.111-2")
        observaciones = validar_ruts(boleta)
        self.assertTrue(any("RUT emisor" in o for o in observaciones))


class TestDuplicados(unittest.TestCase):

    def test_detecta_boletas_duplicadas(self):
        boletas = [
            crear_boleta(),
            crear_boleta(),
        ]
        resultado = buscar_duplicados(boletas)
        self.assertEqual(set(resultado.keys()), {0, 1})

    def test_no_detecta_numeros_distintos_como_duplicados(self):
        boletas = [
            crear_boleta(numero="100"),
            crear_boleta(numero="101"),
        ]
        resultado = buscar_duplicados(boletas)
        self.assertEqual(resultado, {})


class TestRetencion(unittest.TestCase):

    def test_calcula_retencion_2026(self):
        boleta = crear_boleta()
        self.assertEqual(retencion_esperada(boleta), 152500)

    def test_detecta_retencion_incorrecta(self):
        boleta = crear_boleta(retencion=150000)
        observaciones = validar_retencion(boleta)
        self.assertTrue(any("Retención no cuadra" in o for o in observaciones))

    def test_detecta_fecha_invalida(self):
        boleta = crear_boleta(fecha="2026-09-25")
        observaciones = validar_retencion(boleta)
        self.assertTrue(any("Fecha de boleta" in o for o in observaciones))

    def test_no_calcula_retencion_si_no_retiene(self):
        boleta = crear_boleta(
            retiene_receptor="NO",
            retencion=0,
            monto_liquido=1000000,
        )
        self.assertEqual(retencion_esperada(boleta), 0)
        self.assertEqual(validar_retencion(boleta), [])


class TestMontoLiquido(unittest.TestCase):

    def test_monto_liquido_correcto(self):
        boleta = crear_boleta()
        self.assertEqual(validar_monto_liquido(boleta), [])

    def test_detecta_monto_liquido_incorrecto(self):
        boleta = crear_boleta(monto_liquido=800000)
        observaciones = validar_monto_liquido(boleta)
        self.assertTrue(any("Líquido no cuadra" in o for o in observaciones))


class TestAuditoriaGeneral(unittest.TestCase):

    def test_boleta_correcta_queda_como_ok(self):
        resultados = auditar([crear_boleta()])
        self.assertEqual(resultados[0]["estado"], "OK")

    def test_boleta_con_fecha_invalida_queda_como_revisar(self):
        boleta = crear_boleta(fecha="2026-09-25")
        resultados = auditar([boleta])
        self.assertEqual(resultados[0]["estado"], "REVISAR")

class TestResumenSinDuplicados(unittest.TestCase):

    def setUp(self):
        self.boletas = [
            crear_boleta(
                numero="7",
                fecha="08/09/2026",
                nombre_receptor="Empresa Ejemplo",
                estado="OK",
            ),
            crear_boleta(
                numero="7",
                fecha="18/09/2026",
                nombre_receptor="Empresa Ejemplo",
                estado="REVISAR",
            ),
        ]

    def test_resumen_receptor_no_suma_duplicados(self):
        resumen = generar_resumen_receptores(self.boletas)

        self.assertEqual(len(resumen), 1)
        self.assertEqual(resumen.iloc[0]["total_retenido"], 152500)

    def test_resumen_anual_no_suma_duplicados(self):
        resumen = generar_resumen_anual(self.boletas)

        self.assertEqual(len(resumen), 1)
        self.assertEqual(resumen.iloc[0]["cantidad_boletas"], 1)
        self.assertEqual(resumen.iloc[0]["total_bruto"], 1000000)
        self.assertEqual(resumen.iloc[0]["total_retenciones"], 152500)
        self.assertEqual(resumen.iloc[0]["total_liquido"], 847500)

if __name__ == "__main__":
    unittest.main()