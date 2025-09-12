# conftest.py - Configuración global de pytest (VERSIÓN CORREGIDA)
import pytest
import os
import json
import logging
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestEnvironment:
    """Clase para manejar configuración del entorno de testing"""

    def __init__(self):
        # CAMBIAR ESTA RUTA POR LA TUYA:
        self.apk_path = r"C:\Users\smora\Documents\PDC\flutter-poc\demo_appium\build\app\outputs\flutter-apk\app-release.apk"
        self.appium_server = "http://127.0.0.1:4723"
        self.device_name = "emulator-5554"
        self.platform_name = "Android"
        self.automation_name = "UiAutomator2"

        # Directorios
        self.screenshots_dir = "pytest_screenshots"
        self.reports_dir = "pytest_reports"
        self.logs_dir = "pytest_logs"

        # Timeouts
        self.implicit_wait = 10
        self.explicit_wait = 15
        self.command_timeout = 60

    def create_directories(self):
        """Crear directorios necesarios"""
        dirs = [self.screenshots_dir, self.reports_dir, self.logs_dir]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Directorios creados: {', '.join(dirs)}")


# Instancia global del entorno
test_env = TestEnvironment()


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Fixture automático que se ejecuta una vez por sesión completa"""
    logger.info("🚀 Configurando entorno de testing...")

    # Crear directorios
    test_env.create_directories()

    # Verificar que Appium server esté corriendo
    import requests
    try:
        response = requests.get(f"{test_env.appium_server}/status", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Appium server está corriendo")
        else:
            logger.warning("⚠️ Appium server responde pero con status no-200")
    except requests.exceptions.RequestException:
        logger.error("❌ Appium server no está disponible")
        pytest.exit("Appium server no está corriendo. Inicia: 'appium'")

    # Verificar que el APK existe
    if not os.path.exists(test_env.apk_path):
        logger.error(f"❌ APK no encontrado: {test_env.apk_path}")
        pytest.exit("APK no encontrado. Ejecuta: 'flutter build apk --release'")

    logger.info("✅ Entorno de testing configurado correctamente")

    yield test_env  # Esto es lo que reciben las demás fixtures

    # Cleanup después de todos los tests
    logger.info("🧹 Limpieza final del entorno de testing")


@pytest.fixture(scope="function")
def driver(setup_test_environment):
    """Fixture principal para crear driver de Appium por cada test"""
    logger.info("🚀 Iniciando driver de Appium...")

    options = UiAutomator2Options()
    options.platform_name = test_env.platform_name
    options.device_name = test_env.device_name
    options.app = test_env.apk_path
    options.automation_name = test_env.automation_name
    options.new_command_timeout = test_env.command_timeout
    options.no_reset = True
    options.full_reset = False

    # Capacidades adicionales para mejor estabilidad
    options.auto_grant_permissions = True
    options.no_sign = True

    driver_instance = None
    try:
        driver_instance = webdriver.Remote(test_env.appium_server, options=options)
        driver_instance.implicitly_wait(test_env.implicit_wait)

        # Esperar que la app cargue
        import time
        time.sleep(3)

        logger.info("✅ Driver iniciado correctamente")
        yield driver_instance

    except Exception as e:
        logger.error(f"❌ Error iniciando driver: {e}")
        pytest.fail(f"No se pudo inicializar el driver: {e}")

    finally:
        if driver_instance:
            try:
                driver_instance.quit()
                logger.info("🏁 Driver cerrado correctamente")
            except:
                logger.warning("⚠️ Error cerrando driver")


@pytest.fixture
def screenshot(driver, request):
    """Fixture para tomar screenshots automáticamente"""
    screenshots_taken = []

    def take_screenshot(name=""):
        """Función helper para tomar screenshots"""
        test_name = request.node.name.replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # milisegundos

        if name:
            filename = f"{test_name}_{name}_{timestamp}.png"
        else:
            filename = f"{test_name}_{timestamp}.png"

        filepath = os.path.join(test_env.screenshots_dir, filename)

        try:
            driver.save_screenshot(filepath)
            screenshots_taken.append(filepath)
            logger.info(f"📸 Screenshot: {filename}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error tomando screenshot: {e}")
            return None

    # Tomar screenshot automático al inicio del test
    take_screenshot("test_start")

    yield take_screenshot

    # Tomar screenshot automático al final (especialmente útil si el test falla)
    take_screenshot("test_end")

    logger.info(f"📸 Screenshots tomados para {request.node.name}: {len(screenshots_taken)}")


@pytest.fixture
def test_data():
    """Fixture para cargar datos de test desde archivos JSON"""
    test_data_dir = "test_data"

    def load_data(filename):
        """Cargar datos desde archivo JSON"""
        filepath = os.path.join(test_data_dir, f"{filename}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"⚠️ Archivo de datos no encontrado: {filepath}")
            return {}

    return load_data


@pytest.fixture
def device_info(driver):
    """Fixture para obtener información del dispositivo"""
    try:
        info = {
            "screen_size": driver.get_window_size(),
            "current_package": driver.current_package,
            "current_activity": driver.current_activity,
            "device_time": driver.device_time,
        }

        # Intentar obtener más información si está disponible
        try:
            info["orientation"] = driver.orientation
        except:
            pass

        logger.info(f"📱 Device info: {info}")
        return info
    except Exception as e:
        logger.error(f"❌ Error obteniendo info del dispositivo: {e}")
        return {}


# Hooks de pytest para personalizar comportamiento

def pytest_runtest_setup(item):
    """Hook que se ejecuta antes de cada test"""
    logger.info(f"🧪 Iniciando test: {item.name}")

    # Marcar tiempo de inicio
    item.start_time = datetime.now()


def pytest_runtest_teardown(item):
    """Hook que se ejecuta después de cada test"""
    if hasattr(item, 'start_time'):
        duration = datetime.now() - item.start_time
        logger.info(f"⏱️ Test {item.name} completado en {duration.total_seconds():.2f}s")


def pytest_runtest_makereport(item, call):
    """Hook para personalizar reportes de tests"""
    if call.when == "call":
        # Log resultado del test
        if call.excinfo is None:
            logger.info(f"✅ PASSED: {item.name}")
        else:
            logger.error(f"❌ FAILED: {item.name} - {call.excinfo.value}")


def pytest_configure(config):
    """Configuración que se ejecuta al inicio de pytest"""
    # Agregar información al reporte HTML (VERSIÓN CORREGIDA)
    config.metadata = {
        'Project': 'Flutter Appium Testing',
        'Test Environment': test_env.device_name,
        'Appium Server': test_env.appium_server,
        'Platform': test_env.platform_name,
        'APK Path': test_env.apk_path
    }

    logger.info("🔧 Pytest configurado con metadata personalizada")


def pytest_sessionstart(session):
    """Hook al inicio de la sesión de testing"""
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO SESIÓN DE TESTING CON PYTEST")
    logger.info(f"📱 Device: {test_env.device_name}")
    logger.info(f"📦 APK: {test_env.apk_path}")
    logger.info(f"🔗 Appium Server: {test_env.appium_server}")
    logger.info("=" * 60)


def pytest_sessionfinish(session, exitstatus):
    """Hook al final de la sesión de testing"""
    # Recopilar estadísticas
    total_tests = len(session.items) if hasattr(session, 'items') else 0

    logger.info("=" * 60)
    logger.info("🏁 SESIÓN DE TESTING COMPLETADA")
    logger.info(f"📊 Tests totales: {total_tests}")
    logger.info(f"🎯 Exit status: {exitstatus}")

    # Contar screenshots generados
    if os.path.exists(test_env.screenshots_dir):
        screenshots = [f for f in os.listdir(test_env.screenshots_dir) if f.endswith('.png')]
        logger.info(f"📸 Screenshots generados: {len(screenshots)}")

    logger.info("=" * 60)


# Funciones helper globales

def wait_for_element(driver, locator, timeout=15):
    """Helper global para esperar elementos"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located(locator))


def safe_click(element, max_attempts=3):
    """Helper para hacer click seguro con reintentos"""
    for attempt in range(max_attempts):
        try:
            element.click()
            return True
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"❌ Click falló después de {max_attempts} intentos: {e}")
                return False
            logger.warning(f"⚠️ Click falló (intento {attempt + 1}), reintentando...")
            import time
            time.sleep(1)
    return False