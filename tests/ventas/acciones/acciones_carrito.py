import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
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

