import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


from tests.clientes.acciones_clientes import(
    pulsar_boton_central_nav
)

from tests.itinerarios.acciones_itinerarios import(
    registrar_motivo,
    validar_y_contar_actividades_pendientes,
    reactivar_todas_actividades_canceladas
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-PUNTUALES")
    def test_puntual(self, driver, video_recorder):
        try:
            reactivar_todas_actividades_canceladas(driver)
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
