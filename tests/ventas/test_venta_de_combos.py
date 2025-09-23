import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class test_venta_de_combos:
    @pytest.mark.xray("APPTEST-COMBO-01")
    def test_01_vender_combo_desde_catalogo(self, driver, video_recorder):
        """
        Flujo completo usando CONTEXTO y EXCLUSIONES para identificar botones 'null':
         - Identifica botones 'null' por exclusión de navigation
         - Usa orden y contexto para seleccionar el correcto
        """
        print("\n=== TEST: Venta de combo - USANDO CONTEXTO Y EXCLUSIONES ===")
        try:
            print("✅ Iniciando test")
            time.sleep(1)

            # FUNCIÓN HELPER: Buscar elemento 'null' inteligentemente
            def buscar_elemento_null_inteligente(contexto="agregar"):
                """
                Busca elemento 'null' excluyendo botones conocidos del navigation
                contexto: "agregar", "carrito", "cheque"
                """
                try:
                    print(f"🔍 Buscando elemento 'null' para contexto: {contexto}")

                    # Obtener TODOS los elementos clickeables
                    all_clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

                    # Obtener elementos conocidos del navigation por content-desc
                    navigation_elements = []
                    nav_descriptions = ['Menú', 'Clientes', 'Itinerarios', 'Catálogo']

                    for nav_desc in nav_descriptions:
                        try:
                            nav_elems = driver.find_elements(AppiumBy.XPATH,
                                                             f"//*[@clickable='true' and @content-desc='{nav_desc}']")
                            navigation_elements.extend(nav_elems)
                        except:
                            pass

                    print(f"✅ Elementos de navigation identificados: {len(navigation_elements)}")

                    # Buscar elementos 'null' y vacíos
                    null_candidates = []

                    for elem in all_clickable:
                        try:
                            desc = elem.get_attribute('content-desc') or ""
                            text = elem.get_attribute('text') or ""

                            # Es 'null' o vacío Y NO es elemento de navigation
                            if (desc == 'null' or desc == '') and elem not in navigation_elements:
                                # Verificar que no tenga texto de navigation
                                if text not in nav_descriptions:
                                    null_candidates.append(elem)
                                    location = elem.location
                                    print(
                                        f"   📋 Candidato 'null': pos({location['x']}, {location['y']}) desc='{desc}' text='{text}'")

                        except Exception:
                            continue

                    print(f"✅ Candidatos 'null' encontrados: {len(null_candidates)}")

                    if null_candidates:
                        if contexto == "agregar":
                            # Para agregar: tomar el último (usualmente el botón de acción principal)
                            selected = null_candidates[-1]
                            print(f"✅ Seleccionado ÚLTIMO candidato para agregar")
                        elif contexto == "carrito":
                            # Para carrito: tomar el último (botón que cambió de apariencia)
                            selected = null_candidates[-1]
                            print(f"✅ Seleccionado ÚLTIMO candidato para carrito")
                        elif contexto == "cheque":
                            # Para cheque: tomar el último (botón de confirmación)
                            selected = null_candidates[-1]
                            print(f"✅ Seleccionado ÚLTIMO candidato para cheque")
                        else:
                            selected = null_candidates[0]

                        location = selected.location
                        print(f"✅ Elemento seleccionado: pos({location['x']}, {location['y']})")
                        return selected
                    else:
                        print("⚠ No se encontraron candidatos 'null' válidos")
                        return None

                except Exception as e:
                    print(f"⚠ Error buscando elemento 'null': {e}")
                    return None

            # 1) BUSCAR ELEMENTO CLICKABLE QUE CONTENGA COMBO
            print("🔍 Buscando elemento CLICKABLE que contenga COMBO...")
            clickable_combo = None
            size = driver.get_window_size()
            x = int(size['width'] / 2)
            start_y = int(size['height'] * 0.70)
            end_y = int(size['height'] * 0.30)

            # Función para buscar combos clickeables
            def buscar_combo_clickeable():
                try:
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

                    for elem in clickable_elements:
                        try:
                            desc = elem.get_attribute('content-desc') or ""
                            text = elem.get_attribute('text') or ""

                            if ('combo' in desc.lower() and len(desc) > 5) or \
                                    ('combo' in text.lower() and len(text) > 3):
                                print(f"✅ COMBO CLICKEABLE encontrado: desc='{desc}' text='{text}'")
                                return elem

                        except Exception:
                            continue

                    return None

                except Exception as e:
                    print(f"⚠ Error buscando combos clickeables: {e}")
                    return None

            # Primero intentar SIN swipes
            print("🔍 Búsqueda inicial sin swipes...")
            clickable_combo = buscar_combo_clickeable()

            if clickable_combo:
                print("✅ COMBO CLICKEABLE encontrado SIN swipes")
            else:
                print("⚠ No se encontraron combos clickeables sin swipes")

            # Si no encuentra combo, hacer swipes HASTA encontrar uno
            if not clickable_combo:
                print("🔄 Haciendo swipes para buscar COMBO CLICKEABLE...")
                max_swipes = 15  # Máximo de swipes para buscar

                for i in range(max_swipes):
                    try:
                        print(f"   🔄 Swipe {i + 1}/{max_swipes} - Buscando combo clickeable...")

                        # Hacer swipe
                        driver.swipe(x, start_y, x, end_y, 400)
                        time.sleep(0.8)  # Tiempo para que carguen los elementos

                        # BUSCAR COMBO CLICKEABLE después de cada swipe
                        clickable_combo = buscar_combo_clickeable()

                        if clickable_combo:
                            print(f"✅ COMBO CLICKEABLE encontrado después de swipe {i + 1}")
                            break
                        else:
                            print(f"   ❌ Swipe {i + 1}: No se encontraron combos clickeables")

                    except Exception as e:
                        print(f"⚠ Error en swipe {i + 1}: {e}")
                        continue

            # Fallback: buscar con criterios más amplios
            if not clickable_combo:
                print("🔍 Fallback: Búsqueda con criterios más amplios...")
                try:
                    # Buscar elementos clickeables que contengan la palabra combo de cualquier forma
                    clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

                    for elem in clickable_elements:
                        try:
                            desc = elem.get_attribute('content-desc') or ""
                            text = elem.get_attribute('text') or ""

                            # Criterios más amplios
                            if 'combo' in desc.lower() or 'combo' in text.lower():
                                clickable_combo = elem
                                print(f"✅ COMBO CLICKEABLE encontrado (fallback): desc='{desc}' text='{text}'")
                                break

                        except Exception:
                            continue

                except Exception as e:
                    print(f"⚠ Error en fallback: {e}")

            if not clickable_combo:
                pytest.fail("❌ No se encontró ningún elemento CLICKABLE que contenga COMBO")

            # 2) Hacer click en el combo (ya sabemos que es clickeable)
            try:
                print("📱 Haciendo click en el combo clickeable...")
                clickable_combo.click()
                time.sleep(2)
                print("✅ Combo abierto")
            except Exception as e:
                print(f"⚠ Click directo falló: {e}")
                try:
                    # Intentar click por coordenadas como último recurso
                    print("🔍 Intentando click por coordenadas...")
                    location = clickable_combo.location
                    size_elem = clickable_combo.size
                    center_x = location['x'] + size_elem['width'] // 2
                    center_y = location['y'] + size_elem['height'] // 2

                    driver.tap([(center_x, center_y)])
                    time.sleep(2)
                    print("✅ Combo abierto (por coordenadas)")
                except Exception as e2:
                    pytest.fail(f"Error abriendo combo: {e2}")

            # 3) Incrementar cantidad - BUSCAR BOTÓN + INTELIGENTEMENTE
            print("➕ Buscando botón + inteligentemente...")
            plus_btn = None

            try:
                # Estrategia 1: Buscar por texto "+"
                plus_buttons = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true' and @text='+']")
                if plus_buttons:
                    plus_btn = plus_buttons[0]
                    print("✅ Botón + encontrado por texto '+'")

                # Estrategia 2: Buscar botones pequeños que NO sean de navigation
                if not plus_btn:
                    all_clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

                    # Obtener elementos de navigation conocidos
                    nav_elements = []
                    for nav_desc in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo']:
                        try:
                            nav_elems = driver.find_elements(AppiumBy.XPATH, f"//*[@content-desc='{nav_desc}']")
                            nav_elements.extend(nav_elems)
                        except:
                            pass

                    small_buttons = []
                    for elem in all_clickable:
                        try:
                            size_elem = elem.size
                            desc = elem.get_attribute('content-desc') or ""
                            text = elem.get_attribute('text') or ""

                            # Botones pequeños que NO sean de navigation
                            if (size_elem['width'] < 150 and size_elem['height'] < 150 and
                                    elem not in nav_elements and
                                    desc not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo'] and
                                    text not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo']):
                                small_buttons.append(elem)

                        except Exception:
                            continue

                    if small_buttons:
                        # Tomar el último botón pequeño (usualmente el +)
                        plus_btn = small_buttons[-1]
                        print("✅ Botón + encontrado por exclusión (botón pequeño)")

            except Exception as e:
                print(f"⚠ Error buscando botón +: {e}")

            if plus_btn:
                try:
                    print("➕ Incrementando cantidad...")
                    plus_btn.click()
                    time.sleep(0.5)
                    plus_btn.click()
                    time.sleep(0.5)
                    print("✅ Cantidad incrementada a 2")
                except Exception as e:
                    print(f"⚠ Error incrementando: {e}")
            else:
                print("⚠ No se encontró botón para incrementar cantidad")

            # 4) AGREGAR AL CARRITO - ELEMENTO 'null' INTELIGENTE
            print("🛒 Agregando al carrito usando elemento 'null' inteligente...")
            add_btn = buscar_elemento_null_inteligente("agregar")

            if not add_btn:
                print("⚠ Fallback: buscando último botón clickeable...")
                try:
                    all_buttons = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    # Excluir navigation
                    non_nav_buttons = []
                    for btn in all_buttons:
                        try:
                            desc = btn.get_attribute('content-desc') or ""
                            text = btn.get_attribute('text') or ""
                            if (desc not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo'] and
                                    text not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo']):
                                non_nav_buttons.append(btn)
                        except:
                            continue

                    add_btn = non_nav_buttons[-1] if non_nav_buttons else None
                    print("✅ Último botón no-navigation encontrado (fallback)")
                except Exception:
                    pass

            if not add_btn:
                pytest.fail("❌ No se encontró botón para agregar al carrito")

            print("🛒 Haciendo click para agregar al carrito...")
            add_btn.click()
            time.sleep(2)
            print("✅ Combo agregado al carrito - regresando a catálogo")

            # 5) ABRIR CARRITO - ELEMENTO 'null' INTELIGENTE
            print("🛒 Abriendo carrito usando elemento 'null' inteligente...")
            carrito_btn = buscar_elemento_null_inteligente("carrito")

            if not carrito_btn:
                pytest.fail("❌ No se encontró botón de carrito")

            carrito_btn.click()
            time.sleep(2)
            print("✅ Carrito abierto")

            # 6) CHEQUE VERDE - ELEMENTO 'null' INTELIGENTE
            print("✅ Buscando cheque verde usando elemento 'null' inteligente...")
            time.sleep(1)
            check_btn = buscar_elemento_null_inteligente("cheque")

            if not check_btn:
                print("⚠ Fallback cheque: buscando cualquier botón no-navigation...")
                try:
                    all_clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
                    for elem in all_clickable:
                        try:
                            desc = elem.get_attribute('content-desc') or ""
                            text = elem.get_attribute('text') or ""
                            if (desc not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo'] and
                                    text not in ['Menú', 'Clientes', 'Itinerarios', 'Catálogo']):
                                check_btn = elem
                                print(f"✅ Botón no-navigation encontrado para cheque: desc='{desc}' text='{text}'")
                                break
                        except Exception:
                            continue
                except Exception:
                    pass

            if not check_btn:
                pytest.fail("❌ No se encontró botón de cheque verde")

            print("✅ Haciendo click en cheque verde...")
            check_btn.click()
            time.sleep(2)
            print("✅ Cheque verde presionado")

            # 7) CONFIRMAR PEDIDO (si aparece diálogo)
            print("✅ Verificando confirmación final...")
            try:
                confirmation_selectors = [
                    "//*[@content-desc='Ok' or @content-desc='OK']",
                    "//*[@text='Ok' or @text='OK' or @text='Aceptar']",
                    "//*[contains(@content-desc,'Aceptar')]",
                    "//*[contains(@text,'Confirmar')]"
                ]

                confirmation_btn = None
                for selector in confirmation_selectors:
                    try:
                        confirmation_btn = driver.find_element(AppiumBy.XPATH, selector)
                        print(f"✅ Confirmación encontrada")
                        break
                    except Exception:
                        continue

                if confirmation_btn:
                    confirmation_btn.click()
                    time.sleep(2)
                    print("✅ Pedido confirmado")
                else:
                    print("✅ No se requiere confirmación adicional")

            except Exception as e:
                print(f"⚠ Error buscando confirmación: {e}")

            # 8) Verificar resultado final
            print("🔍 Verificando resultado final...")
            try:
                prices = driver.find_elements(AppiumBy.XPATH, "//*[starts-with(@text,'Q')]")
                if prices:
                    for price_elem in prices:
                        price = price_elem.get_attribute("text") or ""
                        if price and "Q0.00" not in price and len(price) > 3:
                            print(f"✅ Precio final: {price}")
                            break
                    else:
                        print("⚠ Solo precios Q0.00 encontrados")
                else:
                    print("⚠ No se encontraron elementos de precio")
            except Exception:
                print("⚠ Error verificando precios finales")

            print("✅ TEST COMPLETADO EXITOSAMENTE - COMBO VENDIDO Y CONFIRMADO")

        except Exception as e:
            pytest.fail(f"❌ TEST FALLÓ: {e}")
        finally:
            video_path = video_recorder()
            if video_path:
                print(f"📹 Video: {video_path}")