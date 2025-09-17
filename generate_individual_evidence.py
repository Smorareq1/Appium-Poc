import os
import sys
import glob
import base64
from datetime import datetime
from pathlib import Path


def generate_individual_html_reports(execution_key=None):
    """Genera un HTML individual para cada test con su video embebido"""

    videos_dir = "pytest_videos"
    evidence_dir = "evidence_reports"

    # Crear directorio para evidencias individuales
    os.makedirs(evidence_dir, exist_ok=True)

    # Mapeo de tests
    tests_mapping = {
        "test_01_click_registrarme": {"key": "APPTEST-10", "name": "Click en Registrarme"},
        "test_02_go_back_with_phone_button": {"key": "APPTEST-11", "name": "Botón atrás del teléfono"},
        "test_03_click_iniciar_sesion": {"key": "APPTEST-12", "name": "Click en Iniciar sesión"},
        "test_04_escribir_email_y_continuar": {"key": "APPTEST-13", "name": "Escribir email y continuar"},
        "test_05_click_usuario_y_contrasena": {"key": "APPTEST-14", "name": "Click en Usuario y contraseña"},
        "test_06_escribir_usuario_y_contrasena": {"key": "APPTEST-15", "name": "Escribir usuario y contraseña"},
        "test_07_flujo_completo_productos_y_salir": {"key": "APPTEST-16", "name": "Flujo completo productos y salir"},
        "test_debug_current_screen": {"key": "APPTEST-17", "name": "Debug current screen"}
    }

    print(f"📁 Generando evidencias individuales en: {evidence_dir}/")
    if execution_key:
        print(f"🎯 Para Test Execution: {execution_key}")

    generated_files = []

    # Buscar videos y generar HTML individual para cada uno
    for test_name, test_info in tests_mapping.items():
        pattern = f"{videos_dir}/{test_name}_*.mp4"
        matching_files = glob.glob(pattern)

        if not matching_files:
            print(f"⚠️ No se encontró video para {test_info['key']}")
            continue

        # Tomar el video más reciente
        video_path = max(matching_files, key=os.path.getmtime)
        video_size = os.path.getsize(video_path)

        print(f"📹 Procesando {test_info['key']}: {os.path.basename(video_path)} ({video_size / (1024 * 1024):.1f} MB)")

        # Nombre del archivo HTML individual
        html_filename = f"{test_info['key']}_evidence.html"
        html_path = os.path.join(evidence_dir, html_filename)

        try:
            # Leer y codificar video en base64
            with open(video_path, "rb") as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

            # Generar HTML individual
            html_content = generate_single_test_html(
                test_info['key'],
                test_info['name'],
                video_path,
                video_base64,
                video_size,
                execution_key
            )

            # Escribir archivo HTML
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            generated_files.append({
                'test_key': test_info['key'],
                'html_path': html_path,
                'video_path': video_path,
                'size': os.path.getsize(html_path)
            })

            print(f"  ✅ Generado: {html_filename} ({os.path.getsize(html_path) / (1024 * 1024):.1f} MB)")

        except Exception as e:
            print(f"  ❌ Error procesando {test_info['key']}: {e}")
            # Crear versión simple sin video embebido
            html_content = generate_fallback_html(
                test_info['key'],
                test_info['name'],
                video_path,
                execution_key
            )

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            generated_files.append({
                'test_key': test_info['key'],
                'html_path': html_path,
                'video_path': video_path,
                'size': os.path.getsize(html_path)
            })

            print(f"  ⚠️ Generado versión fallback: {html_filename}")

    print(f"\n✅ Generados {len(generated_files)} archivos de evidencia")
    return generated_files


def generate_single_test_html(test_key, test_name, video_path, video_base64, video_size, execution_key):
    """Genera HTML para un test individual con video embebido"""

    video_filename = os.path.basename(video_path)
    video_timestamp = datetime.fromtimestamp(os.path.getmtime(video_path))

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidencia - {test_key}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .test-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .test-title {{
            margin: 0;
            font-size: 2em;
            font-weight: 300;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .meta-item {{
            text-align: center;
        }}
        .meta-label {{
            color: #6c757d;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        .meta-value {{
            font-weight: bold;
            color: #495057;
        }}
        .video-section {{
            padding: 30px;
            text-align: center;
        }}
        .video-wrapper {{
            background: #000;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }}
        video {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .controls {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
        }}
        .btn:hover {{
            background: #0056b3;
            transform: translateY(-2px);
        }}
        .btn.secondary {{
            background: #6c757d;
        }}
        .btn.secondary:hover {{
            background: #545b62;
        }}
        .footer {{
            background: #f8f9fa;
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #dee2e6;
        }}
        .status-pass {{
            color: #28a745;
            font-weight: bold;
        }}
        @media (max-width: 768px) {{
            .controls {{
                flex-direction: column;
                align-items: center;
            }}
            .btn {{
                width: 200px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="test-badge">{test_key}</div>
            <h1 class="test-title">{test_name}</h1>
            <div style="margin-top: 10px; opacity: 0.9;">
                Evidencia de Ejecución Automatizada
                {f'• Test Execution: {execution_key}' if execution_key else ''}
            </div>
        </div>

        <div class="metadata">
            <div class="meta-grid">
                <div class="meta-item">
                    <div class="meta-label">📊 Estado</div>
                    <div class="meta-value status-pass">EJECUTADO</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">📁 Archivo</div>
                    <div class="meta-value">{video_filename}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">📏 Tamaño</div>
                    <div class="meta-value">{video_size / (1024 * 1024):.1f} MB</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">🕒 Ejecutado</div>
                    <div class="meta-value">{video_timestamp.strftime('%d/%m/%Y %H:%M')}</div>
                </div>
            </div>
        </div>

        <div class="video-section">
            <h3 style="color: #495057; margin-bottom: 20px;">📹 Video de Evidencia</h3>
            <div class="video-wrapper">
                <video id="evidenceVideo" controls preload="metadata">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    Tu navegador no soporta la reproducción de video.
                </video>
            </div>

            <div class="controls">
                <button class="btn" onclick="playVideo()">▶️ Reproducir</button>
                <button class="btn" onclick="pauseVideo()">⏸️ Pausar</button>
                <button class="btn" onclick="restartVideo()">🔄 Reiniciar</button>
                <button class="btn secondary" onclick="downloadVideo()">💾 Descargar Video</button>
            </div>
        </div>

        <div class="footer">
            Evidencia generada automáticamente por pytest + Appium<br>
            🤖 Framework de Testing Mobile | 📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>

    <script>
        const video = document.getElementById('evidenceVideo');

        function playVideo() {{
            video.play();
        }}

        function pauseVideo() {{
            video.pause();
        }}

        function restartVideo() {{
            video.currentTime = 0;
            video.play();
        }}

        function downloadVideo() {{
            const a = document.createElement('a');
            a.href = video.src;
            a.download = '{video_filename}';
            a.click();
        }}

        // Configuración adicional del video
        video.addEventListener('loadedmetadata', function() {{
            console.log('Video cargado - Duración:', video.duration, 'segundos');
        }});

        video.addEventListener('error', function() {{
            console.error('Error cargando video');
            document.querySelector('.video-wrapper').innerHTML = 
                '<div style="padding: 40px; color: #dc3545;">❌ Error cargando video</div>';
        }});
    </script>
</body>
</html>
"""


def generate_fallback_html(test_key, test_name, video_path, execution_key):
    """Genera HTML fallback sin video embebido para archivos muy grandes"""

    video_filename = os.path.basename(video_path)
    video_size = os.path.getsize(video_path)
    video_timestamp = datetime.fromtimestamp(os.path.getmtime(video_path))

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidencia - {test_key}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
        .info {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{test_key}</h1>
            <h2>{test_name}</h2>
            {f'<p>Test Execution: {execution_key}</p>' if execution_key else ''}
        </div>

        <div class="info">
            <h3>📹 Video de Evidencia</h3>
            <p><strong>Archivo:</strong> {video_filename}</p>
            <p><strong>Tamaño:</strong> {video_size / (1024 * 1024):.1f} MB</p>
            <p><strong>Fecha:</strong> {video_timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Nota:</strong> Video muy grande para embeber en HTML</p>
        </div>

        <div style="text-align: center;">
            <button class="btn" onclick="alert('Video disponible en: {os.path.abspath(video_path)}')">
                📁 Ver Ubicación del Video
            </button>
        </div>

        <div style="margin-top: 30px; text-align: center; color: #6c757d; font-size: 0.9em;">
            Evidencia generada automáticamente<br>
            {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    # Manejar argumentos de línea de comandos
    execution_key = None

    if len(sys.argv) > 1:
        execution_key = sys.argv[1]
        print(f"🎯 Generando evidencias para Test Execution: {execution_key}")
    else:
        print("💡 Uso: python generate_individual_evidence.py [APPTEST-XX]")
        print("📋 Generando evidencias genéricas...")

    # Generar evidencias individuales
    generated_files = generate_individual_html_reports(execution_key)

    if generated_files:
        print("\n🎉 Evidencias individuales generadas exitosamente!")
        print(f"📁 Ubicación: {os.path.abspath('evidence_reports')}/")
        print(f"📊 Total archivos: {len(generated_files)}")

        total_size = sum(f['size'] for f in generated_files)
        print(f"💾 Tamaño total: {total_size / (1024 * 1024):.1f} MB")

        print("\n📋 Archivos generados:")
        for file_info in generated_files:
            print(f"   • {file_info['test_key']}: {os.path.basename(file_info['html_path'])}")

        print("\n🚀 Siguiente paso: Subir como attachments a Xray")
        print("   Ejecuta: python upload_html_attachments.py APPTEST-XX")
    else:
        print("❌ No se generaron archivos de evidencia")