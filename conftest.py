import pytest
import os
import logging
import subprocess
import time
import threading
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
import requests
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# Clase centralizada para manejar la configuración del entorno de testing
class TestEnvironment:
    def __init__(self):
        self.apk_path = os.getenv('APK_PATH', r"C:\Users\smora\Documents\Poc\appium-poc\app-release.apk")
        self.platform_version = os.getenv('PLATFORM_VERSION', "15")
        self.device_name = os.getenv('DEVICE_NAME', "emulator-5554")
        self.appium_server = os.getenv('APPIUM_SERVER', "http://127.0.0.1:4723")
        self.platform_name = "Android"
        self.automation_name = "UiAutomator2"
        self.videos_dir = "pytest_videos"
        self.reports_dir = "pytest_reports"
        self.logs_dir = "pytest_logs"
        self.implicit_wait = 5
        self.command_timeout = 120


# Instancia global del entorno
test_env = TestEnvironment()


class VideoRecorder:
    """Clase para manejar la grabación de video durante los tests"""

    def __init__(self, device_name):
        self.device_name = device_name
        self.recording_process = None
        self.video_path_device = None
        self.video_path_local = None
        self.is_recording = False

    def start_recording(self, test_name):
        """Inicia la grabación de video"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.video_path_device = f"/sdcard/{test_name}_{timestamp}.mp4"
        self.video_path_local = os.path.join(test_env.videos_dir, f"{test_name}_{timestamp}.mp4")

        # Comando para grabar video
        cmd = ['adb', '-s', self.device_name, 'shell', 'screenrecord', self.video_path_device]

        try:
            self.recording_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.is_recording = True
            logger.info(f"🎥 Iniciando grabación de video: {self.video_path_device}")
            time.sleep(1)  # Pequeña pausa para asegurar que la grabación inicie
            return True
        except Exception as e:
            logger.error(f"❌ Error al iniciar grabación: {e}")
            return False

    def stop_recording(self):
        """Detiene la grabación y descarga el video"""
        if not self.is_recording or not self.recording_process:
            return None

        try:
            # Terminar la grabación enviando SIGINT (Ctrl+C)
            self.recording_process.terminate()
            self.recording_process.wait(timeout=10)
            self.is_recording = False

            time.sleep(2)  # Esperar que el archivo se guarde completamente

            # Descargar el video del dispositivo
            pull_cmd = ['adb', '-s', self.device_name, 'pull', self.video_path_device, self.video_path_local]
            result = subprocess.run(pull_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Video descargado: {self.video_path_local}")

                # Limpiar el video del dispositivo
                cleanup_cmd = ['adb', '-s', self.device_name, 'shell', 'rm', self.video_path_device]
                subprocess.run(cleanup_cmd, capture_output=True)

                return self.video_path_local
            else:
                logger.error(f"❌ Error al descargar video: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"❌ Error al detener grabación: {e}")
            return None


# Función helper para ejecutar comandos ADB y manejar errores
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

    os.makedirs(test_env.videos_dir, exist_ok=True)
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


# Smoke test - Valida que el driver se inicie correctamente
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


# Fixture para grabar videos
@pytest.fixture
def video_recorder(request, driver):
    """Fixture para grabar video durante la ejecución del test."""

    recorder = VideoRecorder(test_env.device_name)
    test_name = request.node.name
    video_path = None

    # Iniciar grabación al comenzar el test
    if recorder.start_recording(test_name):
        logger.info(f"🎥 Grabación iniciada para el test: {test_name}")
    else:
        logger.warning(f"⚠️ No se pudo iniciar la grabación para: {test_name}")

    def stop_and_save():
        nonlocal video_path
        video_path = recorder.stop_recording()
        if video_path:
            logger.info(f"✅ Video guardado: {video_path}")
        else:
            logger.warning(f"⚠️ No se pudo guardar el video del test: {test_name}")
        return video_path

    # Registrar función para detener grabación al final del test
    request.addfinalizer(stop_and_save)

    # Retornar función para obtener la ruta del video
    return lambda: video_path