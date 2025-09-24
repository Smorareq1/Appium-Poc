# acciones_cliente.py

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time


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

