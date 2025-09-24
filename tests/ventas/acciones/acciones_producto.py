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


def incrementar_productos_con_botones(driver, clics_base, incremento_clics):
    """
    Busca todos los botones de incremento ('+') en la pantalla y hace clic en ellos
    de forma incremental.

    Esta función está diseñada para interfaces donde cada producto tiene un botón '+'
    en lugar de un campo de texto para ingresar la cantidad.

    :param driver: La instancia del driver de Appium.
    :param clics_base: El número de veces que se hará clic en el botón del PRIMER producto.
    :param incremento_clics: El número de clics adicionales para cada producto subsecuente.
                             Ej: Si es 2, el segundo producto recibirá clics_base + 2 clics,
                             el tercero clics_base + 4, y así sucesivamente.
    """
    print(f"\n--- ACCIÓN: Incrementar productos con botones (Base: {clics_base}, Incremento: +{incremento_clics}) ---")

    try:
        # La clave es localizar todos los botones '+' que son los que añaden cantidad.
        # Usamos XPath porque nos permite ser muy específicos con el content-desc.
        xpath_selector = "//android.widget.Button[@content-desc='+']"
        print(f"🔍 Buscando todos los botones de incremento con XPath: \"{xpath_selector}\"")

        # Buscar todos los botones de incremento
        botones_incremento = driver.find_elements(AppiumBy.XPATH, xpath_selector)

        cantidad_botones = len(botones_incremento)
        print(f"✅ Se encontraron {cantidad_botones} botones de incremento ('+').")

        if cantidad_botones == 0:
            print("⚠️ No se encontraron botones de incremento ('+'). No se realizará ninguna acción.")
            return

        # Iterar sobre cada botón de incremento encontrado
        for i, boton in enumerate(botones_incremento):
            # Calcular cuántos clics corresponden a este botón
            clics_para_este_boton = clics_base + (i * incremento_clics)

            print(f"\n📝 Procesando Botón {i + 1}/{cantidad_botones} - Se harán {clics_para_este_boton} clics.")

            if clics_para_este_boton <= 0:
                print(f"   ⏭️  Saltando botón {i + 1} porque el número de clics es cero o negativo.")
                continue

            try:
                # Hacer clic en el botón la cantidad de veces calculada
                for j in range(clics_para_este_boton):
                    print(f"   🖱️  Haciendo clic {j + 1}/{clics_para_este_boton}...")
                    boton.click()
                    time.sleep(0.2)  # Pequeña pausa para asegurar que la UI procese el clic

                print(f"   ✅ Botón {i + 1} procesado exitosamente con {clics_para_este_boton} clics.")

            except Exception as e:
                print(f"   ⚠️ Error al hacer clic en el botón {i + 1}: {e}")
                # Continuamos con el siguiente botón aunque este falle
                continue

        time.sleep(1)
        print("\n" + "=" * 50)
        print(f"🎉 ✅ PROCESO COMPLETADO: Se procesaron {cantidad_botones} productos.")
        print(f"📊 Patrón de clics aplicado: Base {clics_base}, Incremento por producto {incremento_clics}")
        print("=" * 50)

    except NoSuchElementException:
        print("❌ No se encontraron botones de incremento ('+') en la pantalla.")
        pytest.fail("Fallo crítico: No se encontraron botones de producto para interactuar.")

    except Exception as e:
        print(f"💥 Error general al interactuar con los botones de incremento: {e}")
        pytest.fail(f"Ocurrió un error inesperado durante la interacción con los botones: {e}")



