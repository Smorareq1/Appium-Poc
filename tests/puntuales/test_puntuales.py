import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_venta_directa import (
    ejecutar_venta_directa_completa
)

from tests.itinerarios.acciones_itinerarios import (
    realizar_check_out_si_pendiente
)

from tests.ventas.acciones.acciones_carrito import (
    abrir_carrito
)

from tests.ventas.acciones.acciones_busqueda import (
 seleccionar_primera_tarjeta_producto
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            seleccionar_primera_tarjeta_producto()

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")