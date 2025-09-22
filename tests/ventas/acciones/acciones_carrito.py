import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


def abrir_carrito(driver):
    """
    Hace clic en el botón central de la barra de navegación inferior usando
    coordenadas porcentuales para adaptarse a diferentes tamaños de pantalla.
    """
    print("\n--- ACCIÓN: Abrir el carrito ---")
    try:
        # Obtener el tamaño de la pantalla
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        # Calcular las coordenadas basadas en porcentajes (50% H, 95% V)
        x_coordinate = int(width * 0.50)
        y_coordinate = int(height * 0.95)

        print(f"Dimensiones de la pantalla: {width}x{height}.")
        print(f"Haciendo tap en coordenadas calculadas: ({x_coordinate}, {y_coordinate})")

        # Realizar el tap en las coordenadas calculadas
        # El método tap espera una lista de tuplas de coordenadas
        driver.tap([(x_coordinate, y_coordinate)])

        time.sleep(4)  # Pausa mayor para esperar la transición a la nueva pantalla
        print("✅ Tap realizado exitosamente.")

    except Exception as e:
        pytest.fail(f"Ocurrió un error al intentar hacer tap por coordenadas porcentuales: {e}")

def hacer_swipe_en_resumen_compra(driver):
    """
    Localiza el bloque del resumen de compra y realiza un swipe
    de derecha a izquierda sobre él para revelar opciones.
    """
    print("\n--- ACCIÓN: Swipe en resumen de compra ---")
    try:
        # 1. Localizar el elemento contenedor del resumen
        xpath_selector = "//*[contains(@content-desc, 'Subtotal:')]"
        print(f"Buscando elemento de resumen con XPath: {xpath_selector}")
        elemento_resumen = driver.find_element(AppiumBy.XPATH, xpath_selector)
        print("✅ Elemento de resumen encontrado.")

        # 2. Calcular coordenadas para el swipe relativo al elemento
        location = elemento_resumen.location
        size = elemento_resumen.size

        # El swipe será horizontal, en el centro vertical del elemento
        start_x = location['x'] + size['width'] * 0.9  # Empezar al 90% del ancho (derecha)
        end_x = location['x'] + size['width'] * 0.1  # Terminar al 10% del ancho (izquierda)
        y = location['y'] + size['height'] / 2  # A la mitad de la altura

        print(f"Realizando swipe desde ({start_x}, {y}) hasta ({end_x}, {y})")
        driver.swipe(start_x, y, end_x, y, 500)  # Duración de 500ms
        time.sleep(2)  # Esperar a que la animación termine

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el bloque de resumen de compra que contiene 'Subtotal:'.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al realizar el swipe en el resumen de compra: {e}")

def hacer_clic_en_descuento_puntual(driver):
    """
    Busca y hace clic en el botón revelado después del swipe, usando
    una estrategia de búsqueda relativa al resumen de compra.
    """
    print("\n--- ACCIÓN: Clic en botón revelado post-swipe (Búsqueda Relativa) ---")
    try:
        # 1. Definimos el 'ancla', que es el elemento de resumen que sí podemos encontrar.
        ancla_xpath = "//*[contains(@content-desc, 'Subtotal:')]"

        # 2. Construimos un XPath relativo que sube al padre del ancla y busca el botón.
        # Esto asume que el botón y el texto del resumen comparten un contenedor padre cercano.
        boton_revelado_xpath = f"({ancla_xpath})/parent::*//android.widget.Button[@clickable='true']"

        print(f"Buscando botón revelado con XPath relativo: {boton_revelado_xpath}")

        # Usamos find_elements para evitar un error si hay varios, y filtramos por el que esté visible.
        botones_posibles = driver.find_elements(AppiumBy.XPATH, boton_revelado_xpath)

        boton_a_clickear = None
        for boton in botones_posibles:
            if boton.is_displayed():
                # Verificamos que no sea un botón que ya estaba antes (ej. el de 'atrás')
                # Asumimos que el botón revelado es el que está más a la derecha del ancla.
                # Esta lógica se puede ajustar si es necesario.
                boton_a_clickear = boton
                break  # Nos quedamos con el primero que cumpla la condición

        if boton_a_clickear:
            print("✅ Botón revelado encontrado. Haciendo clic...")
            boton_a_clickear.click()
            time.sleep(2)
        else:
            pytest.fail("No se encontró ningún botón visible y clickeable relativo al resumen de compra.")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el ancla 'Subtotal:' para iniciar la búsqueda relativa.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al hacer clic en el botón revelado: {e}")

def seleccionar_primera_direccion_entrega(driver):
    """
    Encuentra y hace clic en el botón de dirección de entrega, luego selecciona la primera opción.
    """
    print("\n--- ACCIÓN: Seleccionar primera dirección de entrega ---")

    try:
        wait = WebDriverWait(driver, 15)

        # PASO 1: Encontrar el contenedor "Información de entrega"
        print("🔍 Localizando contenedor 'Información de entrega'...")
        contenedor_info_entrega = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Información de entrega')]"))
        )
        print("✅ Contenedor encontrado")

        # PASO 2: Buscar el botón clickeable de dirección
        print("🔍 Buscando botón de dirección...")
        xpath_boton = "//*[contains(@hint, 'Dirección de entrega')]//android.widget.Button[@clickable='true']"

        boton_direccion = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_boton))
        )
        print("✅ Botón de dirección encontrado")

        # PASO 3: Hacer clic en el botón
        print("🎯 Haciendo clic en el botón de dirección...")
        boton_direccion.click()
        time.sleep(3)
        print("✅ Clic realizado")

        # PASO 4: Buscar y seleccionar primera opción del dropdown
        print("🔍 Buscando opciones del dropdown...")
        xpath_opciones = "//android.widget.ScrollView//android.view.View[@clickable='true' and (contains(@text, 'Palencia') or contains(@content-desc, 'Palencia') or contains(@text, 'Testing'))]"

        opciones = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, xpath_opciones))
        )
        print(f"✅ Encontradas {len(opciones)} opciones")

        # Seleccionar primera opción
        print("🎯 Seleccionando primera opción...")
        primera_opcion = opciones[0]
        primera_opcion.click()
        time.sleep(2)

        print("✅ Primera dirección de entrega seleccionada exitosamente")

    except TimeoutException:
        pytest.fail("Timeout: No se encontró el botón de dirección o las opciones del dropdown")
    except Exception as e:
        pytest.fail(f"Error al seleccionar dirección de entrega: {e}")

def escribir_comentario_pedido(driver, comentario="Entrega urgente - Favor contactar antes de llegar"):
    """
    Encuentra el campo de comentarios y escribe un comentario de ejemplo.
    """
    print("\n--- ACCIÓN: Escribir comentario en el pedido ---")

    try:
        wait = WebDriverWait(driver, 10)

        # Buscar el campo de comentarios por hint
        print("🔍 Buscando campo de comentarios...")
        xpath_comentarios = "//*[contains(@hint, 'Comentarios')]"

        campo_comentarios = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_comentarios))
        )
        print("✅ Campo de comentarios encontrado")

        # Hacer clic en el campo
        print("🎯 Haciendo clic en el campo...")
        campo_comentarios.click()
        time.sleep(1)

        # Limpiar campo y escribir comentario
        print(f"✏️ Escribiendo comentario: '{comentario}'")
        campo_comentarios.clear()
        campo_comentarios.send_keys(comentario)
        time.sleep(1)

        print("✅ Comentario escrito exitosamente")

        # Opcional: Ocultar teclado
        try:
            driver.hide_keyboard()
        except:
            pass  # Ignorar si no hay teclado visible

    except TimeoutException:
        pytest.fail("Timeout: No se encontró el campo de comentarios")
    except Exception as e:
        pytest.fail(f"Error al escribir comentario: {e}")

def aceptar_pedido(driver):
    """
    Encuentra y hace clic en el botón para aceptar y finalizar el pedido.
    """
    print("\n--- ACCIÓN: Aceptar y finalizar pedido ---")

    try:
        wait = WebDriverWait(driver, 10)

        # Buscar el botón de aceptar pedido por description
        print("🔍 Buscando botón 'Aceptar pedido'...")
        xpath_boton_aceptar = "//*[@content-desc='Aceptar']"

        boton_aceptar = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_boton_aceptar))
        )
        print("✅ Botón 'Aceptar pedido' encontrado")

        # Hacer clic en el botón
        print("🎯 Haciendo clic en 'Aceptar pedido'...")
        boton_aceptar.click()
        time.sleep(5)

        print("✅ Pedido aceptado y finalizado exitosamente")

    except TimeoutException:
        pytest.fail("Timeout: No se encontró el botón 'Aceptar pedido'")
    except Exception as e:
        pytest.fail(f"Error al aceptar el pedido: {e}")

def click_ok(driver):
    """
    Encuentra y hace clic en el botón OK de cualquier diálogo emergente.
    """
    print("\n--- ACCIÓN: Clic en botón OK ---")

    try:
        wait = WebDriverWait(driver, 10)

        # Buscar el botón OK por content-desc
        print("🔍 Buscando botón 'OK'...")
        xpath_boton_ok = "//*[@content-desc='Ok']"

        boton_ok = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath_boton_ok))
        )
        print("✅ Botón 'OK' encontrado")

        # Hacer clic en el botón
        print("🎯 Haciendo clic en 'OK'...")
        boton_ok.click()
        time.sleep(2)

        print("✅ Clic en 'OK' realizado exitosamente")

    except TimeoutException:
        pytest.fail("Timeout: No se encontró el botón 'OK'")
    except Exception as e:
        pytest.fail(f"Error al hacer clic en 'OK': {e}")