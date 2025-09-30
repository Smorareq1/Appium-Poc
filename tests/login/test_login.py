import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------
# Helpers reutilizables
# ------------------------
def ensure_keyboard_closed(driver):
    """Intentar cerrar el teclado por varios métodos."""
    try:
        driver.hide_keyboard()
        print("Teclado cerrado con hide_keyboard()")
    except Exception:
        try:
            if driver.is_keyboard_shown():
                driver.back()
                print("Teclado cerrado con back()")
        except Exception:
            try:
                size = driver.get_window_size()
                x = int(size['width'] / 2)
                y = int(size['height'] * 0.1)  # zona superior
                driver.tap([(x, y)], 100)
                print("Teclado cerrado con tap en zona vacía")
            except Exception:
                print("No se pudo cerrar el teclado, continuando...")
    time.sleep(0.5)

def wait_clickable(driver, xpath, timeout=8):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
    )

def find_first(driver, xpaths):
    """Devuelve el primer elemento que exista para una lista de XPATHs."""
    for xp in xpaths:
        try:
            el = driver.find_element(AppiumBy.XPATH, xp)
            print(f"Encontrado: {xp}")
            return el
        except NoSuchElementException:
            continue
    return None

def go_back(driver):
    driver.back()
    time.sleep(1)


# ==========================================================
# Suite por FEATURES (uno a uno según la tabla del screenshot)
# ==========================================================
class TestFeaturesAutenticacion:

    @pytest.mark.xray("APPTEST-73")
    def test_click_registrarme(self, driver, video_recorder):

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
            go_back(driver)
            time.sleep(1)

            print("✅ TEST 1 COMPLETADO: Click en Registrarme exitoso")

        except Exception as e:
            pytest.fail(f"TEST 1 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-62")
    def test_iniciar_sesion_con_correo(self, driver, video_recorder):
        """
        Flujo: Home -> 'Iniciar sesión' -> ingresar correo -> 'Continuar'
        Éxito: llegar a pantalla siguiente (p.ej. ver 'Usuario y contraseña' o 'Verificar código')
        """
        print("\n=== FEATURE: Iniciar sesión con correo ===")
        try:
            # Ir a 'Iniciar sesión'
            iniciar = find_first(driver, [
                "//*[@content-desc='Iniciar sesión']",
                "//*[contains(@content-desc,'Iniciar')]"
            ])
            assert iniciar, "No se encontró el botón 'Iniciar sesión'"
            iniciar.click()
            time.sleep(1)

            # Campo correo (ajustado desde tu test del email)
            email_field = find_first(driver, [
                "//*[@hint='Correo empresarial']",
                "//*[contains(@hint,'Correo')]",
                "//android.widget.EditText"
            ])
            assert email_field, "No se encontró el campo de correo"
            email_field.click()
            time.sleep(0.3)
            try:
                email_field.clear()
            except Exception:
                pass

            email_text = "sebastian.morales@grupopdc.com"
            email_field.send_keys(email_text)
            print(f"Escrito correo: {email_text}")
            ensure_keyboard_closed(driver)

            # Botón Continuar
            continuar = None
            try:
                continuar = wait_clickable(driver, "//*[@content-desc='Continuar']", timeout=6)
            except Exception:
                continuar = find_first(driver, ["//*[contains(@content-desc,'Continuar')]"])
            assert continuar, "No se encontró el botón 'Continuar'"
            continuar.click()
            time.sleep(2)

            # 0) Error visible
            error_msg = find_first(driver, [
                "//*[contains(@text,'Ingrese un correo válido') or contains(@content-desc,'Ingrese un correo válido')]"
            ])

            assert error_msg is None, "Se mostró 'Ingrese un correo válido' — el correo ingresado es inválido"

            # 1) Atajo: botón "Validar"
            validar_btn = find_first(driver, [
                "//*[@content-desc='Validar']",
                "//*[contains(@content-desc,'Validar') or contains(@text,'Validar')]"
            ])
            if validar_btn:
                print("✅ Encontrado botón 'Validar' tras enviar correo")
            else:
                # 2) Criterios de llegada alternos
                llego_siguiente = find_first(driver, [
                    "//*[contains(@content-desc,'Verificar') or contains(@text,'Verificar')]",
                    "//*[contains(@content-desc,'código') or contains(@text,'código')]",
                ])
                assert llego_siguiente, "No se detectó pantalla posterior al envío de correo"

                print("✅ Login por CORREO llegó a la siguiente pantalla correctamente")

        except Exception as e:
            pytest.fail(f"Login por correo FALLO: {e}")
        finally:
            ensure_keyboard_closed(driver)
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-63")
    def test_verificar_inicio_de_sesion(self, driver, video_recorder):
        """
        Verificación por OTP:
        1) Recibe el código (variable)
        2) Ingresa dígito por dígito en las 6 casillas
        3) Presiona 'Validar'
        4) Si aparece 'Pin inválido' -> FAIL
        """
        print("\n=== FEATURE: Verificar inicio de sesión (OTP) ===")
        try:
            # 1) Código recibido (reemplaza por tu inyección/mock)
            otp_code = "123456"

            # 2) Localizar las 6 casillas (EditText de 1 carácter)
            otp_inputs = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if not otp_inputs or len(otp_inputs) < 4:
                pytest.fail("Pantalla de OTP no presente (no se hallaron casillas)")

            # Asegurar no escribir más dígitos de los disponibles
            for i, ch in enumerate(otp_code[:len(otp_inputs)]):
                el = otp_inputs[i]
                el.click()
                time.sleep(0.1)
                try:
                    el.clear()
                except Exception:
                    pass
                el.send_keys(ch)
                time.sleep(0.1)

            ensure_keyboard_closed(driver)

            # 3) Botón 'Validar'
            validar_btn = find_first(driver, [
                "//*[@content-desc='Validar']",
                "//*[contains(@content-desc,'Validar') or contains(@text,'Validar')]"
            ])
            assert validar_btn, "No se encontró botón 'Validar'"
            validar_btn.click()
            time.sleep(2)

            # 4) Si aparece mensaje de error -> FAIL
            pin_invalido = find_first(driver, [
                "//*[contains(@text,'Pin inválido') or contains(@content-desc,'Pin inválido')]",
                "//*[contains(@text,'PIN inválido') or contains(@content-desc,'PIN inválido')]",
                "//*[contains(@text,'pin inválido') or contains(@content-desc,'pin inválido')]",
                "//*[contains(@text,'Pin invalido') or contains(@content-desc,'Pin invalido')]"
            ])

            if pin_invalido:
                go_back(driver)
                pytest.fail("Se mostró 'Pin inválido' al validar el OTP")

            print("✅ OTP validado correctamente")

        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Verificación FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-64")
    def test_iniciar_sesion_con_telefono(self, driver, video_recorder):
        """
            Este test debe FALLAR porque el feature no está implementado.
        """
        print("\n=== FEATURE: Iniciar sesión con teléfono ===")
        try:
            # Forzamos el fallo explícito por no implementación
            raise NotImplementedError("Feature 'Iniciar sesión con teléfono' no implementada aún")
        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Login con teléfono FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-65")
    def test_cambiar_contrasena(self, driver, video_recorder):
        print("\n=== FEATURE: Cambiar contraseña ===")
        try:
            btn = find_first(driver, [
                "//*[@content-desc='Usuario y contraseña']",
                "//*[contains(@content-desc,'Usuario')]",
                "//*[contains(@content-desc,'contraseña')]"
            ])
            assert btn, "No se encontró el botón 'Usuario y contraseña'"
            btn.click()
            time.sleep(1)

            cambiar = find_first(driver, [
                "//*[@content-desc='Olvidé mi contraseña']",
                "//*[contains(@content-desc,'Olvidé')]",
            ])
            assert cambiar, "No se encontró opción 'Cambiar contraseña'"
            cambiar.click(); time.sleep(1)

            pytest.fail("Feature 'Cambiar contraseña' no implementada aún)")

        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Cambiar contraseña FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

        # -----------------------------------
        # 3) Verificar inicio de sesión (OTP)
        # -----------------------------------
        @pytest.mark.xray("APPTEST-VERIFICAR-LOGIN")
        def test_04_verificar_inicio_de_sesion(self, driver, video_recorder):
            """
            Plantilla para verificación por correo/SMS: ingresar código OTP y confirmar.
            """
            print("\n=== FEATURE: Verificar inicio de sesión (OTP) ===")
            try:
                otp_box = find_first(driver, [
                    "//*[@hint='Código']",
                    "//*[contains(@hint,'código') or contains(@text,'código')]",
                    "(//android.widget.EditText)[1]"
                ])
                if not otp_box:
                    pytest.skip("Pantalla de OTP no presente (flujo previo no llegó o no aplica)")
                otp_box.send_keys("000000")  # <--- reemplaza por mock/OTP real si lo conectas

                confirmar = find_first(driver, [
                    "//*[@content-desc='Verificar']",
                    "//*[contains(@content-desc,'Verificar')]",
                    "//*[@content-desc='Confirmar']"
                ])
                assert confirmar, "No se encontró botón para confirmar verificación"
                ensure_keyboard_closed(driver)
                confirmar.click()
                time.sleep(2)

                # Espera llegar a home
                home_anchor = find_first(driver, [
                    "//*[@content-desc='Ver productos']",
                    "//*[contains(@content-desc,'productos')]"
                ])
                assert home_anchor, "No llegó a pantalla post-verificación"

                print("✅ Verificación de inicio de sesión OK")
            except pytest.skip.Exception:
                raise
            except Exception as e:
                pytest.fail(f"Verificación FALLO: {e}")
            finally:
                vp = video_recorder()
                if vp:
                    print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-66")
    def test_iniciar_sesion_usuario_contrasena(self, driver, video_recorder):
        """
        Flujo: pantalla post-correo -> 'Usuario y contraseña' -> escribir ambos -> 'Siguiente'
        Éxito: ver un elemento de pantalla principal (ej. 'Ver productos').
        """
        print("\n=== FEATURE: Iniciar sesión con Usuario y Contraseña ===")
        try:
            # Campos usuario/contraseña (reutilizado/compactado)
            usuario = find_first(driver, [
                "//*[@hint='Usuario']",
                "//*[contains(@hint,'usuario')]",
                "(//android.widget.EditText)[1]"
            ])
            assert usuario, "No se encontró el campo de usuario"
            usuario.click();
            time.sleep(0.2)
            try:
                usuario.clear()
            except:
                pass
            usuario.send_keys("Nelson.Zarat")

            contrasena = find_first(driver, [
                "//*[@hint='Contraseña']",
                "//*[contains(@hint,'contraseña')]",
                "(//android.widget.EditText)[2]"
            ])
            assert contrasena, "No se encontró el campo de contraseña"
            contrasena.click();
            time.sleep(0.2)
            try:
                contrasena.clear()
            except:
                pass
            contrasena.send_keys("Admin1234")

            ensure_keyboard_closed(driver)

            # 'Siguiente'
            siguiente = None
            try:
                siguiente = wait_clickable(driver, "//*[@content-desc='Siguiente']", timeout=6)
            except Exception:
                siguiente = find_first(driver, ["//*[contains(@content-desc,'Siguiente')]"])
            assert siguiente, "No se encontró el botón 'Siguiente'"
            siguiente.click()
            time.sleep(2)

            # Ver productos button
            ver_productos = None
            ver_productos = find_first(driver, [
                "//*[@content-desc='Ver productos']",
                "//*[contains(@content-desc,'productos')]"
            ])
            assert ver_productos, "No parece haber navegado a la pantalla principal"
            ver_productos.click()
            time.sleep(2)

            #PDC button
            pdc = None
            pdc = find_first(driver, [
                "//*[@content-desc='PDC']",
                "//*[contains(@content-desc,'PDC')]"
            ])
            assert pdc, "No parece haber navegado a la pantalla principal"
            pdc.click()
            time.sleep(2)

            #Click en FFA solo si aparece
            # Click en FFA solo si aparece
            ffa = None
            try:
                ffa = wait_clickable(driver, "//*[@content-desc='FFA']", timeout=4)
            except Exception:
                ffa = find_first(driver, [
                    "//*[@content-desc='FFA']",
                    "//*[contains(@text,'FFA')]",
                ])

            if ffa:
                print("FFA visible, haciendo click...")
                ffa.click()
                time.sleep(1.5)
            else:
                print("⚠ FFA no apareció; se omite el click.")

            menu_button = find_first(driver, [
                "//*[@content-desc='Menú']",
                "//*[contains(@content-desc,'Menú')]"
            ])

            assert menu_button, "No se pudo encontrar el botón 'Menú'"
            print("✅ Botón 'Menú' encontrado")

            print("✅ Login por USUARIO+CONTRASEÑA exitoso")

        except Exception as e:
            pytest.fail(f"Login usuario/contraseña FALLO: {e}")
        finally:
            ensure_keyboard_closed(driver)
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-67")
    def test_sincronizacion(self, driver, video_recorder):
        """
        Este test debe FALLAR porque el feature no está implementado.
        """
        print("\n=== FEATURE: Sincronizacion ===")
        try:
            # Forzamos el fallo explícito por no implementación
            raise NotImplementedError("Feature 'Sincronizacion' no implementada aún")
        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Sincronizacion FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-71")
    def test_dashboard_de_metas(self, driver, video_recorder):
        """
        Flujo: Navega y hace clic en la opción 'Mis Métricas' desde el menú principal.
        Éxito: El botón es encontrado y se hace clic en él sin errores.
        """
        print("\n=== FEATURE: Dashboard de metas (Mis Métricas) ===")
        try:
            # MENU
            print("Paso 1: Buscando botón 'menu'...")
            menu_button = find_first(driver, [
                "//*[@content-desc='Menú']",
                "//*[contains(@content-desc,'Menú')]"
            ])
            assert menu_button, "No se pudo encontrar el botón 'Menú'"
            print("✅ Botón 'Menú' encontrado")
            menu_button.click()
            time.sleep(1.5)

            # Mis metricas
            print("Buscando el botón 'Mis Métricas'...")
            mis_metricas_button = find_first(driver, [
                "//*[@content-desc='Mis Métricas']",
                "//*[contains(@content-desc,'Métricas')]"
            ])
            assert mis_metricas_button, "No se pudo encontrar el botón 'Mis Métricas' en la pantalla."
            rect = mis_metricas_button.rect
            x = int(rect['x'] + rect['width'] * 0.25)
            y = int(rect['y'] + rect['height'] / 2)
            driver.tap([(x, y)])
            time.sleep(3)

            # Mi progreso
            progreso_button = find_first(driver, [
                "//*[@content-desc='Mi progreso']",
                "//*[contains(@content-desc,'progreso')]"
            ])
            assert progreso_button, "No se pudo encontrar el botón 'Mi Progreso'"
            print("✅ Botón 'Mi progreso' encontrado")
            progreso_button.click()
            time.sleep(1.5)

            # Validar que aparezcan los elementos esperados
            print("Validando elementos en la pantalla 'Mis Métricas'...")
            efectividad_diaria = find_first(driver, [
                "//*[@content-desc='Efectividad de venta diaria']",
                "//*[contains(@content-desc,'Efectividad de venta diaria')]"
            ])
            assert efectividad_diaria, "No se encontró 'Efectividad de venta diaria'"
            print("✅ 'Efectividad de venta diaria' encontrado")

            necesidad_mensual = find_first(driver, [
                "//*[@content-desc='Necesidad venta mensual']",
                "//*[contains(@content-desc,'Necesidad venta mensual')]"
            ])
            assert necesidad_mensual, "No se encontró 'Necesidad venta mensual'"
            print("✅ 'Necesidad venta mensual' encontrado")

            efectividad_mensual = find_first(driver, [
                "//*[@content-desc='Efectividad de venta mensual']",
                "//*[contains(@content-desc,'Efectividad de venta mensual')]"
            ])
            assert efectividad_mensual, "No se encontró 'Efectividad de venta mensual'"
            print("✅ 'Efectividad de venta mensual' encontrado")

            print("✅ Todos los elementos validados correctamente")

            # Regresar en el teléfono
            print("Regresando a la pantalla anterior...")
            driver.back()
            time.sleep(2)

            driver.back()
            time.sleep(1)

            # FFA
            FFA_button = find_first(driver, [
                "//*[@content-desc='FFA']",
                "//*[contains(@content-desc,'FFA')]"
            ])

            assert FFA_button, "No se pudo encontrar el botón 'FFA'"
            print("✅ Botón 'FFA' encontrado")
            FFA_button.click()
            time.sleep(1.5)
            print("✅ TEST COMPLETADO: Validación exitosa y regreso completado.")

        except Exception as e:
            pytest.fail(f"El test de Dashboard de metas FALLÓ: {e}")
        finally:
            # Guardar el video de la ejecución de la prueba
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video de evidencia guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-68")
    def test_cerrar_sesion(self, driver, video_recorder):
        print("\n=== Cerrar Sesión (Menu → Scroll → Salir) ===")
        try:
            # Paso 1: Click en "menu"
            print("Paso 1: Buscando botón 'menu'...")

            menu_button = find_first(driver, [
                "//*[@content-desc='Menú']",
                "//*[contains(@content-desc,'Menú')]"
            ])

            assert menu_button, "No se pudo encontrar el botón 'Menú'"
            print("✅ Botón 'Menú' encontrado")
            menu_button.click()
            time.sleep(1.5)

            # Paso 2: Hacer scroll hacia abajo
            print("Paso 2: Haciendo scroll hacia abajo...")

            # Obtener dimensiones de la pantalla para el scroll
            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            # Scroll desde 80% hasta 20% de la altura de la pantalla
            start_x = screen_width // 2
            start_y = int(screen_height * 0.8)
            end_x = screen_width // 2
            end_y = int(screen_height * 0.2)

            driver.swipe(start_x, start_y, end_x, end_y, 800)  # Reducido de 1000 a 800ms
            time.sleep(0.5)  # Reducido de 1 a 0.5
            print("Scroll hacia abajo completado")

            # Paso 3: Presionar "salir"
            print("Paso 3: Buscando botón 'salir'...")

            salir_button = None
            try:
                salir_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Salir']")
                print("Encontrado 'salir' por content-desc exacto")
            except NoSuchElementException:
                try:
                    salir_button = driver.find_element(AppiumBy.XPATH, "//*[@text='Salir']")
                    print("Encontrado 'salir' por texto exacto")
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
            time.sleep(2)  # Reducido de 3 a 2

            print("✅ TEST 8 COMPLETADO: Flujo Menu → Scroll → Salir exitoso")

        except Exception as e:
            pytest.fail(f"TEST 8 FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-69")
    def test_inicio_sesion_offline(self, driver, video_recorder):
        """
            Este test debe FALLAR porque el feature no está implementado.
        """
        print("\n=== FEATURE: Inicio sesion offline ===")
        try:
            # Forzamos el fallo explícito por no implementación
            raise NotImplementedError("Feature 'Inicio sesion offline' no implementada aún")
        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Inicio sesion offline FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")

    @pytest.mark.xray("APPTEST-70")
    def test_offline_uso_general(self, driver, video_recorder):
        """
        Este test debe FALLAR porque el feature no está implementado.
        """
        print("\n=== FEATURE: Uso offline ===")
        try:
            # Forzamos el fallo explícito por no implementación
            raise NotImplementedError("Feature 'Uso offline' no implementada aún")
        except pytest.skip.Exception:
            raise
        except Exception as e:
            pytest.fail(f"Uso offline FALLO: {e}")
        finally:
            vp = video_recorder()
            if vp:
                print(f"📹 Video: {vp}")
