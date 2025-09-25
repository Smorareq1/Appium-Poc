# acciones_cliente.py

import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def ensure_keyboard_closed(driver):
    """
    Función auxiliar para asegurar que el teclado esté cerrado.
    Intenta múltiples métodos para cerrar el teclado.
    """
    try:
        # Método 1: hide_keyboard()
        driver.hide_keyboard()
        print("Teclado cerrado con hide_keyboard()")
    except Exception:
        try:
            # Método 2: Presionar back si hay teclado
            if driver.is_keyboard_shown():
                driver.back()
                print("Teclado cerrado con back()")
        except Exception:
            try:
                # Método 3: Click en una zona vacía para quitar foco
                size = driver.get_window_size()
                x = int(size['width'] / 2)
                y = int(size['height'] * 0.1)  # Top area
                driver.tap([(x, y)], 100)
                print("Teclado cerrado con tap en zona vacía")
            except Exception:
                print("No se pudo cerrar el teclado, continuando...")

    # Espera breve para asegurar que el teclado se cierre
    time.sleep(0.5)

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
        time.sleep(3)

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
        dpi_xpath = "//*[contains(@hint, 'DPI del representante')]"
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

def seleccionar_vencimiento_dpi(driver, dia, year_actual , timeout=10):
    """
    Selecciona una fecha en el campo "*Vencimiento DPI".
    Versión optimizada que usa solo los selectores que funcionaron.

    Args:
        driver: La instancia del driver de Appium.
        dia (str): El día a seleccionar (ej: "13", "01", "30")
        year_actual (str): Año actual mostrado en el date picker (por defecto "2025")
        timeout (int): Tiempo máximo de espera.
    """
    year_siguiente = str(int(year_actual) + 1)
    print(f"📅 Seleccionando fecha en Vencimiento DPI - Año: {year_siguiente}, Día: '{dia}'")

    try:
        # Paso 1: Hacer click en el campo Vencimiento DPI
        print("🎯 Haciendo click en campo Vencimiento DPI...")
        vencimiento_xpath = "//*[@hint='*Vencimiento DPI']"
        wait = WebDriverWait(driver, timeout)

        vencimiento_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, vencimiento_xpath))
        )

        vencimiento_field.click()
        print("✅ Date picker abierto")
        time.sleep(2)

        # Paso 2: Hacer click en año actual
        print(f"🎯 Seleccionando año {year_actual}...")
        year_current = driver.find_element("xpath", f"//*[contains(@text, '{year_actual}')]")
        year_current.click()
        print(f"✅ Año {year_actual} clickeado")
        time.sleep(1)

        # Paso 3: Seleccionar año siguiente
        print(f"🎯 Seleccionando año {year_siguiente}...")
        year_next = driver.find_element("xpath", f"//*[@content-desc='{year_siguiente}']")
        year_next.click()
        print(f"✅ Año {year_siguiente} seleccionado")
        time.sleep(1)

        # Paso 4: Seleccionar el día
        print(f"🎯 Seleccionando día '{dia}'...")
        day_element = driver.find_element("xpath", f"//*[@content-desc='{dia}']")
        day_element.click()
        print(f"✅ Día '{dia}' seleccionado")
        time.sleep(1)

        # Paso 5: Confirmar con botón "aceptar"
        print("🎯 Confirmando selección...")
        aceptar_button = driver.find_element("xpath", "//*[@content-desc='Aceptar']")
        aceptar_button.click()
        print("✅ Fecha confirmada")

        time.sleep(1)
        print(f"✅ Vencimiento DPI completado - Año: {year_siguiente}, Día: {dia}")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo Vencimiento DPI en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR seleccionando fecha: {e}")
        raise

def escribir_nota(driver, comentario, timeout=10):
    """
    Busca el campo con hint 'Nota', hace click para activarlo,
    y escribe el comentario proporcionado.

    Args:
        driver: La instancia del driver de Appium.
        comentario (str): El texto/comentario a escribir en el campo Nota.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"📝 Escribiendo nota: '{comentario}'")
    try:
        nota_xpath = "//*[@hint='Nota']"
        print("🎯 Buscando campo Nota...")
        wait = WebDriverWait(driver, timeout)

        # Esperar que el campo esté presente y sea clickeable
        nota_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, nota_xpath))
        )

        print("Campo Nota encontrado. Haciendo click para activarlo...")
        nota_field.click()  # CLICK PARA DAR FOCO

        time.sleep(0.5)  # Pequeña pausa para que se active el campo

        print("Limpiando campo y escribiendo nota...")
        nota_field.clear()
        nota_field.send_keys(comentario)

        print("Ocultando teclado...")
        ensure_keyboard_closed(driver)

        print(f"✅ Nota '{comentario}' escrita correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo Nota en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR escribiendo nota: {e}")
        raise

def hacer_click_continuar(driver, timeout=10):
    """
    Busca y hace click en el botón con content-desc 'Continuar'.

    Args:
        driver: La instancia del driver de Appium.
        timeout (int): Tiempo máximo de espera.
    """
    print("🎯 Buscando botón Continuar...")
    try:
        continuar_xpath = "//*[@content-desc='Continuar']"
        wait = WebDriverWait(driver, timeout)

        continuar_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, continuar_xpath))
        )

        print("Botón Continuar encontrado. Haciendo click...")
        continuar_button.click()

        time.sleep(2)  # Pausa para que procese la acción
        print("✅ Botón Continuar presionado correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón Continuar en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR haciendo click en Continuar: {e}")
        raise

def hacer_scroll_hacia_arriba(driver, cantidad_scroll=3):
    try:
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']

        start_y = int(screen_height * 0.2)
        end_y = int(screen_height * 0.8)
        center_x = int(screen_width * 0.5)

        for i in range(cantidad_scroll):
            driver.swipe(center_x, start_y, center_x, end_y, duration=800)
            time.sleep(0.3)
    except:
        pass

# Sucursales
def seleccionar_tipo_de_ruta(driver, timeout=10):
    """
    Hace click en el botón "Tipo de ruta" y selecciona "Venta".

    Args:
        driver: La instancia del driver de Appium.
        timeout (int): Tiempo máximo de espera.
    """
    print("🎯 Seleccionando Tipo de ruta...")

    try:
        # Paso 1: Hacer click en el botón Tipo de ruta
        print("Paso 1: Haciendo click en Tipo de ruta...")
        tipo_ruta_xpath = "//*[contains(@content-desc, 'Tipo de ruta')]"
        wait = WebDriverWait(driver, timeout)

        tipo_ruta_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, tipo_ruta_xpath))
        )

        tipo_ruta_button.click()
        print("✅ Botón Tipo de ruta clickeado")
        time.sleep(2)  # Esperar que aparezcan las opciones

        # Paso 2: Seleccionar "Venta"
        print("Paso 2: Seleccionando opción 'Venta'...")
        venta_xpath = "//*[@content-desc='Venta']"

        venta_option = driver.find_element("xpath", venta_xpath)
        venta_option.click()
        print("✅ Opción 'Venta' seleccionada")

        time.sleep(1)
        print("✅ Tipo de ruta configurado correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón Tipo de ruta en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR seleccionando tipo de ruta: {e}")
        raise

def seleccionar_direccion(driver, opcion_texto, timeout=10):
    """
    Hace click en el botón "Dirección" y selecciona una opción cuyo texto contenga
    la cadena indicada en opcion_texto.

    Args:
        driver: La instancia del driver de Appium.
        opcion_texto (str): Texto parcial de la opción a seleccionar.
        timeout (int): Tiempo máximo de espera.
    """
    print("🎯 Seleccionando Dirección...")

    try:
        # Paso 1: Hacer click en el botón Dirección
        print("Paso 1: Haciendo click en Dirección...")
        direccion_xpath = "//*[contains(@content-desc, 'Dirección')]"
        wait = WebDriverWait(driver, timeout)

        direccion_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, direccion_xpath))
        )
        direccion_button.click()
        print("✅ Botón Dirección clickeado")
        time.sleep(2)  # Esperar que aparezcan las opciones

        # Paso 2: Seleccionar opción según el texto proporcionado
        print(f"Paso 2: Seleccionando opción que contenga '{opcion_texto}'...")
        opcion_xpath = f"//*[contains(@content-desc, '{opcion_texto}')]"

        seleccionar_direccion_option = driver.find_element(AppiumBy.XPATH, opcion_xpath)
        seleccionar_direccion_option.click()
        print(f"✅ Opción con texto '{opcion_texto}' seleccionada")

        time.sleep(1)
        print("✅ Dirección configurada correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón Dirección en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR seleccionando dirección: {e}")
        raise

def llenar_formulario_direccion(driver, campo1="", campo2="", campo3="", campo4="", campo5="", timeout=10):
    """
    Llena el formulario "Añadir dirección" con los datos proporcionados
    y presiona el botón Validar al finalizar.

    Args:
        driver: La instancia del driver de Appium.
        campo1 (str): Valor para el primer campo (puede ser dirección principal)
        campo2 (str): Valor para el segundo campo (puede ser ciudad)
        campo3 (str): Valor para el tercer campo (puede ser código postal)
        campo4 (str): Valor para el cuarto campo (puede ser referencia)
        campo5 (str): Valor para el quinto campo (puede ser notas adicionales)
        timeout (int): Tiempo máximo de espera.
    """
    print("📝 Llenando formulario 'Añadir dirección'...")

    # Lista de valores para los campos
    valores_campos = [campo1, campo2, campo3, campo4, campo5]
    nombres_campos = ["Campo 1", "Campo 2", "Campo 3", "Campo 4", "Campo 5"]

    try:
        wait = WebDriverWait(driver, timeout)

        # Buscar todos los EditText del formulario
        print("🔍 Buscando campos del formulario...")
        campos_edittext = driver.find_elements("class name", "android.widget.EditText")

        if len(campos_edittext) != 5:
            print(f"⚠️ Esperaba 5 campos, encontré {len(campos_edittext)}")

        # Llenar cada campo con su valor correspondiente
        for i, (campo, valor, nombre) in enumerate(zip(campos_edittext, valores_campos, nombres_campos)):
            if valor:  # Solo llenar si el valor no está vacío
                try:
                    print(f"📝 Llenando {nombre}: '{valor}'")

                    # Hacer click para activar el campo
                    campo.click()
                    time.sleep(0.3)

                    # Limpiar y escribir
                    campo.clear()
                    campo.send_keys(valor)

                    print(f"✅ {nombre} completado")

                except Exception as e:
                    print(f"⚠️ Error llenando {nombre}: {e}")
            else:
                print(f"⏭️ {nombre}: vacío, saltando...")

        # Pequeña pausa antes de validar
        time.sleep(1)
        # Presionar ok de android
        driver.press_keycode(66)
        # Presionar el botón Validar
        print("🎯 Presionando botón 'Validar'...")
        validar_button = driver.find_element("xpath", "//*[@content-desc='Validar']")
        validar_button.click()

        time.sleep(2)  # Esperar que procese la validación
        print("✅ Formulario enviado correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se pudo completar el formulario en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR llenando formulario de dirección: {e}")
        raise

def seleccionar_contacto(driver, opcion_texto, timeout=10):
    """
    Hace click en el botón "Contacto" y selecciona una opción cuyo texto contenga
    la cadena indicada en opcion_texto.

    Args:
        driver: La instancia del driver de Appium.
        opcion_texto (str): Texto parcial de la opción a seleccionar.
        timeout (int): Tiempo máximo de espera.
    """
    print("🎯 Seleccionando Contacto...")

    try:
        # Paso 1: Hacer click en el botón Contacto
        print("Paso 1: Haciendo click en Contacto...")
        contacto_xpath = "//*[contains(@content-desc, 'Contacto')]"
        wait = WebDriverWait(driver, timeout)

        contacto_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, contacto_xpath))
        )
        contacto_button.click()
        print("✅ Botón Contacto clickeado")
        time.sleep(2)  # Esperar que aparezcan las opciones

        # Paso 2: Seleccionar opción según el texto proporcionado
        print(f"Paso 2: Seleccionando opción que contenga '{opcion_texto}'...")
        opcion_xpath = f"//*[contains(@content-desc, '{opcion_texto}')]"

        seleccionar_contacto_option = driver.find_element(AppiumBy.XPATH, opcion_xpath)
        seleccionar_contacto_option.click()
        print(f"✅ Opción con texto '{opcion_texto}' seleccionada")

        time.sleep(1)
        print("✅ Contacto configurado correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón Contacto en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR seleccionando contacto: {e}")
        raise

def llenar_formulario_contacto(driver, nombres="", apellidos="", puesto="", correo1="", telefono1="", timeout=10):
    """
    Llena el formulario "Añadir contacto" con los datos proporcionados
    y presiona el botón Validar al finalizar.

    Args:
        driver: La instancia del driver de Appium.
        nombres (str): Nombre(s) del contacto.
        apellidos (str): Apellidos del contacto.
        puesto (str): Puesto o cargo del contacto.
        correo1 (str): Correo electrónico principal.
        telefono1 (str): Teléfono principal.
        timeout (int): Tiempo máximo de espera.
    """
    print("📝 Llenando formulario 'Añadir contacto'...")

    # Lista de valores para los campos
    valores_campos = [nombres, apellidos, puesto, correo1, telefono1]
    nombres_campos = ["Nombres", "Apellidos", "Puesto", "Correo 1", "Teléfono 1"]

    try:
        wait = WebDriverWait(driver, timeout)

        # Buscar todos los EditText del formulario
        print("🔍 Buscando campos del formulario...")
        campos_edittext = driver.find_elements("class name", "android.widget.EditText")

        if len(campos_edittext) != 5:
            print(f"⚠️ Esperaba 5 campos, encontré {len(campos_edittext)}")

        # Llenar cada campo con su valor correspondiente
        for i, (campo, valor, nombre) in enumerate(zip(campos_edittext, valores_campos, nombres_campos)):
            if valor:  # Solo llenar si el valor no está vacío
                try:
                    print(f"📝 Llenando {nombre}: '{valor}'")

                    # Hacer click para activar el campo
                    campo.click()
                    time.sleep(0.3)

                    # Limpiar y escribir
                    campo.clear()
                    campo.send_keys(valor)

                    print(f"✅ {nombre} completado")

                except Exception as e:
                    print(f"⚠️ Error llenando {nombre}: {e}")
            else:
                print(f"⏭️ {nombre}: vacío, saltando...")

        # Pequeña pausa antes de validar
        time.sleep(1)
        # Presionar OK del teclado (Enter en Android)
        driver.press_keycode(66)
        # Presionar el botón Validar
        print("🎯 Presionando botón 'Validar'...")
        validar_button = driver.find_element("xpath", "//*[@content-desc='Validar']")
        validar_button.click()

        time.sleep(2)  # Esperar que procese la validación
        print("✅ Formulario de contacto enviado correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se pudo completar el formulario de contacto en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR llenando formulario de contacto: {e}")
        raise

# Geolozalicaion
def click_asignar_geolocalizacion(driver, timeout=10):
    """
    Hace click en el botón con content-desc que contiene 'Asignar geolocalización'.

    Args:
        driver: La instancia del driver de Appium.
        timeout (int): Tiempo máximo de espera.
    """
    print("📍 Buscando botón 'Asignar geolocalización'...")

    try:
        wait = WebDriverWait(driver, timeout)
        boton_xpath = "//*[contains(@content-desc, 'Asignar geolocalización')]"

        boton = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, boton_xpath))
        )
        boton.click()


        print("✅ Botón 'Asignar geolocalización' clickeado")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón 'Asignar geolocalización' en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR al dar click en 'Asignar geolocalización': {e}")
        raise
def click_capturar(driver, timeout=10):
    print("📍 Buscando botón 'Capturar'...")

    try:
        wait = WebDriverWait(driver, timeout)
        boton_xpath = "//*[contains(@content-desc, 'Capturar') and @clickable='true']"

        boton = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, boton_xpath))
        )
        boton.click()

        print("✅ Botón 'Capturar' clickeado")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón 'Capturar' en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR al dar click en 'Capturar': {e}")
        raise

# Borrar otras sucursales y confirmar
def eliminar_gestiones_extras_iterativo(driver, max_intentos):
    """
    Elimina gestiones extras de forma iterativa:
    1. Busca gestiones que NO sean "Gestión 1"
    2. Elimina la primera que encuentre
    3. Vuelve a buscar (DOM actualizado)
    4. Repite hasta que solo quede "Gestión 1"

    Args:
        driver: La instancia del driver de Appium.
        timeout (int): Tiempo máximo de espera por elemento.
        max_intentos (int): Máximo número de gestiones a eliminar (previene bucle infinito).
    """
    print("🗑️ Eliminando gestiones extras iterativamente...")

    intentos = 0

    while intentos < max_intentos:
        try:
            print(f"\n🔄 Intento {intentos + 1}: Buscando gestiones extras...")

            # Buscar gestiones que NO sean "Gestión 1"
            gestiones_extra_xpath = "//*[contains(@content-desc, 'Gestión') and not(contains(@content-desc, 'Gestión 1'))]"
            gestiones_extras = driver.find_elements("xpath", gestiones_extra_xpath)

            if not gestiones_extras:
                print("✅ No se encontraron más gestiones extras. Solo queda Gestión 1")
                break

            print(f"📋 Encontradas {len(gestiones_extras)} gestiones extras")

            # Tomar la PRIMERA gestión extra encontrada
            primera_gestion = gestiones_extras[0]
            gestion_desc = primera_gestion.get_attribute('content-desc')
            print(f"🎯 Eliminando: {gestion_desc}")

            # Buscar el segundo ImageView dentro de esta gestión
            imageviews = primera_gestion.find_elements("xpath", ".//android.widget.ImageView")

            if len(imageviews) < 2:
                print(f"⚠️ {gestion_desc}: No tiene suficientes ImageViews, saltando...")
                intentos += 1
                continue

            # Hacer click en el segundo ImageView (índice 1)
            segundo_imageview = imageviews[1]
            print("🖱️ Click en segundo ImageView...")
            segundo_imageview.click()

            # Esperar 1 segundo como especificaste
            time.sleep(1)

            # Buscar y hacer click en botón "confirmar"
            print("🔍 Buscando botón 'confirmar'...")
            confirmar_button = driver.find_element("xpath", "//*[@content-desc='Confirmar']")
            confirmar_button.click()
            print(f"✅ {gestion_desc} eliminada")

            # Pausa para que el DOM se actualice
            time.sleep(2)

            intentos += 1

        except NoSuchElementException as e:
            print(f"⚠️ Elemento no encontrado en intento {intentos + 1}: {e}")
            break
        except Exception as e:
            print(f"❌ Error en intento {intentos + 1}: {e}")
            intentos += 1
            continue

    if intentos >= max_intentos:
        print(f"⚠️ Se alcanzó el máximo de intentos ({max_intentos}). Puede que queden gestiones extras")
    else:
        print("✅ Proceso completado: Solo queda Gestión 1")

# Continuar
def hacer_click_boton_sucursal_especifico(driver, timeout=10):
    """
    Versión más específica que busca exactamente el botón por su posición
    relativa al ImageView en Sucursal 1.
    """
    print("🏢 Haciendo click en botón específico de Sucursal 1...")

    try:
        # XPath que busca el botón que está justo después del ImageView en Sucursal 1
        boton_xpath = "//*[@content-desc='Sucursal 1']//android.widget.ImageView/following-sibling::android.widget.Button[1]"

        wait = WebDriverWait(driver, timeout)
        boton_sucursal = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, boton_xpath))
        )

        print("🎯 Haciendo click en botón específico...")
        boton_sucursal.click()

        time.sleep(1)
        print("✅ Click completado")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón específico en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR: {e}")
        raise
def click_continuar(driver, timeout=10):
    print("📍 Buscando botón 'Continuar'...")

    try:
        wait = WebDriverWait(driver, timeout)
        boton_xpath = "//*[contains(@content-desc, 'Continuar') and @clickable='true']"

        boton = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, boton_xpath))
        )
        boton.click()

        print("✅ Botón 'Continuar' clickeado")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón 'Continuar' en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR al dar click en 'Continuar': {e}")
        raise

# Perfilacion
def seleccionar_condicion(driver, opcion_texto, timeout=10):
    """
    Hace click en el botón "Condición" y selecciona una opción cuyo texto contenga
    la cadena indicada en opcion_texto.

    Args:
        driver: La instancia del driver de Appium.
        opcion_texto (str): Texto parcial de la opción a seleccionar.
        timeout (int): Tiempo máximo de espera.
    """
    print("🎯 Seleccionando Condición...")

    try:
        # Paso 1: Hacer click en el botón Condición
        print("Paso 1: Haciendo click en Condición...")
        condicion_xpath = "//*[contains(@content-desc, 'Condición')]"
        wait = WebDriverWait(driver, timeout)

        condicion_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, condicion_xpath))
        )
        condicion_button.click()
        print("✅ Botón Condición clickeado")
        time.sleep(2)  # Esperar que aparezcan las opciones

        # Paso 2: Seleccionar opción según el texto proporcionado
        print(f"Paso 2: Seleccionando opción que contenga '{opcion_texto}'...")
        opcion_xpath = f"//*[contains(@content-desc, '{opcion_texto}')]"

        seleccionar_condicion_option = driver.find_element(AppiumBy.XPATH, opcion_xpath)
        seleccionar_condicion_option.click()
        print(f"✅ Opción con texto '{opcion_texto}' seleccionada")

        time.sleep(1)
        print("✅ Condición configurada correctamente")

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el botón Condición en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR seleccionando condición: {e}")
        raise

#Final
def buscar_cliente(driver, texto_busqueda, timeout=10):
    """
    Busca un cliente específico escribiendo en el campo de búsqueda
    y verifica que aparezca una tarjeta de cliente con ese texto.

    Args:
        driver: La instancia del driver de Appium.
        texto_busqueda (str): Texto a buscar (nombre, código, etc.)
        timeout (int): Tiempo máximo de espera.
    """
    print(f"🔍 Buscando cliente: '{texto_busqueda}'")

    try:
        # Paso 1: Encontrar y hacer click en el campo de búsqueda
        print("Paso 1: Localizando campo de búsqueda...")
        search_xpath = "//*[@hint='Buscar']"
        wait = WebDriverWait(driver, timeout)

        search_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, search_xpath))
        )

        # Hacer click para activar el campo
        search_field.click()
        print("✅ Campo de búsqueda activado")
        time.sleep(0.5)

        # Paso 2: Limpiar y escribir el texto de búsqueda
        print(f"Paso 2: Escribiendo '{texto_busqueda}'...")
        search_field.clear()
        search_field.send_keys(texto_busqueda)

        # Presionar Enter para ejecutar búsqueda
        driver.press_keycode(66)  # Enter
        print("✅ Búsqueda ejecutada")

        # Paso 3: Esperar y verificar que aparezca un resultado
        print("Paso 3: Verificando resultados...")
        time.sleep(2)  # Esperar que aparezcan los resultados

        # Buscar tarjetas de cliente que contengan el texto buscado
        resultado_xpath = f"//*[contains(@content-desc, '{texto_busqueda}')]"

        try:
            resultado = driver.find_element("xpath", resultado_xpath)
            resultado_desc = resultado.get_attribute('content-desc')
            print(f"✅ Cliente encontrado: {resultado_desc}")
            return resultado

        except NoSuchElementException:
            print(f"⚠️ No se encontraron resultados para '{texto_busqueda}'")
            return None

    except TimeoutException:
        print(f"❌ ERROR: No se encontró el campo de búsqueda en {timeout} segundos")
        raise
    except Exception as e:
        print(f"❌ ERROR durante la búsqueda: {e}")
        raise


def buscar_y_seleccionar_cliente(driver, texto_busqueda, timeout=10):
    """
    Busca un cliente y hace click en la primera tarjeta encontrada.

    Args:
        driver: La instancia del driver de Appium.
        texto_busqueda (str): Texto a buscar.
        timeout (int): Tiempo máximo de espera.
    """
    print(f"🎯 Buscando y seleccionando cliente: '{texto_busqueda}'")

    try:
        # Realizar la búsqueda
        resultado = buscar_cliente(driver, texto_busqueda, timeout)

        if resultado:
            # Hacer click en la tarjeta encontrada
            print("🖱️ Haciendo click en el cliente encontrado...")
            resultado.click()
            time.sleep(1)
            print("✅ Cliente seleccionado")
            return resultado
        else:
            raise Exception(f"No se encontraron clientes con '{texto_busqueda}'")

    except Exception as e:
        print(f"❌ ERROR seleccionando cliente: {e}")
        raise


def buscar_cliente_por_codigo(driver, codigo, timeout=10):
    """
    Función específica para buscar por código de cliente (ej: CM20250926).
    """
    print(f"🔍 Buscando cliente por código: '{codigo}'")
    return buscar_cliente(driver, codigo, timeout)


def buscar_cliente_por_nombre(driver, nombre, timeout=10):
    """
    Función específica para buscar por nombre de cliente.
    """
    print(f"🔍 Buscando cliente por nombre: '{nombre}'")
    return buscar_cliente(driver, nombre, timeout)