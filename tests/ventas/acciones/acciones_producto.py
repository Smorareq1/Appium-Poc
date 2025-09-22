import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import pytest

"""
Este archivo contiene funciones reutilizables para las acciones
dentro de la pantalla de detalle de un producto.
"""

"""
Consultar por que con 200 no se aplica el descuento // 120800280
"""


def ingresar_cantidad_producto(driver, cantidad):
    """
    Busca el campo de texto (EditText) en la pantalla de detalle del producto,
    lo limpia e ingresa la cantidad especificada.
    """
    print(f"\n--- ACCIÓN: Ingresar cantidad: {cantidad} ---")
    try:
        print("Buscando el campo de texto para la cantidad...")
        # Basado en el log, solo hay un EditText en esta pantalla.
        campo_cantidad = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
        print("✅ Campo de cantidad encontrado.")

        campo_cantidad.click()

        print("Limpiando y escribiendo la nueva cantidad...")
        campo_cantidad.clear()
        campo_cantidad.send_keys(str(cantidad))
        print("Presionando la tecla de acción (Enter/Cheque) del teclado...")
        driver.press_keycode(66)  # 66 es el código para KEYCODE_ENTER en Android

        # Ocultar teclado por si acaso
        try:
            driver.hide_keyboard()
        except:
            pass  # No hacer nada si no hay teclado visible

        time.sleep(2)
    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el campo de texto (EditText) para ingresar la cantidad.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al ingresar la cantidad: {e}")


def hacer_scroll_hacia_abajo(driver):
    """Realiza un gesto de scroll (swipe) hacia abajo en la pantalla."""
    print("\n--- ACCIÓN: Realizando scroll hacia abajo ---")
    try:
        size = driver.get_window_size()
        start_x = size['width'] / 2
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2

        print(f"Haciendo swipe desde ({start_x}, {start_y}) hasta ({start_x}, {end_y})")
        driver.swipe(start_x, start_y, start_x, end_y, 400)
        time.sleep(2)
    except Exception as e:
        pytest.fail(f"Ocurrió un error al intentar hacer scroll: {e}")


def obtener_unidades_a_bonificar(driver):
    """
    Localiza el texto 'Unidades a bonificar' y extrae el número de la línea siguiente.
    Devuelve el número de unidades como un entero.
    """
    print("\n--- ACCIÓN: Obteniendo unidades a bonificar ---")
    try:
        # 1. Localizar el elemento padre que contiene el texto
        xpath_selector = "//*[contains(@content-desc, 'Unidades a bonificar')]"
        elemento_contenedor = driver.find_element(AppiumBy.XPATH, xpath_selector)

        # 2. Obtener la descripción completa
        descripcion_completa = elemento_contenedor.get_attribute('content-desc')

        # 3. Procesar el texto para encontrar el número
        lineas = descripcion_completa.split('\n')

        # Encontrar el índice de la línea que nos interesa
        indice = lineas.index('Unidades a bonificar')

        # El número está en la línea siguiente
        numero_bonificacion_str = lineas[indice + 1].strip()

        # 4. Convertir a entero y devolver
        numero_bonificacion_int = int(numero_bonificacion_str)
        print(f"✅ Unidades a bonificar encontradas: {numero_bonificacion_int}")
        return numero_bonificacion_int

    except NoSuchElementException:
        pytest.fail("No se encontró el elemento que contiene 'Unidades a bonificar'.")
    except (ValueError, IndexError):
        pytest.fail(
            "Se encontró el texto 'Unidades a bonificar', pero no se pudo extraer el número de la línea siguiente.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al obtener las unidades a bonificar: {e}")


def agregar_producto_al_carrito(driver):
    """
    Hace clic en el botón central de la barra de navegación inferior usando
    coordenadas porcentuales para adaptarse a diferentes tamaños de pantalla.
    """
    print("\n--- ACCIÓN: Hacer clic en el botón para finalizar/revisar pedido (por porcentaje) ---")
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

