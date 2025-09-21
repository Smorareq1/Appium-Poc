import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class Test_Buscar:
    @pytest.mark.xray("APPTEST-****")
    def test_click_buscar(self, driver, video_recorder):
        """Test para hacer click en el campo/botón Buscar"""
        print("\n=== TEST: Click en Buscar ===")

        try:
            buscar_element = None

            # Estrategia 1: Por content-desc exacto
            print("Estrategia 1: Buscando por content-desc exacto 'Buscar'...")
            try:
                buscar_element = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Buscar']")
                print("✅ Encontrado por content-desc exacto")
            except NoSuchElementException:
                print("❌ No encontrado por content-desc exacto")

            # Estrategia 2: Por contains en content-desc
            if not buscar_element:
                print("Estrategia 2: Buscando por contains 'Buscar'...")
                try:
                    buscar_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Buscar')]")
                    print("✅ Encontrado por contains en content-desc")
                except NoSuchElementException:
                    print("❌ No encontrado por contains en content-desc")

            # Verificar que se encontró el elemento
            assert buscar_element is not None, "No se pudo encontrar el elemento 'Buscar'"

            # Hacer click en buscar
            print("Haciendo click en 'Buscar'...")
            buscar_element.click()
            time.sleep(2)  # Esperar que se active el campo de búsqueda

            print("✅ TEST COMPLETADO: Click en 'Buscar' exitoso")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_escribir_texto_busqueda(self, driver, video_recorder):
        """Test para escribir texto en el campo de búsqueda.
        Este test asume que el campo de búsqueda ya ha sido activado."""
        print("\n=== TEST: Escribir texto en búsqueda ===")

        # VARIABLE CONFIGURABLE - Cambia este texto por lo que quieras buscar
        texto_a_buscar = "120800280"

        try:
            # CORRECCIÓN: Después de hacer clic en 'Buscar', el elemento se convierte en un EditText.
            # La nueva estrategia, basada en el log de debug, es buscar por la clase del widget.
            campo_texto_element = None

            # Buscar el campo de búsqueda activo (EditText)
            print("Buscando el campo de texto activo (EditText)...")
            try:
                campo_texto_element = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
                print("✅ Campo de texto (EditText) encontrado por su clase.")
            except NoSuchElementException:
                print("❌ No se pudo encontrar el campo de texto (EditText).")

            assert campo_texto_element is not None, "No se pudo encontrar el campo de texto (EditText)."

            # El campo ya debería estar activo, pero un click asegura el foco.
            print("Asegurando foco en el campo de texto...")
            campo_texto_element.click()
            time.sleep(1)

            # Limpiar campo si tiene texto previo
            try:
                campo_texto_element.clear()
                print("Campo limpiado")
            except Exception:
                print("No se pudo limpiar el campo o ya estaba vacío")

            # Escribir el texto
            print(f"Escribiendo texto: '{texto_a_buscar}'...")
            campo_texto_element.send_keys(texto_a_buscar)
            time.sleep(2)  # Pausa después de escribir

            # Ocultar teclado si aparece
            try:
                driver.hide_keyboard()
                print("Teclado ocultado")
            except Exception:
                print("No se pudo ocultar el teclado o no estaba visible")

            time.sleep(1)  # Pausa final

            print(f"✅ TEST COMPLETADO: Texto '{texto_a_buscar}' escrito exitosamente")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_click_resultado_busqueda(self, driver, video_recorder):
        """Test para hacer click en el resultado único de la búsqueda por SKU."""
        print("\n=== TEST: Click en resultado de búsqueda ===")

        # Usar el mismo SKU del test anterior para consistencia
        texto_buscado = "120800280"

        try:
            resultado_element = None

            # Espera prudencial para que aparezcan los resultados
            print("Esperando a que aparezca el resultado...")
            time.sleep(2)

            # Estrategia 1: Buscar por content-desc que contenga el SKU
            print(f"Estrategia 1: Buscando resultado con content-desc que contenga '{texto_buscado}'...")
            try:
                # Se busca cualquier elemento (*) que contenga el texto en su descripción
                resultado_element = driver.find_element(AppiumBy.XPATH,
                                                        f"//*[contains(@content-desc, '{texto_buscado}')]")
                print("✅ Resultado encontrado por content-desc")
            except NoSuchElementException:
                print("❌ No encontrado por content-desc")

            # Estrategia 2: Buscar por el atributo 'text' que contenga el SKU
            if not resultado_element:
                print(f"Estrategia 2: Buscando resultado con atributo 'text' que contenga '{texto_buscado}'...")
                try:
                    resultado_element = driver.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{texto_buscado}')]")
                    print("✅ Resultado encontrado por atributo 'text'")
                except NoSuchElementException:
                    print("❌ No encontrado por atributo 'text'")

            # Verificar que se encontró el elemento
            assert resultado_element is not None, f"No se pudo encontrar el resultado de la búsqueda para el SKU '{texto_buscado}'"

            # Hacer click en el resultado
            print("Haciendo click en el resultado encontrado...")
            resultado_element.click()
            time.sleep(2)  # Esperar a que la siguiente pantalla cargue

            print("✅ TEST COMPLETADO: Click en el resultado fue exitoso")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_click_primera_tarjeta_producto(self, driver, video_recorder):
        """Test para hacer click en la primera tarjeta de producto disponible."""
        print("\n=== TEST: Click en la primera tarjeta de producto ===")

        try:
            # Espera para asegurar que la pantalla se haya cargado completamente
            print("Esperando a que carguen las tarjetas de producto...")
            time.sleep(3)

            # Estrategia: Buscar todos los ImageView que son clickeables.
            # Basado en el log, estos elementos representan las tarjetas de producto.
            print("Buscando todas las tarjetas de producto (ImageViews clickeables)...")
            tarjetas = driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true']")

            # Verificar que se encontró al menos una tarjeta
            assert len(tarjetas) > 0, "No se encontraron tarjetas de producto (ImageViews clickeables) en la pantalla."

            print(f"✅ Se encontraron {len(tarjetas)} tarjetas. Se seleccionará la primera.")

            # Seleccionar y hacer click en la primera tarjeta de la lista
            primera_tarjeta = tarjetas[0]
            print("Haciendo click en la primera tarjeta...")
            primera_tarjeta.click()

            time.sleep(3)  # Esperar a que se cargue la siguiente pantalla

            print("✅ TEST COMPLETADO: Click en la primera tarjeta fue exitoso.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

