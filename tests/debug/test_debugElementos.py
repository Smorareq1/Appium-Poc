import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class Test_Debug:
    @pytest.mark.xray("APPTEST-18")
    def test_debug_current_screen(self, driver, video_recorder):
        """ Debug COMPLETO - Todos los elementos de la pantalla actual"""
        print("\n" + "=" * 80)
        print("=== DEBUG COMPLETO - ANÁLISIS DE PANTALLA ===")
        print("=" * 80)

        try:
            # 1. INFORMACIÓN BÁSICA DE LA APP
            print("\n📱 INFORMACIÓN BÁSICA:")
            print(f"Package actual: {driver.current_package}")
            print(f"Activity actual: {driver.current_activity}")

            try:
                window_size = driver.get_window_size()
                print(f"Tamaño de pantalla: {window_size['width']}x{window_size['height']}")
            except:
                print("No se pudo obtener tamaño de pantalla")

            # 2. JERARQUÍA COMPLETA XML (para ver estructura)
            print("\n🌳 JERARQUÍA XML DE LA PANTALLA:")
            try:
                page_source = driver.page_source
                # Guardar en archivo para revisión manual
                with open("debug_page_source.xml", "w", encoding="utf-8") as f:
                    f.write(page_source)
                print("✅ Jerarquía XML guardada en: debug_page_source.xml")
                print(f"📏 Longitud del XML: {len(page_source)} caracteres")

                # Contar tipos de elementos
                widget_types = {}
                for line in page_source.split('\n'):
                    if '<' in line and 'android.' in line:
                        widget = line.split()[0].replace('<', '').split()[0]
                        widget_types[widget] = widget_types.get(widget, 0) + 1

                print("\n📊 TIPOS DE WIDGETS ENCONTRADOS:")
                for widget, count in sorted(widget_types.items()):
                    print(f"  {widget}: {count} elementos")

            except Exception as e:
                print(f"❌ Error obteniendo page source: {e}")

            # 3. TODOS LOS ELEMENTOS POR TIPO DE WIDGET
            widget_types_to_check = [
                "android.widget.TextView",
                "android.widget.EditText",
                "android.widget.Button",
                "android.widget.ImageView",
                "android.widget.ImageButton",
                "android.widget.Spinner",  # ComboBoxes/Dropdowns
                "android.widget.CheckBox",
                "android.widget.RadioButton",
                "android.widget.Switch",
                "android.widget.ToggleButton",
                "android.widget.SeekBar",
                "android.widget.ProgressBar",
                "android.widget.ListView",
                "android.widget.RecyclerView",
                "android.widget.ScrollView",
                "android.widget.HorizontalScrollView",
                "android.widget.LinearLayout",
                "android.widget.RelativeLayout",
                "android.widget.FrameLayout",
                "android.widget.GridView",
                "android.widget.TabHost",
                "android.widget.WebView",
                "androidx.recyclerview.widget.RecyclerView"
            ]

            for widget_type in widget_types_to_check:
                elements = driver.find_elements(AppiumBy.CLASS_NAME, widget_type)
                if elements:
                    print(f"\n🔹 {widget_type.split('.')[-1].upper()} ({len(elements)} encontrados):")
                    for i, elem in enumerate(elements):
                        self._print_element_details(elem, i + 1)

            # 4. BÚSQUEDA ESPECÍFICA DE COMBOBOXES/SPINNERS
            print("\n" + "=" * 50)
            print("🔍 ANÁLISIS ESPECÍFICO DE COMBOBOXES/SPINNERS:")
            print("=" * 50)

            # Spinners por clase
            spinners = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Spinner")
            if spinners:
                print(f"\n📋 SPINNERS ENCONTRADOS ({len(spinners)}):")
                for i, spinner in enumerate(spinners):
                    print(f"\n  Spinner #{i + 1}:")
                    self._print_element_details(spinner, "", detailed=True)
            else:
                print("❌ No se encontraron Spinners por clase")

            # Buscar por atributos que podrían indicar dropdowns
            potential_dropdowns = driver.find_elements(AppiumBy.XPATH,
                                                       "//*[contains(@class,'Spinner') or contains(@resource-id,'spinner') or contains(@resource-id,'dropdown')]")
            if potential_dropdowns:
                print(f"\n📋 POSIBLES DROPDOWNS POR ATRIBUTOS ({len(potential_dropdowns)}):")
                for i, elem in enumerate(potential_dropdowns):
                    self._print_element_details(elem, i + 1, detailed=True)

            # 5. ELEMENTOS CLICKEABLES DETALLADOS
            print("\n" + "=" * 50)
            print("🎯 ELEMENTOS CLICKEABLES DETALLADOS:")
            print("=" * 50)
            clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            print(f"\nTotal elementos clickeables: {len(clickable_elements)}")

            for i, elem in enumerate(clickable_elements):
                print(f"\n  Clickeable #{i + 1}:")
                self._print_element_details(elem, "", detailed=True)

            # 6. ELEMENTOS CON TEXTO O CONTENT-DESC
            print("\n" + "=" * 50)
            print("📝 ELEMENTOS CON CONTENIDO:")
            print("=" * 50)

            text_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text != '' or @content-desc != '']")
            print(f"\nTotal elementos con contenido: {len(text_elements)}")

            for i, elem in enumerate(text_elements):
                try:
                    text = elem.get_attribute("text") or ""
                    content_desc = elem.get_attribute("content-desc") or ""
                    if text or content_desc:
                        print(f"\n  Elemento #{i + 1}:")
                        self._print_element_details(elem, "", detailed=False)
                except:
                    continue

            # 7. ELEMENTOS POR ESTADOS ESPECÍFICOS
            print("\n" + "=" * 50)
            print("🔄 ELEMENTOS POR ESTADOS:")
            print("=" * 50)

            states_to_check = {
                "enabled='true'": "Habilitados",
                "enabled='false'": "Deshabilitados",
                "focused='true'": "Con foco",
                "selected='true'": "Seleccionados",
                "checked='true'": "Marcados",
                "displayed='true'": "Visibles"
            }

            for xpath_condition, description in states_to_check.items():
                elements = driver.find_elements(AppiumBy.XPATH, f"//*[@{xpath_condition}]")
                if elements:
                    print(f"\n{description}: {len(elements)} elementos")
                    for i, elem in enumerate(elements[:3]):  # Solo mostrar primeros 3
                        self._print_element_details(elem, i + 1, detailed=False)

            # 8. BÚSQUEDA AVANZADA POR RESOURCE-ID
            print("\n" + "=" * 50)
            print("🆔 ELEMENTOS CON RESOURCE-ID:")
            print("=" * 50)

            id_elements = driver.find_elements(AppiumBy.XPATH, "//*[@resource-id]")
            print(f"Total elementos con resource-id: {len(id_elements)}")

            # Agrupar por resource-id
            resource_ids = {}
            for elem in id_elements:
                try:
                    res_id = elem.get_attribute("resource-id")
                    if res_id:
                        resource_ids[res_id] = resource_ids.get(res_id, 0) + 1
                except:
                    continue

            print("\n📊 Resource-IDs encontrados:")
            for res_id, count in sorted(resource_ids.items()):
                print(f"  {res_id}: {count} elemento(s)")

            print("\n" + "=" * 80)
            print("✅ ANÁLISIS COMPLETO TERMINADO")
            print("📄 Revisa el archivo 'debug_page_source.xml' para ver la estructura completa")
            print("=" * 80)

        except Exception as e:
            print(f"❌ Error en debug completo: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # El video se detiene automáticamente al finalizar el test
            video_path = video_recorder()
            if video_path:
                print(f"\n📹 Video evidencia guardado: {video_path}")

    def _print_element_details(self, element, index, detailed=False):
        """Función auxiliar para imprimir detalles de un elemento"""
        try:
            # Información básica
            tag_name = element.tag_name if hasattr(element, 'tag_name') else "Unknown"
            text = element.get_attribute("text") or "(sin texto)"
            content_desc = element.get_attribute("content-desc") or "(sin descripción)"
            resource_id = element.get_attribute("resource-id") or "(sin ID)"
            class_name = element.get_attribute("class") or "(sin clase)"

            # Estados básicos
            clickable = element.get_attribute("clickable") or "false"
            enabled = element.get_attribute("enabled") or "false"
            displayed = element.get_attribute("displayed") or "false"

            if index:
                print(f"    [{index}] Clase: {class_name.split('.')[-1]}")
            else:
                print(f"    Clase: {class_name.split('.')[-1]}")

            print(f"        Texto: '{text}'")
            print(f"        Descripción: '{content_desc}'")
            print(f"        Resource-ID: {resource_id}")
            print(f"        Estados: Clickeable={clickable}, Habilitado={enabled}, Visible={displayed}")

            if detailed:
                # Información adicional para análisis detallado
                try:
                    bounds = element.get_attribute("bounds") or "(sin bounds)"
                    package = element.get_attribute("package") or "(sin package)"
                    checkable = element.get_attribute("checkable") or "false"
                    checked = element.get_attribute("checked") or "false"
                    focusable = element.get_attribute("focusable") or "false"
                    focused = element.get_attribute("focused") or "false"
                    scrollable = element.get_attribute("scrollable") or "false"
                    selected = element.get_attribute("selected") or "false"

                    print(f"        Package: {package}")
                    print(f"        Bounds: {bounds}")
                    print(f"        Otros estados: Checkeable={checkable}, Marcado={checked}")
                    print(f"        Foco: Enfocable={focusable}, Con foco={focused}")
                    print(f"        Interacción: Scrollable={scrollable}, Seleccionado={selected}")

                    # Para Spinners, intentar obtener opciones
                    if "Spinner" in class_name:
                        try:
                            # Intentar hacer click para ver opciones (sin compromiso)
                            print(
                                f"        🔍 Spinner detectado - para ver opciones hacer click en coordenadas: {bounds}")
                        except:
                            pass

                except Exception as detail_error:
                    print(f"        ⚠️ Error obteniendo detalles adicionales: {detail_error}")

        except Exception as e:
            print(f"    ❌ Error obteniendo información del elemento: {e}")