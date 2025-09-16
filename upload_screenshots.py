import os
import base64
import requests
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("❌ No se encontraron CLIENT_ID o CLIENT_SECRET en el archivo .env")

# 1. Autenticación en Xray
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

# 2. Mapear tests con screenshots
tests = {
    "APPTEST-10": "pytest_screenshots/test_01_click_registrarme_test_01_final_20250915_113356.png",
    "APPTEST-11": "pytest_screenshots/test_02_go_back_with_phone_button_test_02_final_20250915_113408.png",
    "APPTEST-12": "pytest_screenshots/test_03_click_iniciar_sesion_test_03_final_20250915_113432.png",
    "APPTEST-13": "pytest_screenshots/test_04_escribir_email_y_continuar_test_04_final_20250915_113454.png",
    "APPTEST-14": "pytest_screenshots/test_05_click_usuario_y_contrasena_test_06_final_20250915_113458.png",
    "APPTEST-15": "pytest_screenshots/test_06_escribir_usuario_y_contrasena_test_06_final_20250915_113524.png",
    "APPTEST-16": "pytest_screenshots/test_07_flujo_completo_productos_y_salir_test_07_final_20250915_113550.png",
    "APPTEST-17": "pytest_screenshots/test_debug_current_screen_test_05_final_20250915_113556.png",
}

# 3. Construir payload para Xray
xray_payload = {
    "testExecutionKey": "APPTEST-9",  # ejecución que ya subiste
    "tests": []
}

for issue_key, screenshot in tests.items():
    if not os.path.exists(screenshot):
        print(f"⚠️ No se encontró {screenshot}, lo salto")
        continue

    with open(screenshot, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    test_entry = {
        "testKey": issue_key,
        "status": "PASSED",
        "evidences": [
            {
                "data": encoded,
                "filename": os.path.basename(screenshot),
                "contentType": "image/png"
            }
        ]
    }
    xray_payload["tests"].append(test_entry)

# 4. Subir a Xray
print("⬆️ Subiendo resultados y screenshots a Xray...")
resp = requests.post(
    "https://xray.cloud.getxray.app/api/v2/import/execution",
    headers=headers,
    json=xray_payload
)

print(f"📡 Respuesta de Xray: {resp.status_code}")
print(resp.text)
