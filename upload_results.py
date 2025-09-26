import os
import json
import base64
import mimetypes
import requests
import argparse
import glob
import re
from pathlib import Path
from dotenv import load_dotenv


class XrayUploader:
    def __init__(self):
        # Cargar variables del archivo .env
        load_dotenv()

        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.PROJECT_KEY = os.getenv("PROJECT_KEY")

        # Directorios base
        self.BASE_REPORTS_DIR = "pytest_reports"
        self.BASE_VIDEOS_DIR = "pytest_videos"

        # Nuevas variables para Jira REST
        self.JIRA_EMAIL = os.getenv("JIRA_EMAIL")
        self.JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
        self.JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")

        self.token = None

        # Módulos excluidos por defecto
        self.EXCLUDED_MODULES = ["debug", "puntuales"]

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("❌ CLIENT_ID y CLIENT_SECRET deben estar configurados en .env")

    # =========================
    #   AUTENTICACIÓN XRAY
    # =========================
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

        # La API devuelve el JWT como string JSON (ej. "eyJ..."), requests.json() retorna un str
        self.token = token_response.json()
        print("✅ Token generado exitosamente.")
        return True

    # =========================
    #   UTILIDADES REPORTES
    # =========================
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

    def find_videos_by_test_key(self, module_name):
        """
        Devuelve un dict { 'ATC-123': '/ruta/al/video.mp4', ... } para el módulo.
        Toma el .mp4 más reciente cuando hay varios por la misma key.
        """
        mapping = {}
        module_videos_dir = os.path.join(self.BASE_VIDEOS_DIR, module_name)
        if not os.path.exists(module_videos_dir):
            return mapping

        candidates = glob.glob(os.path.join(module_videos_dir, "*.mp4"))
        for path in candidates:
            fname = os.path.basename(path)
            m = self.TEST_KEY_RE.search(fname.upper())
            if not m:
                continue
            key = m.group(1)  # p.ej. ATC-123
            # Mantener el más nuevo si hay duplicados
            if key not in mapping or os.path.getmtime(path) > os.path.getmtime(mapping[key]):
                mapping[key] = path

        return mapping

    # =========================
    #   SUBIR RESULTADOS JUNIT
    # =========================
    def upload_module_results(self, module_name, xml_file_path):
        """Subir resultados de un módulo específico a Xray (JUnit) y devolver (ok, testExecKey)"""
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

                # Parsear respuesta JSON
                try:
                    resp_json = response.json()
                    print(f"   📋 Respuesta de Xray:")
                    print(f"      {json.dumps(resp_json, indent=6)}")
                except Exception as e:
                    print(f"   ⚠️ Error parseando JSON de respuesta: {e}")
                    print(f"   📄 Respuesta raw: {response.text}")
                    resp_json = {}

                # Intentar extraer test_exec_key de diferentes estructuras posibles
                test_exec_key = None

                if isinstance(resp_json, dict):
                    # Opción 1: {"testExecIssue": {"key": "ATC-123"}}
                    if "testExecIssue" in resp_json:
                        test_exec_issue = resp_json["testExecIssue"]
                        if isinstance(test_exec_issue, dict):
                            test_exec_key = test_exec_issue.get("key")

                    # Opción 2: {"key": "ATC-123"}
                    if not test_exec_key:
                        test_exec_key = resp_json.get("key")

                    # Opción 3: {"testExecKey": "ATC-123"}
                    if not test_exec_key:
                        test_exec_key = resp_json.get("testExecKey")

                    # Opción 4: {"id": "ATC-123"}
                    if not test_exec_key:
                        test_exec_key = resp_json.get("id")

                if test_exec_key:
                    print(f"   ✅ TestExecutionKey extraído: {test_exec_key}")
                else:
                    print(f"   ⚠️ No se pudo extraer TestExecutionKey de la respuesta")
                    print(f"   💡 Estructura de respuesta no reconocida. Revisa el formato arriba.")

                return True, test_exec_key
            else:
                print(f"❌ Error subiendo módulo '{module_name}': {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False, None

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {xml_file_path}")
            return False, None
        except Exception as e:
            print(f"❌ Error inesperado subiendo módulo '{module_name}': {e}")
            import traceback
            traceback.print_exc()
            return False, None

    # =========================
    #   GRAPHQL XRAY (EVIDENCIAS)
    # =========================
    XRAY_GRAPHQL_URL = "https://xray.cloud.getxray.app/api/v2/graphql"
    TEST_KEY_RE = re.compile(r'([A-Z][A-Z0-9]+-\d+)')

    def _gql(self, query, variables=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {"query": query, "variables": variables or {}}
        r = requests.post(self.XRAY_GRAPHQL_URL, headers=headers, data=json.dumps(payload))

        # Log de errores amigable (no ocultar el cuerpo del 400)
        if r.status_code != 200:
            try:
                err = r.json()
            except Exception:
                err = r.text
            raise RuntimeError(f"GraphQL HTTP {r.status_code}: {err}")

        data = r.json()
        if "errors" in data and data["errors"]:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")
        return data.get("data", {})

    def _get_runs_with_keys_by_exec_key(self, test_exec_key, limit=100):
        """
        Devuelve lista de tuplas (run_id, test_key) del Test Execution (por KEY).
        """
        print(f"   🔍 Obteniendo Test Runs de {test_exec_key}...")

        issue_id = self._get_issue_id_from_key(test_exec_key)
        if not issue_id:
            raise RuntimeError(f"No se pudo resolver issueId para {test_exec_key}")

        query = """
          query($execIds:[String!]!, $limit:Int!){
            getTestRuns(testExecIssueIds:$execIds, limit:$limit){
              results{
                id
                test { jira(fields:["key","summary"]) }
              }
            }
          }
        """
        data = self._gql(query, {"execIds": [issue_id], "limit": min(limit, 100)})
        results = ((data or {}).get("getTestRuns") or {}).get("results") or []

        runs = []
        for r in results:
            rid = r.get("id")
            test = r.get("test") or {}
            jira = test.get("jira") or {}
            tkey = jira.get("key")
            if rid and tkey:
                runs.append((rid, tkey))
        print(f"   ✅ Encontrados {len(runs)} Test Run(s)")
        return runs

    def _add_video_to_testrun_rest(self, testrun_id, video_path, test_key=None):
        """
        Adjunta video usando REST API de Jira con API Token
        """
        if not test_key:
            test_key = self._get_issue_key_from_testrun(testrun_id)
            if not test_key:
                print(f"      ❌ No se pudo obtener Issue Key del Test Run")
                return None

        # Autenticación básica con email + API token
        jira_email = os.getenv("JIRA_EMAIL")
        jira_token = os.getenv("JIRA_API_TOKEN")

        if not jira_email or not jira_token:
            print(f"      ❌ JIRA_EMAIL o JIRA_API_TOKEN no configurados en .env")
            return None

        url = f"https://{self.JIRA_DOMAIN}.atlassian.net/rest/api/3/issue/{test_key}/attachments"

        # Autenticación básica (Base64)
        import base64
        auth_str = f"{jira_email}:{jira_token}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        headers = {
            "Authorization": f"Basic {auth_b64}",
            "X-Atlassian-Token": "no-check"
        }

        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"      ⬆️ Subiendo video ({size_mb:.1f}MB) via REST API...")

        try:
            with open(video_path, 'rb') as f:
                files = {'file': (os.path.basename(video_path), f, 'video/mp4')}
                response = requests.post(url, headers=headers, files=files, timeout=300)

            if response.status_code in [200, 201]:
                print(f"      ✅ Video adjuntado exitosamente")
                return True
            else:
                print(f"      ❌ Error REST API: {response.status_code}")
                print(f"      {response.text[:200]}")
                return False

        except Exception as e:
            print(f"      ❌ Error: {e}")
            return False

    def _get_issue_id_from_key(self, issue_key: str) -> str | None:
        # Usa JQL para traer el TE por key y quedarte con su issueId (numérico).
        query = """
          query($jql:String!, $limit:Int!){
            getTestExecutions(jql:$jql, limit:$limit){
              results{
                issueId
                jira(fields:["key"])
              }
            }
          }
        """
        jql = f'key = "{issue_key}"'
        data = self._gql(query, {"jql": jql, "limit": 1})
        results = ((data or {}).get("getTestExecutions") or {}).get("results") or []
        if results:
            return results[0].get("issueId")
        return None

    def _get_issue_key_from_testrun(self, testrun_id):
        """Obtener el Issue Key asociado a un Test Run"""
        query = """
          query($id: String!) {
            getTestRun(id: $id) {
              test {
                jira(fields: ["key"])
              }
            }
          }
        """
        data = self._gql(query, {"id": testrun_id})
        test = (data.get("getTestRun") or {}).get("test") or {}
        jira = test.get("jira") or {}
        return jira.get("key")

    # =========================
    #   VIDEOS POR MÓDULO
    # =========================
    def find_video_for_module(self, module_name):
        """
        Retorna el último .mp4 del directorio de videos del módulo, o None si no existe.
        Estructura esperada: pytest_videos/<modulo>/*.mp4
        """
        module_videos_dir = os.path.join(self.BASE_VIDEOS_DIR, module_name)
        if not os.path.exists(module_videos_dir):
            print(f"   ⚠️ Directorio de videos no existe: {module_videos_dir}")
            return None

        mp4s = sorted(
            glob.glob(os.path.join(module_videos_dir, "*.mp4")),
            key=lambda p: os.path.getmtime(p),
            reverse=True
        )

        if mp4s:
            print(f"   🎥 Video encontrado: {os.path.basename(mp4s[0])}")
        else:
            print(f"   ⚠️ No se encontraron videos .mp4 en: {module_videos_dir}")

        return mp4s[0] if mp4s else None

    # =========================
    #   PROCESO PRINCIPAL
    # =========================
    def process_modules(self, modules):
        """Procesar lista de módulos y subir sus resultados + evidencias"""
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

            success, test_exec_key = self.upload_module_results(module_name, xml_file)

            result_entry = {
                'module': module_name,
                'status': 'SUCCESS' if success else 'FAILED',
                'file': os.path.basename(xml_file),
                'testExecutionKey': test_exec_key,
                'video_attached': False
            }

            # Adjuntar evidencia (video) a cada Test Run del Execution
            # Adjuntar evidencia (video) a cada Test Run del Execution
            if success and test_exec_key:
                print(f"\n   🎬 Buscando videos para adjuntar (modo por Test Key)...")

                # 4.1: intentar mapping por Test Key (ATC-123.mp4, etc.)
                videos_by_key = self.find_videos_by_test_key(module_name)

                if videos_by_key:
                    print(f"   🔗 Mapeos detectados: {len(videos_by_key)} archivo(s) por Test Key")
                    try:
                        runs = self._get_runs_with_keys_by_exec_key(test_exec_key, limit=100)
                        if not runs:
                            print("   ⚠️ No se hallaron Test Runs en el Test Execution.")
                            result_entry['video_note'] = 'No Test Runs found'
                        else:
                            ok = 0
                            missing = 0
                            for rid, tkey in runs:
                                video_path = videos_by_key.get(tkey)
                                if not video_path:
                                    # No hay video específico para este test
                                    missing += 1
                                    continue
                                try:
                                    print(f"      📎 {tkey} -> {os.path.basename(video_path)}")
                                    self._add_video_to_testrun_rest(rid, video_path, tkey)
                                    ok += 1
                                except Exception as e:
                                    print(f"      ⚠️ Falló run {rid} ({tkey}): {e}")

                            if ok > 0:
                                print(f"   ✅ Video(s) adjuntado(s) a {ok}/{len(runs)} Test Run(s).")
                                result_entry['video_attached'] = True
                                result_entry['test_runs_count'] = ok
                            if missing > 0:
                                print(f"   ℹ️ {missing} Test Run(s) sin video mapeado por key.")

                    except Exception as e:
                        print(f"   ❌ Error adjuntando evidencia: {e}")
                        import traceback
                        traceback.print_exc()
                        result_entry['video_note'] = f'Error: {str(e)}'

                else:
                    # 4.2: si NO hay nombres por Test Key, caemos al comportamiento anterior (1 video para todos)
                    print(
                        f"   ℹ️ No se encontraron videos con nombre de Test Key en {self.BASE_VIDEOS_DIR}/{module_name}")
                    # Fallback: un solo video (último del módulo)
                    video = self.find_video_for_module(module_name)
                    if video:
                        try:
                            # Reutilizar el fetch de runs (sin keys también sirve)
                            runs = self._get_runs_with_keys_by_exec_key(test_exec_key, limit=100)
                            if not runs:
                                print("   ⚠️ No se hallaron Test Runs en el Test Execution.")
                                result_entry['video_note'] = 'No Test Runs found'
                            else:
                                ok = 0
                                for rid, _ in runs:
                                    try:
                                        self._add_video_to_testrun(rid, video, f"Video {module_name}")
                                        ok += 1
                                    except Exception as e:
                                        print(f"      ⚠️ Falló run {rid}: {e}")
                                if ok > 0:
                                    print(f"   ✅ Video adjuntado a {ok}/{len(runs)} Test Run(s) (fallback).")
                                    result_entry['video_attached'] = True
                                    result_entry['test_runs_count'] = ok
                        except Exception as e:
                            print(f"   ❌ Error en fallback de evidencia: {e}")
                            result_entry['video_note'] = f'Fallback error: {str(e)}'
                    else:
                        print(f"   ℹ️ Tampoco hay video genérico para el módulo '{module_name}'")
                        result_entry['video_note'] = 'No video found'

            results_summary.append(result_entry)

        # Mostrar resumen final
        self.print_summary(results_summary)

    # =========================
    #   RESUMEN
    # =========================
    def print_summary(self, results_summary):
        """Mostrar resumen de resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE SUBIDA A XRAY")
        print("=" * 60)

        success_count = sum(1 for r in results_summary if r['status'] == 'SUCCESS')
        failed_count = sum(1 for r in results_summary if r['status'] == 'FAILED')
        skipped_count = sum(1 for r in results_summary if r['status'] == 'SKIPPED')
        videos_attached = sum(1 for r in results_summary if r.get('video_attached', False))

        print(f"✅ Exitosos: {success_count}")
        print(f"❌ Fallidos: {failed_count}")
        print(f"⏭️ Omitidos: {skipped_count}")
        print(f"🎥 Videos adjuntados: {videos_attached}")
        print(f"📊 Total: {len(results_summary)}")
        print()

        for result in results_summary:
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌" if result['status'] == 'FAILED' else "⏭️"
            print(f"{status_icon} {result['module']} - {result['status']}")

            if 'file' in result:
                print(f"   📄 {result['file']}")

            if result.get('testExecutionKey'):
                print(f"   🔑 {result['testExecutionKey']}")

            if result.get('video_attached'):
                print(f"   🎥 Video adjuntado a {result.get('test_runs_count', '?')} Test Run(s)")
            elif 'video_note' in result:
                print(f"   💭 Video: {result['video_note']}")

            if 'reason' in result:
                print(f"   💭 {result['reason']}")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Subir resultados de tests a Xray por módulos y adjuntar evidencia de video a cada Test Run",
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
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()