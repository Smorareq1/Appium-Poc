# conftest.py - Configuración optimizada para usar solo APK
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
        self.apk_path = r"C:\Users\smora\Documents\Poc\appium-poc\app-release.apk"
        self.appium_server = "http://127.0.0.1:4723"
        self.device_name = "emulator-5554"
        self.platform_name = "Android"
        self.automation_name = "UiAutomator2"

        self.app_package = "com.pdctechco.ffa"
        self.app_activity = ".MainActivity"

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
    logger.info("🚀 Configurando entorno de testing para APK...")

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
        pytest.exit("APK no encontrado. Verifica la ruta en TestEnvironment")

    logger.info("✅ Entorno de testing configurado correctamente")
    yield test_env
    logger.info("🧹 Limpieza final del entorno de testing")


@pytest.fixture(scope="class")
def driver_fresh_install(setup_test_environment):
    """Driver que instala la app desde cero cada vez"""
    logger.info("🚀 Iniciando driver con instalación fresca...")

    options = UiAutomator2Options()
    options.platform_name = test_env.platform_name
    options.device_name = test_env.device_name
    options.app = test_env.apk_path
    options.automation_name = test_env.automation_name
    options.new_command_timeout = test_env.command_timeout

    # Reinstalar app cada vez
    options.no_reset = False
    options.full_reset = True
    options.auto_grant_permissions = True

    driver_instance = None
    try:
        driver_instance = webdriver.Remote(test_env.appium_server, options=options)
        driver_instance.implicitly_wait(test_env.implicit_wait)

        # Esperar que la app cargue
        import time
        time.sleep(3)

        logger.info("✅ Driver iniciado con app instalada")
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


@pytest.fixture(scope="class")
def driver_reuse_app(setup_test_environment):
    """Driver que reutiliza la app ya instalada (más rápido)"""
    logger.info("🚀 Iniciando driver reutilizando app instalada...")

    options = UiAutomator2Options()
    options.platform_name = test_env.platform_name
    options.device_name = test_env.device_name

    # USAR PACKAGE/ACTIVITY en lugar de APK para reutilizar
    options.app_package = test_env.app_package
    options.app_activity = test_env.app_activity

    options.automation_name = test_env.automation_name
    options.new_command_timeout = test_env.command_timeout

    # NO reinstalar
    options.no_reset = True
    options.full_reset = False

    driver_instance = None
    try:
        driver_instance = webdriver.Remote(test_env.appium_server, options=options)
        driver_instance.implicitly_wait(test_env.implicit_wait)

        logger.info("✅ Driver iniciado reutilizando app")
        yield driver_instance

    except Exception as e:
        logger.error(f"❌ Error iniciando driver: {e}")
        # Fallback: intentar con instalación fresca
        logger.info("🔄 Fallback: intentando instalación fresca...")

        options.app = test_env.apk_path
        options.no_reset = False
        options.full_reset = True

        try:
            driver_instance = webdriver.Remote(test_env.appium_server, options=options)
            driver_instance.implicitly_wait(test_env.implicit_wait)
            import time
            time.sleep(3)
            logger.info("✅ Driver iniciado con fallback")
            yield driver_instance
        except Exception as e2:
            pytest.fail(f"No se pudo inicializar el driver ni con fallback: {e2}")

    finally:
        if driver_instance:
            try:
                driver_instance.quit()
                logger.info("🏁 Driver cerrado correctamente")
            except:
                logger.warning("⚠️ Error cerrando driver")


# Alias para compatibilidad con tests existentes
@pytest.fixture(scope="class")
def driver(driver_reuse_app):
    """Fixture principal - usa app reutilizada por defecto"""
    yield driver_reuse_app


@pytest.fixture
def screenshot(driver, request):
    """Fixture para tomar screenshots automáticamente"""
    screenshots_taken = []

    def take_screenshot(name=""):
        """Función helper para tomar screenshots"""
        test_name = request.node.name.replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

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

    yield take_screenshot
    logger.info(f"📸 Screenshots tomados: {len(screenshots_taken)}")


def get_app_package_from_apk(apk_path):
    """Función helper para extraer package name del APK"""
    try:
        import subprocess
        result = subprocess.run([
            'aapt', 'dump', 'badging', apk_path
        ], capture_output=True, text=True)

        for line in result.stdout.split('\n'):
            if line.startswith('package:'):
                # Extraer package name
                package = line.split("name='")[1].split("'")[0]
                return package
    except:
        pass

    return None


def install_app_manually(device_id, apk_path):
    """Función helper para instalar APK manualmente"""
    try:
        import subprocess
        result = subprocess.run([
            'adb', '-s', device_id, 'install', '-r', apk_path
        ], capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"✅ APK instalado manualmente: {apk_path}")
            return True
        else:
            logger.error(f"❌ Error instalando APK: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Error en instalación manual: {e}")
        return False


# Funciones helper mejoradas
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


# Hooks mejorados
def pytest_sessionstart(session):
    """Hook al inicio de la sesión de testing"""
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO TESTING CON APK SOLAMENTE")
    logger.info(f"📱 Device: {test_env.device_name}")
    logger.info(f"📦 APK: {test_env.apk_path}")
    logger.info(f"🔗 Appium Server: {test_env.appium_server}")

    # Intentar detectar package name automáticamente
    detected_package = get_app_package_from_apk(test_env.apk_path)
    if detected_package:
        logger.info(f"📋 Package detectado: {detected_package}")
        test_env.app_package = detected_package
    else:
        logger.warning(f"⚠️ No se pudo detectar package. Usando: {test_env.app_package}")

    logger.info("=" * 60)