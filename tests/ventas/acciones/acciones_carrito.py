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
    Encuentra el botón clickeable dentro de la sección de dirección de entrega
    basado en la estructura XML específica.
    """
    print("\n--- ACCIÓN: Seleccionar primera dirección (botón específico) ---")

    try:
        wait = WebDriverWait(driver, 15)

        # PASO 1: Encontrar el contenedor "Información de entrega"
        print("🔍 Paso 1: Localizando contenedor 'Información de entrega'...")
        xpath_contenedor = "//*[contains(@content-desc, 'Información de entrega')]"

        contenedor_info_entrega = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath_contenedor))
        )
        print("✅ Contenedor 'Información de entrega' encontrado")

        # PASO 2: Buscar el botón clickeable específico de la dirección
        print("🔍 Paso 2: Buscando botón clickeable de dirección...")

        # Estrategias específicas basadas en la estructura XML:
        xpaths_boton_direccion = [
            # A. Buscar Button clickeable que esté dentro de elementos con hint "Dirección de entrega"
            "//*[contains(@hint, 'Dirección de entrega')]//android.widget.Button[@clickable='true']",

            # B. Buscar Button clickeable después del contenedor "Información de entrega"
            xpath_contenedor + "/following::android.widget.Button[@clickable='true'][1]",

            # C. Buscar Button clickeable que esté cerca geográficamente del contenedor
            "//android.widget.Button[@clickable='true' and @bounds]",

            # D. Buscar cualquier elemento clickeable con hint de dirección
            "//*[contains(@hint, 'Dirección')]/*[@clickable='true'] | //*[contains(@hint, 'entrega')]/*[@clickable='true']",
        ]

        boton_direccion = None
        estrategia_usada = ""

        for i, xpath_boton in enumerate(xpaths_boton_direccion, 1):
            try:
                print(f"   Probando estrategia {i}: {xpath_boton}")

                if i == 3:  # Estrategia C - buscar por proximidad geográfica
                    # Obtener posición del contenedor
                    contenedor_location = contenedor_info_entrega.location
                    contenedor_bottom = contenedor_location['y'] + contenedor_info_entrega.size['height']

                    botones_candidatos = driver.find_elements(AppiumBy.XPATH, xpath_boton)
                    print(f"   Encontrados {len(botones_candidatos)} botones clickeables")

                    # Filtrar botones que estén cerca del contenedor (dentro de 500px hacia abajo)
                    for boton in botones_candidatos:
                        try:
                            boton_y = boton.location['y']
                            distancia = boton_y - contenedor_bottom

                            print(
                                f"   Botón en Y: {boton_y}, Contenedor bottom: {contenedor_bottom}, Distancia: {distancia}")

                            # Si está dentro de un rango razonable después del contenedor
                            if 0 <= distancia <= 500:
                                boton_direccion = boton
                                estrategia_usada = f"Estrategia {i} - Por proximidad (distancia: {distancia}px)"
                                print(f"   ✅ {estrategia_usada}")
                                break
                        except:
                            continue
                else:
                    # Estrategias directas por XPath
                    boton_direccion = driver.find_element(AppiumBy.XPATH, xpath_boton)
                    estrategia_usada = f"Estrategia {i}"
                    print(f"   ✅ {estrategia_usada} exitosa")

                if boton_direccion:
                    break

            except Exception as e:
                print(f"   ⚠️ Estrategia {i} falló: {e}")
                continue

        if not boton_direccion:
            print("🔍 Estrategia de respaldo: Buscar por coordenadas específicas...")

            # Basado en la estructura XML, sabemos que el botón está aproximadamente en [912,1340][1038,1466]
            # Buscar botones clickeables en esa área general
            todos_botones = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@clickable='true']")
            print(f"   Total botones clickeables: {len(todos_botones)}")

            for boton in todos_botones:
                try:
                    bounds_str = boton.get_attribute('bounds')
                    if bounds_str:
                        # Extraer coordenadas del bounds [x1,y1][x2,y2]
                        import re
                        matches = re.findall(r'\[(\d+),(\d+)\]', bounds_str)
                        if len(matches) >= 2:
                            x1, y1 = int(matches[0][0]), int(matches[0][1])
                            x2, y2 = int(matches[1][0]), int(matches[1][1])

                            # Verificar si está en el área esperada de la dirección (lado derecho, medio-abajo)
                            if x1 > 800 and y1 > 1200 and y1 < 1600:  # Área aproximada del botón de dirección
                                boton_direccion = boton
                                estrategia_usada = f"Respaldo - Por área geográfica (bounds: {bounds_str})"
                                print(f"   ✅ {estrategia_usada}")
                                break
                except:
                    continue

        if not boton_direccion:
            raise Exception("No se encontró el botón clickeable de dirección con ninguna estrategia")

        # PASO 3: Información del botón encontrado y hacer clic
        print("✅ Botón de dirección encontrado:")

        try:
            texto = boton_direccion.get_attribute('text') or '(sin texto)'
            desc = boton_direccion.get_attribute('content-desc') or '(sin descripción)'
            bounds = boton_direccion.get_attribute('bounds') or '(sin bounds)'
            clase = boton_direccion.get_attribute('class') or '(sin clase)'

            print(f"   Estrategia: {estrategia_usada}")
            print(f"   Clase: {clase}")
            print(f"   Texto: '{texto}'")
            print(f"   Descripción: '{desc}'")
            print(f"   Bounds: {bounds}")

            # Verificar que NO sea el elemento de productos (evitar el error anterior)
            if "Productos:" in desc or "Subtotal:" in desc:
                print("   ⚠️ ADVERTENCIA: Este parece ser el elemento de productos, no de dirección")
                print("   Intentando encontrar otro elemento...")
                raise Exception("Elemento incorrecto detectado (productos en lugar de dirección)")

        except Exception as info_error:
            print(f"   ⚠️ Error obteniendo información del elemento: {info_error}")
            if "Elemento incorrecto" in str(info_error):
                raise info_error

        print("🎯 Haciendo clic en el botón de dirección...")
        boton_direccion.click()
        time.sleep(3)  # Esperar a que se abra el dropdown

        print("✅ Clic realizado en el botón de dirección")

        # PASO 4: Buscar y seleccionar opciones del dropdown
        print("🔍 Paso 4: Buscando opciones del dropdown de direcciones...")

        # Esperar un poco más para la animación
        time.sleep(2)

        # Buscar opciones específicas del dropdown de direcciones
        xpaths_opciones_direccion = [
            # A. Opciones en ScrollView que contengan información de dirección
            "//android.widget.ScrollView//android.view.View[@clickable='true' and (contains(@text, 'Palencia') or contains(@content-desc, 'Palencia') or contains(@text, 'Testing'))]",

            # B. Cualquier opción clickeable en ScrollView después del clic
            "//android.widget.ScrollView//android.view.View[@clickable='true']",

            # C. Elementos clickeables nuevos que aparecieron
            "//*[@clickable='true' and string-length(@text) > 0 and not(contains(@text, 'Menú')) and not(contains(@text, 'Cliente')) and not(contains(@content-desc, 'Productos'))]",
        ]

        opciones_direccion = []

        for i, xpath_opcion in enumerate(xpaths_opciones_direccion, 1):
            try:
                print(f"   Buscando opciones con estrategia {i}...")
                opciones_temp = driver.find_elements(AppiumBy.XPATH, xpath_opcion)

                if opciones_temp:
                    # Filtrar opciones que realmente sean direcciones
                    for opcion in opciones_temp:
                        try:
                            texto_op = opcion.get_attribute('text') or ''
                            desc_op = opcion.get_attribute('content-desc') or ''

                            # Evitar elementos que claramente no son direcciones
                            if any(keyword in desc_op.lower() for keyword in
                                   ['producto', 'subtotal', 'descuento', 'total', 'gtq']):
                                continue

                            opciones_direccion.append(opcion)
                        except:
                            opciones_direccion.append(
                                opcion)  # Agregar de todas formas si no se pueden obtener atributos

                    if opciones_direccion:
                        print(f"   ✅ Encontradas {len(opciones_direccion)} opciones de dirección")
                        break
            except Exception as e:
                print(f"   ⚠️ Error en estrategia {i}: {e}")
                continue

        if opciones_direccion:
            print("🎯 Seleccionando primera opción de dirección...")
            primera_opcion = opciones_direccion[0]

            try:
                texto_opcion = primera_opcion.get_attribute('text') or '(sin texto)'
                desc_opcion = primera_opcion.get_attribute('content-desc') or '(sin descripción)'
                print(f"   Primera opción - Texto: '{texto_opcion}' | Desc: '{desc_opcion[:100]}...'")
            except:
                print("   Primera opción encontrada (sin detalles)")

            primera_opcion.click()
            time.sleep(2)

            print("✅ Primera dirección de entrega seleccionada exitosamente")
        else:
            print("⚠️ No se encontraron opciones del dropdown, pero el clic en el botón se realizó")
            print("   (Es posible que ya estuviera seleccionada la dirección correcta)")

    except Exception as e:
        print(f"\n❌ Error en seleccionar_primera_direccion_entrega: {e}")

        # Debug adicional específico para direcciones
        try:
            print("\n🔍 DEBUG - Elementos relacionados con dirección:")
            elementos_direccion = driver.find_elements(AppiumBy.XPATH,
                                                       "//*[contains(@hint, 'Dirección') or contains(@hint, 'entrega') or contains(@content-desc, 'Información de entrega')]")

            for i, elem in enumerate(elementos_direccion, 1):
                try:
                    clase = elem.get_attribute('class')
                    texto = elem.get_attribute('text') or '(sin texto)'
                    desc = elem.get_attribute('content-desc') or '(sin desc)'
                    hint = elem.get_attribute('hint') or '(sin hint)'
                    clickeable = elem.get_attribute('clickable')
                    bounds = elem.get_attribute('bounds')

                    print(f"   [{i}] Clase: {clase} | Clickeable: {clickeable}")
                    print(f"       Texto: '{texto}' | Desc: '{desc}'")
                    print(f"       Hint: '{hint}' | Bounds: {bounds}")
                    print("       ---")
                except:
                    print(f"   [{i}] Error obteniendo información")
        except:
            pass

        pytest.fail(f"Error al seleccionar dirección de entrega: {e}")
def debug_estructura_direccion_xml(driver):
    """
    Debug específico basado en la estructura XML mostrada
    """
    print("\n🔍 === DEBUG ESTRUCTURA XML DIRECCIÓN ===")

    try:
        # Buscar el elemento "Información de entrega"
        info_entrega = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Información de entrega')]")
        print("✅ Elemento 'Información de entrega' encontrado")
        print(f"   Bounds: {info_entrega.get_attribute('bounds')}")
        print(f"   Clickeable: {info_entrega.get_attribute('clickable')}")

        # Buscar elementos con hint "Dirección de entrega"
        print("\n🔍 Elementos con hint 'Dirección de entrega':")
        elementos_hint = driver.find_elements(AppiumBy.XPATH, "//*[contains(@hint, 'Dirección de entrega')]")

        for i, elem in enumerate(elementos_hint, 1):
            print(f"   [{i}] Clase: {elem.get_attribute('class')}")
            print(f"       Texto: '{elem.get_attribute('text')}' | Hint: '{elem.get_attribute('hint')}'")
            print(f"       Bounds: {elem.get_attribute('bounds')} | Clickeable: {elem.get_attribute('clickable')}")

        # Buscar botones clickeables en la zona
        print(f"\n🔍 Botones clickeables después de 'Información de entrega':")
        botones = driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@clickable='true']")

        info_y = info_entrega.location['y']
        for i, boton in enumerate(botones, 1):
            boton_y = boton.location['y']
            if boton_y > info_y:  # Solo botones que estén después del elemento "Información de entrega"
                distancia = boton_y - info_y
                print(f"   [{i}] Bounds: {boton.get_attribute('bounds')} | Distancia: {distancia}px")
                print(f"       Texto: '{boton.get_attribute('text')}' | Desc: '{boton.get_attribute('content-desc')}'")

    except Exception as e:
        print(f"Error en debug_estructura_direccion_xml: {e}")

