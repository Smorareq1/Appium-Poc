import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_producto import (
incrementar_productos_con_botones
)

from tests.ventas.acciones.acciones_busqueda import (
 seleccionar_primera_tarjeta_producto
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            incrementar_productos_con_botones(driver,2,5)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")