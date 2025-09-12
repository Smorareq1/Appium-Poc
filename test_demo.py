from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import os
from datetime import datetime
import base64


class AppiumTestSuite:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.driver = None
        self.test_results = {
            "test_session": {
                "start_time": datetime.now().isoformat(),
                "device": "emulator-5554",
                "app_path": apk_path
            },
            "tests": [],
            "screenshots": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0
            }
        }
        self.screenshots_dir = "test_screenshots"
        self.reports_dir = "test_reports"

        # Crear directorios
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

    def setup_driver(self):
        """Configurar y inicializar el driver de Appium"""
        print("🚀 Configurando driver de Appium...")

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app = self.apk_path
        options.automation_name = "UiAutomator2"
        options.new_command_timeout = 60
        options.no_reset = True  # No reinstalar app cada vez

        try:
            self.driver = webdriver.Remote(
                command_executor="http://127.0.0.1:4723",
                options=options
            )
            print("✅ Driver configurado exitosamente")
            time.sleep(3)  # Esperar que la app cargue
            return True
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            return False

    def take_screenshot(self, name):
        """Tomar screenshot y guardarlo"""
        if not self.driver:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = os.path.join(self.screenshots_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            self.test_results["screenshots"].append({
                "name": name,
                "timestamp": timestamp,
                "filepath": filepath
            })
            print(f"📸 Screenshot guardado: {filename}")
            return filepath
        except Exception as e:
            print(f"❌ Error tomando screenshot: {e}")
            return None

    def log_test(self, test_name, status, duration, details=None, screenshot=None):
        """Registrar resultado de un test"""
        test_result = {
            "name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "screenshot": screenshot
        }

        self.test_results["tests"].append(test_result)
        self.test_results["summary"]["total_tests"] += 1

        if status == "PASS":
            self.test_results["summary"]["passed"] += 1
            print(f"✅ {test_name}: PASÓ ({duration:.2f}s)")
        else:
            self.test_results["summary"]["failed"] += 1
            print(f"❌ {test_name}: FALLÓ ({duration:.2f}s)")
            if details:
                print(f"   Detalles: {details}")

    def test_app_launch(self):
        """Test 1: Verificar que la app se lanza correctamente"""
        start_time = time.time()

        try:
            # Tomar screenshot inicial
            screenshot = self.take_screenshot("app_launched")

            # Verificar que la app está corriendo
            current_package = self.driver.current_package
            current_activity = self.driver.current_activity

            details = {
                "package": current_package,
                "activity": current_activity,
                "screenshot": screenshot
            }

            duration = time.time() - start_time
            self.log_test("App Launch", "PASS", duration, details, screenshot)
            return True

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("App Launch", "FAIL", duration, str(e))
            return False

    def find_clickable_elements(self):
        """Test 2: Encontrar elementos clickeables en la pantalla"""
        start_time = time.time()

        try:
            # Buscar elementos clickeables
            clickable_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

            elements_info = []
            for i, element in enumerate(clickable_elements):
                try:
                    text = element.get_attribute("text") or element.get_attribute("content-desc") or f"Element_{i + 1}"
                    bounds = element.get_attribute("bounds")
                    class_name = element.get_attribute("class")

                    elements_info.append({
                        "index": i + 1,
                        "text": text,
                        "bounds": bounds,
                        "class": class_name
                    })
                except:
                    elements_info.append({
                        "index": i + 1,
                        "text": f"Element_{i + 1}",
                        "bounds": "unknown",
                        "class": "unknown"
                    })

            screenshot = self.take_screenshot("clickable_elements_found")

            details = {
                "total_clickable": len(clickable_elements),
                "elements": elements_info
            }

            duration = time.time() - start_time
            self.log_test("Find Clickable Elements", "PASS", duration, details, screenshot)
            return clickable_elements

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Find Clickable Elements", "FAIL", duration, str(e))
            return []

    def test_multiple_clicks(self, target_clicks=10):
        """Test 3: Clickear un botón múltiples veces"""
        start_time = time.time()

        try:
            # Intentar encontrar un botón para clickear
            # Primero buscamos por texto común en apps Flutter
            button_selectors = [
                "//*[contains(@text, 'Button') or contains(@text, 'button')]",
                "//*[contains(@text, '+')]",
                "//*[contains(@content-desc, 'button')]",
                "//*[@clickable='true'][1]"  # Primer elemento clickeable
            ]

            button_found = None
            selector_used = None

            for selector in button_selectors:
                try:
                    button_found = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, selector))
                    )
                    selector_used = selector
                    break
                except TimeoutException:
                    continue

            if not button_found:
                # Si no encontramos botón, hacemos clicks en coordenadas fijas (centro de pantalla)
                screen_size = self.driver.get_window_size()
                center_x = screen_size["width"] // 2
                center_y = screen_size["height"] // 2

                successful_clicks = 0
                click_details = []

                for i in range(target_clicks):
                    try:
                        self.driver.tap([(center_x, center_y)], 100)
                        successful_clicks += 1
                        click_details.append({
                            "click_number": i + 1,
                            "coordinates": [center_x, center_y],
                            "status": "success"
                        })
                        time.sleep(0.5)  # Pausa entre clicks
                    except Exception as click_error:
                        click_details.append({
                            "click_number": i + 1,
                            "coordinates": [center_x, center_y],
                            "status": "failed",
                            "error": str(click_error)
                        })

                screenshot = self.take_screenshot("multiple_clicks_coordinates")

                details = {
                    "method": "coordinate_tapping",
                    "target_clicks": target_clicks,
                    "successful_clicks": successful_clicks,
                    "coordinates": [center_x, center_y],
                    "click_details": click_details
                }

            else:
                # Si encontramos un botón, lo clickeamos
                button_text = button_found.get_attribute("text") or button_found.get_attribute(
                    "content-desc") or "Unknown Button"

                successful_clicks = 0
                click_details = []

                for i in range(target_clicks):
                    try:
                        button_found.click()
                        successful_clicks += 1
                        click_details.append({
                            "click_number": i + 1,
                            "element_text": button_text,
                            "status": "success"
                        })
                        time.sleep(0.5)  # Pausa entre clicks
                    except Exception as click_error:
                        click_details.append({
                            "click_number": i + 1,
                            "element_text": button_text,
                            "status": "failed",
                            "error": str(click_error)
                        })

                screenshot = self.take_screenshot("multiple_clicks_button")

                details = {
                    "method": "button_clicking",
                    "button_text": button_text,
                    "selector_used": selector_used,
                    "target_clicks": target_clicks,
                    "successful_clicks": successful_clicks,
                    "click_details": click_details
                }

            duration = time.time() - start_time

            if successful_clicks > 0:
                self.log_test("Multiple Clicks Test", "PASS", duration, details, screenshot)
            else:
                self.log_test("Multiple Clicks Test", "FAIL", duration, details, screenshot)

            return successful_clicks

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Multiple Clicks Test", "FAIL", duration, str(e))
            return 0

    def test_gestures(self):
        """Test 4: Probar gestos (scroll, swipe)"""
        start_time = time.time()

        try:
            screen_size = self.driver.get_window_size()
            width = screen_size["width"]
            height = screen_size["height"]

            gestures_performed = []

            # Scroll hacia abajo
            try:
                self.driver.swipe(width // 2, height * 0.8, width // 2, height * 0.2, 800)
                gestures_performed.append({"type": "scroll_down", "status": "success"})
                time.sleep(1)
            except Exception as e:
                gestures_performed.append({"type": "scroll_down", "status": "failed", "error": str(e)})

            # Scroll hacia arriba
            try:
                self.driver.swipe(width // 2, height * 0.2, width // 2, height * 0.8, 800)
                gestures_performed.append({"type": "scroll_up", "status": "success"})
                time.sleep(1)
            except Exception as e:
                gestures_performed.append({"type": "scroll_up", "status": "failed", "error": str(e)})

            # Swipe lateral izquierda
            try:
                self.driver.swipe(width * 0.8, height // 2, width * 0.2, height // 2, 800)
                gestures_performed.append({"type": "swipe_left", "status": "success"})
                time.sleep(1)
            except Exception as e:
                gestures_performed.append({"type": "swipe_left", "status": "failed", "error": str(e)})

            screenshot = self.take_screenshot("gestures_test")

            successful_gestures = len([g for g in gestures_performed if g["status"] == "success"])

            details = {
                "screen_size": screen_size,
                "gestures_attempted": len(gestures_performed),
                "successful_gestures": successful_gestures,
                "gesture_details": gestures_performed
            }

            duration = time.time() - start_time

            if successful_gestures > 0:
                self.log_test("Gestures Test", "PASS", duration, details, screenshot)
            else:
                self.log_test("Gestures Test", "FAIL", duration, details, screenshot)

            return successful_gestures

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Gestures Test", "FAIL", duration, str(e))
            return 0

    def test_performance_metrics(self):
        """Test 5: Métricas de rendimiento básicas"""
        start_time = time.time()

        try:
            # Tiempo de respuesta de la app
            response_times = []

            for i in range(5):
                action_start = time.time()

                # Realizar una acción simple (tomar screenshot)
                self.driver.save_screenshot(f"temp_perf_{i}.png")

                action_duration = time.time() - action_start
                response_times.append(action_duration)

                # Limpiar archivo temporal
                try:
                    os.remove(f"temp_perf_{i}.png")
                except:
                    pass

                time.sleep(0.5)

            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)

            # Información del dispositivo
            device_info = {
                "screen_size": self.driver.get_window_size(),
                "current_package": self.driver.current_package,
                "current_activity": self.driver.current_activity
            }

            screenshot = self.take_screenshot("performance_metrics")

            details = {
                "response_times": response_times,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "min_response_time": min_response_time,
                "device_info": device_info
            }

            duration = time.time() - start_time
            self.log_test("Performance Metrics", "PASS", duration, details, screenshot)

            return True

        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Performance Metrics", "FAIL", duration, str(e))
            return False

    def generate_html_report(self):
        """Generar reporte HTML detallado"""

        # Calcular duración total
        total_duration = sum([test["duration"] for test in self.test_results["tests"]])
        self.test_results["summary"]["duration"] = total_duration
        self.test_results["test_session"]["end_time"] = datetime.now().isoformat()

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appium Test Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); padding: 30px; }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric {{ background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; border-left: 4px solid #667eea; }}
        .metric h3 {{ margin: 0; color: #333; }}
        .metric .value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .test {{ background: white; margin: 15px 0; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }}
        .test.pass {{ border-left: 5px solid #28a745; }}
        .test.fail {{ border-left: 5px solid #dc3545; }}
        .test-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .status.pass {{ background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        .status.fail {{ background: #dc3545; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        .details {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; }}
        .screenshot {{ max-width: 300px; border-radius: 8px; margin: 10px 0; }}
        pre {{ background: #f1f1f1; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Appium Test Report</h1>
            <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>

        <div class="summary">
            <div class="metric">
                <h3>Tests Totales</h3>
                <div class="value">{self.test_results['summary']['total_tests']}</div>
            </div>
            <div class="metric">
                <h3>✅ Pasaron</h3>
                <div class="value" style="color: #28a745;">{self.test_results['summary']['passed']}</div>
            </div>
            <div class="metric">
                <h3>❌ Fallaron</h3>
                <div class="value" style="color: #dc3545;">{self.test_results['summary']['failed']}</div>
            </div>
            <div class="metric">
                <h3>⏱️ Duración</h3>
                <div class="value">{total_duration:.2f}s</div>
            </div>
        </div>

        <h2>📋 Resultados Detallados</h2>
        """

        for test in self.test_results["tests"]:
            status_class = "pass" if test["status"] == "PASS" else "fail"
            status_text = "PASÓ" if test["status"] == "PASS" else "FALLÓ"

            html_content += f"""
        <div class="test {status_class}">
            <div class="test-header">
                <h3>{test['name']}</h3>
                <span class="status {status_class}">{status_text}</span>
            </div>
            <p><strong>Duración:</strong> {test['duration']:.2f} segundos</p>
            <p><strong>Timestamp:</strong> {test['timestamp']}</p>
            """

            if test.get('screenshot'):
                html_content += f'<img src="{test["screenshot"]}" alt="Screenshot" class="screenshot">'

            if test.get('details'):
                html_content += f"""
            <div class="details">
                <strong>Detalles:</strong>
                <pre>{json.dumps(test['details'], indent=2, ensure_ascii=False)}</pre>
            </div>
            """

            html_content += "</div>"

        html_content += """
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; text-align: center;">
            <p>🤖 Generado automáticamente por Appium Test Suite</p>
        </div>
    </div>
</body>
</html>
        """

        # Guardar reporte HTML
        report_path = os.path.join(self.reports_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📊 Reporte HTML generado: {report_path}")
        return report_path

    def generate_json_report(self):
        """Generar reporte JSON"""
        json_path = os.path.join(self.reports_dir, f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)

        print(f"📄 Reporte JSON generado: {json_path}")
        return json_path

    def run_all_tests(self):
        """Ejecutar toda la suite de tests"""
        print("🚀 Iniciando Appium Test Suite...")
        print("=" * 50)

        if not self.setup_driver():
            return False

        try:
            # Ejecutar todos los tests
            print("\n1️⃣ Test: Lanzamiento de App")
            self.test_app_launch()

            print("\n2️⃣ Test: Elementos Clickeables")
            elements = self.find_clickable_elements()

            print("\n3️⃣ Test: Clicks Múltiples (10 veces)")
            clicks = self.test_multiple_clicks(10)

            print("\n4️⃣ Test: Gestos y Swipes")
            gestures = self.test_gestures()

            print("\n5️⃣ Test: Métricas de Rendimiento")
            self.test_performance_metrics()

            # Generar reportes
            print("\n📊 Generando reportes...")
            html_report = self.generate_html_report()
            json_report = self.generate_json_report()

            # Resumen final
            print("\n" + "=" * 50)
            print("🎉 RESUMEN FINAL:")
            print(f"✅ Tests pasaron: {self.test_results['summary']['passed']}")
            print(f"❌ Tests fallaron: {self.test_results['summary']['failed']}")
            print(f"⏱️ Duración total: {self.test_results['summary']['duration']:.2f}s")
            print(f"📊 Reporte HTML: {html_report}")
            print(f"📄 Reporte JSON: {json_report}")

            return True

        except Exception as e:
            print(f"❌ Error durante la ejecución de tests: {e}")
            return False

        finally:
            if self.driver:
                self.driver.quit()
                print("🏁 Driver cerrado")


def main():
    # AJUSTAR ESTA RUTA A TU APK
    apk_path = r"C:\Users\smora\Documents\PDC\flutter-poc\demo_appium\build\app\outputs\flutter-apk\app-release.apk"

    # Crear y ejecutar la suite de tests
    test_suite = AppiumTestSuite(apk_path)
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()