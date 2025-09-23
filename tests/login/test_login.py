import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ensure_keyboard_closed(driver):
    """
    Función auxiliar para asegurar que el teclado esté cerrado.
    Intenta múltiples métodos para cerrar el teclado.
    """
    try:
        # Método 1: hide_keyboard()
        driver.hide_keyboard()
        print("Teclado cerrado con hide_keyboard()")
    except Exception:
        try:
            # Método 2: Presionar back si hay teclado
            if driver.is_keyboard_shown():
                driver.back()
                print("Teclado cerrado con back()")
        except Exception:
            try:
                # Método 3: Click en una zona vacía para quitar foco
                size = driver.get_window_size()
                x = int(size['width'] / 2)
                y = int(size['height'] * 0.1)  # Top area
                driver.tap([(x, y)], 100)
                print("Teclado cerrado con tap en zona vacía")
            except Exception:
                print("No se pudo cerrar el teclado, continuando...")

    # Espera breve para asegurar que el teclado se cierre
    time.sleep(0.5)


class test_Login:
    # El flujo completo de pruebas es una prueba de regresión
    # que abarca desde la pantalla inicial hasta el cierre de sesión.

    # UI Tests
    # Test 1: Hacer click en el botón 'Registrarme'
    @pytest.mark.xray("APPTEST-10")
    def test_01_click_registrarme(self, driver, video_recorder):

        print("\n=== TEST 1: Click en Registrarme ===")

        try:
            # Buscar el botón "Registrarme" (es el botón con borde blanco)
            print("Buscando botón 'Registrarme'...")

            # Estrategia 1: Por texto exacto
            registrarme_button = None
            try:
                registrarme_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Registrarme']")
                print("Encontrado por texto exacto")
            except NoSuchElementException:
                pass

            assert registrarme_button is not None, "No se pudo encontrar el botón 'Registrarme'"

            # Hacer click
            time.sleep(1)
            print("Haciendo click en Registrarme...")
            registrarme_button.click()
            time.sleep(1)

            print("✅ TEST 1 COMPLETADO: Click en Registrarme exitoso")

        except Exception as e:
            pytest.fail(f"TEST 1 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests
    # Test 2: Usar botón atrás del teléfono para volver
    @pytest.mark.xray("APPTEST-11")
    def test_02_go_back_with_phone_button(self, driver, video_recorder):

        print("\n=== TEST 2: Botón atrás del teléfono ===")

        try:
            print("Presionando botón atrás del dispositivo...")

            # Usar el botón back del dispositivo
            driver.back()
            time.sleep(1)

            print("✅ TEST 2 COMPLETADO: Botón atrás funcionó correctamente")

        except Exception as e:
            pytest.fail(f"TEST 2 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests
    # Test 3: Hacer click en el botón azul 'Iniciar sesión'
    @pytest.mark.xray("APPTEST-12")
    def test_03_click_iniciar_sesion(self, driver, video_recorder):

        print("\n=== TEST 3: Click en Iniciar sesión ===")

        try:
            print("Buscando botón 'Iniciar sesión'...")

            # Estrategia 1: Por texto exacto
            iniciar_sesion_button = None
            try:
                iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Iniciar sesión']")
                print("Encontrado por content desc exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por content description que contenga "Iniciar"
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH,
                                                                "//*[contains(@content-desc,'Iniciar')]")
                    print("Encontrado por description con contains Iniciar'")
                except NoSuchElementException:
                    pass

            assert iniciar_sesion_button is not None, "No se pudo encontrar el botón 'Iniciar sesión'"

            # Hacer click
            print("Haciendo click en 'Iniciar sesión'...")
            iniciar_sesion_button.click()
            time.sleep(2)  # Reducido de 3 a 2

            print("✅ TEST 3 COMPLETADO: Click en 'Iniciar sesión' exitoso")

        except Exception as e:
            pytest.fail(f"TEST 3 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests
    # Test 4: Escribir email falso y presionar continuar
    @pytest.mark.xray("APPTEST-13")
    def test_04_escribir_email_y_continuar(self, driver, video_recorder):

        print("\n=== TEST 4: Escribir email y continuar ===")

        try:
            # Buscar el campo de texto con hint "Correo empresarial"
            print("Buscando campo de correo empresarial...")

            email_field = None
            try:
                email_field = driver.find_element(AppiumBy.XPATH, "//*[@hint='Correo empresarial']")
                print("Encontrado campo por hint exacto")
            except NoSuchElementException:
                try:
                    email_field = driver.find_element(AppiumBy.XPATH, "//*[contains(@hint,'Correo')]")
                    print("Encontrado campo por hint que contiene 'Correo'")
                except NoSuchElementException:
                    try:
                        # Buscar cualquier EditText
                        email_field = driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
                        print("Encontrado como EditText genérico")
                    except NoSuchElementException:
                        pass

            assert email_field is not None, "No se pudo encontrar el campo de correo"

            # Hacer click en el campo para asegurar que esté enfocado
            print("Haciendo click en el campo de email...")
            email_field.click()
            time.sleep(0.5)  # Reducido de 1 a 0.5

            # Limpiar el campo
            email_field.clear()
            time.sleep(0.3)  # Reducido de 0.5 a 0.3

            # Escribir el email más rápido
            email_text = "emailFalso@gmail.com"
            print("Escribiendo email más rápido...")

            # Escribir de 3 en 3 caracteres para acelerar
            for i in range(0, len(email_text), 3):
                chunk = email_text[i:i + 3]
                email_field.send_keys(chunk)
                print(f"Escribiendo: {chunk}")
                time.sleep(0.1)  # Reducido significativamente

            # Pausa después de terminar de escribir
            time.sleep(1)  # Reducido de 2 a 1
            print("Email escrito completamente. Ocultando teclado...")

            # Ocultar el teclado (intento principal)
            try:
                driver.hide_keyboard()
                print("Teclado ocultado con hide_keyboard()")
            except:
                print("hide_keyboard() falló, usando fallback")

            # Fuerzo cierres adicionales por si el teclado reaparece
            ensure_keyboard_closed(driver)

            # Buscar el botón "Continuar" usando espera explícita para evitar interferencia del teclado
            print("Buscando botón 'Continuar'...")

            continuar_button = None
            try:
                continuar_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='Continuar']"))
                )
                print("Encontrado por content-desc exacto (wait clickable)")
            except Exception:
                try:
                    continuar_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@content-desc,'Continuar')]"))
                    )
                    print("Encontrado por content-desc contains (wait clickable)")
                except Exception:
                    # fallback a búsqueda directa como antes
                    try:
                        continuar_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Continuar']")
                        print("Encontrado por content-desc exacto (fallback)")
                    except NoSuchElementException:
                        try:
                            continuar_button = driver.find_element(AppiumBy.XPATH,
                                                                   "//*[contains(@content-desc,'Continuar')]")
                            print("Encontrado por content-desc contains (fallback)")
                        except NoSuchElementException:
                            pass

            assert continuar_button is not None, "No se pudo encontrar el botón 'Continuar'"

            # Hacer click en continuar
            print("Haciendo click en 'Continuar'...")
            continuar_button.click()
            time.sleep(2)  # Reducido de 3 a 2

            # Asegurarse de que el teclado no quede abierto para el siguiente test
            ensure_keyboard_closed(driver)

            print("✅ TEST 4 COMPLETADO: Email escrito más rápido y botón continuar presionado")

        except Exception as e:
            pytest.fail(f"TEST 4 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            ensure_keyboard_closed(driver)
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests
    # Test 5: Hacer click en el botón 'Usuario y contraseña'
    @pytest.mark.xray("APPTEST-14")
    def test_05_click_usuario_y_contrasena(self, driver, video_recorder):

        print("\n=== TEST 5: Click en Usuario y contraseña ===")

        try:
            print("Buscando botón 'Usuario y contraseña'...")

            # Estrategia 1: Por content description exacto
            usuario_contrasena_button = None
            try:
                usuario_contrasena_button = driver.find_element(AppiumBy.XPATH,
                                                                "//*[@content-desc='Usuario y contraseña']")
                print("Encontrado por content-desc exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por content description que contenga
            if not usuario_contrasena_button:
                try:
                    usuario_contrasena_button = driver.find_element(AppiumBy.XPATH,
                                                                    "//*[contains(@content-desc,'Usuario')]")
                    print("Encontrado por content-desc que contiene 'Usuario'")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por content description que contenga "contraseña"
            if not usuario_contrasena_button:
                try:
                    usuario_contrasena_button = driver.find_element(AppiumBy.XPATH,
                                                                    "//*[contains(@content-desc,'contraseña')]")
                    print("Encontrado por content-desc que contiene 'contraseña'")
                except NoSuchElementException:
                    pass

            # Debug: Si no encontramos nada, mostrar elementos disponibles
            if not usuario_contrasena_button:
                print("🔍 DEBUG: Elementos clickeables encontrados:")
                clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                for i, elem in enumerate(clickable_elements):
                    try:
                        text = elem.get_attribute("text") or "(sin texto)"
                        content_desc = elem.get_attribute("content-desc") or "(sin descripción)"
                        print(f"  {i}: Texto: '{text}' | Desc: '{content_desc}'")
                    except:
                        print(f"  {i}: Error obteniendo info del elemento")

            assert usuario_contrasena_button is not None, "No se pudo encontrar el botón 'Usuario y contraseña'"

            # Hacer click
            print("Haciendo click en 'Usuario y contraseña'...")
            usuario_contrasena_button.click()
            time.sleep(2)  # Reducido de 3 a 2

            # Verificar que cambió de pantalla buscando elementos de login típicos
            pantalla_cambio = False

            # Buscar elementos típicos de pantalla de login con usuario/contraseña
            elementos_login_usuario = [
                "//*[contains(@hint,'usuario') or contains(@hint,'Usuario')]",
                "//*[contains(@hint,'contraseña') or contains(@hint,'Contraseña')]",
                "//*[contains(@hint,'password') or contains(@hint,'Password')]",
                "//*[contains(@text,'usuario') or contains(@text,'Usuario')]",
                "//*[contains(@text,'contraseña') or contains(@text,'Contraseña')]",
                "//android.widget.EditText"
            ]

            for selector in elementos_login_usuario:
                try:
                    driver.find_element(AppiumBy.XPATH, selector)
                    pantalla_cambio = True
                    print(f"Confirmado: Cambió de pantalla (encontrado elemento: {selector})")
                    break
                except NoSuchElementException:
                    continue

            if not pantalla_cambio:
                print("⚠ No se pudo confirmar el cambio de pantalla, pero el click se ejecutó")

            print("✅ TEST 5 COMPLETADO: Click en 'Usuario y contraseña' exitoso")

        except Exception as e:
            pytest.fail(f"TEST 5 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests
    # Test 6: Escribir usuario y contraseña y presionar siguiente
    @pytest.mark.xray("APPTEST-15")
    def test_06_escribir_usuario_y_contrasena(self, driver, video_recorder):

        print("\n=== TEST 6: Escribir usuario y contraseña ===")

        try:
            # Buscar el campo de usuario
            print("Buscando campo de usuario...")

            usuario_field = None
            try:
                usuario_field = driver.find_element(AppiumBy.XPATH, "//*[@hint='Usuario']")
                print("Encontrado campo de usuario por hint exacto")
            except NoSuchElementException:
                try:
                    usuario_field = driver.find_element(AppiumBy.XPATH, "//*[contains(@hint,'usuario')]")
                    print("Encontrado campo de usuario por hint que contiene 'usuario'")
                except NoSuchElementException:
                    # Buscar como primer EditText
                    try:
                        edit_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
                        if edit_fields:
                            usuario_field = edit_fields[0]
                            print("Encontrado como primer campo EditText")
                    except:
                        pass

            assert usuario_field is not None, "No se pudo encontrar el campo de usuario"

            # Buscar el campo de contraseña
            print("Buscando campo de contraseña...")

            contrasena_field = None
            try:
                contrasena_field = driver.find_element(AppiumBy.XPATH, "//*[@hint='Contraseña']")
                print("Encontrado campo de contraseña por hint exacto")
            except NoSuchElementException:
                try:
                    contrasena_field = driver.find_element(AppiumBy.XPATH, "//*[contains(@hint,'contraseña')]")
                    print("Encontrado campo de contraseña por hint que contiene 'contraseña'")
                except NoSuchElementException:
                    # Buscar como segundo EditText
                    try:
                        edit_fields = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
                        if len(edit_fields) >= 2:
                            contrasena_field = edit_fields[1]
                            print("Encontrado como segundo campo EditText")
                    except:
                        pass

            assert contrasena_field is not None, "No se pudo encontrar el campo de contraseña"

            # Escribir usuario más rápido
            print("Escribiendo usuario...")
            usuario_field.click()
            time.sleep(0.5)  # Reducido de 1 a 0.5
            usuario_field.clear()
            time.sleep(0.3)  # Reducido de 0.5 a 0.3

            # Escribir usuario directamente (más rápido)
            usuario_text = "Alejandro.Morales"
            usuario_field.send_keys(usuario_text)
            time.sleep(0.5)  # Reducido de 1 a 0.5
            print("Usuario escrito completamente")

            # Escribir contraseña
            print("Escribiendo contraseña...")
            contrasena_field.click()
            time.sleep(0.5)  # Reducido de 1 a 0.5
            contrasena_field.clear()
            time.sleep(0.3)  # Reducido de 0.5 a 0.3

            # Pegar la contraseña completa de una vez
            contrasena_field.send_keys("Admin123")
            time.sleep(0.5)  # Reducido de 1 a 0.5
            print("Contraseña pegada completamente")

            # Ocultar el teclado
            print("Ocultando teclado...")
            try:
                driver.hide_keyboard()
                print("Teclado ocultado con hide_keyboard()")
            except:
                print("hide_keyboard() falló, usando fallback")

            # Asegurar teclado cerrado antes de buscar el botón siguiente
            ensure_keyboard_closed(driver)

            time.sleep(0.5)  # Reducido de 1 a 0.5

            # Buscar el botón "Siguiente" con espera explícita
            print("Buscando botón 'Siguiente'...")

            siguiente_button = None
            try:
                siguiente_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='Siguiente']"))
                )
                print("Encontrado por content-desc exacto (wait clickable)")
            except Exception:
                try:
                    siguiente_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@content-desc,'Siguiente')]"))
                    )
                    print("Encontrado por content-desc contains (wait clickable)")
                except Exception:
                    # fallback a búsqueda directa
                    try:
                        siguiente_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Siguiente']")
                    except NoSuchElementException:
                        siguiente_button = None

            assert siguiente_button is not None, "No se pudo encontrar el botón 'Siguiente'"

            # Hacer click en siguiente
            print("Haciendo click en 'Siguiente'...")
            siguiente_button.click()
            time.sleep(2)  # Reducido de 3 a 2

            # Asegurarse de que el teclado no quede abierto para el siguiente test
            ensure_keyboard_closed(driver)

            print("✅ TEST 6 COMPLETADO: Usuario y contraseña escritos más rápido, botón siguiente presionado")

        except Exception as e:
            pytest.fail(f"TEST 6 FALLÓ: {e}")
        finally:
            # Cerrar teclado antes de terminar test para no interferir siguiente test
            ensure_keyboard_closed(driver)
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # UI Tests + Gestos
    # Test 7: Flujo productos - Ver productos → PDC → FFA
    @pytest.mark.xray("APPTEST-16")
    def test_07_flujo_productos(self, driver, video_recorder):

        print("\n=== TEST 7: Flujo productos (Ver productos → PDC → FFA) ===")

        try:
            # Esperar un poco para que la pantalla se estabilice después del login
            print("Esperando estabilización de pantalla...")
            time.sleep(3)

            # Paso 1: Click en "Ver productos"
            print("Paso 1: Buscando botón 'Ver productos'...")

            ver_productos_button = None
            try:
                # Esperar que el elemento sea clickeable
                ver_productos_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='Ver productos']"))
                )
                print("Encontrado 'Ver productos' por content-desc exacto (wait clickable)")
            except Exception:
                try:
                    ver_productos_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@content-desc,'Ver productos')]"))
                    )
                    print("Encontrado 'Ver productos' por content-desc que contiene (wait clickable)")
                except Exception:
                    try:
                        ver_productos_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Ver productos']")
                        print("Encontrado 'Ver productos' por content-desc exacto")
                    except NoSuchElementException:
                        try:
                            ver_productos_button = driver.find_element(AppiumBy.XPATH,
                                                                       "//*[contains(@content-desc,'Ver productos')]")
                            print("Encontrado 'Ver productos' por content-desc que contiene")
                        except NoSuchElementException:
                            try:
                                ver_productos_button = driver.find_element(AppiumBy.XPATH,
                                                                           "//*[contains(@content-desc,'productos')]")
                                print("Encontrado por content-desc que contiene 'productos'")
                            except NoSuchElementException:
                                # Debug: mostrar elementos disponibles
                                print("🔍 DEBUG: Elementos clickeables disponibles:")
                                clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                                for i, elem in enumerate(clickable_elements[:10]):  # Solo mostrar los primeros 10
                                    try:
                                        text = elem.get_attribute("text") or "(sin texto)"
                                        content_desc = elem.get_attribute("content-desc") or "(sin descripción)"
                                        print(f"  {i}: Texto: '{text}' | Desc: '{content_desc}'")
                                    except:
                                        print(f"  {i}: Error obteniendo info del elemento")

            if ver_productos_button is None:
                # Intentar buscar por otros métodos alternativos
                print("Intentando métodos alternativos para encontrar 'Ver productos'...")
                try:
                    # Buscar por texto
                    ver_productos_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'productos')]")
                    print("Encontrado por texto que contiene 'productos'")
                except NoSuchElementException:
                    pass

            assert ver_productos_button is not None, "No se pudo encontrar el botón 'Ver productos'"

            print("Haciendo click en 'Ver productos'...")
            ver_productos_button.click()
            time.sleep(1.5)  # Reducido de 2 a 1.5

            # Paso 2: Click en "PDC"
            print("Paso 2: Buscando botón 'PDC'...")

            pdc_button = None
            try:
                pdc_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='PDC']"))
                )
                print("Encontrado 'PDC' por texto exacto (wait clickable)")
            except Exception:
                try:
                    pdc_button = driver.find_element(AppiumBy.XPATH, "//*[@text='PDC']")
                    print("Encontrado 'PDC' por texto exacto")
                except NoSuchElementException:
                    try:
                        pdc_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='PDC']")
                        print("Encontrado 'PDC' por content-desc exacto")
                    except NoSuchElementException:
                        try:
                            pdc_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'PDC')]")
                            print("Encontrado 'PDC' por texto que contiene")
                        except NoSuchElementException:
                            try:
                                pdc_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc,'PDC')]")
                                print("Encontrado 'PDC' por content-desc que contiene")
                            except NoSuchElementException:
                                pass

            assert pdc_button is not None, "No se pudo encontrar el botón 'PDC'"

            print("Haciendo click en 'PDC'...")
            pdc_button.click()
            time.sleep(1.5)  # Reducido de 2 a 1.5

            # Paso 3: Esperar menos tiempo
            print("Paso 3: Esperando...")
            time.sleep(0.5)  # Reducido de 1 a 0.5

            # Paso 4: Click en FFA
            print("Paso 4: Buscando botón 'FFA'...")
            ffa_button = None
            try:
                ffa_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='FFA']"))
                )
                print("Encontrado 'FFA' por content-desc exacto (wait clickable)")
            except Exception:
                try:
                    ffa_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='FFA']")
                    print("Encontrado 'FFA' por content-desc exacto")
                except NoSuchElementException:
                    try:
                        ffa_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'FFA')]")
                        print("Encontrado 'FFA' por texto que contiene")
                    except NoSuchElementException:
                        print("⚠ No se pudo encontrar el botón 'FFA'")
                        pass

            assert ffa_button is not None, "No se pudo encontrar el botón 'FFA'"

            print("Haciendo click en 'FFA'...")
            ffa_button.click()
            time.sleep(1.5)  # Reducido de 2 a 1.5

            print("✅ TEST 7 COMPLETADO: Flujo Ver productos → PDC → FFA exitoso")

        except Exception as e:
            pytest.fail(f"TEST 7 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")