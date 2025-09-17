import os
import sys
import requests
import glob
import json
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ No se encontraron CLIENT_ID o CLIENT_SECRET en el archivo .env")

# 1. Leer parámetro de ejecución desde la consola
if len(sys.argv) < 2:
    print("❌ Uso: python upload_videos_multipart.py APPTEST-XX")
    sys.exit(1)

TARGET_EXECUTION = sys.argv[1]

# 2. Autenticación en Xray
print("🔑 Generando token de autenticación...")
try:
    auth_resp = requests.post(
        "https://xray.cloud.getxray.app/api/v2/authenticate",
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    )
    auth_resp.raise_for_status()  # Lanza una excepción para códigos de error HTTP
    token = auth_resp.json()
    print("✅ Token generado.")
except requests.exceptions.RequestException as e:
    print(f"❌ Error al autenticar: {e}")
    if 'auth_resp' in locals():
        print(f"📄 Respuesta del servidor: {auth_resp.text}")
    sys.exit(1)

# 3. Buscar videos automáticamente en la carpeta pytest_videos
videos_dir = "pytest_videos"
tests_mapping = {
    "test_01_click_registrarme": "APPTEST-10",
    "test_02_go_back_with_phone_button": "APPTEST-11",
    "test_03_click_iniciar_sesion": "APPTEST-12",
    "test_04_escribir_email_y_continuar": "APPTEST-13",
    "test_05_click_usuario_y_contrasena": "APPTEST-14",
    "test_06_escribir_usuario_y_contrasena": "APPTEST-15",
    "test_07_flujo_completo_productos_y_salir": "APPTEST-16",
    "test_debug_current_screen": "APPTEST-17"
}

print("🔍 Buscando videos en la carpeta pytest_videos...")

# 4. Buscar videos y mapearlos con tests
videos_encontrados = {}
for test_name, issue_key in tests_mapping.items():
    pattern = os.path.join(videos_dir, f"{test_name}_*.mp4")
    matching_files = glob.glob(pattern)

    if matching_files:
        latest_video = max(matching_files, key=os.path.getmtime)
        videos_encontrados[issue_key] = latest_video
        print(f"✅ {issue_key}: {latest_video}")
    else:
        print(f"⚠️ No se encontró video para {test_name}")

if not videos_encontrados:
    print("❌ No se encontraron videos para subir.")
    sys.exit(1)

# 5. Crear JSON de metadatos y preparar archivos para multipart
print("📝 Creando JSON de metadatos y preparando archivos...")

xray_metadata = {
    "testExecutionKey": TARGET_EXECUTION,
    "tests": []
}

multipart_files = []
videos_procesados = 0
videos_fallidos = 0

for issue_key, video_path in videos_encontrados.items():
    if not os.path.exists(video_path):
        print(f"⚠️ Archivo {video_path} no existe, saltando...")
        videos_fallidos += 1
        continue

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"📹 Procesando {issue_key}: {os.path.basename(video_path)} ({file_size_mb:.1f} MB)")

    video_filename = os.path.basename(video_path)

    test_entry = {
        "testKey": issue_key,
        "status": "EXECUTING",
        "evidence": [
            {
                "filename": video_filename,
                "contentType": "video/mp4"
            }
        ]
    }
    xray_metadata["tests"].append(test_entry)

    try:
        # El nombre del campo para los archivos debe ser 'evidence'
        video_file_tuple = ('evidence', (video_filename, open(video_path, 'rb'), 'video/mp4'))
        multipart_files.append(video_file_tuple)
        videos_procesados += 1
        print(f"   ✅ {issue_key} preparado para subir con el nombre {video_filename}")
    except Exception as e:
        print(f"   ❌ Error procesando {issue_key}: {e}")
        videos_fallidos += 1

if videos_procesados == 0:
    print("❌ No se procesaron videos para subir")
    sys.exit(1)

# 6. Preparar datos multipart
headers = {
    "Authorization": f"Bearer {token}"
}
# CAMBIO CLAVE: El JSON se envía en el parámetro 'data'
form_data = {
    'info': json.dumps(xray_metadata)
}

# 7. Subir usando endpoint multipart oficial
print(f"⬆️ Subiendo {videos_procesados} videos usando endpoint MULTIPART...")
print(f"🎯 Test Execution: {TARGET_EXECUTION}")
print("⏳ Esto puede tomar varios minutos debido al tamaño de los videos...")

try:
    multipart_url = "https://xray.cloud.getxray.app/api/v2/import/execution/multipart"

    # CAMBIO CLAVE: Se usan los parámetros 'data' y 'files' por separado
    response = requests.post(
        multipart_url,
        headers=headers,
        data=form_data,
        files=multipart_files,
        timeout=600
    )

    print(f"📡 Respuesta de Xray: {response.status_code}")

    if response.status_code == 200:
        print("✅ ¡Videos subidos exitosamente usando multipart!")
        print(f"📊 Respuesta: {response.json()}")
        print(f"\n🎉 {videos_procesados} videos disponibles como evidencias en Test Execution: {TARGET_EXECUTION}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except requests.exceptions.Timeout:
    print("⏰ Timeout al subir videos multipart. Los archivos pueden ser muy grandes.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado durante la subida: {e}")
finally:
    print("🧹 Cerrando archivos...")
    for _, file_tuple in multipart_files:
        try:
            file_tuple[1].close()
        except:
            pass

# 8. Resumen final
print("\n" + "=" * 60)
print("📊 RESUMEN DE SUBIDA DE VIDEOS MULTIPART")
print("=" * 60)
print(f"📁 Videos encontrados: {len(videos_encontrados)}")
print(f"✅ Videos procesados: {videos_procesados}")
print(f"❌ Videos fallidos: {videos_fallidos}")
print(f"🎯 Test Execution: {TARGET_EXECUTION}")
print(f"📡 Método: Xray Multipart (/api/v2/import/execution/multipart)")

if 'response' in locals() and response.status_code == 200:
    print("🎉 Estado: EXITOSO")
else:
    print("❌ Estado: ERROR")

