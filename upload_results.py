import os
import json
import requests
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PROJECT_KEY = os.getenv("PROJECT_KEY", "APPTEST")
RESULT_FILE = "resultado.xml"

# 1. Autenticación en Xray
auth_url = "https://xray.cloud.getxray.app/api/v2/authenticate"
auth_payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}
auth_headers = {"Content-Type": "application/json"}

print("🔑 Generando token de autenticación...")
token_response = requests.post(auth_url, headers=auth_headers, data=json.dumps(auth_payload))

if token_response.status_code != 200:
    print("❌ Error al autenticar:", token_response.text)
    exit(1)

token = token_response.json()
print("✅ Token generado.")

# 2. Subir resultados JUnit
upload_url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={PROJECT_KEY}"
upload_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/xml"
}

print(f"⬆️ Subiendo resultados a Xray (proyecto {PROJECT_KEY})...")
with open(RESULT_FILE, "rb") as f:
    r = requests.post(upload_url, headers=upload_headers, data=f)

print("📡 Respuesta de Xray:", r.status_code)
print(r.text)
