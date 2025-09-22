import pytest

# Importamos las acciones del carrito
from tests.itinerarios.acciones_itinerarios import (
    spin_semana,
    buscar_primer_dia_con_clientes,
    hacer_click_pendientes,
    hacer_click_primer_cliente,
    hacer_click_en_check_in,
    hacer_click_en_capturar_ubicacion,
    hacer_click_en_Ok
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            hacer_click_en_Ok(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")