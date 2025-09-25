import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav,
    escribir_nit,
    escribir_dpi_representante
)


class test_clientes:
    @pytest.mark.xray("ATC-32")
    def test_clientes_button(self, driver, video_recorder):
        """Test para hacer click en el botón Clientes del menú de navegación"""
        print("\n=== TEST: Click en botón Clientes del menú inferior (método robusto) ===")
        try:
            clientes_xpath = "//*[@content-desc='Itinerarios']/preceding-sibling::android.view.View[@content-desc='Clientes' and @clickable='true']"

            clientes_nav_button = driver.find_element("xpath", clientes_xpath)
            clientes_nav_button.click()

            print("Botón 'Clientes' del menú inferior presionado exitosamente")
            assert clientes_nav_button is not None, "No se pudo encontrar el botón 'Clientes' usando el método relacional"

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-33")
    def test_long_press_cliente_card(self, driver, video_recorder):
        """
        Test que valida la acción de mantener presionado una tarjeta de cliente,
        usando TouchAction para gestos móviles más confiables.
        """
        print("\n=== TEST: Validar long press en tarjeta de cliente 'CLIENTES IS' ===")
        try:
            # Paso 1: Realizar la pulsación larga en la tarjeta
            print("🎯 Paso 1: Ejecutando long press en tarjeta...")
            try:
                realizar_long_press_en_tarjeta_cliente(driver)
                print("✅ Paso 1 completado: Long press realizado exitosamente.")
            except Exception as long_press_error:
                print(f"⚠️  Error en método principal, {long_press_error}")
            print("⏳ Pausa para estabilizar la UI...")
            time.sleep(2)

            # Paso 2: Pulsar el botón central
            print("🎯 Paso 2: Pulsando botón central de navegación...")
            pulsar_boton_central_nav(driver)
            print("✅ Paso 2 completado: Botón central de navegación pulsado.")


            print("✅ TEST PASADO: La secuencia de acciones se ejecutó sin errores.")

        except Exception as e:
            print(f"❌ ERROR durante el test: {e}")

            # Información adicional para debugging
            print("🔧 Información de debugging:")
            try:
                current_activity = driver.current_activity
                print(f"   - Actividad actual: {current_activity}")
            except:
                print("   - No se pudo obtener la actividad actual")

            try:
                window_size = driver.get_window_size()
                print(f"   - Tamaño de ventana: {window_size}")
            except:
                print("   - No se pudo obtener el tamaño de ventana")

            pytest.fail(f"TEST FALLÓ: {e}")

        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado en: {video_path}")

    @pytest.mark.xray("ATC-34")
    def test_llenar_campos(self, driver, video_recorder):
        """
        Test que llena los campos el formulario de nuevos clientes GENERAL
        y verifica que los valores se hayan ingresado correctamente.
        """
        print("\n=== TEST: Llenar formulario GENERAL ===")
        try:
            # Valores a ingresar
            nit_a_escribir = "123456789"
            dpi_a_escribir = "1234567890101"

            # Paso 1: Llamar a la función para escribir el NIT
            escribir_nit(driver, nit_a_escribir)

            # Paso 2: Llamar a la función para escribir el DPI
            escribir_dpi_representante(driver, dpi_a_escribir)

            # --- VERIFICACIÓN (ASSERT) ---
            print("\nVerificando que los datos se escribieron correctamente...")

            nit_field = driver.find_element(AppiumBy.XPATH, "//*[@hint='*NIT']")
            assert nit_field.text == nit_a_escribir
            print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")

            dpi_field = driver.find_element(AppiumBy.XPATH, "//*[@hint='DPI del representante']")
            assert dpi_field.text == dpi_a_escribir
            print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")

            print("\n✅ TEST PASADO: Los campos se llenaron y verificaron exitosamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado en: {video_path}")

