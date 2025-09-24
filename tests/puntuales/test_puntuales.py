import time

import pytest

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav
)
from tests.ventas.acciones.acciones_carrito import abrir_carrito


class test_puntuales:
    @pytest.mark.xray("APPTEST-****")
    def test_carrito(self, driver, video_recorder):
        try:
            # Paso 1: Realizar la pulsación larga en la tarjeta
            realizar_long_press_en_tarjeta_cliente(driver)
            print("Paso 1 completado: Long press realizado.")

            # Opcional: Pausa breve para observar el estado de selección
            time.sleep(1)

            # Paso 2: Pulsar el botón central. En este punto, es normal que la
            # tarjeta del paso 1 se deseleccione.
            pulsar_boton_central_nav(driver)
            print("Paso 2 completado: Botón central de navegación pulsado.")

            # Aquí podrías añadir una aserción para verificar que estás en la
            # pantalla correcta después de pulsar el botón del carrito.
            print("✅ TEST PASADO: La secuencia de acciones se ejecutó sin errores.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")