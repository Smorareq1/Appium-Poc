import os
import sys
import glob
import base64
from datetime import datetime
from pathlib import Path


def generate_html_report_with_videos(execution_key=None):
    """Genera un reporte HTML con videos embebidos como evidencia"""

    videos_dir = "pytest_videos"

    # Si se especifica execution key, incluirlo en el nombre del archivo
    if execution_key:
        output_file = f"pytest_reports/video_evidence_{execution_key}.html"
        print(f"🎯 Generando reporte para Test Execution: {execution_key}")
    else:
        output_file = "pytest_reports/video_evidence_report.html"
        print("📋 Generando reporte genérico (sin Test Execution específico)")

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

    print("🎬 Generando reporte HTML con videos embebidos...")

    # Buscar videos
    videos_encontrados = {}
    for test_name, test_info in tests_mapping.items():
        pattern = f"{videos_dir}/{test_name}_*.mp4"
        matching_files = glob.glob(pattern)

        if matching_files:
            latest_video = max(matching_files, key=os.path.getmtime)
            videos_encontrados[test_name] = {
                "path": latest_video,
                "key": test_info["key"],
                "name": test_info["name"],
                "size": os.path.getsize(latest_video)
            }
            print(f"📹 {test_info['key']}: {latest_video}")

    if not videos_encontrados:
        print("❌ No se encontraron videos para el reporte")
        return

    # Crear directorio de reportes si no existe
    os.makedirs("pytest_reports", exist_ok=True)

    # Generar HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidencias de Video - Testing Mobile</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .subtitle {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #495057;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .test-section {{
            margin: 0;
            border-bottom: 1px solid #dee2e6;
        }}
        .test-header {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #28a745;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .test-header:hover {{
            background: #e9ecef;
        }}
        .test-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #495057;
            margin: 0 0 5px 0;
        }}
        .test-key {{
            background: #007bff;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .test-info {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #6c757d;
        }}
        .video-container {{
            padding: 20px;
            display: none;
        }}
        .video-container.active {{
            display: block;
        }}
        .video-wrapper {{
            position: relative;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        video {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .video-controls {{
            padding: 15px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }}
        .control-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            margin-right: 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
        }}
        .control-btn:hover {{
            background: #0056b3;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }}
        .toggle-icon {{
            float: right;
            transition: transform 0.3s;
        }}
        .toggle-icon.rotated {{
            transform: rotate(180deg);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 Evidencias de Video</h1>
            <div class="subtitle">
                Suite de Pruebas Mobile - {datetime.now().strftime('%d/%m/%Y %H:%M')}
                {f' • Test Execution: {execution_key}' if execution_key else ''}
            </div>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(videos_encontrados)}</div>
                <div class="stat-label">Tests con Video</div>
            </div>
            <div class="stat">
                <div class="stat-number">{sum(v['size'] for v in videos_encontrados.values()) / (1024 * 1024):.1f} MB</div>
                <div class="stat-label">Tamaño Total</div>
            </div>
            <div class="stat">
                <div class="stat-number">{datetime.now().strftime('%H:%M')}</div>
                <div class="stat-label">Hora Generación</div>
            </div>
        </div>
"""

    # Agregar cada test con su video
    for i, (test_name, video_info) in enumerate(videos_encontrados.items()):
        video_path = video_info["path"]

        # Convertir video a base64 para embeber en HTML
        try:
            with open(video_path, "rb") as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

            html_content += f"""
        <div class="test-section">
            <div class="test-header" onclick="toggleVideo('video-{i}')">
                <div class="test-title">
                    {video_info['name']}
                    <span class="toggle-icon" id="icon-{i}">▼</span>
                </div>
                <span class="test-key">{video_info['key']}</span>
                <div class="test-info">
                    📁 {os.path.basename(video_path)} • 
                    📏 {video_info['size'] / (1024 * 1024):.1f} MB • 
                    🕒 {datetime.fromtimestamp(os.path.getmtime(video_path)).strftime('%H:%M:%S')}
                </div>
            </div>
            <div class="video-container" id="video-{i}">
                <div class="video-wrapper">
                    <video id="player-{i}" controls preload="none" poster="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB2aWV3Qm94PSIwIDAgMjQgMjQiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iIzAwMCIvPgo8cGF0aCBkPSJNOCAxMEwyMCAxMkw4IDE0VjEwWiIgZmlsbD0iI2ZmZiIvPgo8L3N2Zz4K">
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                        Tu navegador no soporta video HTML5.
                    </video>
                </div>
                <div class="video-controls">
                    <button class="control-btn" onclick="playVideo('player-{i}')">▶️ Reproducir</button>
                    <button class="control-btn" onclick="pauseVideo('player-{i}')">⏸️ Pausar</button>
                    <button class="control-btn" onclick="restartVideo('player-{i}')">🔄 Reiniciar</button>
                    <button class="control-btn" onclick="downloadVideo('player-{i}', '{os.path.basename(video_path)}')">💾 Descargar</button>
                </div>
            </div>
        </div>
"""
        except Exception as e:
            print(f"❌ Error embebiendo video {video_path}: {e}")
            # Si el video es muy grande, solo mostrar un enlace
            html_content += f"""
        <div class="test-section">
            <div class="test-header">
                <div class="test-title">{video_info['name']}</div>
                <span class="test-key">{video_info['key']}</span>
                <div class="test-info">
                    ⚠️ Video muy grande para embeber - <a href="file://{os.path.abspath(video_path)}" target="_blank">Abrir archivo</a>
                </div>
            </div>
        </div>
"""

    # Cerrar HTML con JavaScript
    html_content += f"""
        <div class="footer">
            Generado automáticamente por pytest con grabación de video<br>
            {f'🎯 Test Execution: {execution_key} | ' if execution_key else ''}
            🎯 Para usar en Xray: Descarga los videos individuales y súbelos manualmente como evidencias
        </div>
    </div>

    <script>
        function toggleVideo(videoId) {{
            const container = document.getElementById(videoId);
            const icon = document.getElementById('icon-' + videoId.split('-')[1]);

            if (container.classList.contains('active')) {{
                container.classList.remove('active');
                icon.textContent = '▼';
                icon.classList.remove('rotated');
            }} else {{
                // Cerrar otros videos
                document.querySelectorAll('.video-container.active').forEach(v => {{
                    v.classList.remove('active');
                    const idx = v.id.split('-')[1];
                    document.getElementById('icon-' + idx).textContent = '▼';
                    document.getElementById('icon-' + idx).classList.remove('rotated');
                }});

                container.classList.add('active');
                icon.textContent = '▲';
                icon.classList.add('rotated');
            }}
        }}

        function playVideo(playerId) {{
            document.getElementById(playerId).play();
        }}

        function pauseVideo(playerId) {{
            document.getElementById(playerId).pause();
        }}

        function restartVideo(playerId) {{
            const video = document.getElementById(playerId);
            video.currentTime = 0;
            video.play();
        }}

        function downloadVideo(playerId, filename) {{
            const video = document.getElementById(playerId);
            const a = document.createElement('a');
            a.href = video.src;
            a.download = filename;
            a.click();
        }}

        // Auto-play cuando se abre un video
        document.querySelectorAll('video').forEach(video => {{
            video.addEventListener('loadstart', function() {{
                console.log('Video cargando:', this.id);
            }});
        }});
    </script>
</body>
</html>
"""

    # Escribir archivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Reporte generado: {output_file}")
    print(f"🔗 Abrir en navegador: file://{os.path.abspath(output_file)}")
    print(f"📊 Videos incluidos: {len(videos_encontrados)}")

    return output_file


if __name__ == "__main__":
    # Manejar argumentos de línea de comandos
    execution_key = None

    if len(sys.argv) > 1:
        execution_key = sys.argv[1]
        print(f"🎯 Generando reporte para Test Execution: {execution_key}")
    else:
        print("💡 Uso: python generate_video_report.py [APPTEST-XX]")
        print("📋 Generando reporte genérico...")

    # Generar el reporte
    output_file = generate_html_report_with_videos(execution_key)

    if output_file:
        print("\n🎉 Reporte de evidencias generado exitosamente!")
        if execution_key:
            print(f"📎 Asociado al Test Execution: {execution_key}")
        print(f"📂 Ubicación: {os.path.abspath(output_file)}")
        print("\n💡 Para usar en Xray Cloud:")
        print("   • Abre el reporte HTML en tu navegador")
        print("   • Descarga videos individuales desde el reporte")
        print("   • Súbelos manualmente a Xray Cloud como attachments")