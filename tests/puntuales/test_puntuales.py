import pytest

# Importamos las acciones del carrito
from tests.ventas.acciones.acciones_venta_putual import (
    obtener_total_pedido,
    ingresar_descuento_y_confirmar,
    click_boton_marca,
    click_monto_especifico_marca_producto,
    click_boton_producto,
)

class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            # Descuento sobre producto
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

        except Exception as e:
            pytest.fail(f"TEST FALLÓ al estar dentro del carrito {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")