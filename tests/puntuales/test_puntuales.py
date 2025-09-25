import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    seleccionar_tipo_de_ruta,
    seleccionar_direccion,
    llenar_formulario_direccion,
seleccionar_contacto,
llenar_formulario_contacto,
click_asignar_geolocalizacion,
click_capturar,
eliminar_gestiones_extras_iterativo
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
        try:
            eliminar_gestiones_extras_iterativo(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
