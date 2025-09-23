import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_venta_directa import (
    ejecutar_venta_directa_completa
)

from tests.itinerarios.acciones_itinerarios import (
    realizar_check_out_si_pendiente
)
class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            #ejecutar_venta_directa_completa(driver, "Cloro", 5)
            realizar_check_out_si_pendiente(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")