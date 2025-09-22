import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Importamos las acciones del carrito
from tests.itinerarios.acciones_itinerarios import (
    spin_semana,
)

class test_itinerarios:
    @pytest.mark.xray("APPTEST-****")
    def test_itinerarios_button(self, driver, video_recorder):
        """Test para hacer click en el botón Itinerarios"""
        print("\n=== TEST: Click en botón Itinerarios ===")
        try:
            itinerarios_button = driver.find_element("xpath", "//*[@content-desc='Itinerarios']")
            itinerarios_button.click()
            assert itinerarios_button is not None, "No se pudo encontrar el botón 'Itinerarios'"

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_click_semana_anterior_y_verificar_alerta(self, driver, video_recorder):
        """
        Test para hacer clic en el botón 'semana anterior' y verificar que se
        muestra el mensaje de advertencia 'No es posible visualizar semanas pasadas'.
        """
        print("\n=== TEST: Click semana anterior y verificar mensaje de advertencia ===")
        try:
            wait = WebDriverWait(driver, 10)

            # Esperar a que el calendario sea visible
            lunes_ref_xpath = "//*[@content-desc='L\n22']"
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lunes_ref_xpath)))
            print("✅ Calendario visible")

            # Encontrar y hacer clic en el botón "semana anterior"
            boton_anterior_xpath = f"{lunes_ref_xpath}/preceding-sibling::android.widget.Button"
            boton_semana_anterior = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, boton_anterior_xpath))
            )
            boton_semana_anterior.click()
            print("✅ Clic en semana anterior realizado")

            # Verificar que aparece el mensaje de advertencia
            mensaje_xpath = "//*[@content-desc='No es posible visualizar semanas pasadas']"
            mensaje_advertencia = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mensaje_xpath))
            )

            assert mensaje_advertencia is not None, "No se encontró el mensaje de advertencia"
            print("✅ Mensaje de advertencia verificado correctamente")

        except TimeoutException:
            pytest.fail("Timeout: No se encontró el calendario, botón o mensaje de advertencia")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video de evidencia guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_spin_semana(self, driver, video_recorder):
        """Test para hacer spin en los días de la semana y verificar clientes"""
        print("\n=== TEST: Spin en días de la semana ===")
        try:
            spin_semana(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")