import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_puntual(self, driver, video_recorder):
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

            #Mis metricas
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

            #Mi progreso
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
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
