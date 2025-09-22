import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class test_itinerarios:
    @pytest.mark.xray("APPTEST-****")
    def test_itinerarios_button(self, driver, video_recorder):
        """Test para hacer click en el botón Itinerarios"""
        print("\n=== TEST: Click en botón Itinerarios ===")
        try:
            itinerarios_button = None
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
    def test_click_mes_anterior_button(self, driver, video_recorder):
        """
        Test para hacer clic en el botón de flecha 'mes anterior' en el calendario.
        """
        print("\n=== TEST: Click en botón 'Mes Anterior' del calendario ===")
        try:
            # 🎯 Estrategia Corregida: Localizar el botón como un hermano directo del día Lunes.
            #    El XPath busca el elemento 'Lunes' y luego selecciona el 'Button'
            #    que le precede inmediatamente en el mismo nivel jerárquico.
            wait = WebDriverWait(driver, 10)

            # El punto de referencia (día Lunes) no cambia
            lunes_ref_xpath = "//*[@content-desc='L\n22']"

            # Se espera a que la referencia sea visible para asegurar que el calendario ha cargado
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lunes_ref_xpath)))
            print("✅ Calendario visible (referencia 'Lunes' encontrada).")

            # NUEVO XPATH: Busca el 'Button' que es hermano precedente de nuestra referencia.
            boton_anterior_xpath = f"{lunes_ref_xpath}/preceding-sibling::android.widget.Button"

            print(f"Buscando el botón del mes anterior con XPath corregido: {boton_anterior_xpath}")

            boton_mes_anterior = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, boton_anterior_xpath))
            )

            print("✅ Botón 'Mes Anterior' encontrado y es clickeable.")

            # Hacemos clic
            boton_mes_anterior.click()

            print("👍 Clic en 'Mes Anterior' realizado exitosamente.")

        except TimeoutException:
            pytest.fail(
                "TEST FALLÓ: No se encontró el botón 'Mes Anterior' en el tiempo esperado. Verificar XPath y visibilidad.")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado: {e}")
        finally:
            # 📹 Guardar el video de evidencia
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video de evidencia guardado en: {video_path}")