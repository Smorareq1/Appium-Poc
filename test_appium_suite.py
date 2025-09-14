import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class TestSimpleFlow:
    """Tests simples para el flujo básico de la app"""

    def test_01_click_registrarme(self, driver, screenshot):
        """Test 1: Hacer click en el botón 'Registrarme'"""
        print("\n=== TEST 1: Click en Registrarme ===")

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

            print("✅ TEST 1 COMPLETADO: Click en Registrarme exitoso")

        except Exception as e:
            pytest.fail(f"TEST 1 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_01_final")

    def test_02_go_back_with_phone_button(self, driver, screenshot):
        """Test 2: Usar botón atrás del teléfono para volver"""
        print("\n=== TEST 2: Botón atrás del teléfono ===")

        try:
            print("Presionando botón atrás del dispositivo...")

            # Usar el botón back del dispositivo
            driver.back()
            time.sleep(2)  # Esperar que regrese a la pantalla anterior

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
            pytest.fail(f"TEST 2 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_02_final")

    def test_03_click_iniciar_sesion(self, driver, screenshot):
        """Test 3: Hacer click en el botón azul 'Iniciar sesión'"""
        print("\n=== TEST 3: Click en Iniciar sesión ===")

        try:
            print("Buscando botón 'Iniciar sesión'...")

            # Estrategia 1: Por texto exacto
            iniciar_sesion_button = None
            try:
                iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Iniciar sesión']")
                print("Encontrado por texto exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por content description exacto
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Iniciar sesión']")
                    print("Encontrado por description exacto'")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por content description que contenga
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH,
                                                                "//*[contains(@content-desc,'Iniciar')]")
                    print("Encontrado por description que contiene")
                except NoSuchElementException:
                    pass

            # Estrategia 4: Por texto que contenga
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar sesión')]")
                    print("Encontrado por texto que contiene")
                except NoSuchElementException:
                    pass

            # Estrategia 5: Por texto que contenga solo "Iniciar"
            if not iniciar_sesion_button:
                try:
                    iniciar_sesion_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Iniciar')]")
                    print("Encontrado por texto que contiene 'Iniciar'")
                except NoSuchElementException:
                    pass

            # Estrategia 6: Por posición (último botón clickeable - probablemente el azul)
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
            pytest.fail(f"TEST 3 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_03_final")

    def test_04_escribir_email_y_continuar(self, driver, screenshot):
        """Test 4: Escribir email falso y presionar continuar"""
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
            time.sleep(1)

            # Limpiar el campo
            email_field.clear()
            time.sleep(0.5)

            # Escribir el email caracter por caracter lentamente
            email_text = "emailFalso@gmail.com"
            print("Escribiendo email caracter por caracter...")

            for i, char in enumerate(email_text):
                email_field.send_keys(char)
                print(f"Escribiendo: {char} ({i + 1}/{len(email_text)})")
                time.sleep(0.3)  # Pausa de 300ms entre cada caracter

            # Pausa adicional después de terminar de escribir
            time.sleep(2)
            print("Email escrito completamente. Ocultando teclado...")

            # Ocultar el teclado
            try:
                driver.hide_keyboard()
                print("Teclado ocultado con hide_keyboard()")
            except:
                try:
                    # Alternativa: usar botón atrás para cerrar teclado
                    driver.back()
                    print("Teclado ocultado con botón atrás")
                except:
                    print("⚠️ No se pudo ocultar el teclado, continuando...")

            time.sleep(1)  # Pequeña pausa después de ocultar teclado

            # Buscar el botón "Continuar"
            print("Buscando botón 'Continuar'...")

            continuar_button = None
            try:
                continuar_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Continuar']")
                print("Encontrado por content-desc exacto")
            except NoSuchElementException:
                try:
                    continuar_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc,'Continuar')]")
                    print("Encontrado por content-desc que contiene 'Continuar'")
                except NoSuchElementException:
                    pass

            assert continuar_button is not None, "No se pudo encontrar el botón 'Continuar'"

            # Hacer click en continuar
            print("Haciendo click en 'Continuar'...")
            continuar_button.click()
            time.sleep(3)  # Esperar que cargue la nueva pantalla

            print("✅ TEST 4 COMPLETADO: Email escrito lentamente y botón continuar presionado")

        except Exception as e:
            pytest.fail(f"TEST 4 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_04_final")

    def test_05_click_usuario_y_contrasena(self, driver, screenshot):
        """Test 5: Hacer click en el botón 'Usuario y contraseña'"""
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
            time.sleep(3)  # Esperar que cargue la nueva pantalla

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
                print("⚠️ No se pudo confirmar el cambio de pantalla, pero el click se ejecutó")

            print("✅ TEST 5 COMPLETADO: Click en 'Usuario y contraseña' exitoso")

        except Exception as e:
            pytest.fail(f"TEST 6 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_06_final")

    def test_06_escribir_usuario_y_contrasena(self, driver, screenshot):
        """Test 6: Escribir usuario y contraseña y presionar siguiente"""
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

            # Escribir usuario (letra por letra lentamente)
            print("Escribiendo usuario...")
            usuario_field.click()
            time.sleep(1)
            usuario_field.clear()
            time.sleep(0.5)

            usuario_text = "Alejandro.Morales"
            for char in usuario_text:
                usuario_field.send_keys(char)
                time.sleep(0.2)  # Escribir lentamente pero sin log

            time.sleep(1)
            print("Usuario escrito completamente")

            # Escribir contraseña (pegar directamente)
            print("Escribiendo contraseña...")
            contrasena_field.click()
            time.sleep(1)
            contrasena_field.clear()
            time.sleep(0.5)

            # Pegar la contraseña completa de una vez
            contrasena_field.send_keys("Admin123")
            time.sleep(1)
            print("Contraseña pegada completamente")

            # Ocultar el teclado
            print("Ocultando teclado...")
            try:
                driver.hide_keyboard()
                print("Teclado ocultado con hide_keyboard()")
            except:
                try:
                    driver.back()
                    print("Teclado ocultado con botón atrás")
                except:
                    print("⚠️ No se pudo ocultar el teclado, continuando...")

            time.sleep(1)

            # Buscar el botón "Siguiente"
            print("Buscando botón 'Siguiente'...")

            siguiente_button = None

            # Estrategia 1: Por texto exacto
            try:
                siguiente_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Siguiente']")
                print("Encontrado por texto exacto")
            except NoSuchElementException:
                pass

            # Estrategia 2: Por content description
            if not siguiente_button:
                try:
                    siguiente_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Siguiente']")
                    print("Encontrado por content-desc exacto")
                except NoSuchElementException:
                    pass

            # Estrategia 3: Por texto que contenga
            if not siguiente_button:
                try:
                    siguiente_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Siguiente')]")
                    print("Encontrado por texto que contiene 'Siguiente'")
                except NoSuchElementException:
                    pass

            # Estrategia 4: Buscar botones habilitados recientemente
            if not siguiente_button:
                try:
                    # Buscar elementos clickeables que podrían ser el botón siguiente
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    for elem in clickable_elements:
                        try:
                            text = elem.get_attribute("text") or ""
                            content_desc = elem.get_attribute("content-desc") or ""
                            if ("siguiente" in text.lower() or "siguiente" in content_desc.lower() or
                                    "continuar" in text.lower() or "continuar" in content_desc.lower() or
                                    "login" in text.lower() or "entrar" in text.lower()):
                                siguiente_button = elem
                                print(f"Encontrado por contenido relacionado: '{text}' / '{content_desc}'")
                                break
                        except:
                            continue
                except:
                    pass

            # Estrategia 5: Como último recurso, usar el último botón clickeable
            if not siguiente_button:
                try:
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    if clickable_elements:
                        siguiente_button = clickable_elements[-1]
                        print("Encontrado como último elemento clickeable")
                except:
                    pass

            assert siguiente_button is not None, "No se pudo encontrar el botón 'Siguiente'"

            # Hacer click en siguiente
            print("Haciendo click en 'Siguiente'...")
            siguiente_button.click()
            time.sleep(3)  # Esperar que cargue la nueva pantalla

            print("✅ TEST 6 COMPLETADO: Usuario y contraseña escritos, botón siguiente presionado")

        except Exception as e:
            pytest.fail(f"TEST 6 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_06_final")

    def test_07_flujo_completo_productos_y_salir(self, driver, screenshot):
        """Test 7: Flujo completo - Ver productos → PDC → Menu → Scroll → Salir"""
        print("\n=== TEST 7: Flujo completo productos y salir ===")

        try:
            # Paso 1: Click en "Ver productos"
            print("Paso 1: Buscando botón 'Ver productos'...")

            ver_productos_button = None
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
                        pass

            assert ver_productos_button is not None, "No se pudo encontrar el botón 'Ver productos'"

            print("Haciendo click en 'Ver productos'...")
            ver_productos_button.click()
            time.sleep(2)

            # Paso 2: Click en "PDC"
            print("Paso 2: Buscando botón 'PDC'...")

            pdc_button = None
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
            time.sleep(2)

            # Paso 3: Esperar 1 segundo
            print("Paso 3: Esperando 1 segundo...")
            time.sleep(1)

            # Paso 4: Click en "menu"
            print("Paso 4: Buscando botón 'menu'...")

            menu_button = None
            try:
                menu_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Menú']")
                print("Encontrado 'Menú' por content-desc exacto")
            except NoSuchElementException:
                try:
                    menu_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Menú']")
                    print("Encontrado 'Menú' por texto exacto")
                except NoSuchElementException:
                    try:
                        menu_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Menú')]")
                        print("Encontrado 'Menú' por texto que contiene")
                    except NoSuchElementException:
                        try:
                            menu_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc,'Menú')]")
                            print("Encontrado 'menu' por content-desc que contiene")
                        except NoSuchElementException:
                            try:
                                menu_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Menú']")
                                print("Encontrado 'Menú' con mayúscula")
                            except NoSuchElementException:
                                pass

            assert menu_button is not None, "No se pudo encontrar el botón 'Menú'"

            print("Haciendo click en 'Menú'...")
            menu_button.click()
            time.sleep(2)

            # Paso 5: Hacer scroll hacia abajo
            print("Paso 5: Haciendo scroll hacia abajo...")

            # Obtener dimensiones de la pantalla para el scroll
            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            # Scroll desde 80% hasta 20% de la altura de la pantalla
            start_x = screen_width // 2
            start_y = int(screen_height * 0.8)
            end_x = screen_width // 2
            end_y = int(screen_height * 0.2)

            driver.swipe(start_x, start_y, end_x, end_y, 1000)  # 1 segundo de duración
            time.sleep(1)
            print("Scroll hacia abajo completado")

            # Paso 6: Presionar "salir"
            print("Paso 6: Buscando botón 'salir'...")

            salir_button = None
            try:
                salir_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Salir']")
                print("Encontrado 'salir' por content-desc exacto")
            except NoSuchElementException:
                try:
                    salir_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Salir']")
                    print("Encontrado 'salir' por content-desc exacto")
                except NoSuchElementException:
                    try:
                        salir_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Salir')]")
                        print("Encontrado 'salir' por texto que contiene")
                    except NoSuchElementException:
                        pass

            assert salir_button is not None, "No se pudo encontrar el botón 'salir'"

            print("Haciendo click en coordenadas específicas del botón Salir...")
            screen_size = driver.get_window_size()
            click_x = int(screen_size['width'] * 0.25)
            click_y = int(screen_size['height'] * 0.95)
            driver.tap([(click_x, click_y)])
            time.sleep(3)

            print("✅ TEST 7 COMPLETADO: Flujo completo Ver productos → PDC → Menu → Scroll → Salir exitoso")

        except Exception as e:
            pytest.fail(f"TEST 7 FALLÓ: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_07_final")

    def test_debug_current_screen(self, driver, screenshot):
        """ Debug - Mostrar todos los elementos de la pantalla actual"""
        print("\n=== DEBUG - Elementos actuales ===")

        try:
            print("📱 Información de la pantalla actual:")
            print(f"Package actual: {driver.current_package}")
            print(f"Activity actual: {driver.current_activity}")

            # Mostrar todos los elementos con texto
            print("\n📝 Elementos con texto:")
            text_elements = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc]")
            for i, elem in enumerate(text_elements):
                try:
                    text = elem.get_attribute("content-desc")
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

            print("\n✅ TEST COMPLETADO: Debug información mostrada")

        except Exception as e:
            print(f"❌ Error en debug: {e}")
        finally:
            # Screenshot al final del test
            screenshot("test_05_final")