import time
import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import pytest

"""
Este archivo contiene funciones reutilizables para las acciones
dentro de la pantalla de 'Solicitud de descuento' o bonificación puntual.
"""


def obtener_total_pedido(driver):
    """
    Busca el texto 'Total:' y extrae el valor numérico asociado a él.
    Utiliza una búsqueda relativa para encontrar el monto.

    Devuelve:
        float: El valor numérico del total (ej: 20.99).
    """
    print("\n--- ACCIÓN: Obteniendo el total del pedido ---")
    try:
        # 1. Usamos XPath para encontrar el elemento del total basado en su relación
        # con la etiqueta "Total:". Buscamos el siguiente 'android.view.View' hermano.
        xpath_selector = "//*[contains(@content-desc, 'Total:')]/following-sibling::android.view.View"
        print(f"Buscando monto total con XPath: {xpath_selector}")
        elemento_total = driver.find_element(AppiumBy.XPATH, xpath_selector)

        # 2. Obtenemos el texto completo (ej: 'GTQ. 20.99')
        texto_total = elemento_total.get_attribute('content-desc')
        print(f"Texto del total encontrado: '{texto_total}'")

        # 3. Usamos una expresión regular para extraer solo los números y el punto.
        match = re.search(r'(\d+\.\d+)', texto_total)
        if match:
            valor_numerico = float(match.group(1))
            print(f"✅ Valor numérico extraído: {valor_numerico}")
            return valor_numerico
        else:
            pytest.fail(f"No se pudo extraer un valor numérico del texto: '{texto_total}'")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar la etiqueta 'Total:' o el monto asociado en la pantalla.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al obtener el total del pedido: {e}")

def ingresar_descuento_y_confirmar(driver, monto):
    """
    Busca el único campo de texto en la pantalla, ingresa el monto del descuento
    y presiona la tecla de acción para confirmar.
    """
    print(f"\n--- ACCIÓN: Ingresar descuento de '{monto}' ---")
    try:
        # 1. Buscamos el único EditText en la pantalla.
        print("Buscando el campo de texto para el descuento...")
        campo_descuento = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
        print("✅ Campo de descuento encontrado.")

        # 2. Interactuamos con el campo.
        campo_descuento.click()
        time.sleep(1)  # Pausa para que el teclado aparezca

        print(f"Limpiando y escribiendo el monto: '{monto}'")
        campo_descuento.clear()
        campo_descuento.send_keys(str(monto))

        # 3. Presionamos la tecla de acción (Enter/cheque) del teclado numérico.
        print("Confirmando con la tecla de acción (keycode 66)...")
        driver.press_keycode(66)

        time.sleep(2)
        print("✅ Descuento ingresado y confirmado.")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el campo de texto (EditText) para ingresar el descuento.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al ingresar el descuento: {e}")

def click_boton_marca(driver):
    """
    Busca y hace click en el botón de 'Marca' en la pantalla de descuento puntual.
    """
    print("\n--- ACCIÓN: Haciendo click en el botón 'Marca' ---")
    try:
        # 1. Buscamos el botón por su content desc.
        print("Buscando el botón 'Marca'...")
        boton_marca = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Marca']")
        print("✅ Botón 'Marca' encontrado.")

        # 2. Hacemos click en el botón.
        boton_marca.click()
        time.sleep(2)  # Pausa para que la acción se procese

        print("✅ Click en el botón 'Marca' realizado.")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el botón 'Marca' en la pantalla.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al hacer click en el botón 'Marca': {e}")

def click_monto_especifico_marca_producto(driver):
    """
    Busca y hace click en el monto de la marca en la pantalla de descuento puntual.
    """
    print("\n--- ACCIÓN: Aplicar descuento puntual ---")
    try:
        # Estrategia: Búsqueda relativa. Encontrar el EditText y luego buscar
        # el primer 'View' clickeable que sea su hermano y esté después.
        xpath_selector = "//android.widget.EditText/following-sibling::android.view.View[@clickable='true'][1]"
        print(f"Buscando botón de aplicar con XPath relativo: {xpath_selector}")

        boton_aplicar = driver.find_element(AppiumBy.XPATH, xpath_selector)
        print("✅ Botón de aplicar descuento encontrado.")

        boton_aplicar.click()
        print("✅ Clic realizado en el botón de aplicar descuento.")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el botón para aplicar el descuento relativo al EditText.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al aplicar el descuento puntual: {e}")

def click_boton_producto(driver):
    """
    Busca y hace click en el botón de 'Marca' en la pantalla de descuento puntual.
    """
    print("\n--- ACCIÓN: Haciendo click en el botón 'Producto' ---")
    try:
        # 1. Buscamos el botón por su content desc.
        print("Buscando el botón 'Producto'...")
        boton_producto = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Producto']")
        print("✅ Botón 'Producto' encontrado.")

        # 2. Hacemos click en el botón.
        boton_producto.click()
        time.sleep(2)  # Pausa para que la acción se procese

        print("✅ Click en el botón 'Producto' realizado.")

    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el botón 'Producto' en la pantalla.")
    except Exception as e:
        pytest.fail(f"Ocurrió un error al hacer click en el botón 'Producto': {e}")


