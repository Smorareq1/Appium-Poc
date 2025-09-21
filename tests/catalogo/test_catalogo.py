import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class test_catalogo:
    @pytest.mark.xray("APPTEST-9999") #KEY
    def test_click_catalogo_button(self, driver, video_recorder):
        """Test para hacer click en el botón Catálogo"""
        print("\n=== TEST: Click en botón Catálogo ===")

        try:
            catalogo_button = None

            # Estrategia 1: Por content-desc exacto
            print("Buscando botón 'Catálogo' por content-desc exacto...")
            try:
                catalogo_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Catálogo']")
                print("✅ Encontrado por content-desc exacto")
            except NoSuchElementException:
                print("❌ No encontrado por content-desc exacto")

            # Estrategia 2: Por contains en content-desc
            if not catalogo_button:
                print("Buscando botón 'Catálogo' por contains en content-desc...")
                try:
                    catalogo_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Catálogo')]")
                    print("✅ Encontrado por contains en content-desc")
                except NoSuchElementException:
                    print("❌ No encontrado por contains en content-desc")

            # Verificar que se encontró el botón
            assert catalogo_button is not None, "No se pudo encontrar el botón 'Catálogo'"

            # Hacer click en el botón
            print("Haciendo click en botón 'Catálogo'...")
            catalogo_button.click()
            time.sleep(2)  # Esperar que cargue la pantalla

            print("✅ TEST COMPLETADO: Click en botón 'Catálogo' exitoso")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-9999")
    def test_click_combobox_selecciona_cliente(self, driver, video_recorder):
        """Test para hacer click en el combobox 'Selecciona un cliente'"""
        print("\n=== TEST: Click en combobox 'Selecciona un cliente' ===")

        try:
            # Buscar elemento clickeable cerca del texto "Selecciona un cliente"
            print("Buscando elemento clickeable cerca del texto...")

            # Primero ubicar el texto como referencia
            texto_elemento = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Selecciona un cliente']")
            print("✅ Texto 'Selecciona un cliente' encontrado como referencia")

            # Buscar el primer elemento clickeable (que debería ser el dropdown)
            elementos_clickeables = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            assert elementos_clickeables, "No se encontraron elementos clickeables"

            # El primer clickeable es el dropdown según el debug
            combobox_element = elementos_clickeables[0]
            print("✅ Encontrado elemento clickeable (dropdown)")

            # Hacer click en el combobox
            print("Haciendo click en el combobox...")
            combobox_element.click()
            time.sleep(2)  # Esperar que se abra el dropdown

            print("✅ TEST COMPLETADO: Click en combobox exitoso")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    # Seleccionar al primer cliente encontrado
    @pytest.mark.xray("APPTEST-9999")
    def test_seleccionar_primer_cliente(self, driver, video_recorder):
        """Test para seleccionar el primer cliente disponible"""
        print("\n=== TEST: Seleccionar primer cliente disponible ===")

        try:
            cliente_element = None

            # Estrategia 1: Buscar todos los clientes y tomar el primero
            print("Estrategia 1: Buscando todos los clientes con 'CLIENTES IS'...")
            try:
                elementos_clientes = driver.find_elements(AppiumBy.XPATH,
                                                          "//*[contains(@content-desc, 'CLIENTES IS')]")
                if elementos_clientes:
                    cliente_element = elementos_clientes[0]  # Tomar el primero
                    cliente_desc = cliente_element.get_attribute("content-desc")
                    print(f"✅ Encontrado primer cliente: '{cliente_desc}' - Estrategia 1")
                else:
                    print("❌ No se encontraron clientes con 'CLIENTES IS'")
            except NoSuchElementException:
                print("❌ Error en Estrategia 1")

            # Estrategia 2: Buscar por patrón "CM" y "IS"
            if not cliente_element:
                print("Estrategia 2: Buscando por patrón 'CM' y 'IS'...")
                try:
                    elementos_clientes = driver.find_elements(AppiumBy.XPATH,
                                                              "//*[contains(@content-desc, 'CM') and contains(@content-desc, 'IS')]")
                    if elementos_clientes:
                        cliente_element = elementos_clientes[0]  # Tomar el primero
                        cliente_desc = cliente_element.get_attribute("content-desc")
                        print(f"✅ Encontrado primer cliente: '{cliente_desc}' - Estrategia 2")
                    else:
                        print("❌ No se encontraron clientes con patrón 'CM' e 'IS'")
                except NoSuchElementException:
                    print("❌ Error en Estrategia 2")

            # Estrategia 3: Buscar elementos clickeables que no sean botones
            if not cliente_element:
                print("Estrategia 3: Buscando elementos clickeables que no sean botones...")
                try:
                    elementos_clickeables = driver.find_elements(AppiumBy.XPATH,
                                                                 "//android.view.View[@clickable='true']")
                    # Filtrar los que no sean 'Cancelar', 'Cerrar', etc.
                    for elemento in elementos_clickeables:
                        try:
                            desc = elemento.get_attribute("content-desc") or ""
                            if desc and "CM" in desc and "IS" in desc:
                                cliente_element = elemento
                                print(f"✅ Encontrado cliente clickeable: '{desc}' - Estrategia 3")
                                break
                        except:
                            continue

                    if not cliente_element:
                        print("❌ No se encontró cliente clickeable válido")
                except NoSuchElementException:
                    print("❌ Error en Estrategia 3")

            # Verificar que se encontró el cliente
            assert cliente_element is not None, "No se pudo encontrar ningún cliente para seleccionar"

            # Hacer click en el cliente
            cliente_desc = cliente_element.get_attribute("content-desc")
            print(f"Haciendo click en cliente: '{cliente_desc}'...")
            cliente_element.click()
            time.sleep(2)  # Esperar que se procese la selección

            print("✅ TEST COMPLETADO: Cliente seleccionado exitosamente")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")

    @pytest.mark.xray("APPTEST-9999")
    def test_clicl_seleccionar_button(self, driver, video_recorder):
        """Test para hacer click en el botón 'Seleccionar'"""
        print("\n=== TEST: Click en botón 'Seleccionar' ===")

        try:
            seleccionar_button = None

            # Estrategia 1: Por content-desc exacto
            print("Buscando botón 'Seleccionar' por content-desc exacto...")
            try:
                seleccionar_button = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Seleccionar']")
                print("✅ Encontrado por content-desc exacto")
            except NoSuchElementException:
                print("❌ No encontrado por content-desc exacto")

            # Estrategia 2: Por contains en content-desc
            if not seleccionar_button:
                print("Buscando botón 'Seleccionar' por contains en content-desc...")
                try:
                    seleccionar_button = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Seleccionar')]")
                    print("✅ Encontrado por contains en content-desc")
                except NoSuchElementException:
                    print("❌ No encontrado por contains en content-desc")

            # Verificar que se encontró el botón
            assert seleccionar_button is not None, "No se pudo encontrar el botón 'Seleccionar'"

            # Hacer click en el botón
            print("Haciendo click en botón 'Seleccionar'...")
            seleccionar_button.click()
            time.sleep(2)  # Esperar que cargue la pantalla

            print("✅ TEST COMPLETADO: Click en botón 'Seleccionar' exitoso")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado: {video_path}")