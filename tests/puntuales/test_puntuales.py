import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav,
    escribir_nit,
    escribir_dpi_representante,
    hacer_scroll_hacia_abajo,
    escribir_version_dpi,
    seleccionar_vencimiento_dpi,
    escribir_nota,
    hacer_click_continuar,
    hacer_scroll_hacia_arriba
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
        try:
           pass

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
