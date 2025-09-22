import pytest

# Importamos las acciones de búsqueda
from tests.ventas.acciones.acciones_busqueda import (
    realizar_click_en_buscar,
    escribir_y_buscar_sku,
    seleccionar_resultado_por_sku,
    seleccionar_primera_tarjeta_producto
)

# Importamos las nuevas acciones de producto
from tests.ventas.acciones.acciones_producto import (
    ingresar_cantidad_producto,
    hacer_scroll_hacia_abajo,
    obtener_unidades_a_bonificar,
    agregar_producto_al_carrito
)

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_carrito import (
    abrir_carrito,
    hacer_swipe_en_resumen_compra,
    hacer_clic_en_descuento_puntual
)

# Importamos las acciones del descuento puntual
from tests.ventas.acciones.acciones_venta_putual import (
    obtener_total_pedido,
    ingresar_descuento_y_confirmar,
    click_boton_marca,
    click_monto_especifico_marca_producto,
    click_boton_producto,
)

class Test_Venta_Completa:

    @pytest.mark.xray("APPTEST-****")
    def test_flujo_busqueda_y_seleccion(self, driver, video_recorder):
        """
        Este test ejecuta la primera parte del flujo: buscar un producto por SKU
        y seleccionarlo para ver su detalle.
        """
        print("\n=== INICIO TEST: Flujo de Búsqueda y Selección ===")

        # Parámetro configurable para este flujo
        sku_a_vender = "120800710"

        try:
            # --- Flujo de Búsqueda ---
            # Paso 1: Hacer click en el botón de buscar
            realizar_click_en_buscar(driver)

            # Paso 2: Escribir el SKU en el campo de búsqueda
            escribir_y_buscar_sku(driver, sku_a_vender)

            # Paso 3: Seleccionar el resultado que aparece
            seleccionar_resultado_por_sku(driver, sku_a_vender)

            # Paso 4: Seleccionar la primera tarjeta del producto encontrado
            seleccionar_primera_tarjeta_producto(driver)

            print("\n✅ TEST COMPLETADO: Flujo de Búsqueda y Selección finalizado exitosamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ durante el flujo de búsqueda: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la búsqueda guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_configurar_y_agregar_producto(self, driver, video_recorder):
        """
        Este test ejecuta la segunda parte del flujo: configurar la cantidad
        de un producto y agregarlo al carrito.
        NOTA: Este test depende de que el anterior haya finalizado correctamente.
        """
        print("\n=== INICIO TEST: Configurar y Agregar Producto al Carrito ===")

        # Parámetro configurable para este flujo
        cantidad_a_ingresar = 100

        try:
            # Paso 1: Ingresar la cantidad deseada
            ingresar_cantidad_producto(driver, cantidad_a_ingresar)

            # Paso 2: Validar informacion
            unidades_bonificar = obtener_unidades_a_bonificar(driver)
            print(f"Unidades a bonificar según la app: {unidades_bonificar}")
            if unidades_bonificar != 10:
                pytest.fail(
                    f"La cantidad esperada para {cantidad_a_ingresar} es 10, "
                    f"pero la app mostró {unidades_bonificar}"
                )

            # Paso 3: Hacer scroll para ver más opciones
            hacer_scroll_hacia_abajo(driver)

            # Paso 4: Agregar el producto al carrito
            agregar_producto_al_carrito(driver)

            print("\n✅ TEST COMPLETADO: Producto configurado exitosamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al configurar o agregar el producto: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_carrito_inicial(self, driver, video_recorder):
        """
            Este test ejecuta la tercera parte del flujo: carrito
            NOTA: Este test depende de que el anterior haya finalizado correctamente.
        """
        print("\n=== INICIO TEST: Validaciones carrito ===")

        try:
            abrir_carrito(driver)
            hacer_swipe_en_resumen_compra(driver)
            hacer_clic_en_descuento_puntual(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al estar dentro del carrito {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_descuento_puntual(self, driver, video_recorder):
        """
            Este test ejecuta la cuarta parte del flujo: descuento puntual
            NOTA: Este test depende de que el anterior haya finalizado correctamente.
        """
        print("\n=== INICIO TEST: Validaciones descuento puntual ===")

        try:
            # Descuento sobre el total
            monto = 5
            total = obtener_total_pedido(driver)
            print(f"Total del pedido obtenido: {total}")
            ingresar_descuento_y_confirmar(driver, monto)
            descuento = obtener_total_pedido(driver)
            print(f"Total del pedido con descuento aplicado: {descuento}")

            esperado = total * ((100 - monto) / 100)
            esperado = round(esperado, 2)

            if descuento != esperado:
                pytest.fail(
                    f"La cantidad esperada para {descuento} no coincide con {esperado}"
                )

            # Descuento sobre marca
            click_boton_marca(driver)
            click_monto_especifico_marca_producto(driver)

            monto = 1
            total = obtener_total_pedido(driver)
            print(f"Total del pedido obtenido: {total}")
            ingresar_descuento_y_confirmar(driver, monto)
            descuento = obtener_total_pedido(driver)
            print(f"Total del pedido con descuento aplicado: {descuento}")
            if descuento != (total - monto):
                pytest.fail(
                    f"La cantidad esperada para {descuento} no es correcta"
                )

            #Descuento sobre producto
            click_boton_producto(driver)
            click_monto_especifico_marca_producto(driver)
            monto = 2
            total = obtener_total_pedido(driver)
            print(f"Total del pedido obtenido: {total}")
            ingresar_descuento_y_confirmar(driver, monto)
            descuento = obtener_total_pedido(driver)
            print(f"Total del pedido con descuento aplicado: {descuento}")
            if descuento != (total - monto):
                pytest.fail(
                    f"La cantidad esperada para {descuento} no es correcta"
                )
            # Abrir el carrito
            abrir_carrito(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al estar dentro de bonificacion puntual {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("APPTEST-****")
    def test_validar_carrito_final(self, driver, video_recorder):
        """
            Este test ejecuta la quinta parte del flujo: validar carrito final
            NOTA: Este test depende de que el anterior haya finalizado correctamente.
        """
        print("\n=== INICIO TEST: Validaciones carrito final ===")

        try:
            pass

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al estar dentro del carrito {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")