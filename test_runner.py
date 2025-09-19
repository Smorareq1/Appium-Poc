#!/usr/bin/env python3
"""
Script de gestión para ejecutar tests con reportes separados por módulo
Permite ejecutar tests individuales, por carpeta, o todos con reportes organizados
"""

import os
import sys
import subprocess
import argparse
import glob
from datetime import datetime
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_reports_dir = "pytest_reports"
        self.base_videos_dir = "pytest_videos"
        self.base_logs_dir = "pytest_logs"
        self.tests_dir = "tests"

        # Crear directorios base
        for dir_path in [self.base_reports_dir, self.base_videos_dir, self.base_logs_dir]:
            os.makedirs(dir_path, exist_ok=True)

    def get_test_modules(self):
        """Obtiene lista de módulos de test disponibles"""
        test_files = []
        test_dirs = []

        # Buscar archivos de test en el directorio raíz de tests
        for pattern in ["test_*.py", "*_test.py"]:
            test_files.extend(glob.glob(f"{self.tests_dir}/{pattern}"))

        # Buscar subdirectorios con tests
        for root, dirs, files in os.walk(self.tests_dir):
            if root != self.tests_dir:  # Evitar el directorio raíz
                for pattern in ["test_*.py", "*_test.py"]:
                    if glob.glob(f"{root}/{pattern}"):
                        test_dirs.append(root)
                        break

        return test_files, test_dirs

    def get_module_name(self, path):
        """Convierte ruta a nombre de módulo para reportes"""
        if os.path.isfile(path):
            # Para archivos: test_login.py -> login
            basename = os.path.basename(path)
            name = basename.replace("test_", "").replace("_test", "").replace(".py", "")
            return name
        else:
            # Para directorios: tests/login -> login
            return os.path.basename(path)

    def run_single_module(self, module_path, module_name=None, verbose=True, capture=False):
        """Ejecuta un módulo específico con reporte individual"""
        if not module_name:
            module_name = self.get_module_name(module_path)

        # Crear subdirectorio para este módulo
        module_reports_dir = os.path.join(self.base_reports_dir, module_name)
        os.makedirs(module_reports_dir, exist_ok=True)

        # Nombres de archivos de reporte
        html_report = os.path.join(module_reports_dir, f"report_{module_name}_{self.timestamp}.html")
        xml_report = os.path.join(module_reports_dir, f"result_{module_name}_{self.timestamp}.xml")

        # Comando pytest personalizado con opciones de debug
        cmd = [
            "python", "-m", "pytest",
            module_path,
            f"--html={html_report}",
            "--self-contained-html",
            f"--junitxml={xml_report}",
            f"--junit-prefix={module_name}",
        ]

        # Agregar opciones de verbosidad y captura
        if verbose:
            cmd.extend(["-v", "-vv"])  # Doble verbosidad para más detalle

        if not capture:
            cmd.append("-s")  # No capturar output para ver prints

        # Opciones adicionales de debug
        cmd.extend([
            "--tb=short",  # Traceback corto pero informativo
            "--show-capture=all",  # Mostrar todo el output capturado
            "--capture=no" if not capture else "--capture=sys",  # Control de captura
        ])

        print(f"\n{'=' * 60}")
        print(f"🚀 EJECUTANDO TESTS: {module_name}")
        print(f"📁 Módulo: {module_path}")
        print(f"📄 HTML: {html_report}")
        print(f"📄 XML: {xml_report}")
        print(f"🔍 Verbosidad: {'Alta' if verbose else 'Normal'}")
        print(f"📺 Debug output: {'Visible' if not capture else 'Capturado'}")
        print(f"{'=' * 60}")

        # Establecer variables de entorno para organizar videos por módulo
        env = os.environ.copy()
        env['PYTEST_MODULE_NAME'] = module_name
        env['PYTEST_REPORTS_DIR'] = module_reports_dir

        try:
            # Mostrar comando completo cuando está en modo debug
            if verbose and not capture:
                print(f"🔧 Comando ejecutándose:")
                print(f"   {' '.join(cmd)}")
                print()

            result = subprocess.run(cmd, env=env, capture_output=False)

            if result.returncode == 0:
                print(f"✅ Tests de {module_name} completados exitosamente")
            else:
                print(f"⚠️ Tests de {module_name} completados con fallos")

            return result.returncode, html_report, xml_report

        except Exception as e:
            print(f"❌ Error ejecutando tests de {module_name}: {e}")
            return 1, None, None

    def run_all_modules(self, verbose=True, capture=False):
        """Ejecuta todos los módulos por separado"""
        test_files, test_dirs = self.get_test_modules()
        all_results = []

        print(f"\n🔍 MÓDULOS ENCONTRADOS:")
        print(f"📄 Archivos: {[self.get_module_name(f) for f in test_files]}")
        print(f"📁 Directorios: {[self.get_module_name(d) for d in test_dirs]}")

        # Ejecutar archivos individuales
        for test_file in test_files:
            module_name = self.get_module_name(test_file)
            returncode, html_report, xml_report = self.run_single_module(
                test_file, module_name, verbose=verbose, capture=capture
            )
            all_results.append({
                'module': module_name,
                'path': test_file,
                'returncode': returncode,
                'html_report': html_report,
                'xml_report': xml_report
            })

        # Ejecutar directorios
        for test_dir in test_dirs:
            module_name = self.get_module_name(test_dir)
            returncode, html_report, xml_report = self.run_single_module(
                test_dir, module_name, verbose=verbose, capture=capture
            )
            all_results.append({
                'module': module_name,
                'path': test_dir,
                'returncode': returncode,
                'html_report': html_report,
                'xml_report': xml_report
            })

        self.generate_summary_report(all_results)
        return all_results

    def generate_summary_report(self, results):
        """Genera un reporte resumen de todos los módulos"""
        summary_file = os.path.join(self.base_reports_dir, f"summary_{self.timestamp}.md")

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Reporte Resumen de Tests\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Estadísticas generales
            total_modules = len(results)
            passed_modules = sum(1 for r in results if r['returncode'] == 0)
            failed_modules = total_modules - passed_modules

            f.write(f"## 📊 Estadísticas Generales\n")
            f.write(f"- **Total de módulos:** {total_modules}\n")
            f.write(f"- **Módulos exitosos:** {passed_modules}\n")
            f.write(f"- **Módulos con fallos:** {failed_modules}\n\n")

            # Detalles por módulo
            f.write(f"## 📋 Detalles por Módulo\n\n")
            for result in results:
                status = "✅ EXITOSO" if result['returncode'] == 0 else "❌ FALLÓ"
                f.write(f"### {result['module']} - {status}\n")
                f.write(f"- **Ruta:** `{result['path']}`\n")
                if result['html_report']:
                    f.write(f"- **Reporte HTML:** `{result['html_report']}`\n")
                if result['xml_report']:
                    f.write(f"- **Reporte XML:** `{result['xml_report']}`\n")
                f.write(f"\n")

        print(f"\n📋 Reporte resumen generado: {summary_file}")

    def list_modules(self):
        """Lista todos los módulos disponibles"""
        test_files, test_dirs = self.get_test_modules()

        print(f"\n📋 MÓDULOS DISPONIBLES:")
        print(f"\n📄 Archivos de test:")
        for test_file in test_files:
            module_name = self.get_module_name(test_file)
            print(f"  - {module_name} ({test_file})")

        print(f"\n📁 Directorios de test:")
        for test_dir in test_dirs:
            module_name = self.get_module_name(test_dir)
            print(f"  - {module_name} ({test_dir})")

    def merge_xml_reports(self, output_file="merged_results.xml"):
        """Combina todos los reportes XML en uno solo para Xray"""
        xml_files = glob.glob(f"{self.base_reports_dir}/**/result_*.xml", recursive=True)

        if not xml_files:
            print("⚠️ No se encontraron reportes XML para combinar")
            return

        print(f"\n🔗 Combinando {len(xml_files)} reportes XML...")

        try:
            import xml.etree.ElementTree as ET

            # Crear elemento raíz combinado
            root = ET.Element("testsuites")
            root.set("name", "CombinedAppiumTests")
            root.set("time", "0")
            root.set("tests", "0")
            root.set("failures", "0")
            root.set("errors", "0")

            total_tests = 0
            total_failures = 0
            total_errors = 0
            total_time = 0.0

            for xml_file in xml_files:
                try:
                    tree = ET.parse(xml_file)
                    testsuite = tree.getroot()

                    # Agregar testsuite al root combinado
                    root.append(testsuite)

                    # Sumar estadísticas
                    total_tests += int(testsuite.get("tests", 0))
                    total_failures += int(testsuite.get("failures", 0))
                    total_errors += int(testsuite.get("errors", 0))
                    total_time += float(testsuite.get("time", 0))

                except Exception as e:
                    print(f"⚠️ Error procesando {xml_file}: {e}")

            # Actualizar estadísticas totales
            root.set("tests", str(total_tests))
            root.set("failures", str(total_failures))
            root.set("errors", str(total_errors))
            root.set("time", str(total_time))

            # Guardar archivo combinado
            output_path = os.path.join(self.base_reports_dir, output_file)
            tree = ET.ElementTree(root)
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

            print(f"✅ Reporte XML combinado generado: {output_path}")
            print(f"📊 Total tests: {total_tests}, Fallos: {total_failures}, Errores: {total_errors}")

        except ImportError:
            print("❌ xml.etree.ElementTree no disponible para combinar reportes")
        except Exception as e:
            print(f"❌ Error combinando reportes XML: {e}")


def main():
    parser = argparse.ArgumentParser(description="Ejecutor de tests con reportes separados")
    parser.add_argument('--module', '-m', help='Ejecutar módulo específico')
    parser.add_argument('--all', '-a', action='store_true', help='Ejecutar todos los módulos')
    parser.add_argument('--list', '-l', action='store_true', help='Listar módulos disponibles')
    parser.add_argument('--merge', action='store_true', help='Combinar reportes XML existentes')

    # Opciones de debug y verbosidad
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Modo silencioso (menos verbosidad)')
    parser.add_argument('--capture', '-c', action='store_true',
                        help='Capturar output (ocultar prints)')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Modo debug máximo (implica --no-capture)')

    args = parser.parse_args()

    # Determinar configuración de verbosidad
    if args.debug:
        verbose = True
        capture = False
        print("🔧 MODO DEBUG ACTIVADO - Máxima verbosidad y output visible")
    elif args.quiet:
        verbose = False
        capture = True
        print("🔇 MODO SILENCIOSO - Mínima verbosidad")
    else:
        # Configuración por defecto: verboso y sin captura (como antes)
        verbose = True
        capture = False
        print("🔍 MODO NORMAL - Verbosidad alta, output visible (equivalente a -v -s)")

    runner = TestRunner()

    if args.list:
        runner.list_modules()
    elif args.merge:
        runner.merge_xml_reports()
    elif args.module:
        # Buscar el módulo específico
        test_files, test_dirs = runner.get_test_modules()
        all_paths = test_files + test_dirs

        # Buscar coincidencia por nombre
        target_path = None
        for path in all_paths:
            if args.module in runner.get_module_name(path):
                target_path = path
                break

        if target_path:
            runner.run_single_module(target_path, verbose=verbose, capture=capture)
        else:
            print(f"❌ Módulo '{args.module}' no encontrado")
            print("💡 Usa --list para ver módulos disponibles")
    elif args.all:
        runner.run_all_modules(verbose=verbose, capture=capture)
    else:
        parser.print_help()
        print("\n💡 Configuración por defecto: equivalente a pytest -v -s")
        print("   Usa --quiet para menos verbosidad o --debug para máximo detalle")


if __name__ == "__main__":
    main()