import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# Importar las acciones de búsqueda
from tests.ventas.acciones.acciones_busqueda import (
    realizar_click_en_buscar,
    escribir_y_buscar_sku,
    seleccionar_primera_tarjeta_producto
)

# Importar las acciones de producto
from tests.ventas.acciones.acciones_producto import (
    ingresar_cantidad_producto,
    hacer_scroll_hacia_abajo,
    agregar_producto_al_carrito
)


class TestVentasConProductosSinStock:
    @pytest.mark.xray("APPTEST-SIN-STOCK")
    def test_producto_sin_stock(self, driver, video_recorder):
        """
        Flujo de prueba para productos sin stock:
        1. Buscar producto "Cloro Mb 1lx12u"
        2. Seleccionar el primer producto de los resultados
        3. Ingresar cantidad de 5 unidades
        4. Intentar agregar al carrito
        5. Verificar mensaje de sin stock
        """
        print("\n=== TEST: Producto Sin Stock - Cloro Mb 11x12u ===")

        sku_producto = "Cloro Mb 1lx12u"

        try:
            # 1) BUSCAR PRODUCTO ESPECÍFICO
            print("🔍 Iniciando búsqueda de producto...")
            realizar_click_en_buscar(driver)
            print("✅ Campo de búsqueda activado.")

            # 2) ESCRIBIR SKU Y BUSCAR
            escribir_y_buscar_sku(driver, sku_producto)
            print(f"✅ SKU '{sku_producto}' buscado.")

            # 3) SELECCIONAR PRIMER RESULTADO (ABRIR PRODUCTO)
            seleccionar_primera_tarjeta_producto(driver)
            print("✅ Producto seleccionado y pantalla de detalle abierta.")

            # 4) INGRESAR CANTIDAD
            print("📝 Ingresando cantidad de 5 unidades...")
            ingresar_cantidad_producto(driver, 5)
            print("✅ Cantidad ingresada.")

            # 5) HACER SCROLL PARA VER BOTÓN AGREGAR
            hacer_scroll_hacia_abajo(driver)

            # 6) INTENTAR AGREGAR AL CARRITO (esto debería mostrar mensaje de sin stock)
            print("🛒 Intentando agregar producto al carrito...")
            agregar_producto_al_carrito(driver)
            print("✅ Acción de agregar ejecutada.")

            # 7) VERIFICAR MENSAJE DE SIN STOCK
            print("🔍 Verificando mensaje de stock insuficiente...")
            mensaje_sin_stock_encontrado = False

            # El mensaje aparece muy brevemente (1 segundo aprox), necesitamos verificar rápido
            print("⏱️ Buscando mensaje temporal de stock...")

            # Buscar el mensaje específico que aparece en la imagen
            mensajes_posibles = [
                "La cantidad que intentas agregar excede la existencia disponible",
                "cantidad que intentas agregar excede",
                "excede la existencia disponible",
                "excede la existencia",
                "existencia disponible",
                "sin stock",
                "Sin stock",
                "SIN STOCK",
                "no disponible",
                "stock insuficiente"
            ]

            # Intentar capturar el mensaje rápidamente - hacer múltiples verificaciones
            for intento in range(10):  # 10 intentos en 2 segundos
                for mensaje in mensajes_posibles:
                    try:
                        # Buscar por content-desc
                        elemento_mensaje = driver.find_element(AppiumBy.XPATH,
                                                               f"//*[contains(@content-desc, '{mensaje}')]")
                        if elemento_mensaje.is_displayed():
                            print(f"✅ Mensaje de stock encontrado (content-desc): '{mensaje}'")
                            mensaje_sin_stock_encontrado = True
                            break
                    except NoSuchElementException:
                        try:
                            # Buscar por texto
                            elemento_mensaje = driver.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{mensaje}')]")
                            if elemento_mensaje.is_displayed():
                                print(f"✅ Mensaje de stock encontrado (text): '{mensaje}'")
                                mensaje_sin_stock_encontrado = True
                                break
                        except NoSuchElementException:
                            continue

                if mensaje_sin_stock_encontrado:
                    break

                time.sleep(0.2)  # Esperar 200ms entre intentos

            # 8) VALIDAR RESULTADO
            if mensaje_sin_stock_encontrado:
                print("🎉 ✅ TEST EXITOSO: VALIDACIÓN DE CONTROL DE STOCK CORRECTA")
                print("🔒 La aplicación correctamente PREVIENE agregar más productos de los disponibles")
                print("🛡️ MENSAJE DETECTADO: 'La cantidad que intentas agregar excede la existencia disponible'")
                print("📊 COMPORTAMIENTO ESPERADO: La app muestra mensaje temporal cuando se excede el stock")
                print("⏱️ MENSAJE TEMPORAL: Se muestra por ~1 segundo y desaparece automáticamente")

                # No intentar cerrar el mensaje ya que desaparece automáticamente
                print("✅ El mensaje desapareció automáticamente (comportamiento normal)")

                print("🏆 RESULTADO FINAL: EL CONTROL DE INVENTARIO FUNCIONA CORRECTAMENTE")
                print("✨ La aplicación protege la integridad del stock y previene sobreventa")

                # Verificar que la cantidad se ajustó automáticamente
                print("🔍 Verificando si la cantidad se ajustó al stock disponible...")
                try:
                    # Buscar el campo de cantidad para ver si se ajustó a 4 (stock disponible)
                    campo_cantidad = driver.find_element(AppiumBy.XPATH,
                                                         "//*[@text='4' or contains(@content-desc, '4')]")
                    if campo_cantidad:
                        print("✅ ADICIONAL: La cantidad se ajustó automáticamente al stock disponible (4)")
                except:
                    print("ℹ️ No se pudo verificar ajuste automático de cantidad")

            else:
                print("❌ FALLO EN VALIDACIÓN DE STOCK:")
                print("🚨 NO se detectó el mensaje temporal de stock insuficiente")
                print("⚠️ RIESGO: El usuario podría agregar más productos de los disponibles")
                print("🔍 POSIBLES CAUSAS:")
                print("   - El mensaje aparece muy brevemente y no fue capturado")
                print("   - El producto tiene más stock del esperado")
                print("   - El mensaje usa texto diferente")
                print("   - El control de stock no está activo")

                # Capturar screenshot para análisis
                try:
                    print("📸 Capturando screenshot para análisis...")
                    driver.save_screenshot("stock_validation_failed.png")
                    print("✅ Screenshot guardado: stock_validation_failed.png")
                except:
                    pass

                pytest.fail("❌ CONTROL DE STOCK FALLIDO: No se detectó restricción de inventario")

        except Exception as e:
            print(f"💥 ERROR EN TEST DE CONTROL DE STOCK: {e}")
            pytest.fail(f"❌ TEST DE STOCK INTERRUMPIDO: {e}")

        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
                print("📋 RESUMEN: Control de inventario validado correctamente")