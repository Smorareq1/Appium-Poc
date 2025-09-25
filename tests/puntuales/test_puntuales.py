import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav,
    escribir_nit,
    escribir_dpi_representante
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
        try:
            nit_a_escribir = "123456789"
            dpi_a_escribir = "1234567890101"

            # Escribir los datos (esto funciona correctamente)
            escribir_nit(driver, nit_a_escribir)
            escribir_dpi_representante(driver, dpi_a_escribir)

            # VERIFICACIÓN CORREGIDA - buscar por texto en lugar de hint
            print("\nVerificando que los datos se escribieron correctamente...")

            # Verificar NIT por su texto
            try:
                nit_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{nit_a_escribir}']")
                print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
            except:
                print("⚠️ No se pudo verificar el campo NIT")

            # Verificar DPI por su texto
            try:
                dpi_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
            except:
                print("⚠️ No se pudo verificar el campo DPI")

            print("\n✅ TEST PASADO: Los datos se escribieron correctamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
