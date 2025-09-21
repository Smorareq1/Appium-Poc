import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class MenuTest:
    # UI Tests + Gestos
    # Test 10 Menu → Scroll → Salir
    @pytest.mark.xray("APPTEST-17")
    def test_08_flujo_menu_y_salir(self, driver, video_recorder):

        print("\n=== TEST 8: Flujo menú y salir (Menu → Scroll → Salir) ===")

        try:
            # Paso 1: Click en "menu"
            print("Paso 1: Buscando botón 'menu'...")

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
            time.sleep(1.5)  # Reducido de 2 a 1.5

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