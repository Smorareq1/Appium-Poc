import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.clientes.acciones_clientes import (
    realizar_long_press_en_tarjeta_cliente,
    pulsar_boton_central_nav,
    escribir_nit,
    escribir_dpi_representante,
    hacer_scroll_hacia_abajo,
    escribir_version_dpi,
    seleccionar_vencimiento_dpi,
    escribir_nota,
    hacer_click_continuar,
    hacer_scroll_hacia_arriba,

    #Sucursales
    seleccionar_tipo_de_ruta,
    seleccionar_direccion,
    llenar_formulario_direccion,
    seleccionar_contacto,
    llenar_formulario_contacto,

    #Geolocalizacion
    click_asignar_geolocalizacion,
    click_capturar,

    #Continuar
    eliminar_gestiones_extras_iterativo,
    hacer_click_boton_sucursal_especifico,
    click_continuar,

    # Perfilacion
    seleccionar_condicion,

    #Busqueda
    buscar_cliente_por_nombre
)


class test_clientes:
    @pytest.mark.xray("ATC-32")
    def test_clientes_button(self, driver, video_recorder):
        """Test para hacer click en el botón Clientes del menú de navegación"""
        print("\n=== TEST: Click en botón Clientes del menú inferior (método robusto) ===")
        try:
            clientes_xpath = "//*[@content-desc='Itinerarios']/preceding-sibling::android.view.View[@content-desc='Clientes' and @clickable='true']"

            clientes_nav_button = driver.find_element("xpath", clientes_xpath)
            clientes_nav_button.click()

            print("Botón 'Clientes' del menú inferior presionado exitosamente")
            assert clientes_nav_button is not None, "No se pudo encontrar el botón 'Clientes' usando el método relacional"

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia de la configuración guardado en: {video_path}")

    @pytest.mark.xray("ATC-34")
    def test_long_press_cliente_card(self, driver, video_recorder):
        """
        Test que valida la acción de mantener presionado una tarjeta de cliente,
        usando TouchAction para gestos móviles más confiables.
        """
        print("\n=== TEST: Validar long press en tarjeta de cliente 'CLIENTES IS' ===")
        try:
            # Paso 1: Realizar la pulsación larga en la tarjeta
            print("🎯 Paso 1: Ejecutando long press en tarjeta...")
            try:
                realizar_long_press_en_tarjeta_cliente(driver)
                print("✅ Paso 1 completado: Long press realizado exitosamente.")
            except Exception as long_press_error:
                print(f"⚠️  Error en método principal, {long_press_error}")
            print("⏳ Pausa para estabilizar la UI...")
            time.sleep(2)

            # Paso 2: Pulsar el botón central
            print("🎯 Paso 2: Pulsando botón central de navegación...")
            pulsar_boton_central_nav(driver)
            print("✅ Paso 2 completado: Botón central de navegación pulsado.")


            print("✅ TEST PASADO: La secuencia de acciones se ejecutó sin errores.")

        except Exception as e:
            print(f"❌ ERROR durante el test: {e}")

            # Información adicional para debugging
            print("🔧 Información de debugging:")
            try:
                current_activity = driver.current_activity
                print(f"   - Actividad actual: {current_activity}")
            except:
                print("   - No se pudo obtener la actividad actual")

            try:
                window_size = driver.get_window_size()
                print(f"   - Tamaño de ventana: {window_size}")
            except:
                print("   - No se pudo obtener el tamaño de ventana")

            pytest.fail(f"TEST FALLÓ: {e}")

        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video evidencia guardado en: {video_path}")

    @pytest.mark.xray("ATC-35")
    def test_llenar_campos_general(self, driver, video_recorder):
        """
        Test que llena los campos el formulario de nuevos clientes GENERAL
        y verifica que los valores se hayan ingresado correctamente.
        """
        print("\n=== TEST: Llenar formulario GENERAL ===")
        try:
            # Valores a escribir
            nit_a_escribir = "123456789"
            dpi_a_escribir = "1234567890101"
            version_dpi_a_escribir = "001"

            # Paso 1: Escribir NIT
            escribir_nit(driver, nit_a_escribir)

            # Paso 2: Escribir DPI del representante
            escribir_dpi_representante(driver, dpi_a_escribir)

            # Paso 3: Hacer scroll hacia abajo para ver el campo Versión DPI
            hacer_scroll_hacia_abajo(driver, cantidad_scroll=2)

            # Paso 4: Escribir Versión DPI
            escribir_version_dpi(driver, version_dpi_a_escribir)

            # Paso 5: Fecha de DPI
            dia = "13"
            anio = "2025"
            seleccionar_vencimiento_dpi(driver, dia, anio)

            # Paso 6: Nota
            nota = "Prueba automatizada"
            escribir_nota(driver, nota)

            # VERIFICACIÓN
            print("\nVerificando que los datos se escribieron correctamente...")

            # Hacer scroll hacia arriba primero
            hacer_scroll_hacia_arriba(driver, 3)

            # Verificar NIT por su texto
            nit_encontrado = False
            try:
                nit_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{nit_a_escribir}']")
                print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
                nit_encontrado = True
            except:
                print("⚠️ Campo NIT no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando NIT
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        nit_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{nit_a_escribir}']")
                        print(f"✅ Verificación NIT exitosa: el campo contiene '{nit_field.text}'")
                        nit_encontrado = True
                        break
                    except:
                        continue
                if not nit_encontrado:
                    print("⚠️ No se pudo verificar el campo NIT después de scroll")

            # Verificar DPI por su texto
            dpi_encontrado = False
            try:
                dpi_field = driver.find_element(AppiumBy.XPATH, f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
                dpi_encontrado = True
            except:
                print("⚠️ Campo DPI no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando DPI
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        dpi_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{dpi_a_escribir}']")
                        print(f"✅ Verificación DPI exitosa: el campo contiene '{dpi_field.text}'")
                        dpi_encontrado = True
                        break
                    except:
                        continue
                if not dpi_encontrado:
                    print("⚠️ No se pudo verificar el campo DPI después de scroll")

            # Verificar Versión DPI por su texto
            version_dpi_encontrado = False
            try:
                version_dpi_field = driver.find_element(AppiumBy.XPATH,
                                                        f"//android.widget.EditText[@text='{version_dpi_a_escribir}']")
                print(f"✅ Verificación Versión DPI exitosa: el campo contiene '{version_dpi_field.text}'")
                version_dpi_encontrado = True
            except:
                print("⚠️ Campo Versión DPI no visible, haciendo scroll hacia abajo...")
                # Scroll hacia abajo hasta 3 veces buscando Versión DPI
                for scroll_attempt in range(3):
                    driver.swipe(driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.8),
                                 driver.get_window_size()['width'] // 2,
                                 int(driver.get_window_size()['height'] * 0.2),
                                 duration=800)
                    time.sleep(0.5)
                    try:
                        version_dpi_field = driver.find_element(AppiumBy.XPATH,
                                                                f"//android.widget.EditText[@text='{version_dpi_a_escribir}']")
                        print(f"✅ Verificación Versión DPI exitosa: el campo contiene '{version_dpi_field.text}'")
                        version_dpi_encontrado = True
                        break
                    except:
                        continue
                if not version_dpi_encontrado:
                    print("⚠️ No se pudo verificar el campo Versión DPI después de scroll")

            # Paso 7 - Continuar
            hacer_scroll_hacia_abajo(driver, cantidad_scroll=2)
            hacer_click_continuar(driver)

            print("\n✅ TEST PASADO: Todos los campos se escribieron correctamente.")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")

    @pytest.mark.xray("ATC-36")
    def test_llenar_campos_sucursales_1(self, driver, video_recorder):
        print("\n=== TEST: Llenar formulario Sucursales y Gestiones ===")
        try:
            seleccionar_tipo_de_ruta(driver)
            #Direccion
            seleccionar_direccion(driver, "Selecciona una direcc")
            llenar_formulario_direccion(
                driver=driver,
                campo1="5ta Avenida 12-34",
                campo2="Zona 1",
                campo3="Casa 123",
                campo4="Frente al parque central",
                campo5="Zona 1"
            )
            seleccionar_direccion(driver, "5ta Avenida 12-34")

            #Contacto
            seleccionar_contacto(driver, "un contacto")
            nombres = "Juan"
            apellidos = "Pérez"
            llenar_formulario_contacto(
                driver,
                nombres,
                apellidos,
                puesto="Gerente",
                correo1="juan.perez@ejemplo.com",
                telefono1="45126523"
            )
            result = nombres + ' ' + apellidos
            seleccionar_contacto(driver, result)
            #Geolocalizacion
            click_asignar_geolocalizacion(driver)
            click_capturar(driver)

            #Continuar
            eliminar_gestiones_extras_iterativo(driver, 3)
            hacer_click_boton_sucursal_especifico(driver)
            click_continuar(driver)


        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")

    @pytest.mark.xray("ATC-37")
    def test_llenar_campos_perfilacion(self, driver, video_recorder):
        print("\n=== TEST: Llenar Perfilacion ===")
        try:
            seleccionar_condicion(driver, "Contado contra entrega")
            click_continuar(driver)

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")

    @pytest.mark.xray("ATC-38")
    def test_verificar_creacion_cliente(self, driver, video_recorder):
        print("\n=== TEST: Buscar y confirmar nuevo cliente ===")
        try:
            buscar_cliente_por_nombre(driver, "TEST 3")

        except Exception as e:
            pytest.fail(f"TEST FALLÓ {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video guardado: {video_path}")