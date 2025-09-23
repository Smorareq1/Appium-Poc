import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# Importar acciones reutilizables existentes
from tests.ventas.acciones.acciones_producto import ingresar_cantidad_producto, hacer_scroll_hacia_abajo, \
    agregar_producto_al_carrito
from tests.ventas.acciones.acciones_carrito import abrir_carrito, click_ok


def buscar_producto(driver, nombre_producto, max_swipes=6):
    """
    Busca un producto específico en la vista actual, haciendo swipes si es necesario.

    Args:
        driver: WebDriver de Appium
        nombre_producto: Nombre del producto a buscar
        max_swipes: Número máximo de swipes a realizar

    Returns:
        WebElement del producto encontrado

    Raises:
        Exception si no se encuentra el producto
    """
    print(f"🔍 Buscando producto {nombre_producto}...")

    # Intentar encontrar el producto por content-desc primero
    try:
        producto_element = driver.find_element(
            AppiumBy.XPATH,
            f"//*[contains(@content-desc,'{nombre_producto}')]"
        )
        print(f"✅ {nombre_producto} encontrado por content-desc.")
        return producto_element
    except NoSuchElementException:
        print("... no encontrado por content-desc, intentando por texto.")

    # Intentar por texto
    try:
        producto_element = driver.find_element(
            AppiumBy.XPATH,
            f"//*[contains(@text,'{nombre_producto}')]"
        )
        print(f"✅ {nombre_producto} encontrado por text.")
        return producto_element
    except NoSuchElementException:
        print("... no encontrado en la vista actual.")

    # Si no se encuentra, hacer swipes para buscarlo
    print(f"🔄 Haciendo swipes para buscar {nombre_producto}...")
    size = driver.get_window_size()
    x = int(size['width'] / 2)
    start_y = int(size['height'] * 0.70)
    end_y = int(size['height'] * 0.30)

    for i in range(max_swipes):
        driver.swipe(x, start_y, x, end_y, 400)
        time.sleep(0.5)
        print(f"   Swipe {i + 1}/{max_swipes}")

        try:
            producto_element = driver.find_element(
                AppiumBy.XPATH,
                f"//*[contains(@content-desc,'{nombre_producto}')]"
            )
            print(f"✅ {nombre_producto} encontrado después de swipe {i + 1}")
            return producto_element
        except NoSuchElementException:
            continue

    # Si después de todos los swipes no se encuentra
    raise Exception(f"❌ No se encontró producto {nombre_producto} después de {max_swipes} swipes.")


def abrir_producto(driver, producto_element):
    """
    Abre un producto haciendo clic en su elemento.

    Args:
        driver: WebDriver de Appium
        producto_element: WebElement del producto a abrir
    """
    print("📱 Abriendo producto...")
    producto_element.click()
    time.sleep(2)
    print("✅ Producto abierto.")


def procesar_checkout_carrito(driver):
    """
    Procesa el checkout del carrito: abre el carrito, acepta el pedido y confirma.

    Args:
        driver: WebDriver de Appium
    """
    # Abrir carrito con cheque verde
    abrir_carrito(driver)
    print("✅ Carrito abierto con cheque verde.")

    # Aceptar pedido con cheque verde (reutilizamos la misma función)
    abrir_carrito(driver)
    print("✅ Pedido aceptado con cheque verde.")

    # Confirmar pedido
    click_ok(driver)
    print("✅ Pedido confirmado.")


def ejecutar_venta_directa_completa(driver, nombre_producto, cantidad):
    """
    Ejecuta el flujo completo de venta directa.

    Args:
        driver: WebDriver de Appium
        nombre_producto: Nombre del producto a vender
        cantidad: Cantidad del producto a agregar

    Raises:
        Exception si algún paso del flujo falla
    """
    print(f"\n=== EJECUTANDO VENTA DIRECTA: {nombre_producto} x{cantidad} ===")

    try:
        # 1. Buscar producto
        producto_element = buscar_producto(driver, nombre_producto)

        # 2. Abrir producto
        abrir_producto(driver, producto_element)

        # 3. Ingresar cantidad
        ingresar_cantidad_producto(driver, cantidad)

        # 4. Hacer scroll hacia abajo
        hacer_scroll_hacia_abajo(driver)

        # 5. Agregar producto al carrito
        agregar_producto_al_carrito(driver)
        print("✅ Producto agregado al carrito.")

        # 6. Procesar checkout completo
        procesar_checkout_carrito(driver)

        print(f"🎉 VENTA DIRECTA COMPLETADA EXITOSAMENTE - {nombre_producto.upper()} {cantidad} UNIDADES VENDIDO")

    except Exception as e:
        raise Exception(f"❌ VENTA DIRECTA FALLÓ: {e}")


def ejecutar_venta_directa_cloro_5_unidades(driver):
    """
    Función específica para el caso de prueba de Cloro 5 unidades.
    Wrapper de la función general para mantener compatibilidad.

    Args:
        driver: WebDriver de Appium
    """
    ejecutar_venta_directa_completa(driver, "Cloro", 5)