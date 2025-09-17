import os
import sys
import base64
import requests
import glob
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ No se encontraron CLIENT_ID o CLIENT_SECRET en el archivo .env")

# 1. Leer parámetro de ejecución desde la consola
if len(sys.argv) < 2:
    print("❌ Uso: python upload_videos_xray_format.py APPTEST-XX")
    sys.exit(1)

TARGET_EXECUTION = sys.argv[1]

# 2. Autenticación en Xray
print("🔑 Generando token de autenticación...")
auth_resp = requests.post(
    "https://xray.cloud.getxray.app/api/v2/authenticate",
    json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
)

if auth_resp.status_code != 200:
    raise RuntimeError(f"❌ Error al autenticar: {auth_resp.status_code} - {auth_resp.text}")

token = auth_resp.text.strip('"')
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print("✅ Token generado.")

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
    pattern = f"{videos_dir}/{test_name}_*.mp4"
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

# 5. Construir payload usando formato JSON oficial de Xray
print("📝 Construyendo payload según formato JSON oficial de Xray...")

# Estructura JSON según documentación oficial
xray_payload = {
    "testExecutionKey": TARGET_EXECUTION,
    "tests": []
}

videos_procesados = 0
videos_fallidos = 0

for issue_key, video_path in videos_encontrados.items():
    if not os.path.exists(video_path):
        print(f"⚠️ Archivo {video_path} no existe, saltando...")
        videos_fallidos += 1
        continue

    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)

    print(f"📹 Procesando {issue_key}: {os.path.basename(video_path)} ({file_size_mb:.1f} MB)")

    # Verificar tamaño del archivo (limite razonable para base64)
    if file_size > 50 * 1024 * 1024:  # 50MB
        print(f"   ⚠️ Archivo muy grande ({file_size_mb:.1f} MB), saltando...")
        print(f"   💡 Considera usar endpoint multipart para archivos > 50MB")
        videos_fallidos += 1
        continue

    try:
        # Leer y codificar video en base64
        with open(video_path, "rb") as video_file:
            video_base64 = base64.b64encode(video_file.read()).decode("utf-8")

        # Crear objeto test según formato oficial Xray JSON
        test_entry = {
            "testKey": issue_key,
            "evidence": [  # Nota: "evidence" no "evidences"
                {
                    "data": video_base64,
                    "filename": os.path.basename(video_path),
                    "contentType": "video/mp4"
                }
            ]
        }

        xray_payload["tests"].append(test_entry)
        videos_procesados += 1
        print(f"   ✅ {issue_key} agregado al payload")

    except Exception as e:
        print(f"   ❌ Error procesando {issue_key}: {e}")
        videos_fallidos += 1

if videos_procesados == 0:
    print("❌ No se procesaron videos para subir")
    sys.exit(1)

# 6. Subir usando endpoint oficial /api/v2/import/execution
print(f"⬆️ Subiendo {videos_procesados} videos usando formato JSON oficial de Xray...")
print(f"🎯 Test Execution: {TARGET_EXECUTION}")
print("⏳ Esto puede tomar varios minutos debido al tamaño de los videos...")

try:
    # Usar EXACTAMENTE el mismo endpoint que funciona para screenshots
    response = requests.post(
        "https://xray.cloud.getxray.app/api/v2/import/execution",
        headers=headers,
        json=xray_payload,
        timeout=300  # 5 minutos para archivos grandes
    )

    print(f"📡 Respuesta de Xray: {response.status_code}")

    if response.status_code == 200:
        print("✅ Videos subidos exitosamente como evidencias!")
        print(f"📊 Respuesta: {response.text}")

        print(f"\n🎉 {videos_procesados} videos disponibles como evidencias en Test Execution: {TARGET_EXECUTION}")
        print("💡 Ve a Xray Cloud para ver los videos adjuntos a cada test")

    elif response.status_code == 400:
        print("❌ Error 400: Formato de datos incorrecto")
        print(f"📄 Respuesta completa: {response.text}")
        print("\n💡 Posibles causas:")
        print("   • contentType 'video/mp4' no soportado")
        print("   • Archivos muy grandes para base64")
        print("   • Estructura JSON incorrecta")
        print("   • Límites de tamaño de Xray Cloud")

    elif response.status_code == 413:
        print("❌ Error 413: Payload muy grande")
        print("💡 Solución: Usar endpoint multipart para archivos grandes")

    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except requests.exceptions.Timeout:
    print("⏰ Timeout al subir videos")
    print("💡 Los archivos son muy grandes para el método JSON con base64")
    print("💡 Considera usar el endpoint multipart")

except Exception as e:
    print(f"❌ Error al subir: {e}")

# 7. Resumen final
print("\n" + "=" * 60)
print("📊 RESUMEN DE SUBIDA DE VIDEOS")
print("=" * 60)
print(f"📁 Videos encontrados: {len(videos_encontrados)}")
print(f"✅ Videos procesados: {videos_procesados}")
print(f"❌ Videos fallidos: {videos_fallidos}")
print(f"🎯 Test Execution: {TARGET_EXECUTION}")
print(f"📡 Método: Xray JSON Format (/api/v2/import/execution)")

if response.status_code == 200:
    print("🎉 Estado: EXITOSO")
else:
    print("❌ Estado: ERROR")
    print("\n💡 Alternativas si falla:")
    print("   1. Usar endpoint multipart para archivos grandes")
    print("   2. Convertir videos a formato más pequeño")
    print("   3. Subir screenshots PNG en lugar de videos")
    print("   4. Comprimir videos antes de subir")
    print("   5. Verificar límites de tamaño de Xray Cloud")