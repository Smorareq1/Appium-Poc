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
def hacer_click_pendientes(driver, wait):
    """
    Función auxiliar para hacer clic en el botón 'Pendientes'
    """
    try:
        print("🔍 Buscando botón 'Pendientes'...")
        xpath_pendientes = "//*[@content-desc='Pendientes']"

        boton_pendientes = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_pendientes))
        )

        print("✅ Botón 'Pendientes' encontrado, haciendo clic...")
        boton_pendientes.click()
        time.sleep(2)

        print("🎉 ¡Clic en 'Pendientes' realizado exitosamente!")

    except TimeoutException:
        print("❌ Error: No se encontró el botón 'Pendientes'")
        pytest.fail("No se pudo encontrar el botón 'Pendientes'")
    except Exception as e:
        print(f"❌ Error haciendo clic en 'Pendientes': {e}")
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

# Completar cliente
def hacer_click_primer_cliente(driver):
    """
    Hace clic en la primera card de cliente que aparece en la lista.
    Localiza todas las cards de cliente y selecciona la primera del listado.
    """
    print("\n--- ACCIÓN: Hacer clic en el primer cliente (Método Corregido) ---")

    try:
        wait = WebDriverWait(driver, 15) # Aumentamos un poco el tiempo de espera por si acaso

        # Estrategia:
        # 1. Buscamos TODOS los elementos que cumplan el patrón de una "card de cliente".
        # 2. Appium devuelve la lista en el orden en que aparecen en pantalla.
        # 3. Simplemente seleccionamos el primer elemento de esa lista (índice 0).

        print("🔍 Buscando todas las cards de cliente disponibles...")
        xpath_cliente = "//android.view.View[@clickable='true' and contains(@content-desc, 'Clientes IS')]"

        # Esperamos a que al menos UNA card de cliente esté presente y obtenemos la lista
        lista_clientes = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, xpath_cliente))
        )

        print(f"✅ Se encontraron {len(lista_clientes)} cards de cliente.")

        # Verificamos que la lista no esté vacía
        if not lista_clientes:
            raise Exception("No se encontró ninguna card de cliente en la pantalla.")

        # El primer cliente es el primer elemento de la lista
        primer_cliente = lista_clientes[0]

        # Obtenemos información para el log antes de hacer clic
        desc = primer_cliente.get_attribute('content-desc') or '(sin descripción)'
        print(f" Seleccionando la primera card:")
        print(f" Descripción: {desc.replace(chr(10), ' | ')}") # Reemplaza saltos de línea para un log más limpio

        # Hacemos clic
        primer_cliente.click()
        time.sleep(2)  # Pausa para la transición de pantalla

        print("👍 Clic en el primer cliente realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No apareció ninguna card de cliente en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en el primer cliente: {e}")
def hacer_click_en_check_in(driver):
    """
    Busca y hace clic en la tarjeta de tarea pendiente que contiene 'Check-in'.
    Esta función asume que ya se está en la pantalla de detalles de un cliente.
    """
    print("\n--- ACCIÓN: Hacer clic en la tarea 'Check-in' ---")
    try:
        wait = WebDriverWait(driver, 15)

        # Este selector es robusto: busca un elemento clickeable (`android.view.View`)
        check_in_xpath = "//android.view.View[contains(@content-desc, 'Check-in')]"

        print(f"🔍 Buscando la tarea de Check-in con XPath: {check_in_xpath}")

        check_in_card = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, check_in_xpath))
        )

        print("✅ Tarea 'Check-in' encontrada y es clickeable.")

        check_in_card.click()
        time.sleep(2)  # Pausa para esperar la animación/carga de la nueva pantalla

        print("👍 Clic en 'Check-in' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró la tarea 'Check-in' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Check-in': {e}")
def hacer_click_en_capturar_ubicacion(driver):
    """
    En la pantalla que aparece después del Check-in, busca y hace clic
    en el botón 'Capturar ubicación'.
    """
    print("\n--- ACCIÓN: Hacer clic en 'Capturar ubicación' ---")
    try:
        wait = WebDriverWait(driver, 15)

        # La estrategia más fiable para botones en Flutter es usar el 'content-desc',
        # que Appium trata como el Accessibility ID.
        capturar_ubicacion_id = "Capturar ubicación"

        print(f"🔍 Buscando el botón por Accessibility ID: '{capturar_ubicacion_id}'")

        boton_capturar = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, capturar_ubicacion_id))
        )

        print("✅ Botón 'Capturar ubicación' encontrado y es clickeable.")

        boton_capturar.click()
        # Pausa un poco más larga para dar tiempo a que el GPS o la cámara se inicien.
        time.sleep(3)

        print("👍 Clic en 'Capturar ubicación' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró el botón 'Capturar ubicación' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Capturar ubicación': {e}")
def hacer_click_en_Ok(driver):
    """
    Hace clic en el botón 'Ok' que aparece en un diálogo emergente.
    """
    print("\n--- ACCIÓN: Hacer clic en 'Ok' ---")
    try:
        wait = WebDriverWait(driver, 10)

        ok_xpath = "//*[@content-desc='Ok']"

        print(f"🔍 Buscando el botón 'Ok' con XPath: {ok_xpath}")

        boton_ok = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ok_xpath))
        )

        print("✅ Botón 'Ok' encontrado y es clickeable.")

        boton_ok.click()
        time.sleep(2)  # Pausa para esperar la acción

        print("👍 Clic en 'Ok' realizado exitosamente.")

    except TimeoutException:
        pytest.fail("TEST FALLÓ: Timeout. No se encontró el botón 'Ok' en el tiempo esperado.")
    except Exception as e:
        pytest.fail(f"TEST FALLÓ: Ocurrió un error inesperado al hacer clic en 'Ok': {e}")
