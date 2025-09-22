import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import pytest

"""
Este archivo contiene funciones reutilizables para las acciones de búsqueda
y selección de productos, para ser llamadas desde diferentes clases de test.
"""


def realizar_click_en_buscar(driver):
    """Hace click en el campo/botón 'Buscar' inicial."""
    print("\n--- ACCIÓN: Click en Buscar ---")
    buscar_element = None
    try:
        # Estrategia 1: Por content-desc exacto
        print("Estrategia 1: Buscando por content-desc exacto 'Buscar'...")
        buscar_element = driver.find_element(AppiumBy.XPATH, "//*[@content-desc='Buscar']")
        print("✅ Encontrado por content-desc exacto")
    except NoSuchElementException:
        print("❌ No encontrado por content-desc exacto. Intentando Estrategia 2...")
        # Estrategia 2: Por contains en content-desc
        try:
            buscar_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc, 'Buscar')]")
            print("✅ Encontrado por contains en content-desc")
        except NoSuchElementException:
            pytest.fail("No se pudo encontrar el elemento 'Buscar' con ninguna estrategia.")

    print("Haciendo click en 'Buscar'...")
    buscar_element.click()
    time.sleep(2)


def escribir_y_buscar_sku(driver, sku):
    """Escribe un SKU en el campo de búsqueda ya activo."""
    print(f"\n--- ACCIÓN: Escribir SKU: {sku} ---")
    campo_texto_element = None
    try:
        print("Buscando el campo de texto activo (EditText)...")
        campo_texto_element = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
        print("✅ Campo de texto (EditText) encontrado por su clase.")
    except NoSuchElementException:
        pytest.fail("No se pudo encontrar el campo de texto (EditText).")

    print("Asegurando foco y limpiando el campo de texto...")
    campo_texto_element.click()
    time.sleep(1)
    try:
        campo_texto_element.clear()
    except Exception:
        print("Advertencia: No se pudo limpiar el campo o ya estaba vacío.")

    print(f"Escribiendo texto: '{sku}'...")
    campo_texto_element.send_keys(sku)
    time.sleep(2)
    try:
        driver.hide_keyboard()
    except Exception:
        print("Advertencia: No se pudo ocultar el teclado o no estaba visible.")


def seleccionar_resultado_por_sku(driver, sku):
    """Selecciona el resultado que aparece después de buscar un SKU."""
    print(f"\n--- ACCIÓN: Seleccionar resultado para SKU: {sku} ---")
    resultado_element = None
    print("Esperando a que aparezca el resultado...")
    time.sleep(3)
    try:
        print(f"Estrategia 1: Buscando resultado con content-desc que contenga '{sku}'...")
        resultado_element = driver.find_element(AppiumBy.XPATH, f"//*[contains(@content-desc, '{sku}')]")
        print("✅ Resultado encontrado por content-desc")
    except NoSuchElementException:
        print(f"❌ No encontrado. Estrategia 2: Buscando con atributo 'text' que contenga '{sku}'...")
        try:
            resultado_element = driver.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{sku}')]")
            print("✅ Resultado encontrado por atributo 'text'")
        except NoSuchElementException:
            pytest.fail(f"No se pudo encontrar el resultado para el SKU '{sku}'.")

    print("Haciendo click en el resultado encontrado...")
    resultado_element.click()
    time.sleep(3)


def seleccionar_primera_tarjeta_producto(driver):
    """Hace click en la primera tarjeta de producto que encuentra en pantalla."""
    print("\n--- ACCIÓN: Click en la primera tarjeta de producto ---")
    print("Esperando a que carguen las tarjetas de producto...")
    time.sleep(3)
    try:
        print("Buscando todas las tarjetas de producto (ImageViews clickeables)...")
        tarjetas = driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true']")
        assert len(tarjetas) > 0, "No se encontraron tarjetas de producto."

        print(f"✅ Se encontraron {len(tarjetas)} tarjetas. Seleccionando la primera.")
        primera_tarjeta = tarjetas[0]
        print("Haciendo click en la primera tarjeta...")
        primera_tarjeta.click()
        time.sleep(3)
    except (NoSuchElementException, AssertionError) as e:
        pytest.fail(f"Fallo al intentar seleccionar la primera tarjeta de producto: {e}")
