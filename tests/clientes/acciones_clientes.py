# acciones_cliente.py

import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def realizar_long_press_en_tarjeta_cliente(driver):
    """
    Realiza long press en la primera tarjeta de cliente encontrada.
    Usa el método más simple y compatible con Appium 3.
    """
    print("🎯 Realizando long press en tarjeta de cliente...")

    card_xpath = "(//android.view.View[starts-with(@content-desc, 'CLIENTES IS') and .//android.widget.ImageView and .//android.widget.Button])[1]"

    try:
        # Esperar y encontrar la tarjeta
        wait = WebDriverWait(driver, 10)
        cliente_card = wait.until(
            EC.presence_of_element_located(("xpath", card_xpath))
        )

        # Long press usando el método nativo de Appium 3
        driver.execute_script('mobile: longClickGesture', {
            'elementId': cliente_card.id,
            'duration': 2000
        })

        print("✅ Long press completado")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error en long press: {e}")
        raise

def pulsar_boton_central_nav(driver):
    """
    Pulsa el botón central de navegación.
    En debug_mode mantiene presionado para ver dónde está clickeando.
    """
    print("🎯 Buscando botón central de navegación...")

    # XPath corregido: busca un View clickeable sin content-desc que esté entre los botones de navegación
    # Basado en la estructura XML, debe estar al mismo nivel que Clientes, Itinerarios, etc.
    cart_button_xpath = "//android.view.View[@clickable='true' and not(@content-desc) and @bounds]"

    try:
        wait = WebDriverWait(driver, 10)

        # Buscar todos los elementos sin content-desc
        elementos_sin_desc = driver.find_elements("xpath", cart_button_xpath)
        print(f"📍 Encontrados {len(elementos_sin_desc)} elementos sin content-desc")

        # Filtrar por posición (el botón central debería estar en el medio)
        boton_central = None
        for elemento in elementos_sin_desc:
            bounds = elemento.get_attribute('bounds')
            print(f"📍 Elemento sin content-desc encontrado en bounds: {bounds}")

            # El botón central debería tener coordenadas X aproximadamente en el centro (around 456-624 según el XML)
            if bounds and '[456,' in bounds:
                boton_central = elemento
                print(f"✅ Botón central identificado en: {bounds}")
                break

        if not boton_central:
            # Fallback: tomar el primer elemento sin content-desc
            print("⚠️ Usando fallback: primer elemento sin content-desc")
            boton_central = elementos_sin_desc[0]


        print("🎯 Haciendo click normal...")
        boton_central.click()
        print("✅ Botón central pulsado")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error buscando botón central: {e}")
        raise

def escribir_nit(driver, nit, timeout=10):
    """
    Busca el campo de texto con el hint '*NIT', hace click para activarlo,
    lo limpia, escribe el valor proporcionado y presiona Enter.

    Args:
        driver: La instancia del driver de Appium.
        nit (str): El número de NIT a escribir.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"--- ACCIÓN: Escribir NIT: '{nit}' ---")
    try:
        nit_xpath = "//*[@hint='*NIT']"
        print(f"Buscando campo NIT con XPath: {nit_xpath}")
        wait = WebDriverWait(driver, timeout)

        # Esperar que el campo esté presente y sea clickeable
        nit_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, nit_xpath))
        )

        print("Campo NIT encontrado. Haciendo click para activarlo...")
        nit_field.click()  # CLICK PARA DAR FOCO

        time.sleep(0.5)  # Pequeña pausa para que se active el campo

        print("Limpiando campo y escribiendo NIT...")
        nit_field.clear()
        nit_field.send_keys(nit)

        print("Presionando Enter...")
        driver.press_keycode(66)  # Enter

        print(f"✅ NIT '{nit}' escrito correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo NIT en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR escribiendo NIT: {e}")
        raise

def escribir_dpi_representante(driver, dpi, timeout=10):
    """
    Busca el campo de texto con el hint 'DPI del representante',
    hace click para activarlo, lo limpia, escribe el valor y presiona Enter.

    Args:
        driver: La instancia del driver de Appium.
        dpi (str): El número de DPI a escribir.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"--- ACCIÓN: Escribir DPI del representante: '{dpi}' ---")
    try:
        dpi_xpath = "//*[@hint='*DPI del representante']"
        print(f"Buscando campo DPI con XPath: {dpi_xpath}")
        wait = WebDriverWait(driver, timeout)

        # Esperar que el campo esté presente y sea clickeable
        dpi_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, dpi_xpath))
        )

        print("Campo DPI encontrado. Haciendo click para activarlo...")
        dpi_field.click()  # CLICK PARA DAR FOCO

        time.sleep(0.5)  # Pequeña pausa para que se active el campo

        print("Limpiando campo y escribiendo DPI...")
        dpi_field.clear()
        dpi_field.send_keys(dpi)

        print("Presionando Enter...")
        driver.press_keycode(66)  # Enter

        print(f"✅ DPI '{dpi}' escrito correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo DPI en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR escribiendo DPI: {e}")
        raise

def escribir_en_campo_generico(driver, hint_text, valor, timeout=10):
    """
    Función genérica para escribir en cualquier campo de texto por su hint.

    Args:
        driver: La instancia del driver de Appium.
        hint_text (str): El texto del hint del campo a buscar.
        valor (str): El valor a escribir.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"--- ACCIÓN: Escribir '{valor}' en campo con hint '{hint_text}' ---")
    try:
        campo_xpath = f"//*[@hint='{hint_text}']"
        wait = WebDriverWait(driver, timeout)

        # Esperar que el campo esté presente y sea clickeable
        campo = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, campo_xpath))
        )

        print(f"Campo encontrado. Haciendo click para activarlo...")
        campo.click()  # CLICK PARA DAR FOCO

        time.sleep(0.5)  # Pausa para activación

        print("Limpiando y escribiendo...")
        campo.clear()
        campo.send_keys(valor)

        print("Presionando Enter...")
        driver.press_keycode(66)

        print(f"✅ Valor '{valor}' escrito en campo '{hint_text}'")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró campo con hint '{hint_text}' en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR escribiendo en campo: {e}")
        raise

def hacer_scroll_hacia_abajo(driver, cantidad_scroll=3):
    """
    Realiza scroll hacia abajo en la pantalla.

    Args:
        driver: La instancia del driver de Appium.
        cantidad_scroll (int): Número de scrolls a realizar.
    """
    print(f"📜 Haciendo scroll hacia abajo ({cantidad_scroll} veces)...")

    try:
        # Obtener dimensiones de la pantalla
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']

        # Calcular coordenadas para el scroll (desde el 80% hasta el 20% de la altura)
        start_y = int(screen_height * 0.8)
        end_y = int(screen_height * 0.2)
        center_x = int(screen_width * 0.5)

        for i in range(cantidad_scroll):
            print(f"Scroll {i + 1}/{cantidad_scroll}")

            # Realizar swipe hacia arriba (scroll hacia abajo)
            driver.swipe(center_x, start_y, center_x, end_y, duration=800)
            time.sleep(0.5)  # Pausa entre scrolls

        print("✅ Scroll hacia abajo completado")

    except Exception as e:
        print(f"❌ Error haciendo scroll: {e}")
        raise

def escribir_version_dpi(driver, version_dpi, timeout=10):
    """
    Busca el campo de texto con el hint '*Versión DPI', hace click para activarlo,
    lo limpia, escribe el valor proporcionado y presiona Enter.

    Args:
        driver: La instancia del driver de Appium.
        version_dpi (str): El valor de versión DPI a escribir.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"--- ACCIÓN: Escribir Versión DPI: '{version_dpi}' ---")
    try:
        version_dpi_xpath = "//*[@hint='*Versión DPI']"
        print(f"Buscando campo Versión DPI con XPath: {version_dpi_xpath}")
        wait = WebDriverWait(driver, timeout)

        # Esperar que el campo esté presente y sea clickeable
        version_dpi_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, version_dpi_xpath))
        )

        print("Campo Versión DPI encontrado. Haciendo click para activarlo...")
        version_dpi_field.click()  # CLICK PARA DAR FOCO

        time.sleep(0.5)  # Pequeña pausa para que se active el campo

        print("Limpiando campo y escribiendo Versión DPI...")
        version_dpi_field.clear()
        version_dpi_field.send_keys(version_dpi)

        print("Presionando Enter...")
        driver.press_keycode(66)  # Enter

        print(f"✅ Versión DPI '{version_dpi}' escrito correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo Versión DPI en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR escribiendo Versión DPI: {e}")
        raise



