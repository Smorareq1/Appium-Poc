#!/usr/bin/env python3
"""
Script para ejecutar pruebas completas con video y subir resultados a Xray
"""

import os
import sys
import subprocess
import time
from datetime import datetime


def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    print(f"   Comando: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completado")
            if "FAILED" in result.stdout or "ERROR" in result.stdout:
                print("⚠️ Se detectaron fallos en las pruebas")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"   Código de salida: {e.returncode}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def main():
    print("=" * 60)
    print("🚀 SUITE COMPLETA DE PRUEBAS MOBILE CON VIDEO")
    print("=" * 60)

    # Verificar archivos necesarios
    required_files = [
        "conftest.py",
        "test_simple_flow.py",
        "upload_results.py",
        "upload_videos.py",
        ".env"
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        sys.exit(1)

    print("✅ Todos los archivos necesarios están presentes")

    # Paso 1: Ejecutar pruebas con pytest (genera XML + videos)
    print("\n" + "=" * 60)
    print("📱 PASO 1: EJECUTANDO PRUEBAS MOBILE")
    print("=" * 60)

    pytest_cmd = [
        "pytest",
        "test_simple_flow.py",
        "-v",
        "--tb=short",
        "--junitxml=resultado.xml",
        "--html=pytest_reports/report.html",
        "--self-contained-html"
    ]

    start_time = time.time()
    pytest_result = run_command(pytest_cmd, "Ejecutando suite de pruebas", check=False)
    end_time = time.time()

    duration = end_time - start_time
    print(f"⏱️ Duración de las pruebas: {duration:.1f} segundos")

    # Verificar que se generaron los archivos esperados
    if not os.path.exists("resultado.xml"):
        print("❌ No se generó resultado.xml")
        sys.exit(1)

    print("✅ Archivo resultado.xml generado")

    # Verificar videos
    videos_dir = "pytest_videos"
    if os.path.exists(videos_dir):
        video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
        print(f"📹 Videos generados: {len(video_files)}")
        for video in video_files:
            size_mb = os.path.getsize(os.path.join(videos_dir, video)) / (1024 * 1024)
            print(f"   • {video} ({size_mb:.1f} MB)")
    else:
        print("⚠️ No se encontró carpeta de videos")

    # Paso 2: Obtener execution key de Xray
    print("\n" + "=" * 60)
    print("📊 PASO 2: SUBIENDO RESULTADOS A XRAY")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("❌ Falta especificar el Test Execution Key")
        print("   Uso: python run_tests.py APPTEST-XX")
        print("   Donde APPTEST-XX es tu Test Execution en Xray")
        sys.exit(1)

    execution_key = sys.argv[1]
    print(f"🎯 Test Execution: {execution_key}")

    # Paso 3: Subir resultados XML a Xray
    upload_results_cmd = ["python", "upload_results.py"]
    run_command(upload_results_cmd, "Subiendo resultados XML a Xray")

    # Paso 4: Subir videos como evidencia
    print("\n" + "=" * 60)
    print("🎥 PASO 3: SUBIENDO VIDEOS COMO EVIDENCIA")
    print("=" * 60)

    if video_files:
        upload_videos_cmd = ["python", "upload_videos.py", execution_key]
        run_command(upload_videos_cmd, "Subiendo videos a Xray", check=False)
    else:
        print("⚠️ No hay videos para subir")

    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)

    print(f"🕒 Inicio: {datetime.fromtimestamp(start_time).strftime('%H:%M:%S')}")
    print(f"🕒 Fin: {datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}")
    print(f"⏱️ Duración total: {duration:.1f} segundos")

    if pytest_result.returncode == 0:
        print("✅ Todas las pruebas pasaron")
    else:
        print("⚠️ Algunas pruebas fallaron - revisa los reportes")

    print(f"📊 Resultados subidos a: {execution_key}")
    print(f"📹 Videos de evidencia: {len(video_files) if 'video_files' in locals() else 0}")

    # Enlaces útiles
    print(f"🔗 Reporte HTML: file://{os.path.abspath('pytest_reports/report.html')}")
    if os.path.exists("resultado.xml"):
        print(f"🔗 XML JUnit: file://{os.path.abspath('resultado.xml')}")

    print("\n🎉 Proceso completado!")


if __name__ == "__main__":
    main()