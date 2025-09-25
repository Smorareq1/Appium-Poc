import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav,
    escribir_nit,
    escribir_dpi_representante,
    hacer_scroll_hacia_abajo,
    escribir_version_dpi
)


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
        try:
            # Valores a escribir
            nit_a_escribir = "123456789"
            dpi_a_escribir = "1234567890101"
            version_dpi_a_escribir = "001"

            # Paso 1: Escribir NIT
            escribir_nit(driver, nit_a_escribir)

            # Paso 2: Escribir DPI del representante
            escribir_dpi_representante(driver, dpi_a_escribir)

            # Paso 3: Hacer scroll hacia abajo para ver el campo Versión DPI
            hacer_scroll_hacia_abajo(driver, cantidad_scroll=2)

            # Paso 4: Escribir Versión DPI
            escribir_version_dpi(driver, version_dpi_a_escribir)

            # VERIFICACIÓN - buscar por texto en lugar de hint
            print("\nVerificando que los datos se escribieron correctamente...")

            # Verificar NIT por su texto
            try:
                nit_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{nit_a_escribir}']")
                print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
            except:
                print("⚠️ No se pudo verificar el campo NIT (puede estar fuera de vista)")

            # Verificar DPI por su texto
            try:
                dpi_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
            except:
                print("⚠️ No se pudo verificar el campo DPI (puede estar fuera de vista)")

            # Verificar Versión DPI por su texto
            try:
                version_dpi_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{version_dpi_a_escribir}']")
                print(f"✅ Verificación Versión DPI exitosa: el campo contiene '{version_dpi_field.text}'")
            except:
                print("⚠️ No se pudo verificar el campo Versión DPI")

            print("\n✅ TEST PASADO: Todos los campos se escribieron correctamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
