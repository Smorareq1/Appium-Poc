import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_carrito import (
    abrir_carrito,
    hacer_swipe_en_resumen_compra,
    hacer_clic_en_descuento_puntual
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        """
            Este test ejecuta la tercera parte del flujo: carrito
            NOTA: Este test depende de que el anterior haya finalizado correctamente.
        """
        print("\n=== INICIO TEST: Validaciones carrito ===")

        try:
            hacer_swipe_en_resumen_compra(driver)
            hacer_clic_en_descuento_puntual(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al estar dentro del carrito {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")