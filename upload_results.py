import os
import json
import requests
import argparse
import glob
from pathlib import Path
from dotenv import load_dotenv


class XrayUploader:
    def __init__(self):
        # Cargar variables del archivo .env
        load_dotenv()

        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.PROJECT_KEY = os.getenv("PROJECT_KEY")
        self.BASE_REPORTS_DIR = "pytest_reports"
        self.token = None

        # Módulos excluidos por defecto
        self.EXCLUDED_MODULES = ["debug", "puntuales"]

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("❌ CLIENT_ID y CLIENT_SECRET deben estar configurados en .env")

    def authenticate(self):
        """Autenticar con Xray y obtener token"""
        auth_url = "https://xray.cloud.getxray.app/api/v2/authenticate"
        auth_payload = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }
        auth_headers = {"Content-Type": "application/json"}

        print("🔑 Generando token de autenticación...")
        token_response = requests.post(auth_url, headers=auth_headers, data=json.dumps(auth_payload))

        if token_response.status_code != 200:
            print("❌ Error al autenticar:", token_response.text)
            return False

        self.token = token_response.json()
        print("✅ Token generado exitosamente.")
        return True

    def find_xml_files_for_module(self, module_name):
        """Buscar archivos XML para un módulo específico"""
        module_dir = os.path.join(self.BASE_REPORTS_DIR, module_name)

        if not os.path.exists(module_dir):
            print(f"⚠️ Directorio no encontrado: {module_dir}")
            return []

        # Buscar archivos con patrón result_<module_name>*.xml
        pattern = os.path.join(module_dir, f"result_{module_name}*.xml")
        xml_files = glob.glob(pattern)

        if not xml_files:
            print(f"⚠️ No se encontraron archivos XML para módulo: {module_name}")
            print(f"   Patrón buscado: {pattern}")

        return xml_files

    def get_available_modules(self):
        """Obtener lista de módulos disponibles (excluyendo los de desarrollo)"""
        if not os.path.exists(self.BASE_REPORTS_DIR):
            return []

        modules = []
        for item in os.listdir(self.BASE_REPORTS_DIR):
            item_path = os.path.join(self.BASE_REPORTS_DIR, item)
            if os.path.isdir(item_path) and item not in self.EXCLUDED_MODULES:
                # Verificar que tenga archivos XML
                if self.find_xml_files_for_module(item):
                    modules.append(item)

        return sorted(modules)

    def upload_module_results(self, module_name, xml_file_path):
        """Subir resultados de un módulo específico a Xray"""
        upload_url = f"https://xray.cloud.getxray.app/api/v2/import/execution/junit?projectKey={self.PROJECT_KEY}"
        upload_headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/xml"
        }

        print(f"⬆️ Subiendo resultados de módulo '{module_name}' a Xray...")
        print(f"   Archivo: {xml_file_path}")

        try:
            with open(xml_file_path, "rb") as f:
                response = requests.post(upload_url, headers=upload_headers, data=f)

            if response.status_code == 200:
                print(f"✅ Módulo '{module_name}' subido exitosamente")
                print(f"   Respuesta: {response.text}")
                return True
            else:
                print(f"❌ Error subiendo módulo '{module_name}': {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {xml_file_path}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado subiendo módulo '{module_name}': {e}")
            return False

    def process_modules(self, modules):
        """Procesar lista de módulos y subir sus resultados"""
        if not modules:
            print("❌ No hay módulos para procesar")
            return

        print(f"\n📋 Módulos a procesar: {modules}")
        print(f"🎯 Proyecto Xray: {self.PROJECT_KEY}")
        print(f"📁 Directorio base: {self.BASE_REPORTS_DIR}")
        print("=" * 60)

        results_summary = []

        for module_name in modules:
            print(f"\n🔍 Procesando módulo: {module_name}")

            xml_files = self.find_xml_files_for_module(module_name)

            if not xml_files:
                results_summary.append({
                    'module': module_name,
                    'status': 'SKIPPED',
                    'reason': 'No XML files found'
                })
                continue

            # Si hay múltiples archivos XML, usar el más reciente
            if len(xml_files) > 1:
                xml_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                print(f"   📄 Encontrados {len(xml_files)} archivos, usando el más reciente")

            xml_file = xml_files[0]
            print(f"   📄 Archivo seleccionado: {os.path.basename(xml_file)}")

            success = self.upload_module_results(module_name, xml_file)

            results_summary.append({
                'module': module_name,
                'status': 'SUCCESS' if success else 'FAILED',
                'file': os.path.basename(xml_file)
            })

        # Mostrar resumen final
        self.print_summary(results_summary)

    def print_summary(self, results_summary):
        """Mostrar resumen de resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE SUBIDA A XRAY")
        print("=" * 60)

        success_count = sum(1 for r in results_summary if r['status'] == 'SUCCESS')
        failed_count = sum(1 for r in results_summary if r['status'] == 'FAILED')
        skipped_count = sum(1 for r in results_summary if r['status'] == 'SKIPPED')

        print(f"✅ Exitosos: {success_count}")
        print(f"❌ Fallidos: {failed_count}")
        print(f"⏭️ Omitidos: {skipped_count}")
        print(f"📊 Total: {len(results_summary)}")
        print()

        for result in results_summary:
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌" if result['status'] == 'FAILED' else "⏭️"
            print(f"{status_icon} {result['module']} - {result['status']}")
            if 'file' in result:
                print(f"   📄 {result['file']}")
            if 'reason' in result:
                print(f"   💭 {result['reason']}")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Subir resultados de tests a Xray por módulos",
        epilog="""
Ejemplos de uso:
  python upload_results.py --all
  python upload_results.py login catalogo
  python upload_results.py ventas itinerarios --list-first
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'modules',
        nargs='*',
        help='Nombres de módulos específicos a subir'
    )

    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Subir todos los módulos disponibles (excluyendo debug y puntuales)'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Listar módulos disponibles y salir'
    )

    parser.add_argument(
        '--list-first',
        action='store_true',
        help='Mostrar módulos disponibles antes de procesar'
    )

    parser.add_argument(
        '--exclude',
        nargs='+',
        default=[],
        help='Módulos adicionales a excluir (además de debug y puntuales)'
    )

    args = parser.parse_args()

    try:
        uploader = XrayUploader()

        # Agregar exclusiones adicionales
        if args.exclude:
            uploader.EXCLUDED_MODULES.extend(args.exclude)
            print(f"🚫 Módulos excluidos: {uploader.EXCLUDED_MODULES}")

        # Listar módulos disponibles si se solicita
        if args.list or args.list_first:
            available_modules = uploader.get_available_modules()
            print("📋 MÓDULOS DISPONIBLES:")
            if available_modules:
                for module in available_modules:
                    xml_files = uploader.find_xml_files_for_module(module)
                    print(f"  ✅ {module} ({len(xml_files)} archivo(s) XML)")
            else:
                print("  ⚠️ No se encontraron módulos con archivos XML")

            if args.list:
                return

        # Autenticar con Xray
        if not uploader.authenticate():
            return

        # Determinar qué módulos procesar
        if args.all:
            modules_to_process = uploader.get_available_modules()
            if not modules_to_process:
                print("❌ No hay módulos disponibles para procesar")
                return
        elif args.modules:
            modules_to_process = args.modules
            # Validar que los módulos existen
            available_modules = uploader.get_available_modules()
            invalid_modules = [m for m in modules_to_process if m not in available_modules]
            if invalid_modules:
                print(f"⚠️ Módulos no encontrados o sin archivos XML: {invalid_modules}")
                print(f"📋 Módulos disponibles: {available_modules}")
                # Continuar solo con módulos válidos
                modules_to_process = [m for m in modules_to_process if m in available_modules]
                if not modules_to_process:
                    print("❌ No hay módulos válidos para procesar")
                    return
        else:
            print("❌ Debes especificar --all o nombres de módulos específicos")
            parser.print_help()
            return

        # Procesar módulos
        uploader.process_modules(modules_to_process)

    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()