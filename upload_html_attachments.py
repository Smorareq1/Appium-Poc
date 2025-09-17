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
    print("❌ Uso: python upload_html_evidence.py APPTEST-XX")
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

# 3. Buscar archivos HTML de evidencia
evidence_dir = "evidence_reports"

if not os.path.exists(evidence_dir):
    print(f"❌ Directorio {evidence_dir} no existe")
    print("💡 Ejecuta primero: python generate_individual_evidence.py")
    sys.exit(1)

# Mapear tests con archivos HTML
tests_mapping = {
    "APPTEST-10": f"{evidence_dir}/APPTEST-10_evidence.html",
    "APPTEST-11": f"{evidence_dir}/APPTEST-11_evidence.html",
    "APPTEST-12": f"{evidence_dir}/APPTEST-12_evidence.html",
    "APPTEST-13": f"{evidence_dir}/APPTEST-13_evidence.html",
    "APPTEST-14": f"{evidence_dir}/APPTEST-14_evidence.html",
    "APPTEST-15": f"{evidence_dir}/APPTEST-15_evidence.html",
    "APPTEST-16": f"{evidence_dir}/APPTEST-16_evidence.html",
    "APPTEST-17": f"{evidence_dir}/APPTEST-17_evidence.html",
}

print("🔍 Verificando archivos de evidencia...")

# 4. Construir payload para Xray (MISMO MÉTODO QUE SCREENSHOTS)
xray_payload = {
    "testExecutionKey": TARGET_EXECUTION,
    "tests": []
}

evidences_found = 0

for issue_key, html_file in tests_mapping.items():
    if not os.path.exists(html_file):
        print(f"⚠️ No se encontró {html_file}, lo salto")
        continue

    file_size = os.path.getsize(html_file)
    print(f"📄 Procesando {issue_key}: {os.path.basename(html_file)} ({file_size / (1024 * 1024):.1f} MB)")

    try:
        # Leer y codificar HTML en base64 (IGUAL QUE SCREENSHOTS)
        with open(html_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        # Crear entrada de test con evidencia (MISMA ESTRUCTURA QUE SCREENSHOTS)
        test_entry = {
            "testKey": issue_key,
            "evidences": [
                {
                    "data": encoded,
                    "filename": os.path.basename(html_file),
                    "contentType": "text/html"  # Cambio principal: HTML en lugar de image/png
                }
            ]
        }
        xray_payload["tests"].append(test_entry)
        evidences_found += 1
        print(f"   ✅ {issue_key} agregado al payload")

    except Exception as e:
        print(f"   ❌ Error procesando {issue_key}: {e}")

if evidences_found == 0:
    print("❌ No se encontraron evidencias para subir")
    sys.exit(1)

# 5. Subir a Xray usando EXACTAMENTE EL MISMO ENDPOINT QUE SCREENSHOTS
print(f"⬆️ Subiendo {evidences_found} evidencias HTML a Xray en {TARGET_EXECUTION}...")
print("⏳ Esto puede tomar varios minutos debido al tamaño de los archivos HTML...")

try:
    resp = requests.post(
        "https://xray.cloud.getxray.app/api/v2/import/execution",  # MISMO ENDPOINT
        headers=headers,  # MISMOS HEADERS
        json=xray_payload,  # MISMO FORMATO
        timeout=300  # 5 minutos timeout para archivos grandes
    )

    print(f"📡 Respuesta de Xray: {resp.status_code}")

    if resp.status_code == 200:
        print("✅ Evidencias HTML subidas exitosamente!")
        print(resp.text)

        print(f"\n🎉 {evidences_found} evidencias HTML disponibles en Test Execution: {TARGET_EXECUTION}")
        print("💡 Ve a Xray Cloud para ver las evidencias HTML adjuntas a cada test")

    else:
        print(f"❌ Error al subir evidencias: {resp.text}")

except requests.exceptions.Timeout:
    print("⏰ Timeout al subir evidencias HTML. Los archivos pueden ser muy grandes.")
    print("💡 Considera reducir el tamaño de los videos embebidos.")
except Exception as e:
    print(f"❌ Error al subir a Xray: {e}")

# 6. Resumen
print("\n" + "=" * 50)
print("📊 RESUMEN DE SUBIDA DE EVIDENCIAS HTML")
print("=" * 50)
print(f"📁 Evidencias procesadas: {evidences_found}")
print(f"🎯 Test Execution: {TARGET_EXECUTION}")
print(f"📡 Método usado: Xray Import Execution API (igual que screenshots)")

if resp.status_code == 200:
    print("✅ Estado: EXITOSO")
    print("💡 Las evidencias HTML aparecerán como attachments en cada test")
else:
    print("❌ Estado: ERROR")
    print("💡 Revisa los mensajes de error arriba")