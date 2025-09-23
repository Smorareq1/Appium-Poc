import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# Importar SOLO las acciones que necesitas
from tests.ventas.acciones.acciones_producto import ingresar_cantidad_producto, hacer_scroll_hacia_abajo, \
    agregar_producto_al_carrito
from tests.ventas.acciones.acciones_carrito import abrir_carrito, aceptar_pedido, click_ok


class TestVentaDirecta:
    @pytest.mark.xray("APPTEST-CLORO-5U")
    def test_flujo_cloro_5_checkout(self, driver, video_recorder):
        """
        Flujo SIMPLE de venta directa - como test_venta_completa pero más básico
        """
        print("\n=== TEST: Venta Directa SIMPLE ===")
        try:
            # 1) BUSCAR PRODUCTO CLORO
            print("🔍 Buscando producto Cloro...")
            cloro_element = None
            try:
                cloro_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc,'Cloro')]")
                print("✅ Cloro encontrado por content-desc.")
            except NoSuchElementException:
                print("... no encontrado por content-desc, intentando por texto.")
                try:
                    cloro_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Cloro')]")
                    print("✅ Cloro encontrado por text.")
                except NoSuchElementException:
                    print("... no encontrado en la vista actual.")

            if not cloro_element:
                print("🔄 Haciendo swipes para buscar Cloro...")
                size = driver.get_window_size()
                x = int(size['width'] / 2)
                start_y = int(size['height'] * 0.70)
                end_y = int(size['height'] * 0.30)

                for i in range(6):
                    driver.swipe(x, start_y, x, end_y, 400)
                    time.sleep(0.5)
                    print(f"   Swipe {i + 1}/6")
                    try:
                        cloro_element = driver.find_element(AppiumBy.XPATH, "//*[contains(@content-desc,'Cloro')]")
                        print(f"✅ Cloro encontrado después de swipe {i + 1}")
                        break
                    except NoSuchElementException:
                        continue

            if not cloro_element:
                pytest.fail("❌ No se encontró producto Cloro después de varios swipes.")

            # 2) ABRIR PRODUCTO CLORO
            print("📱 Abriendo producto Cloro...")
            cloro_element.click()
            time.sleep(2)
            print("✅ Producto Cloro abierto.")

            # 3) INGRESAR CANTIDAD (usando función reutilizable)
            ingresar_cantidad_producto(driver, 5)

            # 4) HACER SCROLL (usando función reutilizable)
            hacer_scroll_hacia_abajo(driver)

            # 5) AGREGAR AL CARRITO (usando función reutilizable)
            agregar_producto_al_carrito(driver)
            print("✅ Producto agregado al carrito.")

            # 6) HACER CLIC EN CHEQUE VERDE PARA ABRIR CARRITO (usando función reutilizable)
            abrir_carrito(driver)
            print("✅ Carrito abierto con cheque verde.")

            # 7) HACER CLIC EN CHEQUE VERDE PARA ACEPTAR PEDIDO (usando función reutilizable)
            abrir_carrito(driver)  # Misma función, diferente contexto
            print("✅ Pedido aceptado con cheque verde.")

            # 8) CONFIRMAR PEDIDO (usando función reutilizable)
            click_ok(driver)
            print("✅ Pedido confirmado.")

            print("🎉 TEST COMPLETADO EXITOSAMENTE - CLORO 5 UNIDADES VENDIDO")

        except Exception as e:
            pytest.fail(f"❌ TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video: {video_path}")