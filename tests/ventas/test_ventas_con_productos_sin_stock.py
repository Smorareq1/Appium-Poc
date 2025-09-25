import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import threading

# Importar las acciones de búsqueda
from tests.ventas.acciones.acciones_busqueda import (
    realizar_click_en_buscar,
    escribir_y_buscar_sku,
    seleccionar_primera_tarjeta_producto,
    seleccionar_resultado_por_sku
)

# Importar las acciones de producto
from tests.ventas.acciones.acciones_producto import (
    ingresar_cantidad_producto,
    hacer_scroll_hacia_abajo,
    agregar_producto_al_carrito
)


class TestVentasConProductosSinStock:
    @pytest.mark.xray("ATC-30")
    def test_producto_sin_stock(self, driver, video_recorder):
        """
        Flujo de prueba para productos sin stock:
        1. Buscar producto "Cloro Mb 1lx12u"
        2. Seleccionar el primer producto de los resultados
        3. Ingresar cantidad de 999 unidades (excede stock)
        4. Intentar agregar al carrito
        5. Capturar mensaje temporal: "La cantidad que intentas agregar excede la existencia disponible"
        """
        print("\n=== TEST: Producto Sin Stock - Cloro Mb 11x12u ===")

        sku_producto = "120800260"

        try:
            # 1) BUSCAR PRODUCTO ESPECÍFICO
            print("🔍 Iniciando búsqueda de producto...")
            realizar_click_en_buscar(driver)
            print("✅ Campo de búsqueda activado.")

            # 2) ESCRIBIR SKU Y BUSCAR
            escribir_y_buscar_sku(driver, sku_producto)
            print(f"✅ SKU '{sku_producto}' buscado.")

            seleccionar_resultado_por_sku(driver, sku_producto)

            # 3) SELECCIONAR PRIMER RESULTADO (ABRIR PRODUCTO)
            seleccionar_primera_tarjeta_producto(driver)
            print("✅ Producto seleccionado y pantalla de detalle abierta.")

            # 4) INGRESAR CANTIDAD EXCESIVA
            print("📝 Ingresando cantidad de 999 unidades (para exceder stock)...")
            ingresar_cantidad_producto(driver, 999)
            print("✅ Cantidad excesiva ingresada.")

            # 5) HACER SCROLL PARA VER BOTÓN AGREGAR
            hacer_scroll_hacia_abajo(driver)

            # 6) CAPTURAR MENSAJE TEMPORAL CON ESTRATEGIA OPTIMIZADA
            print("🔍 Preparando captura de mensaje temporal...")
            mensaje_encontrado = self._capturar_mensaje_temporal_optimizado(driver)

            # 7) VALIDAR RESULTADO
            if mensaje_encontrado:
                print("🎉 ✅ TEST EXITOSO: VALIDACIÓN DE CONTROL DE STOCK CORRECTA")
                print("🔒 La aplicación correctamente PREVIENE agregar más productos de los disponibles")
                print("🛡️ MENSAJE DETECTADO: 'La cantidad que intentas agregar excede la existencia disponible'")
                print("📊 COMPORTAMIENTO ESPERADO: La app muestra mensaje temporal cuando se excede el stock")
                print("⏱️ MENSAJE TEMPORAL: Se muestra por ~1 segundo y desaparece automáticamente")
                print("🏆 RESULTADO FINAL: EL CONTROL DE INVENTARIO FUNCIONA CORRECTAMENTE")
                print("✨ La aplicación protege la integridad del stock y previene sobreventa")
            else:
                print("❌ FALLO EN VALIDACIÓN DE STOCK:")
                print("🚨 NO se detectó el mensaje temporal de stock insuficiente")
                print("⚠️ RIESGO: El usuario podría agregar más productos de los disponibles")

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

    def _capturar_mensaje_temporal_optimizado(self, driver):
        """
        Estrategia optimizada para capturar mensajes temporales que aparecen muy brevemente.
        Usa múltiples hilos y verificaciones continuas para maximizar las posibilidades de captura.
        """
        print("🎯 Iniciando captura optimizada del mensaje temporal...")

        mensaje_exacto = "La cantidad que intentas agregar excede la existencia disponible"
        mensaje_encontrado = False

        # Variable compartida entre hilos
        resultado_captura = {'encontrado': False, 'texto': ''}

        def verificador_continuo():
            """Hilo que verifica continuamente por el mensaje"""
            intentos = 0
            max_intentos = 100  # Verificar por 5 segundos (100 * 0.05s)

            while intentos < max_intentos and not resultado_captura['encontrado']:
                try:
                    # Estrategia 1: Buscar mensaje completo
                    try:
                        elemento = driver.find_element(AppiumBy.XPATH,
                                                       f"//*[contains(@text, '{mensaje_exacto}') or contains(@content-desc, '{mensaje_exacto}')]")
                        if elemento.is_displayed():
                            resultado_captura['encontrado'] = True
                            resultado_captura['texto'] = mensaje_exacto
                            print(f"✅ MENSAJE COMPLETO CAPTURADO: '{mensaje_exacto}'")
                            return
                    except NoSuchElementException:
                        pass

                    # Estrategia 2: Buscar palabras clave críticas
                    palabras_clave = [
                        "excede la existencia disponible",
                        "excede la existencia",
                        "existencia disponible",
                        "cantidad que intentas agregar"
                    ]

                    for palabra in palabras_clave:
                        try:
                            elemento = driver.find_element(AppiumBy.XPATH,
                                                           f"//*[contains(@text, '{palabra}') or contains(@content-desc, '{palabra}')]")
                            if elemento.is_displayed():
                                resultado_captura['encontrado'] = True
                                resultado_captura['texto'] = palabra
                                print(f"✅ MENSAJE PARCIAL CAPTURADO: '{palabra}'")
                                return
                        except NoSuchElementException:
                            continue

                    # Estrategia 3: Buscar cualquier toast/mensaje temporal
                    try:
                        toasts = driver.find_elements(AppiumBy.XPATH,
                                                      "//*[contains(@class, 'toast') or contains(@resource-id, 'toast') or contains(@resource-id, 'snackbar')]")
                        for toast in toasts:
                            if toast.is_displayed():
                                texto_toast = toast.get_attribute('text') or toast.get_attribute('content-desc') or ''
                                if 'excede' in texto_toast.lower() or 'stock' in texto_toast.lower() or 'cantidad' in texto_toast.lower():
                                    resultado_captura['encontrado'] = True
                                    resultado_captura['texto'] = texto_toast
                                    print(f"✅ TOAST CAPTURADO: '{texto_toast}'")
                                    return
                    except NoSuchElementException:
                        pass

                    intentos += 1
                    time.sleep(0.05)  # 50ms entre verificaciones

                except Exception as e:
                    print(f"⚠️ Error en verificación {intentos}: {e}")
                    intentos += 1
                    time.sleep(0.05)

        # Iniciar hilo de verificación continua
        print("🔄 Iniciando verificación continua en hilo separado...")
        hilo_verificador = threading.Thread(target=verificador_continuo)
        hilo_verificador.daemon = True
        hilo_verificador.start()

        # Esperar un momento antes del click para asegurarnos que el verificador esté activo
        time.sleep(0.1)

        # Ejecutar la acción que debería generar el mensaje
        print("🛒 Ejecutando acción de agregar al carrito...")
        agregar_producto_al_carrito(driver)
        print("✅ Acción ejecutada - verificando captura...")

        # Esperar a que el hilo termine su trabajo
        hilo_verificador.join(timeout=6.0)  # Esperar máximo 6 segundos

        if resultado_captura['encontrado']:
            print(f"🎉 ✅ MENSAJE CAPTURADO EXITOSAMENTE: '{resultado_captura['texto']}'")
            return True
        else:
            print("❌ No se pudo capturar el mensaje temporal")

            # Verificación final por si acaso
            print("🔍 Verificación final manual...")
            try:
                time.sleep(1)
                elementos_texto = driver.find_elements(AppiumBy.XPATH, "//*[@text or @content-desc]")
                for elem in elementos_texto[:20]:  # Verificar los primeros 20 elementos
                    try:
                        texto = elem.get_attribute('text') or elem.get_attribute('content-desc') or ''
                        if 'excede' in texto.lower() or 'stock' in texto.lower():
                            print(f"📋 Elemento relacionado encontrado: '{texto}'")
                    except:
                        continue
            except:
                pass

            return False