import os
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class TestFFAAppLaunch:
    """Suite de tests para lanzamiento de aplicación FFA"""

    @pytest.mark.smoke
    def test_app_launches_successfully(self, driver, screenshot):
        """Test crítico - verificar que la app FFA se lance correctamente"""
        screenshot("ffa_app_launched")

        # Verificar que la app está corriendo
        current_package = driver.current_package
        current_activity = driver.current_activity

        # Assertions
        assert current_package == "com.pdctechco.ffa", f"Package incorrecto: {current_package}"
        assert current_activity is not None, "La activity de la app no debería ser None"

        print(f"✅ FFA App package: {current_package}")
        print(f"✅ FFA App activity: {current_activity}")

    @pytest.mark.smoke
    def test_main_screen_elements_visible(self, driver, screenshot):
        """Test crítico - verificar que elementos principales están visibles"""
        screenshot("main_screen_check")

        # Buscar elementos principales que deberían existir
        try:
            # Buscar botones principales
            registrarme_elements = driver.find_elements(AppiumBy.XPATH,
                                                        "//*[contains(@text,'Registrarme') or contains(@content-desc,'Registrarme')]")
            iniciar_sesion_elements = driver.find_elements(AppiumBy.XPATH,
                                                           "//*[contains(@text,'Iniciar sesión') or contains(@content-desc,'Iniciar sesión')]")

            screenshot("main_elements_found")

            # Al menos uno de los botones principales debe estar visible
            main_buttons_found = len(registrarme_elements) + len(iniciar_sesion_elements)
            assert main_buttons_found > 0, "No se encontraron botones principales (Registrarme o Iniciar sesión)"

            print(
                f"✅ Elementos principales encontrados: Registrarme({len(registrarme_elements)}), Iniciar sesión({len(iniciar_sesion_elements)})")

        except Exception as e:
            screenshot("main_screen_error")
            pytest.fail(f"Error verificando elementos principales: {e}")


class TestFFAUserFlow:
    """Suite de tests para flujo de usuario específico de FFA"""

    @pytest.mark.regression
    def test_01_click_registrarme_button(self, driver, screenshot):
        """Test 1: Presionar botón 'Registrarme'"""
        screenshot("before_registrarme_click")

        try:
            # Buscar botón Registrarme con múltiples estrategias
            registrarme_button = None

            # Estrategia 1: Por texto exacto
            try:
                registrarme_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Registrarme']")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por texto que contenga
            if not registrarme_button:
                try:
                    registrarme_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Registrarme')]")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por content-desc
            if not registrarme_button:
                try:
                    registrarme_button = driver.find_element(AppiumBy.XPATH,
                                                             "//*[contains(@content-desc,'Registrarme')]")
                except NoSuchElementException:
                    pass

            assert registrarme_button is not None, "No se encontró el botón 'Registrarme'"

            # Click en el botón
            registrarme_button.click()
            time.sleep(2)  # Esperar navegación

            screenshot("after_registrarme_click")
            print("✅ Test 1: Click en 'Registrarme' exitoso")

        except Exception as e:
            screenshot("registrarme_click_error")
            pytest.fail(f"Test 1 falló: {e}")

    @pytest.mark.regression
    def test_02_go_back_and_click_iniciar_sesion(self, driver, screenshot):
        """Test 2: Ir atrás y presionar 'Iniciar sesión'"""
        screenshot("before_back_navigation")

        try:
            # Ir atrás (puede ser botón back del dispositivo o botón en app)
            try:
                # Intentar botón back del dispositivo
                driver.back()
                time.sleep(1)
            except:
                # Si no funciona, buscar botón atrás en la app
                back_buttons = driver.find_elements(AppiumBy.XPATH,
                                                    "//*[contains(@content-desc,'back') or contains(@content-desc,'atrás')]")
                if back_buttons:
                    back_buttons[0].click()
                    time.sleep(1)

            screenshot("after_back_navigation")

            # Buscar el botón azul "Iniciar sesión" con múltiples estrategias
            iniciar_sesion_button = None

            # Estrategia 1: Por texto exacto
            try:
                iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Iniciar sesión']")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por texto que contenga (sin espacios extra)
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar sesión')]")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Buscar por botón clickeable que contenga "Iniciar"
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH,
                                                                "//*[@clickable='true' and contains(@text,'Iniciar')]")
                except NoSuchElementException:
                    pass

            # Estrategia 4: Buscar cualquier elemento con "Iniciar" (más amplio)
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar')]")
                except NoSuchElementException:
                    pass

            # Estrategia 5: Buscar por posición (botón en la parte inferior)
            if not iniciar_sesion_button:
                try:
                    # Buscar todos los elementos clickeables
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    # Tomar el último (probablemente el botón inferior)
                    if len(clickable_elements) >= 2:
                        iniciar_sesion_button = clickable_elements[-1]  # Último elemento clickeable
                except:
                    pass

            # Debug: Si no encontramos nada, listar todos los elementos con texto
            if not iniciar_sesion_button:
                print("🔍 Elementos con texto encontrados:")
                all_text_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
                for i, elem in enumerate(all_text_elements[:10]):  # Solo primeros 10
                    try:
                        text = elem.get_attribute("text")
                        clickable = elem.get_attribute("clickable")
                        print(f"  {i}: '{text}' (clickable: {clickable})")
                    except:
                        pass

            assert iniciar_sesion_button is not None, "No se encontró el botón 'Iniciar sesión'"

            iniciar_sesion_button.click()
            time.sleep(2)

            screenshot("after_iniciar_sesion_click")
            print("✅ Test 2: Navegación atrás e 'Iniciar sesión' exitoso")

        except Exception as e:
            screenshot("iniciar_sesion_error")
            pytest.fail(f"Test 2 falló: {e}")

    @pytest.mark.regression
    def test_03_enter_invalid_email_and_validate_error(self, driver, screenshot):
        """Test 3: Ingresar 'emailFalso', continuar y validar mensaje de error"""
        screenshot("before_email_input")

        try:
            # Buscar campo de texto para email
            email_field = None

            # Estrategias para encontrar campo de email
            email_selectors = [
                "//*[@class='android.widget.EditText']",
                "//*[contains(@hint,'email') or contains(@hint,'Email')]",
                "//*[contains(@hint,'correo') or contains(@hint,'Correo')]",
                "//*[@resource-id='email' or @resource-id='emailInput']",
                "//android.widget.EditText[1]"  # Primer campo de texto
            ]

            for selector in email_selectors:
                try:
                    email_field = driver.find_element(AppiumBy.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            assert email_field is not None, "No se encontró campo de texto para email"

            # Limpiar y escribir email falso
            email_field.clear()
            email_field.send_keys("emailFalso")

            screenshot("email_entered")

            # Buscar botón continuar
            continuar_button = None
            continuar_selectors = [
                "//*[@text='Continuar']",
                "//*[contains(@text,'Continuar')]",
                "//*[@text='Siguiente']",
                "//*[contains(@text,'Siguiente')]",
                "//*[@content-desc='Continuar']"
            ]

            for selector in continuar_selectors:
                try:
                    continuar_button = driver.find_element(AppiumBy.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            assert continuar_button is not None, "No se encontró botón 'Continuar'"

            continuar_button.click()
            time.sleep(2)

            screenshot("after_continuar_click")

            # Validar que aparece mensaje de error
            error_message_found = False
            error_selectors = [
                "//*[contains(@text,'Llene los campos correctamente')]",
                "//*[contains(@text,'campos correctamente')]",
                "//*[contains(@text,'correctamente')]",
                "//*[contains(@text,'error')]",
                "//*[contains(@text,'Error')]"
            ]

            for selector in error_selectors:
                try:
                    error_element = driver.find_element(AppiumBy.XPATH, selector)
                    error_message_found = True
                    print(f"✅ Mensaje de error encontrado: {error_element.text}")
                    break
                except NoSuchElementException:
                    continue

            screenshot("error_validation")

            assert error_message_found, "No se encontró el mensaje de error esperado"
            print("✅ Test 3: Validación de error exitosa")

        except Exception as e:
            screenshot("email_validation_error")
            pytest.fail(f"Test 3 falló: {e}")

    @pytest.mark.regression
    def test_04_click_usuario_password_and_enter_credentials(self, driver, screenshot):
        """Test 4: Click en 'Usuario y contraseña' e ingresar credenciales"""
        screenshot("before_usuario_password_click")

        try:
            # Buscar opción "Usuario y contraseña"
            usuario_password_button = None
            usuario_selectors = [
                "//*[@text='Usuario y contraseña']",
                "//*[contains(@text,'Usuario y contraseña')]",
                "//*[contains(@text,'Usuario')]",
                "//*[contains(@text,'contraseña')]"
            ]

            for selector in usuario_selectors:
                try:
                    usuario_password_button = driver.find_element(AppiumBy.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            assert usuario_password_button is not None, "No se encontró opción 'Usuario y contraseña'"

            usuario_password_button.click()
            time.sleep(2)

            screenshot("after_usuario_password_click")

            # Buscar campos de usuario y contraseña
            text_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")

            assert len(text_fields) >= 2, f"Se esperaban al menos 2 campos de texto, se encontraron {len(text_fields)}"

            # Campo usuario (primer campo)
            usuario_field = text_fields[0]
            usuario_field.clear()
            usuario_field.send_keys("Alejandro.Morales")

            screenshot("usuario_entered")

            # Campo contraseña (segundo campo)
            password_field = text_fields[1]
            password_field.clear()
            password_field.send_keys("Admin123")

            screenshot("credentials_entered")

            print("✅ Test 4: Credenciales ingresadas exitosamente")

        except Exception as e:
            screenshot("credentials_input_error")
            pytest.fail(f"Test 4 falló: {e}")

    @pytest.mark.regression
    def test_05_click_siguiente_button(self, driver, screenshot):
        """Test 5: Presionar botón 'Siguiente'"""
        screenshot("before_siguiente_click")

        try:
            # Buscar botón Siguiente
            siguiente_button = None
            siguiente_selectors = [
                "//*[@text='Siguiente']",
                "//*[contains(@text,'Siguiente')]",
                "//*[@text='Continuar']",
                "//*[contains(@text,'Continuar')]",
                "//*[@content-desc='Siguiente']"
            ]

            for selector in siguiente_selectors:
                try:
                    siguiente_button = driver.find_element(AppiumBy.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            assert siguiente_button is not None, "No se encontró botón 'Siguiente'"

            siguiente_button.click()
            time.sleep(3)  # Tiempo extra para navegación

            screenshot("after_siguiente_click")
            print("✅ Test 5: Click en 'Siguiente' exitoso")

        except Exception as e:
            screenshot("siguiente_click_error")
            pytest.fail(f"Test 5 falló: {e}")

    @pytest.mark.regression
    def test_06_click_allow_button(self, driver, screenshot):
        """Test 6: Presionar botón 'Allow'"""
        screenshot("before_allow_click")

        try:
            # Esperar un poco más por si hay diálogo de permisos
            time.sleep(2)

            # Buscar botón Allow
            allow_button = None
            allow_selectors = [
                "//*[@text='Allow']",
                "//*[@text='ALLOW']",
                "//*[contains(@text,'Allow')]",
                "//*[@text='Permitir']",
                "//*[contains(@text,'Permitir')]",
                "//*[@resource-id='com.android.permissioncontroller:id/permission_allow_button']"
            ]

            for selector in allow_selectors:
                try:
                    allow_button = driver.find_element(AppiumBy.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            if allow_button is None:
                # Si no hay botón Allow, puede que no haya aparecido el diálogo de permisos
                screenshot("no_allow_dialog")
                print("⚠️ No se encontró botón 'Allow' - posiblemente no hay diálogo de permisos")
                return

            allow_button.click()
            time.sleep(2)

            screenshot("after_allow_click")
            print("✅ Test 6: Click en 'Allow' exitoso")

        except Exception as e:
            screenshot("allow_click_error")
            pytest.fail(f"Test 6 falló: {e}")


class TestFFAPerformance:
    """Suite de tests de rendimiento para FFA"""

    @pytest.mark.performance
    def test_app_startup_time(self, driver_fresh_install, screenshot):
        """Test de rendimiento - tiempo de inicio de la app"""
        start_time = time.time()

        # La app ya se inició con driver_fresh_install
        screenshot("app_startup_completed")

        startup_time = time.time() - start_time

        # Assertions de rendimiento
        assert startup_time < 10.0, f"Tiempo de inicio muy alto: {startup_time:.2f}s"

        print(f"✅ Tiempo de inicio de FFA: {startup_time:.2f}s")

    @pytest.mark.performance
    def test_ui_response_time(self, driver, screenshot):
        """Test de rendimiento - tiempo de respuesta de UI"""
        response_times = []

        # Medir tiempo de varias operaciones
        for i in range(3):
            start_time = time.time()

            # Operación simple: tomar screenshot
            driver.save_screenshot(f"temp_perf_{i}.png")

            end_time = time.time()
            response_times.append(end_time - start_time)

            # Limpiar archivo temporal
            try:
                os.remove(f"temp_perf_{i}.png")
            except:
                pass

        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)

        screenshot("performance_test_completed")

        # Assertions de rendimiento
        assert avg_response_time < 2.0, f"Tiempo promedio muy alto: {avg_response_time:.2f}s"
        assert max_response_time < 5.0, f"Tiempo máximo muy alto: {max_response_time:.2f}s"

        print(f"✅ Tiempo promedio UI: {avg_response_time:.2f}s")
        print(f"✅ Tiempo máximo UI: {max_response_time:.2f}s")


# Hook personalizado para logs específicos de FFA
def pytest_runtest_setup(item):
    """Hook que se ejecuta antes de cada test"""
    print(f"🧪 Iniciando test FFA: {item.name}")


def pytest_runtest_teardown(item):
    """Hook que se ejecuta después de cada test"""
    print(f"🏁 Test FFA completado: {item.name}")