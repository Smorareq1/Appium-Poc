import pytest
import json
import os
from appium.webdriver.common.appiumby import AppiumBy


class TestDataDrivenSuite:
    """Suite de tests que usa datos externos (perfecto para Jira/Xray integration)"""

    @pytest.fixture(scope="class")
    def load_test_scenarios(self):
        """Cargar escenarios de test desde archivo JSON"""
        test_data_file = "test_data/click_scenarios.json"

        if not os.path.exists(test_data_file):
            # Crear datos de ejemplo si no existe el archivo
            os.makedirs("test_data", exist_ok=True)
            sample_data = {
                "click_scenarios": [
                    {
                        "test_id": "TC001",
                        "name": "Quick Clicks Test",
                        "click_count": 5,
                        "delay_between_clicks": 0.3,
                        "expected_success_rate": 0.8,
                        "jira_ticket": "PROJ-123"
                    },
                    {
                        "test_id": "TC002",
                        "name": "Standard Clicks Test",
                        "click_count": 10,
                        "delay_between_clicks": 0.5,
                        "expected_success_rate": 0.9,
                        "jira_ticket": "PROJ-124"
                    },
                    {
                        "test_id": "TC003",
                        "name": "Stress Clicks Test",
                        "click_count": 15,
                        "delay_between_clicks": 0.2,
                        "expected_success_rate": 0.7,
                        "jira_ticket": "PROJ-125"
                    }
                ]
            }
            with open(test_data_file, 'w') as f:
                json.dump(sample_data, f, indent=2)
            print(f"📝 Archivo de datos de ejemplo creado: {test_data_file}")

        with open(test_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def test_click_scenarios_from_data(self, driver, screenshot, load_test_scenarios):
        """Test que ejecuta múltiples escenarios definidos en JSON"""

        scenarios = load_test_scenarios.get('click_scenarios', [])

        for scenario in scenarios:
            test_id = scenario['test_id']
            name = scenario['name']
            click_count = scenario['click_count']
            delay = scenario['delay_between_clicks']
            expected_rate = scenario['expected_success_rate']
            jira_ticket = scenario.get('jira_ticket', 'N/A')

            print(f"🧪 Ejecutando: {test_id} - {name} (Jira: {jira_ticket})")

            # Tomar screenshot inicial para este escenario
            screenshot(f"scenario_{test_id}_start")

            # Buscar elementos clickeables
            clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

            successful_clicks = 0

            if clickable_elements:
                target_element = clickable_elements[0]

                for i in range(click_count):
                    try:
                        target_element.click()
                        successful_clicks += 1
                        import time
                        time.sleep(delay)
                    except Exception as e:
                        print(f"❌ Click {i + 1} falló: {e}")
            else:
                # Fallback a coordenadas
                screen_size = driver.get_window_size()
                center_x = screen_size["width"] // 2
                center_y = screen_size["height"] // 2

                for i in range(click_count):
                    try:
                        driver.tap([(center_x, center_y)], 100)
                        successful_clicks += 1
                        import time
                        time.sleep(delay)
                    except:
                        pass

            # Calcular success rate
            actual_success_rate = successful_clicks / click_count

            # Screenshot final del escenario
            screenshot(f"scenario_{test_id}_end")

            # Assertion basada en los datos del escenario
            assert actual_success_rate >= expected_rate, \
                f"Scenario {test_id} failed: {actual_success_rate:.2%} < {expected_rate:.2%} expected (Jira: {jira_ticket})"

            print(f"✅ {test_id} PASSED: {successful_clicks}/{click_count} clicks ({actual_success_rate:.2%})")

    @pytest.mark.parametrize("scenario_data", [
        {"test_id": "TC001", "clicks": 3, "expected_rate": 0.8},
        {"test_id": "TC002", "clicks": 7, "expected_rate": 0.9},
        {"test_id": "TC003", "clicks": 12, "expected_rate": 0.7},
    ])
    def test_parametrized_clicks(self, driver, screenshot, scenario_data):
        """Test parametrizado que simula casos definidos en Jira"""

        test_id = scenario_data["test_id"]
        click_count = scenario_data["clicks"]
        expected_rate = scenario_data["expected_rate"]

        print(f"🎯 Test parametrizado: {test_id} ({click_count} clicks)")

        screenshot(f"param_test_{test_id}_start")

        # Lógica del test
        successful_clicks = 0

        # Buscar botón o usar coordenadas
        try:
            clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            if clickable_elements:
                element = clickable_elements[0]
                for _ in range(click_count):
                    try:
                        element.click()
                        successful_clicks += 1
                        import time
                        time.sleep(0.2)
                    except:
                        pass
            else:
                # Fallback a tap en centro
                screen_size = driver.get_window_size()
                for _ in range(click_count):
                    try:
                        driver.tap([(screen_size["width"] // 2, screen_size["height"] // 2)], 100)
                        successful_clicks += 1
                        import time
                        time.sleep(0.2)
                    except:
                        pass
        except Exception as e:
            pytest.fail(f"Error en test {test_id}: {e}")

        screenshot(f"param_test_{test_id}_end")

        # Validación
        actual_rate = successful_clicks / click_count

        assert actual_rate >= expected_rate, \
            f"Test {test_id}: Rate {actual_rate:.2%} < {expected_rate:.2%} expected"

        print(f"✅ {test_id}: {successful_clicks}/{click_count} ({actual_rate:.2%})")


class TestCompatibilityJira:
    """Tests diseñados específicamente para integración con Jira/Xray"""

    @pytest.mark.jira("PROJ-100")
    @pytest.mark.smoke
    def test_critical_app_launch(self, driver, screenshot):
        """Test crítico mapeado a ticket Jira PROJ-100"""
        screenshot("critical_test_start")

        # Verificar que la app se lanza
        assert driver.current_package is not None
        assert driver.current_activity is not None

        screenshot("critical_test_end")

        print("✅ Critical app launch test completed (Jira: PROJ-100)")

    @pytest.mark.jira("PROJ-101")
    @pytest.mark.regression
    def test_ui_elements_visibility(self, driver, screenshot):
        """Test de regresión mapeado a ticket Jira PROJ-101"""
        screenshot("ui_elements_test")

        # Buscar elementos en la UI
        all_elements = driver.find_elements(AppiumBy.XPATH, "//*")
        clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")

        # Validaciones
        assert len(all_elements) > 0, "Should find at least some UI elements"
        assert len(clickable_elements) >= 0, "Clickable elements search should not fail"

        print(
            f"✅ UI elements test completed - Found {len(all_elements)} total, {len(clickable_elements)} clickable (Jira: PROJ-101)")


# Función para generar reportes compatibles con Jira/Xray
def generate_xray_report(test_results):
    """Generar reporte en formato compatible con Xray"""

    xray_format = {
        "testExecutionKey": "DEMO-123",
        "info": {
            "summary": "Automated Flutter App Tests",
            "description": "Test execution from Pytest Appium suite",
            "user": "automation@company.com",
            "startDate": "2024-01-15T09:00:00Z",
            "finishDate": "2024-01-15T09:30:00Z"
        },
        "tests": []
    }

    # Convertir resultados de pytest a formato Xray
    for test in test_results:
        xray_test = {
            "testKey": test.get("test_id", "UNKNOWN"),
            "status": "PASS" if test["passed"] else "FAIL",
            "comment": test.get("comment", ""),
            "evidences": []
        }

        # Agregar screenshots como evidencias
        if test.get("screenshots"):
            for screenshot in test["screenshots"]:
                xray_test["evidences"].append({
                    "data": screenshot,
                    "filename": f"{test['test_id']}_evidence.png",
                    "contentType": "image/png"
                })

        xray_format["tests"].append(xray_test)

    return xray_format


# Hook personalizado para capturar datos para Xray
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capturar datos de tests para generar reporte Xray"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Extraer información del test para Xray
        if hasattr(item, 'funcargs'):
            # Buscar test_id en los parámetros
            scenario_data = item.funcargs.get('scenario_data')
            if scenario_data and isinstance(scenario_data, dict):
                test_id = scenario_data.get('test_id')
                if test_id:
                    report.test_id = test_id

        # Marcar si el test pasó o falló
        report.passed = report.outcome == "passed"

        # Agregar metadatos adicionales
        report.test_metadata = {
            "execution_time": getattr(report, 'duration', 0),
            "node_id": item.nodeid,
            "markers": [mark.name for mark in item.iter_markers()]
        }


# Configuración para markers de Jira
def pytest_configure(config):
    """Registrar marker personalizado para Jira tickets"""
    config.addinivalue_line(
        "markers", "jira(ticket): mark test as linked to specific Jira ticket"
    )