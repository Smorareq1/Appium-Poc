# Appium Mobile Testing Framework

Framework de automatización para testing de aplicaciones móviles usando Appium y Pytest, con reportes organizados por módulos y grabación de video automática.

## Características Principales

- **Ejecución por módulos**: Tests organizados en carpetas separadas con reportes independientes
- **Grabación automática**: Video de cada test guardado automáticamente
- **Reportes múltiples**: HTML y XML generados por módulo, combinables para Xray
- **Debug avanzado**: Múltiples niveles de verbosidad (equivalente a `pytest -v -s` por defecto)
- **Scripts de gestión**: Comandos simplificados para Windows y Linux/Mac
- **Configuración centralizada**: Variables de entorno y configuración flexible

## Estructura del Proyecto

```
proyecto/
├── tests/                          # Directorio principal de tests
│   ├── login/                      # Módulo de login
│   │   ├── test_login.py          # Tests de autenticación
│   │   └── test_user_auth.py      # Tests adicionales de usuario
│   ├── navigation/                 # Módulo de navegación
│   │   ├── test_menu.py           # Tests de menú
│   │   └── test_sidebar.py        # Tests de sidebar
│   └── test_simple_flow.py        # Tests individuales
├── pytest_reports/                # Reportes organizados por módulo
│   ├── login/
│   │   ├── report_login_20240101_120000.html
│   │   └── result_login_20240101_120000.xml
│   ├── navigation/
│   │   ├── report_navigation_20240101_120000.html
│   │   └── result_navigation_20240101_120000.xml
│   ├── summary_20240101_120000.md  # Resumen de todos los módulos
│   └── merged_results.xml          # Combinado para Xray
├── pytest_videos/                 # Videos organizados por módulo
│   ├── login/
│   │   └── test_01_click_registrarme_20240101_120000.mp4
│   └── navigation/
│       └── test_navigation_flow_20240101_120000.mp4
├── pytest_logs/                   # Logs por módulo
├── conftest.py                     # Configuración de fixtures
├── pytest.ini                     # Configuración de pytest
├── test_runner.py                  # Script gestor principal
├── run_tests.bat                   # Script para Windows
├── run_tests.sh                    # Script para Linux/Mac
├── .env                           # Variables de entorno
└── README.md                      # Esta documentación
```

## Requisitos del Sistema

### Software Requerido

- **Python 3.8+**
- **Android SDK** (platform-tools en PATH)
- **Appium Server** 2.0+
- **Emulador Android** o dispositivo físico

### Dependencias Python

```bash
pip install pytest
pip install appium-python-client
pip install selenium
pip install pytest-html
pip install python-dotenv
pip install requests
```

## Configuración Inicial

### 1. Variables de Entorno

Crear archivo `.env` en el directorio raíz:

```env
# Ruta del APK a testear
APK_PATH=C:\Users\usuario\ruta\a\tu\app-release.apk

# Configuración del dispositivo
DEVICE_NAME=emulator-5554
PLATFORM_VERSION=15

# Servidor Appium
APPIUM_SERVER=http://127.0.0.1:4723
```

### 2. Verificar ADB

```bash
# Verificar que ADB está en PATH
adb version

# Listar dispositivos conectados
adb devices
```

### 3. Iniciar Appium Server

```bash
# Iniciar servidor Appium
appium server --port 4723
```

### 4. Preparar Scripts (Linux/Mac)

```bash
# Hacer ejecutable el script
chmod +x run_tests.sh
```

## Uso Básico

### Comandos Principales

#### Listar Módulos Disponibles

```bash
# Windows
run_tests.bat list

# Linux/Mac
./run_tests.sh list
```

#### Ejecutar Módulo Específico

```bash
# Windows
run_tests.bat module login
run_tests.bat login

# Linux/Mac
./run_tests.sh module login
./run_tests.sh login
```

#### Ejecutar Todos los Módulos

```bash
# Windows
run_tests.bat all

# Linux/Mac
./run_tests.sh all
```

#### Combinar Reportes XML

```bash
# Windows
run_tests.bat merge

# Linux/Mac
./run_tests.sh merge
```

### Opciones de Debug

#### Modo Normal (Por Defecto)
Equivalente a `pytest -v -s` - máxima verbosidad con output visible

```bash
# Estos comandos usan modo normal por defecto
./run_tests.sh module login
run_tests.bat all
```

#### Modo Debug Máximo

```bash
# Windows
run_tests.bat module login --debug
run_tests.bat debug

# Linux/Mac
./run_tests.sh module login --debug
./run_tests.sh debug
```

#### Modo Silencioso

```bash
# Windows
run_tests.bat module login --quiet
run_tests.bat quiet

# Linux/Mac
./run_tests.sh module login --quiet
./run_tests.sh quiet
```

### Uso Directo con Python

```bash
# Comando básico
python test_runner.py --module login

# Con opciones de debug
python test_runner.py --module login --debug
python test_runner.py --all --quiet

# Listar módulos
python test_runner.py --list

# Combinar reportes
python test_runner.py --merge
```

## Organización de Tests

### Estructura por Módulos

**Opción 1: Por Carpetas**
```
tests/
├── login/
│   ├── test_auth.py
│   └── test_passwords.py
└── navigation/
    └── test_menu.py
```

**Opción 2: Por Archivos**
```
tests/
├── test_login.py
├── test_navigation.py
└── test_simple_flow.py
```

### Convenciones de Nombres

- **Archivos**: `test_*.py` o `*_test.py`
- **Clases**: `Test*` o nombres específicos como `Login`
- **Funciones**: `test_*`
- **Módulos**: Se detectan automáticamente del nombre de carpeta/archivo

## Reportes y Videos

### Estructura de Reportes

Cada módulo genera:
- **HTML**: Reporte visual detallado
- **XML**: Compatible con Xray/JIRA
- **Videos**: Grabación automática de cada test
- **Logs**: Output detallado por módulo

### Nombres de Archivos

```
pytest_reports/login/
├── report_login_20240315_143022.html
└── result_login_20240315_143022.xml

pytest_videos/login/
└── test_01_click_registrarme_20240315_143022.mp4
```

### Reporte Resumen

Archivo `summary_TIMESTAMP.md` con estadísticas de todos los módulos:

```markdown
# Reporte Resumen de Tests
**Fecha:** 2024-03-15 14:30:22

## Estadísticas Generales
- **Total de módulos:** 3
- **Módulos exitosos:** 2
- **Módulos con fallos:** 1

## Detalles por Módulo
### login - ✅ EXITOSO
- **Ruta:** `tests/login/`
- **Reporte HTML:** `pytest_reports/login/report_login_20240315_143022.html`
```

## Configuración de Fixtures

### Driver Compartido

El driver se crea **una vez por sesión** y se reutiliza entre tests del mismo módulo para mayor velocidad.

### Grabación de Video

- Automática para cada test
- Organizada por módulo
- Limpieza automática del dispositivo

### Variables de Entorno por Módulo

```python
# En conftest.py
test_env.module_name = os.getenv('PYTEST_MODULE_NAME', 'general')
test_env.videos_dir = os.path.join("pytest_videos", module_name)
```

## Integración con Xray/JIRA

### Markers de Tests

```python
@pytest.mark.xray("APPTEST-10")
def test_01_click_registrarme(self, driver, video_recorder):
    # Test implementation
```

### Subir Resultados a Xray

```bash
# Generar reporte combinado
./run_tests.sh merge

# El archivo merged_results.xml se puede subir directamente a Xray
```

## Troubleshooting

### Problemas Comunes

#### 1. Dispositivo No Autorizado

```bash
# Verificar estado
adb devices

# Si aparece "unauthorized":
# - Acepta el diálogo en la pantalla del emulador
# - Reinicia adb: adb kill-server && adb start-server
```

#### 2. Appium Server No Disponible

```bash
# Verificar servidor
curl http://127.0.0.1:4723/status

# Iniciar servidor
appium server --port 4723
```

#### 3. APK No Encontrado

```bash
# Verificar ruta en .env
echo $APK_PATH

# Verificar que existe
ls -la "path/to/app.apk"
```

#### 4. Tests No Detectados

```bash
# Listar módulos detectados
python test_runner.py --list

# Verificar estructura de nombres
ls tests/test_*.py tests/*_test.py
```

### Debug de Tests

#### Ver Output Completo

```bash
# Modo debug máximo
./run_tests.sh module login --debug

# Comando pytest equivalente
python -m pytest tests/login/ -v -vv -s --tb=short --show-capture=all
```

#### Ejecutar Test Individual

```bash
# Ejecutar un test específico
python -m pytest tests/login/test_login.py::Login::test_01_click_registrarme -v -s
```

## Desarrollo y Contribución

### Agregar Nuevos Tests

1. **Crear estructura**:
   ```bash
   mkdir tests/nuevo_modulo
   touch tests/nuevo_modulo/test_nuevo_modulo.py
   ```

2. **Seguir convenciones**:
   ```python
   import pytest
   from appium.webdriver.common.appiumby import AppiumBy

   class TestNuevoModulo:
       @pytest.mark.xray("APPTEST-XX")
       def test_nueva_funcionalidad(self, driver, video_recorder):
           # Test implementation
           pass
   ```

3. **Verificar detección**:
   ```bash
   ./run_tests.sh list
   ```

### Modificar Configuración

- **pytest.ini**: Configuración global de pytest
- **conftest.py**: Fixtures y configuración de sesión
- **test_runner.py**: Lógica de ejecución y reportes

### Variables de Entorno Personalizadas

```env
# Agregar al .env
CUSTOM_TIMEOUT=30
CUSTOM_DEVICE=pixel_5
```

```python
# Usar en conftest.py
custom_timeout = os.getenv('CUSTOM_TIMEOUT', '15')
```

## Comandos de Referencia Rápida

```bash
# Configuración inicial
./run_tests.sh list                    # Ver módulos disponibles

# Ejecución básica
./run_tests.sh module login            # Ejecutar módulo específico
./run_tests.sh all                     # Ejecutar todos los módulos

# Con opciones de debug
./run_tests.sh module login --debug    # Máximo detalle
./run_tests.sh all --quiet             # Mínimo output

# Gestión de reportes
./run_tests.sh merge                   # Combinar XML para Xray

# Debug directo
python test_runner.py --list           # Comando directo
python -m pytest tests/login/ -v -s    # Pytest tradicional
```