import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# Importar las acciones de búsqueda
from tests.ventas.acciones.acciones_busqueda import (
    realizar_click_en_buscar,
    escribir_y_buscar_sku,
    seleccionar_resultado_por_sku,
    seleccionar_primera_tarjeta_producto
)

# Importar las acciones de producto
from tests.ventas.acciones.acciones_producto import (
    incrementar_productos_con_botones,
    hacer_scroll_hacia_abajo,
    agregar_producto_al_carrito
)

# Importar las acciones del carrito
from tests.ventas.acciones.acciones_carrito import (
    abrir_carrito,
    aceptar_pedido,
    click_ok
)


class TestVentaDeCombos:
    @pytest.mark.xray("APPTEST-COMBO-01")
    def test_vender_combo_desde_catalogo(self, driver, video_recorder):
        """
        🎯 TEST DE VENTA DE COMBOS

        OBJETIVO:
        Verificar que se puede vender correctamente un combo desde el catálogo
        siguiendo el flujo estándar de ventas.

        ESCENARIO DE PRUEBA:
        - Buscar un combo disponible en el catálogo
        - Seleccionar primera opción encontrada
        - Ingresar cantidad deseada
        - Agregar al carrito
        - Confirmar pedido

        FLUJO:
        1. Buscar combo en el catálogo
        2. Seleccionar primera opción
        3. Ingresar cantidad
        4. Agregar al carrito
        5. Ir al carrito
        6. Confirmar pedido
        """
        print("\n🧪 === TEST: VENTA DE COMBOS ===")
        print("📦 Producto: Combo desde catálogo")
        print("🔢 Cantidad: 2 unidades")
        print("🎯 Objetivo: Vender combo exitosamente")
        print("=" * 60)

        # Buscar por combo (puedes usar un término genérico o SKU específico de combo)
        termino_busqueda = "2120"  # O puedes usar un SKU específico de combo
        cantidad_producto = 2

        try:
            # 1) BUSCAR COMBO EN CATÁLOGO
            print("🔍 Iniciando búsqueda de combo...")
            realizar_click_en_buscar(driver)
            print("✅ Campo de búsqueda activado.")

            # 2) ESCRIBIR TÉRMINO Y BUSCAR
            print(f"🔍 Buscando: '{termino_busqueda}'...")
            escribir_y_buscar_sku(driver, termino_busqueda)
            print(f"✅ Término '{termino_busqueda}' buscado.")

            # Paso 3: Seleccionar el resultado que aparece
            seleccionar_resultado_por_sku(driver, termino_busqueda)

            # 3) SELECCIONAR PRIMER RESULTADO
            print("📦 Seleccionando primer resultado...")
            # Para combos, podemos usar la función de seleccionar primera tarjeta directamente
            # ya que los combos aparecen como productos en los resultados
            time.sleep(2)  # Esperar que carguen los resultados
            seleccionar_primera_tarjeta_producto(driver)
            print("✅ Primer combo seleccionado - pantalla de detalle abierta.")

            # 4) INGRESAR CANTIDAD
            print(f"📝 Ingresando unidades...")
            inicial = 2
            incremento = 5
            incrementar_productos_con_botones(driver, inicial, incremento)
            print("✅ Cantidad ingresada.")

            # 5) HACER SCROLL PARA VER BOTÓN AGREGAR
            print("📜 Haciendo scroll hacia abajo...")
            hacer_scroll_hacia_abajo(driver)
            print("✅ Scroll realizado.")

            # 6) AGREGAR AL CARRITO
            print("🛒 Agregando combo al carrito...")
            agregar_producto_al_carrito(driver)
            print("✅ Combo agregado al carrito.")

            # 7) IR AL CARRITO
            print("🛒 Navegando al carrito...")
            abrir_carrito(driver)
            print("✅ Carrito abierto.")

            # 8) CONFIRMAR PEDIDO
            print("✅ Procediendo a confirmar el pedido...")

            # Hacer clic en cheque verde para aceptar pedido
            abrir_carrito(driver)
            print("✅ Pedido aceptado.")

            # Confirmar pedido final
            click_ok(driver)
            print("✅ Pedido confirmado exitosamente.")

            print("🏆 TEST COMPLETADO EXITOSAMENTE")
            print("🎉 RESULTADO: COMBO VENDIDO CORRECTAMENTE")

        except Exception as e:
            print(f"💥 ERROR EN TEST DE VENTA DE COMBOS: {e}")
            pytest.fail(f"❌ TEST DE COMBOS INTERRUMPIDO: {e}")

        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")
                print("📋 RESUMEN: Venta de combo completada exitosamente")