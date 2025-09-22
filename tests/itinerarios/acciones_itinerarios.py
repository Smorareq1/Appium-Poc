import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

#Spin semana (L a D)
def spin_semana(driver):
    """
    Hace clic en todos los días de la semana (L hasta D) empezando siempre por L
    """
    print("\n--- ACCIÓN: Spin semana (L hasta D) ---")

    try:
        wait = WebDriverWait(driver, 10)

        # PASO 1: Siempre empezar haciendo clic en L (Lunes)
        print("\n🔍 PASO 1: Haciendo clic inicial en Lunes (L)")

        # Buscar L sin número específico (dinámico)
        xpath_lunes = "//*[starts-with(@content-desc, 'L\n')]"
        elemento_lunes = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_lunes))
        )

        print("✅ Lunes encontrado, haciendo clic inicial...")
        elemento_lunes.click()
        time.sleep(2)

        # Verificar mensaje para L
        try:
            driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
            print("⏭️ Día L: No hay clientes")
        except:
            print("📜 Día L: Haciendo scroll...")
            scroll_hacia_abajo(driver)

        # PASO 2: Continuar con el resto de días usando posición relativa
        print("\n🔍 PASO 2: Continuando con días M hasta D")

        dias_restantes = ["M", "X", "J", "V", "S", "D"]

        for i, dia in enumerate(dias_restantes, 1):  # i = 1,2,3,4,5,6
            print(f"\n🔍 Procesando día: {dia}")

            # Usar posición relativa desde L para todos los días restantes
            xpath_dia_relativo = f"{xpath_lunes}/following-sibling::*[{i}]"

            try:
                elemento_dia = wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath_dia_relativo))
                )

                print(f"✅ Día {dia} encontrado (posición {i} desde L), haciendo clic...")
                elemento_dia.click()
                time.sleep(2)

                # Verificar mensaje
                try:
                    driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
                    print(f"⏭️ Día {dia}: No hay clientes")
                except:
                    print(f"📜 Día {dia}: Haciendo scroll...")
                    scroll_hacia_abajo(driver)

            except Exception as e:
                print(f"❌ Error procesando día {dia}: {e}")
                continue

        print("\n✅ Spin semana completado - Todos los días procesados")

    except Exception as e:
        print(f"\n❌ Error general en spin_semana: {e}")
        pytest.fail(f"Error en spin_semana: {e}")
def scroll_hacia_abajo(driver):
    """
    Función auxiliar para hacer scroll hacia abajo
    """
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] // 2
    start_y = int(screen_size['height'] * 0.8)
    end_y = int(screen_size['height'] * 0.2)

    driver.swipe(start_x, start_y, start_x, end_y, duration=800)
def verificar_no_hay_clientes(driver):
    """
    Función auxiliar para verificar si existe el mensaje "No hay clientes para mostrar"
    Returns True si encuentra el mensaje, False si no lo encuentra
    """
    try:
        xpath_no_clientes = "//*[@content-desc='No hay clientes para mostrar']"
        driver.find_element(AppiumBy.XPATH, xpath_no_clientes)
        return True
    except NoSuchElementException:
        return False
# Itinerario - Cliente
def hacer_clic_pendientes(driver, wait):
    """
    Función auxiliar para hacer clic en el botón 'Pendientes'
    """
    try:
        print("Buscando botón 'Pendientes'...")
        xpath_pendientes = "//*[@content-desc='Pendientes']"

        boton_pendientes = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_pendientes))
        )

        print("Botón 'Pendientes' encontrado, haciendo clic...")
        boton_pendientes.click()
        time.sleep(2)

        print("¡Clic en 'Pendientes' realizado exitosamente!")

    except TimeoutException:
        print("Error: No se encontró el botón 'Pendientes'")
        pytest.fail("No se pudo encontrar el botón 'Pendientes'")
    except Exception as e:
        print(f"Error haciendo clic en 'Pendientes': {e}")
        pytest.fail(f"Error al hacer clic en 'Pendientes': {e}")
def buscar_primer_dia_con_clientes(driver):
    """
    Busca el primer día con clientes
    """
    print("\n--- ACCIÓN: Buscar primer día con clientes (solo búsqueda) ---")

    try:
        wait = WebDriverWait(driver, 10)
        xpath_lunes = "//*[starts-with(@content-desc, 'L\n')]"

        # Lista completa de días
        todos_los_dias = ["L", "M", "X", "J", "V", "S", "D"]

        for i, dia in enumerate(todos_los_dias):
            print(f"\n Verificando día: {dia}")

            if i == 0:  # Lunes (L)
                xpath_dia = xpath_lunes
            else:  # Resto de días por posición relativa
                xpath_dia = f"{xpath_lunes}/following-sibling::*[{i}]"

            try:
                elemento_dia = wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath_dia))
                )

                elemento_dia.click()
                time.sleep(2)

                # Verificar clientes
                try:
                    driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
                    print(f"Día {dia}: No hay clientes")
                except NoSuchElementException:
                    print(f"¡Día {dia} tiene clientes!")
                    return dia  # Retornar el día que tiene clientes

            except Exception as e:
                print(f"❌ Error con día {dia}: {e}")
                continue

        print(" No se encontraron clientes en toda la semana")
        return None

    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return None