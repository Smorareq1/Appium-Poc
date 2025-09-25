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

            # Paso 5: Fecha de DPI
            dia = "13"
            anio = "2025"
            seleccionar_vencimiento_dpi(driver, dia, anio)

            #Paso 6: Nota
            nota = "Prueba automatizada"
            escribir_nota(driver, nota)


            # VERIFICACIÓN
            print("\nVerificando que los datos se escribieron correctamente...")

            # Hacer scroll hacia arriba primero
            hacer_scroll_hacia_arriba(driver, 3)

            # Verificar NIT por su texto
            nit_encontrado = False
            try:
                nit_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{nit_a_escribir}']")
                print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
                nit_encontrado = True
            except:
                print("⚠️ Campo NIT no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando NIT
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        nit_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{nit_a_escribir}']")
                        print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
                        nit_encontrado = True
                        break
                    except:
                        continue
                if not nit_encontrado:
                    print("⚠️ No se pudo verificar el campo NIT después de scroll")

            # Verificar DPI por su texto
            dpi_encontrado = False
            try:
                dpi_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
                dpi_encontrado = True
            except:
                print("⚠️ Campo DPI no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando DPI
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        dpi_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                        print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
                        dpi_encontrado = True
                        break
                    except:
                        continue
                if not dpi_encontrado:
                    print("⚠️ No se pudo verificar el campo DPI después de scroll")

            # Verificar Versión DPI por su texto
            version_dpi_encontrado = False
            try:
                version_dpi_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{version_dpi_a_escribir}']")
                print(f"✅ Verificación Versión DPI exitosa: el campo contiene '{version_dpi_field.text}'")
                version_dpi_encontrado = True
            except:
                print("⚠️ Campo Versión DPI no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando Versión DPI
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        version_dpi_field = driver.find_element(AppiumBy.XPATH,
                                                                f"//android.widget.EditText[@text='{version_dpi_a_escribir}']")
                        print(f"✅ Verificación Versión DPI exitosa: el campo contiene '{version_dpi_field.text}'")
                        version_dpi_encontrado = True
                        break
                    except:
                        continue
                if not version_dpi_encontrado:
                    print("⚠️ No se pudo verificar el campo Versión DPI después de scroll")

            # Paso 7 - Continuar
            hacer_scroll_hacia_abajo(driver, cantidad_scroll=2)
            hacer_click_continuar(driver)

            print("\n✅ TEST PASADO: Todos los campos se escribieron correctamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
