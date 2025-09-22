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
    agregar_producto_al_carrito
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
        sku_a_vender = "120800280"

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
        cantidad_a_ingresar = 200

        try:
            # Paso 1: Ingresar la cantidad deseada
            ingresar_cantidad_producto(driver, cantidad_a_ingresar)

            # Paso 2: Hacer scroll para ver más opciones
            hacer_scroll_hacia_abajo(driver)

            # Paso 3: Agregar el producto al carrito
            agregar_producto_al_carrito(driver)

            print("\n✅ TEST COMPLETADO: Producto configurado exitosamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al configurar o agregar el producto: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

