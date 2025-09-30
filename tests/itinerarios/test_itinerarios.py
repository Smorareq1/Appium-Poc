import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tests.itinerarios.acciones_itinerarios import (
    spin_semana,
    buscar_primer_dia_con_clientes,
    hacer_click_pendientes,
    hacer_click_primer_cliente,
    realizar_check_in_si_pendiente,
    realizar_venta_directa_si_pendiente,
    realizar_check_out_si_pendiente,
    hacer_click_en_atras
)

class test_itinerarios:
    @pytest.mark.xray("ATC-18")
    def test_itinerarios_button(self, driver, video_recorder):
        print("\n=== TEST: Click en botón Itinerarios ===")
        try:
            itinerarios_button = driver.find_element("xpath", "//*[@content-desc='Itinerarios']")
            itinerarios_button.click()
            assert itinerarios_button is not None, "No se pudo encontrar el botón 'Itinerarios'"

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-19")
    #Agregado
    def test_click_semana_anterior_y_verificar_alerta(self, driver, video_recorder):
        print("\n=== TEST: Click semana anterior y verificar mensaje de advertencia ===")
        try:
            wait = WebDriverWait(driver, 10)

            lunes_ref_xpath = "//*[@content-desc='L\n22']"
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lunes_ref_xpath)))
            print("✅ Calendario visible")

            boton_anterior_xpath = f"{lunes_ref_xpath}/preceding-sibling::android.widget.Button"
            boton_semana_anterior = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, boton_anterior_xpath))
            )
            boton_semana_anterior.click()
            print("✅ Clic en semana anterior realizado")

            mensaje_xpath = "//*[@content-desc='No es posible visualizar semanas pasadas']"
            mensaje_advertencia = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mensaje_xpath))
            )

            assert mensaje_advertencia is not None, "No se encontró el mensaje de advertencia"
            print("✅ Mensaje de advertencia verificado correctamente")

        except TimeoutException:
            pytest.fail("Timeout: No se encontró el calendario, botón o mensaje de advertencia")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video de evidencia guardado en: {video_path}")



    @pytest.mark.xray("ATC-20")
    def test_actividades_programadas(self, driver, video_recorder):
        print("\n=== TEST: Buscar cliente en itinerario (Lógica Refactorizada) ===")
        try:
            wait = WebDriverWait(driver, 10)

            dia_con_clientes = buscar_primer_dia_con_clientes(driver)

            if dia_con_clientes:
                print(f"✅ Se encontraron clientes en día {dia_con_clientes}")
                hacer_click_pendientes(driver, wait)
                hacer_click_primer_cliente(driver)

                check_in_realizado = realizar_check_in_si_pendiente(driver)
                if check_in_realizado:
                    print("✅ El proceso de Check-in se ha completado en este test.")
                else:
                    print("Se omite el flujo de Check-in ya que no estaba pendiente o ya se había completado.")

                venta_realizada = realizar_venta_directa_si_pendiente(driver)
                if venta_realizada:
                    print("✅ El proceso de Venta se ha completado en este test.")
                else:
                    print("Se omite el flujo de Venta ya que no estaba pendiente o ya se había completado.")

                check_out_realizado = realizar_check_out_si_pendiente(driver)
                if check_out_realizado:
                    print("✅ El proceso de Check-out se ha completado en este test.")
                else:
                    print("Se omite el flujo de Check-out ya que no estaba pendiente o ya se había completado.")

                acciones_realizadas = []
                if check_in_realizado:
                    acciones_realizadas.append("Check-in")
                if venta_realizada:
                    acciones_realizadas.append("Venta")
                if check_out_realizado:
                    acciones_realizadas.append("Check-out")

                if acciones_realizadas:
                    print(f"Test completado exitosamente. Acciones realizadas: {', '.join(acciones_realizadas)}")
                else:
                    print("Test completado. No había tareas pendientes para realizar.")

                hacer_click_en_atras(driver)

            else:
                pytest.fail("No hay clientes disponibles en la semana")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ con una excepción inesperada: {str(e)}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_filtrar_por_fecha(self, driver, video_recorder):
        print("\n=== TEST: Spin en días de la semana ===")
        try:
            spin_semana(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_filtrar_por_estado(self, driver, video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_crear_actividad(self, driver, video_recorder):
        print("\n=== TEST: Crear actividad desde itinerario ===")
        try:
            pytest.fail("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_no_se_puede_realizar(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_reactivar_actividades(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_check_in(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_log_actividad(self,driver, video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_venta(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    #Agregado
    def test_check_out(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_verificar_estados(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-")
    def test_comision(self,driver,video_recorder):
        try:
            pytest.skip("No se ha implementado la funcionalidad")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-41")
    #Agregado
    def test_click_semana_siguiente_6_veces_y_verificar_alerta(self, driver, video_recorder):
        print("\n=== TEST: Click semana siguiente 6 veces y verificar mensaje de advertencia ===")
        try:
            wait = WebDriverWait(driver, 10)
            wait_rapido = WebDriverWait(driver, 2)

            domingo_ref_xpath = "//*[starts-with(@content-desc, 'D\n')]"
            wait.until(EC.presence_of_element_located((AppiumBy.XPATH, domingo_ref_xpath)))
            print("✅ Calendario visible")

            boton_siguiente_xpath = f"{domingo_ref_xpath}/following-sibling::android.widget.Button"

            for i in range(1, 7):
                print(f"Haciendo clic #{i} en semana siguiente...")

                boton_semana_siguiente = wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, boton_siguiente_xpath))
                )
                boton_semana_siguiente.click()

                if i == 6:
                    print("Capturando mensaje de advertencia rápidamente...")
                    mensaje_xpath = "//*[@content-desc='No es posible visualizar más de 5 semanas futuras']"
                    try:
                        mensaje_advertencia = wait_rapido.until(
                            EC.presence_of_element_located((AppiumBy.XPATH, mensaje_xpath))
                        )
                        assert mensaje_advertencia is not None, "No se encontró el mensaje de advertencia"
                        print("✅ Mensaje de advertencia capturado y verificado correctamente")
                    except TimeoutException:
                        pytest.fail("No se pudo capturar el mensaje de advertencia a tiempo (desapareció muy rápido)")
                else:
                    time.sleep(0.5)
                    print(f"✅ Clic #{i} realizado")

            print("✅ Se completaron los 6 clics en semana siguiente")

        except TimeoutException:
            pytest.fail("Timeout: No se encontró el calendario, botón o mensaje de advertencia")
        except Exception as e:
            pytest.fail(f"TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"Video de evidencia guardado en: {video_path}")
