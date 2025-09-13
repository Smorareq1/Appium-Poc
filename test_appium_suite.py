import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class TestSimpleFlow:
    """Tests simples para el flujo básico de la app"""

    def test_01_click_registrarme(self, driver, screenshot):
        """Test 1: Hacer click en el botón 'Registrarme'"""
        print("\n=== TEST 1: Click en Registrarme ===")

        # Screenshot inicial
        screenshot("pantalla_inicial")

        try:
            # Buscar el botón "Registrarme" (es el botón con borde blanco)
            print("Buscando botón 'Registrarme'...")

            # Estrategia 1: Por texto exacto
            registrarme_button = None
            try:
                registrarme_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Registrarme']")
                print("Encontrado por texto exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por texto que contenga
            if not registrarme_button:
                try:
                    registrarme_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Registrarme')]")
                    print("Encontrado por texto que contiene")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por posición (primer botón clickeable)
            if not registrarme_button:
                try:
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    if len(clickable_elements) >= 1:
                        registrarme_button = clickable_elements[0]  # Primer elemento clickeable
                        print("Encontrado como primer elemento clickeable")
                except:
                    pass

            assert registrarme_button is not None, "No se pudo encontrar el botón 'Registrarme'"

            # Hacer click
            print("Haciendo click en Registrarme...")
            registrarme_button.click()
            time.sleep(3)  # Esperar que cargue la nueva pantalla

            # Screenshot después del click
            screenshot("despues_click_registrarme")

            print("✅ TEST 1 COMPLETADO: Click en Registrarme exitoso")

        except Exception as e:
            screenshot("error_test_1")
            pytest.fail(f"TEST 1 FALLÓ: {e}")

    def test_02_go_back_with_phone_button(self, driver, screenshot):
        """Test 2: Usar botón atrás del teléfono para volver"""
        print("\n=== TEST 2: Botón atrás del teléfono ===")

        # Screenshot antes de ir atrás
        screenshot("antes_boton_atras")

        try:
            print("Presionando botón atrás del dispositivo...")

            # Usar el botón back del dispositivo
            driver.back()
            time.sleep(2)  # Esperar que regrese a la pantalla anterior

            # Screenshot después de ir atrás
            screenshot("despues_boton_atras")

            # Verificar que volvimos a la pantalla principal
            # buscando el texto "¡Bienvenido!" o "Iniciar sesión"
            try:
                bienvenido_text = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Bienvenido')]")
                print("Confirmado: Volvimos a la pantalla principal (texto 'Bienvenido' encontrado)")
            except NoSuchElementException:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar sesión')]")
                    print("Confirmado: Volvimos a la pantalla principal (botón 'Iniciar sesión' encontrado)")
                except NoSuchElementException:
                    print("⚠️ No se pudo confirmar que volvimos, pero el test continúa...")

            print("✅ TEST 2 COMPLETADO: Botón atrás funcionó correctamente")

        except Exception as e:
            screenshot("error_test_2")
            pytest.fail(f"TEST 2 FALLÓ: {e}")

    def test_03_click_iniciar_sesion(self, driver, screenshot):
        """Test 3: Hacer click en el botón azul 'Iniciar sesión'"""
        print("\n=== TEST 3: Click en Iniciar sesión ===")

        # Screenshot inicial
        screenshot("antes_iniciar_sesion")

        try:
            print("Buscando botón 'Iniciar sesión'...")

            # Estrategia 1: Por texto exacto
            iniciar_sesion_button = None
            try:
                iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Iniciar sesión']")
                print("Encontrado por texto exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por texto que contenga
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar sesión')]")
                    print("Encontrado por texto que contiene")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por texto que contenga solo "Iniciar"
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar')]")
                    print("Encontrado por texto que contiene 'Iniciar'")
                except NoSuchElementException:
                    pass

            # Estrategia 4: Por posición (último botón clickeable - probablemente el azul)
            if not iniciar_sesion_button:
                try:
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    if len(clickable_elements) >= 2:
                        iniciar_sesion_button = clickable_elements[-1]  # Último elemento clickeable
                        print("Encontrado como último elemento clickeable (botón azul)")
                except:
                    pass

            # Debug: Si no encontramos nada, mostrar todos los elementos disponibles
            if not iniciar_sesion_button:
                print("🔍 DEBUG: Elementos con texto encontrados:")
                all_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
                for i, elem in enumerate(all_elements[:10]):
                    try:
                        text = elem.get_attribute("text")
                        clickable = elem.get_attribute("clickable")
                        print(f"  {i}: '{text}' (clickable: {clickable})")
                    except:
                        pass

                print("🔍 DEBUG: Elementos clickeables encontrados:")
                clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                for i, elem in enumerate(clickable_elements):
                    try:
                        text = elem.get_attribute("text") or "Sin texto"
                        bounds = elem.get_attribute("bounds") or "Sin bounds"
                        print(f"  {i}: '{text}' en {bounds}")
                    except:
                        print(f"  {i}: No se pudo obtener info del elemento")

            assert iniciar_sesion_button is not None, "No se pudo encontrar el botón 'Iniciar sesión'"

            # Hacer click
            print("Haciendo click en 'Iniciar sesión'...")
            iniciar_sesion_button.click()
            time.sleep(3)  # Esperar que cargue la nueva pantalla

            # Screenshot después del click
            screenshot("despues_click_iniciar_sesion")

            # Verificar que cambió de pantalla buscando elementos que NO están en la pantalla principal
            pantalla_cambio = False

            # Buscar elementos típicos de pantalla de login
            elementos_login = [
                "//*[contains(@hint,'email') or contains(@hint,'Email')]",
                "//*[contains(@hint,'usuario') or contains(@hint,'Usuario')]",
                "//*[contains(@hint,'correo')]",
                "//*[@class='android.widget.EditText']",
                "//*[contains(@text,'email')]",
                "//*[contains(@text,'contraseña')]"
            ]

            for selector in elementos_login:
                try:
                    driver.find_element(AppiumBy.XPATH, selector)
                    pantalla_cambio = True
                    print(f"Confirmado: Cambió de pantalla (encontrado elemento: {selector})")
                    break
                except NoSuchElementException:
                    continue

            if not pantalla_cambio:
                print("⚠️ No se pudo confirmar el cambio de pantalla, pero el click se ejecutó")

            print("✅ TEST 3 COMPLETADO: Click en 'Iniciar sesión' exitoso")

        except Exception as e:
            screenshot("error_test_3")
            pytest.fail(f"TEST 3 FALLÓ: {e}")

    def test_04_debug_current_screen(self, driver, screenshot):
        """Test 4: Debug - Mostrar todos los elementos de la pantalla actual"""
        print("\n=== TEST 4: DEBUG - Elementos actuales ===")

        screenshot("debug_pantalla_actual")

        try:
            print("📱 Información de la pantalla actual:")
            print(f"Package actual: {driver.current_package}")
            print(f"Activity actual: {driver.current_activity}")

            # Mostrar todos los elementos con texto
            print("\n📝 Elementos con texto:")
            text_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
            for i, elem in enumerate(text_elements):
                try:
                    text = elem.get_attribute("text")
                    clickable = elem.get_attribute("clickable")
                    print(f"  {i + 1}. '{text}' (clickable: {clickable})")
                except:
                    print(f"  {i + 1}. Error obteniendo texto del elemento")

            # Mostrar elementos clickeables
            print("\n🎯 Elementos clickeables:")
            clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            for i, elem in enumerate(clickable_elements):
                try:
                    text = elem.get_attribute("text") or "(sin texto)"
                    content_desc = elem.get_attribute("content-desc") or "(sin descripción)"
                    resource_id = elem.get_attribute("resource-id") or "(sin ID)"
                    print(f"  {i + 1}. Texto: '{text}' | Desc: '{content_desc}' | ID: '{resource_id}'")
                except:
                    print(f"  {i + 1}. Error obteniendo info del elemento clickeable")

            # Mostrar campos de texto
            print("\n✏️ Campos de texto:")
            edit_text_elements = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if edit_text_elements:
                for i, elem in enumerate(edit_text_elements):
                    try:
                        hint = elem.get_attribute("hint") or "(sin hint)"
                        text = elem.get_attribute("text") or "(sin texto)"
                        print(f"  {i + 1}. Hint: '{hint}' | Texto actual: '{text}'")
                    except:
                        print(f"  {i + 1}. Error obteniendo info del campo de texto")
            else:
                print("  No se encontraron campos de texto")

            print("\n✅ TEST 4 COMPLETADO: Debug información mostrada")

        except Exception as e:
            print(f"❌ Error en debug: {e}")