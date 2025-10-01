import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from tests.ventas.acciones.acciones_venta_directa import (
    ejecutar_venta_directa_completa
)


def spin_semana(driver):
    print("\n--- ACCIÓN: Spin semana (L hasta D) ---")

    try:
        wait = WebDriverWait(driver, 10)

        print("\nPASO 1: Haciendo clic inicial en Lunes (L)")

        xpath_lunes = "//*[starts-with(@content-desc, 'L\n')]"
        elemento_lunes = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_lunes))
        )

        print("✅ Lunes encontrado, haciendo clic inicial...")
        elemento_lunes.click()
        time.sleep(2)

        try:
            driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
            print("Día L: No hay clientes")
        except:
            print("Día L: Haciendo scroll...")
            scroll_hacia_abajo(driver)

        print("\nPASO 2: Continuando con días M hasta D")

        dias_restantes = ["M", "X", "J", "V", "S", "D"]

        for i, dia in enumerate(dias_restantes, 1):
            print(f"\nProcesando día: {dia}")

            xpath_dia_relativo = f"{xpath_lunes}/following-sibling::*[{i}]"

            try:
                elemento_dia = wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath_dia_relativo))
                )

                print(f"✅ Día {dia} encontrado (posición {i} desde L), haciendo clic...")
                elemento_dia.click()
                time.sleep(2)

                try:
                    driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
                    print(f"Día {dia}: No hay clientes")
                except:
                    print(f"Día {dia}: Haciendo scroll...")
                    scroll_hacia_abajo(driver)

            except Exception as e:
                print(f"❌ Error procesando día {dia}: {e}")
                continue

        print("\n✅ Spin semana completado - Todos los días procesados")

    except Exception as e:
        print(f"\n❌ Error general en spin_semana: {e}")
        pytest.fail(f"Error en spin_semana: {e}")


def scroll_hacia_abajo(driver):
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] // 2
    start_y = int(screen_size['height'] * 0.8)
    end_y = int(screen_size['height'] * 0.2)

    driver.swipe(start_x, start_y, start_x, end_y, duration=800)


def verificar_no_hay_clientes(driver):
    try:
        xpath_no_clientes = "//*[@content-desc='No hay clientes para mostrar']"
        driver.find_element(AppiumBy.XPATH, xpath_no_clientes)
        return True
    except NoSuchElementException:
        return False


def hacer_click_pendientes(driver, wait):
    try:
        print("Buscando botón 'Pendientes'...")
        xpath_pendientes = "//*[@content-desc='Pendientes']"

        boton_pendientes = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_pendientes))
        )

        print("✅ Botón 'Pendientes' encontrado, haciendo clic...")
        boton_pendientes.click()
        time.sleep(2)

        print("Clic en 'Pendientes' realizado exitosamente")

    except TimeoutException:
        print("❌ Error: No se encontró el botón 'Pendientes'")
        pytest.fail("No se pudo encontrar el botón 'Pendientes'")
    except Exception as e:
        print(f"❌ Error haciendo clic en 'Pendientes': {e}")
        pytest.fail(f"Error al hacer clic en 'Pendientes': {e}")
def hacer_click_ver_todos(wait):
    try:
        print("Buscando boton 'Ver todoos'")
        xpath_ver_todos = "//*[@content-desc='Ver todos']"
        boton_ver_todos = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_ver_todos))
        )
        print("Boton ver todos encontrado")
        boton_ver_todos.click()
        time.sleep(2)
        print("Clic en 'Ver todoos' realizado exitosamente")
    except TimeoutException:
        print("❌ Error: No se encontró el botón 'Ver todos'")
        pytest.fail("No se pudo encontrar el botón 'Ver todos'")
    except Exception as e:
        print(f"❌ Error haciendo clic en 'Ver todos': {e}")
        pytest.fail(f"Error al hacer clic en 'Ver todos': {e}")
def hacer_click_visitados(wait):
    try:
        print("Buscando boton 'Visitados'")
        xpath_visitados = "//*[@content-desc='Visitados']"
        boton_visitados = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_visitados))
        )
        print("Boton visitados encontrado")
        boton_visitados.click()
        time.sleep(2)
        print("Clic en 'Visitados' realizado exitosamente")
    except TimeoutException:
        print("❌ Error: No se encontró el botón 'Visitados'")
        pytest.fail("No se pudo encontrar el botón 'Visitados'")
    except Exception as e:
        print(f"❌ Error haciendo clic en 'Visitados': {e}")
        pytest.fail(f"Error al hacer clic en 'Visitados': {e}")

def seleccionar_dia(driver, dia):
    print(f" Seleccionando día '{dia}'...")
    day_element = driver.find_element("xpath", f"//*[@content-desc='{dia}']")
    day_element.click()
    print(f"✅ Día '{dia}' seleccionado")
    time.sleep(1)
    print(" Confirmando selección...")
    aceptar_button = driver.find_element("xpath", "//*[@content-desc='Aceptar']")
    aceptar_button.click()
    print("✅ Fecha confirmada")

def registrar_motivo(driver, wait, motivo_texto, fecha_inicio, comentario):
    # 1. Clic en botón "Motivo"
    print("Buscando y haciendo clic en botón Motivo...")
    boton_motivo = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='Motivo\nMotivo']"))
    )
    boton_motivo.click()
    time.sleep(1)

    # 2. Seleccionar el motivo deseado (ej: "Enfermedad")
    print(f"Seleccionando motivo: {motivo_texto}")
    opcion_motivo = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                    f'new UiSelector().descriptionContains("{motivo_texto}")'))
    )
    opcion_motivo.click()
    time.sleep(1)

    # 3. Clic en fecha inicio
    print("Haciendo clic en campo de Fecha inicio...")
    campo_fecha = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@hint='Fecha inicio']"))
    )
    campo_fecha.click()
    time.sleep(1)

    # Seleccionar fecha según parámetro (depende de cómo se renderiza tu datepicker)
    print(f"Seleccionando fecha: {fecha_inicio}")
    seleccionar_dia(driver, fecha_inicio)
    time.sleep(1)

    # 4. Escribir comentario
    print(f"Escribiendo comentario: {comentario}")
    campo_comentario = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[@hint='Comentario']"))
    )
    campo_comentario.send_keys(comentario)
    time.sleep(1)

    print("✅ Registro de motivo completado")

def buscar_primer_dia_con_clientes(driver):
    print("\n--- ACCIÓN: Buscar primer día con clientes (solo búsqueda) ---")

    try:
        wait = WebDriverWait(driver, 10)
        xpath_lunes = "//*[starts-with(@content-desc, 'L\n')]"

        todos_los_dias = ["L", "M", "X", "J", "V", "S", "D"]

        for i, dia in enumerate(todos_los_dias):
            print(f"\nVerificando día: {dia}")

            if i == 0:
                xpath_dia = xpath_lunes
            else:
                xpath_dia = f"{xpath_lunes}/following-sibling::*[{i}]"

            try:
                elemento_dia = wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath_dia))
                )

                elemento_dia.click()
                time.sleep(2)

                try:
                    driver.find_element(AppiumBy.XPATH, "//*[@content-desc='No hay clientes para mostrar']")
                    print(f"Día {dia}: No hay clientes")
                except NoSuchElementException:
                    print(f"¡Día {dia} tiene clientes!")
                    return dia

            except Exception as e:
                print(f"❌ Error con día {dia}: {e}")
                continue

        print("No se encontraron clientes en toda la semana")
        return None

    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return None


def hacer_click_primer_cliente(driver):
    print("\n--- ACCIÓN: Hacer clic en el primer cliente ---")

    try:
        wait = WebDriverWait(driver, 15)

        print("Buscando todas las cards de cliente disponibles...")
        xpath_cliente = "//android.view.View[@clickable='true' and contains(@content-desc, 'Clientes IS')]"

        lista_clientes = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, xpath_cliente))
        )

        print(f"✅ Se encontraron {len(lista_clientes)} cards de cliente.")

        if not lista_clientes:
            raise Exception("No se encontró ninguna card de cliente en la pantalla.")

        primer_cliente = lista_clientes[0]

        desc = primer_cliente.get_attribute('content-desc') or '(sin descripción)'
        print(f"Seleccionando la primera card:")
        print(f"Descripción: {desc.replace(chr(10), ' | ')}")

        primer_cliente.click()
        time.sleep(2)

        print("Clic en el primer cliente realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No apareció ninguna card de cliente en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en el primer cliente: {e}")


def realizar_check_in_si_pendiente(driver):
    print("\n--- LÓGICA: Verificando y realizando 'Check-in' si está pendiente ---")
    try:
        wait = WebDriverWait(driver, 10)

        check_in_pendiente_xpath = "//android.view.View[contains(@content-desc, 'Check-in') and contains(@content-desc, 'Pendiente')]"

        print(f"Buscando tarea de Check-in PENDIENTE con XPath: {check_in_pendiente_xpath}")

        check_in_card = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, check_in_pendiente_xpath))
        )

        print("✅ Tarea 'Check-in' pendiente encontrada. Procediendo a completarla...")
        check_in_card.click()
        time.sleep(2)

        hacer_click_en_capturar_ubicacion(driver)
        hacer_click_en_Ok(driver)

        print("Flujo de Check-in completado exitosamente.")
        return True

    except TimeoutException:
        print("No se encontró una tarea de 'Check-in' en estado 'Pendiente'.")
        try:
            driver.find_element(AppiumBy.XPATH,
                                "//android.view.View[contains(@content-desc, 'Check-in') and contains(@content-desc, 'Finalizado')]")
            print("✅ Se confirma que la tarea 'Check-in' ya estaba marcada como 'Finalizado'.")
        except:
            print("No se encontró ninguna tarea de 'Check-in' (ni pendiente ni finalizada).")

        return False

    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado durante el proceso de check-in: {e}")
        return False


def realizar_venta_directa_si_pendiente(driver):
    print("\n--- LÓGICA: Verificando y realizando 'Venta tiendas de barrio' si está pendiente ---")
    try:
        wait = WebDriverWait(driver, 10)

        check_in_pendiente_xpath = "//android.view.View[contains(@content-desc, 'Venta') and contains(@content-desc, 'Pendiente')]"

        print(f"Buscando tarea de Venta tiendas de barrio PENDIENTE con XPath: {check_in_pendiente_xpath}")

        check_in_card = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, check_in_pendiente_xpath))
        )

        print("✅ Tarea 'Ventas tienda de barrio' pendiente encontrada. Procediendo a completarla...")
        check_in_card.click()
        time.sleep(2)

        ejecutar_venta_directa_completa(driver, "Cloro", 5)

        print("Flujo de Venta tiendas de barrio completado exitosamente.")
        return True

    except TimeoutException:
        print("No se encontró una tarea de 'Venta' en estado 'Pendiente'.")
        try:
            driver.find_element(AppiumBy.XPATH,
                                "//android.view.View[contains(@content-desc, 'Venta') and contains(@content-desc, 'Finalizado')]")
            print("✅ Se confirma que la tarea 'Venta' ya estaba marcada como 'Finalizado'.")
        except:
            print("No se encontró ninguna tarea de 'Venta' (ni pendiente ni finalizada).")

        return False

    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado durante el proceso de check-in: {e}")
        return False


def realizar_check_out_si_pendiente(driver):
    print("\n--- LÓGICA: Verificando y realizando 'Check-out' si está pendiente ---")
    try:
        wait = WebDriverWait(driver, 10)

        check_out_pendiente_xpath = "//android.view.View[contains(@content-desc, 'Check-out') and contains(@content-desc, 'Pendiente')]"

        print(f"Buscando tarea de Check-out PENDIENTE con XPath: {check_out_pendiente_xpath}")

        check_out_card = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, check_out_pendiente_xpath))
        )

        print("✅ Tarea 'Check-out' pendiente encontrada. Procediendo a completarla...")
        check_out_card.click()
        time.sleep(2)

        hacer_click_en_capturar_ubicacion(driver)
        hacer_click_en_Ok(driver)

        print("Flujo de Check-out completado exitosamente.")
        return True

    except TimeoutException:
        print("No se encontró una tarea de 'Check-out' en estado 'Pendiente'.")
        try:
            driver.find_element(AppiumBy.XPATH,
                                "//android.view.View[contains(@content-desc, 'Check-out') and contains(@content-desc, 'Finalizado')]")
            print("✅ Se confirma que la tarea 'Check-out' ya estaba marcada como 'Finalizado'.")
        except:
            print("No se encontró ninguna tarea de 'Check-out' (ni pendiente ni finalizada).")

        return False

    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado durante el proceso de check-out: {e}")
        return False


def hacer_click_en_capturar_ubicacion(driver):
    print("\n--- ACCIÓN: Hacer clic en 'Capturar ubicación' ---")
    try:
        wait = WebDriverWait(driver, 15)

        capturar_ubicacion_id = "Capturar ubicación"

        print(f"Buscando el botón por Accessibility ID: '{capturar_ubicacion_id}'")

        boton_capturar = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, capturar_ubicacion_id))
        )

        print("✅ Botón 'Capturar ubicación' encontrado y es clickeable.")

        boton_capturar.click()
        time.sleep(3)

        print("Clic en 'Capturar ubicación' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró el botón 'Capturar ubicación' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Capturar ubicación': {e}")


def hacer_click_en_Ok(driver):
    print("\n--- ACCIÓN: Hacer clic en 'Ok' ---")
    try:
        wait = WebDriverWait(driver, 10)

        ok_xpath = "//*[@content-desc='Ok']"

        print(f"Buscando el botón 'Ok' con XPath: {ok_xpath}")

        boton_ok = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ok_xpath))
        )

        print("✅ Botón 'Ok' encontrado y es clickeable.")

        boton_ok.click()
        time.sleep(2)

        print("Clic en 'Ok' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró el botón 'Ok' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Ok': {e}")


def hacer_click_en_atras(driver):
    print("\n--- ACCIÓN: Hacer clic en 'Atrás' ---")
    try:
        wait = WebDriverWait(driver, 10)

        atras_xpath = "//*[@content-desc='Atrás']"

        print(f"Buscando el botón 'Atrás' con XPath: {atras_xpath}")

        boton_atras = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, atras_xpath))
        )

        print("✅ Botón 'Atrás' encontrado y es clickeable.")

        boton_atras.click()
        time.sleep(2)

        print("Clic en 'Atrás' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró el botón 'Atrás' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Atrás': {e}")
