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
            # 1) Código recibido (reemplaza por tu inyección/mock)
            otp_code = "476338"

            # 2) Localizar las 6 casillas (EditText de 1 carácter)
            otp_inputs = driver.find_elements(AppiumBy.XPATH, "//android.widget.EditText")
            if not otp_inputs or len(otp_inputs) < 4:
                pytest.skip("Pantalla de OTP no presente (no se hallaron casillas)")

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
                "//*[contains(@text,'Pin invalido') or contains(@content-desc,'Pin invalido')]"  # sin tilde
            ])
            assert pin_invalido is None, "Se mostró 'Pin inválido' al validar el OTP"

            print("✅ OTP validado correctamente")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
