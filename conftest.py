import pytest
import os
import logging
import subprocess
import time
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
import requests

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#Clase centralizada para manejar la configuración del entorno de testing
class TestEnvironment:
    def __init__(self):
        self.apk_path = os.getenv('APK_PATH', r"C:\Users\smora\Documents\Poc\appium-poc\app-release.apk")
        self.platform_version = os.getenv('PLATFORM_VERSION', "16")
        self.device_name = os.getenv('DEVICE_NAME', "emulator-5554")
        self.platform_name = "Android"

        self.platform_version = "15"
        self.automation_name = "UiAutomator2"
        self.screenshots_dir = "pytest_screenshots"
        self.reports_dir = "pytest_reports"
        self.logs_dir = "pytest_logs"
        self.implicit_wait = 5
        self.command_timeout = 120


# Instancia global del entorno
test_env = TestEnvironment()

#Función helper para ejecutar comandos ADB y manejar errores
def _run_adb_command(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        pytest.exit(
            "❌ Error: 'adb' no encontrado. Asegúrate de que el SDK de Android (platform-tools) esté en el PATH del sistema."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Falló el comando ADB: {' '.join(command)}\nError: {e.stderr}")
        return None

# Función para verificar que el dispositivo esté listo y autorizado
def check_device_is_ready(device_name, timeout=30):
    logger.info(f"Verificando que el dispositivo '{device_name}' esté listo y autorizado...")
    end_time = time.time() + timeout
    last_known_output = "No se pudo obtener la lista de dispositivos."

    while time.time() < end_time:
        result = _run_adb_command(['adb', 'devices'])
        if result:
            devices_output = result.stdout.strip()
            last_known_output = devices_output
            logger.debug(f"Salida de 'adb devices':\n{devices_output}")

            for line in devices_output.splitlines():
                if device_name in line and 'device' in line:
                    logger.info(f"✅ Dispositivo '{device_name}' está en línea y autorizado.")
                    time.sleep(2)
                    return

        time.sleep(2)

    pytest.exit(
        f"❌ CRÍTICO: El dispositivo '{device_name}' no está listo después de {timeout} segundos.\n"
        f"Última salida de 'adb devices':\n---\n{last_known_output}\n---\n"
        f"Posibles causas:\n"
        f"1. El emulador no está corriendo.\n"
        f"2. El estado es 'unauthorized'. Acepta el diálogo 'Permitir depuración USB' en la pantalla del emulador.\n"
        f"3. El estado es 'offline'. Reinicia el emulador."
    )

# Fixture de configuración del entorno - Se ejecuta UNA VEZ por sesión
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Fixture que se ejecuta UNA VEZ por sesión para preparar todo el entorno."""
    logger.info("=" * 60)
    logger.info("🚀 CONFIGURANDO ENTORNO DE TESTING (UNA SOLA VEZ POR SESIÓN)")

    os.makedirs(test_env.screenshots_dir, exist_ok=True)
    os.makedirs(test_env.reports_dir, exist_ok=True)
    os.makedirs(test_env.logs_dir, exist_ok=True)

    try:
        requests.get(f"{test_env.appium_server}/status", timeout=5)
        logger.info(f"✅ Appium server está corriendo en {test_env.appium_server}")
    except requests.exceptions.RequestException:
        pytest.exit(f"❌ Appium server no disponible en {test_env.appium_server}. Inícialo.")

    if not os.path.exists(test_env.apk_path):
        pytest.exit(f"❌ APK no encontrado en la ruta: {test_env.apk_path}")

    check_device_is_ready(test_env.device_name)

    logger.info("✅ Entorno configurado correctamente.")
    logger.info("=" * 60)
    yield
    logger.info("=" * 60)
    logger.info("🧹 LIMPIEZA FINAL DEL ENTORNO DE TESTING")
    logger.info("=" * 60)


#Smoke test - Valida que el driver se inicie correctamente
@pytest.fixture(scope="session")
def driver(request):
    """Fixture que crea el driver de Appium UNA SOLA VEZ por sesión de pruebas."""
    logger.info("🚀 Iniciando driver de Appium para TODA LA SESIÓN DE PRUEBAS...")

    options = UiAutomator2Options()
    options.platform_name = test_env.platform_name
    options.device_name = test_env.device_name
    options.app = test_env.apk_path  # 👈 Aquí le decimos que use el APK
    options.automation_name = test_env.automation_name
    options.platform_version = test_env.platform_version
    options.new_command_timeout = test_env.command_timeout
    options.auto_grant_permissions = True
    options.full_reset = False
    options.no_reset = True

    driver_instance = None
    try:
        driver_instance = webdriver.Remote(test_env.appium_server, options=options)
        driver_instance.implicitly_wait(test_env.implicit_wait)
        logger.info("✅ Driver iniciado exitosamente. La app se mantendrá abierta.")

        def finalizer():
            if driver_instance:
                try:
                    driver_instance.quit()
                    logger.info("🏁 Driver cerrado correctamente al final de la sesión.")
                except Exception as e:
                    logger.warning(f"⚠️ No se pudo cerrar el driver correctamente: {e}")

        request.addfinalizer(finalizer)

        return driver_instance
    except Exception as e:
        pytest.fail(f"❌ CRÍTICO: No se pudo inicializar el driver de Appium. Error: {e}")

# Fixture para tomar screenshots
@pytest.fixture
def screenshot(request, driver):
    """Fixture para tomar screenshots en puntos clave o al fallar."""

    def take_screenshot(name):
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{name}_{timestamp}.png"
        filepath = os.path.join(test_env.screenshots_dir, filename)

        try:
            driver.save_screenshot(filepath)
            logger.info(f"📸 Screenshot guardado: {filepath}")
        except Exception as e:
            logger.error(f"❌ Error al guardar screenshot '{filename}': {e}")

    return take_screenshot
