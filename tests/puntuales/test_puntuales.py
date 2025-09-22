import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_carrito import (
    seleccionar_primera_direccion_entrega
)

from tests.ventas.acciones.acciones_producto import (
    hacer_scroll_hacia_abajo,
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
           hacer_scroll_hacia_abajo(driver)
           seleccionar_primera_direccion_entrega(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")