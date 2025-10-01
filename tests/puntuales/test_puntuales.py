import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.clientes.acciones_clientes import(
    pulsar_boton_central_nav
)

from tests.itinerarios.acciones_itinerarios import(
    registrar_motivo
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
        try:
            pulsar_boton_central_nav(driver)
            wait = WebDriverWait(driver, 10)
            motivo = "Enfermedad"
            fecha = "10"
            comentario = "No puedo asistir por motivos médicos"

            # Llamada a la función que armamos
            registrar_motivo(driver, wait, motivo, fecha, comentario)
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
