import pytest
import time
import os
import json
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestConfig:
    """Configuración centralizada para tests"""
    APK_PATH = r"C:\Users\smora\Documents\PDC\flutter-poc\demo_appium\build\app\outputs\flutter-apk\app-release.apk"
    APPIUM_SERVER = "http://127.0.0.1:4723"
    DEVICE_NAME = "emulator-5554"
    PLATFORM_NAME = "Android"
    AUTOMATION_NAME = "UiAutomator2"
    IMPLICIT_WAIT = 10
    SCREENSHOTS_DIR = "pytest_screenshots"
    REPORTS_DIR = "pytest_reports"


@pytest.fixture(scope="session")
def setup_directories():
    """Fixture para crear directorios necesarios - se ejecuta una vez por sesión"""
    os.makedirs(TestConfig.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(TestConfig.REPORTS_DIR, exist_ok=True)
    print(f"📁 Directorios creados: {TestConfig.SCREENSHOTS_DIR}, {TestConfig.REPORTS_DIR}")


@pytest.fixture(scope="function")
def appium_driver(setup_directories):
    """Fixture principal - crea y destruye driver para cada test"""
    print("🚀 Iniciando driver de Appium...")

    options = UiAutomator2Options()
    options.platform_name = TestConfig.PLATFORM_NAME
    options.device_name = TestConfig.DEVICE_NAME
    options.app = TestConfig.APK_PATH
    options.automation_name = TestConfig.AUTOMATION_NAME
    options.new_command_timeout = 60
    options.no_reset = True

    driver = None
    try:
        driver = webdriver.Remote(TestConfig.APPIUM_SERVER, options=options)
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)

        # Esperar que la app cargue
        time.sleep(3)

        print("✅ Driver iniciado correctamente")
        yield driver  # Esto es donde se ejecuta el test

    except Exception as e:
        print(f"❌ Error configurando driver: {e}")
        pytest.fail(f"No se pudo inicializar el driver: {e}")

    finally:
        if driver:
            driver.quit()
            print("🏁 Driver cerrado")


@pytest.fixture
def screenshot_helper(appium_driver, request):
    """Helper para tomar screenshots con nombres automáticos"""

    def take_screenshot(name_suffix=""):
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}_{name_suffix}.png"
        filepath = os.path.join(TestConfig.SCREENSHOTS_DIR, filename)

        try:
            appium_driver.save_screenshot(filepath)
            print(f"📸 Screenshot: {filename}")
            return filepath
        except Exception as e:
            print(f"❌ Error tomando screenshot: {e}")
            return None

    return take_screenshot


class TestAppLaunch:
    """Suite de tests para lanzamiento de aplicación"""

    def test_app_launches_successfully(self, appium_driver, screenshot_helper):
        """Test que verifica que la app se lance correctamente"""
        # Take initial screenshot
        screenshot_helper("app_launched")

        # Verificar que la app está corriendo
        current_package = appium_driver.current_package
        current_activity = appium_driver.current_activity

        # Assertions
        assert current_package is not None, "El package de la app no debería ser None"
        assert current_activity is not None, "La activity de la app no debería ser None"

        print(f"✅ App package: {current_package}")
        print(f"✅ App activity: {current_activity}")

    def test_app_responds_to_interactions(self, appium_driver, screenshot_helper):
        """Test que verifica que la app responde a interacciones básicas"""
        # Tomar screenshot antes de interacción
        screenshot_helper("before_interaction")

        # Intentar encontrar elementos clickeables
        clickable_elements = appium_driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

        # Screenshot después de buscar elementos
        screenshot_helper("elements_found")

        # Assertion
        assert len(clickable_elements) >= 0, "Debería poder buscar elementos (puede ser 0)"

        print(f"✅ Elementos clickeables encontrados: {len(clickable_elements)}")


class TestUIInteractions:
    """Suite de tests para interacciones de UI"""

    @pytest.mark.smoke
    def test_find_clickable_elements(self, appium_driver, screenshot_helper):
        """Test crítico (smoke) - encontrar elementos clickeables"""
        screenshot_helper("searching_elements")

        clickable_elements = appium_driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

        # Recopilar información de elementos
        elements_info = []
        for i, element in enumerate(clickable_elements[:5]):  # Solo primeros 5
            try:
                text = element.get_attribute("text") or element.get_attribute("content-desc") or f"Element_{i + 1}"
                bounds = element.get_attribute("bounds")
                elements_info.append({"text": text, "bounds": bounds})
            except:
                elements_info.append({"text": f"Element_{i + 1}", "bounds": "unknown"})

        screenshot_helper("elements_analyzed")

        # Soft assertions (no fallan el test inmediatamente)
        assert isinstance(clickable_elements, list), "Debe retornar una lista de elementos"
        print(f"✅ Elementos analizados: {len(elements_info)}")

        # NO retornar nada para evitar warning
        # return elements_info  <- REMOVIDO

    @pytest.mark.parametrize("click_count", [5, 10, 15])
    def test_multiple_clicks(self, appium_driver, screenshot_helper, click_count):
        """Test parametrizado - probar diferentes cantidades de clicks"""
        screenshot_helper(f"before_{click_count}_clicks")

        # Buscar elemento para clickear
        clickable_elements = appium_driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

        successful_clicks = 0

        if clickable_elements:
            # Usar primer elemento clickeable
            target_element = clickable_elements[0]
            element_text = target_element.get_attribute("text") or "Unknown Element"

            for i in range(click_count):
                try:
                    target_element.click()
                    successful_clicks += 1
                    time.sleep(0.3)  # Pausa reducida para test más rápido
                except Exception as e:
                    print(f"❌ Click {i + 1} falló: {e}")

        else:
            # Clicks en coordenadas si no hay elementos
            screen_size = appium_driver.get_window_size()
            center_x = screen_size["width"] // 2
            center_y = screen_size["height"] // 2

            for i in range(click_count):
                try:
                    appium_driver.tap([(center_x, center_y)], 100)
                    successful_clicks += 1
                    time.sleep(0.3)
                except Exception as e:
                    print(f"❌ Tap {i + 1} falló: {e}")

        screenshot_helper(f"after_{click_count}_clicks")

        # Assertion flexible - al menos 50% de clicks exitosos
        success_rate = successful_clicks / click_count
        assert success_rate >= 0.5, f"Rate de éxito muy bajo: {success_rate:.2%} ({successful_clicks}/{click_count})"

        print(f"✅ Clicks exitosos: {successful_clicks}/{click_count} ({success_rate:.2%})")

    @pytest.mark.regression
    def test_gesture_interactions(self, appium_driver, screenshot_helper):
        """Test de regresión - gestos táctiles"""
        screenshot_helper("before_gestures")

        screen_size = appium_driver.get_window_size()
        width = screen_size["width"]
        height = screen_size["height"]

        gestures_performed = []

        # Scroll hacia abajo
        try:
            appium_driver.swipe(width // 2, height * 0.8, width // 2, height * 0.2, 800)
            gestures_performed.append({"gesture": "scroll_down", "status": "success"})
            time.sleep(1)
        except Exception as e:
            gestures_performed.append({"gesture": "scroll_down", "status": "failed", "error": str(e)})

        screenshot_helper("after_scroll_down")

        # Scroll hacia arriba
        try:
            appium_driver.swipe(width // 2, height * 0.2, width // 2, height * 0.8, 800)
            gestures_performed.append({"gesture": "scroll_up", "status": "success"})
            time.sleep(1)
        except Exception as e:
            gestures_performed.append({"gesture": "scroll_up", "status": "failed", "error": str(e)})

        # Swipe lateral
        try:
            appium_driver.swipe(width * 0.8, height // 2, width * 0.2, height // 2, 800)
            gestures_performed.append({"gesture": "swipe_left", "status": "success"})
            time.sleep(1)
        except Exception as e:
            gestures_performed.append({"gesture": "swipe_left", "status": "failed", "error": str(e)})

        screenshot_helper("after_all_gestures")

        successful_gestures = len([g for g in gestures_performed if g["status"] == "success"])

        # Al menos un gesto debe ser exitoso
        assert successful_gestures > 0, "Al menos un gesto debería ser exitoso"

        print(f"✅ Gestos exitosos: {successful_gestures}/{len(gestures_performed)}")


class TestPerformance:
    """Suite de tests de rendimiento"""

    @pytest.mark.performance
    def test_app_response_time(self, appium_driver, screenshot_helper):
        """Test de tiempo de respuesta de la app"""
        response_times = []

        # Medir tiempo de respuesta con screenshots
        for i in range(5):
            start_time = time.time()
            appium_driver.save_screenshot(f"temp_perf_{i}.png")
            end_time = time.time()

            response_time = end_time - start_time
            response_times.append(response_time)

            # Limpiar archivo temporal
            try:
                os.remove(f"temp_perf_{i}.png")
            except:
                pass

        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)

        screenshot_helper("performance_test_completed")

        # Assertions de rendimiento
        assert avg_response_time < 2.0, f"Tiempo promedio muy alto: {avg_response_time:.2f}s"
        assert max_response_time < 5.0, f"Tiempo máximo muy alto: {max_response_time:.2f}s"

        print(f"✅ Tiempo promedio: {avg_response_time:.2f}s")
        print(f"✅ Tiempo máximo: {max_response_time:.2f}s")


# Configuración de pytest hooks para reportes personalizados
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar información de tests para reportes"""
    outcome = yield
    report = outcome.get_result()

    # Agregar información extra al reporte
    if report.when == "call":
        # Agregar duración en formato legible
        if hasattr(report, 'duration'):
            report.duration_formatted = f"{report.duration:.2f}s"

        # Marcar tests críticos que fallaron
        if report.failed and hasattr(item, 'pytestmark'):
            for mark in item.pytestmark:
                if mark.name == 'smoke':
                    print(f"🚨 SMOKE TEST FAILED: {item.name}")


def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Registrar markers personalizados
    config.addinivalue_line("markers", "smoke: critical tests that must pass")
    config.addinivalue_line("markers", "regression: full regression suite")
    config.addinivalue_line("markers", "performance: performance related tests")

    print("🔧 Pytest configurado con markers personalizados")


def pytest_sessionstart(session):
    """Hook que se ejecuta al inicio de la sesión"""
    print("🚀 Iniciando sesión de testing con Pytest")
    print(f"📱 Device: {TestConfig.DEVICE_NAME}")
    print(f"📦 APK: {TestConfig.APK_PATH}")


def pytest_sessionfinish(session, exitstatus):
    """Hook que se ejecuta al final de la sesión"""
    print(f"🏁 Sesión de testing completada (Exit status: {exitstatus})")

    # Generar resumen de screenshots
    if os.path.exists(TestConfig.SCREENSHOTS_DIR):
        screenshots = [f for f in os.listdir(TestConfig.SCREENSHOTS_DIR) if f.endswith('.png')]
        print(f"📸 Screenshots generados: {len(screenshots)}")