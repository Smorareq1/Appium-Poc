@echo off
REM ========================================
REM Scripts para ejecutar tests con reportes separados
REM Con opciones de debug (equivalente a -v -s por defecto)
REM ========================================

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="list" goto list
if "%1"=="all" goto all
if "%1"=="merge" goto merge
if "%1"=="module" goto module
if "%1"=="login" goto login
if "%1"=="navigation" goto navigation
if "%1"=="debug" goto debug
if "%1"=="quiet" goto quiet

:help
echo.
echo ========================================
echo EJECUTOR DE TESTS CON REPORTES SEPARADOS
echo ========================================
echo.
echo Uso: run_tests.bat [comando] [opciones]
echo.
echo Comandos disponibles:
echo   help        - Muestra esta ayuda
echo   list        - Lista todos los módulos disponibles
echo   all         - Ejecuta todos los módulos por separado
echo   module ^<nombre^> - Ejecuta un módulo específico
echo   merge       - Combina todos los reportes XML
echo.
echo Atajos específicos:
echo   login       - Ejecuta solo tests de login
echo   navigation  - Ejecuta solo tests de navegación
echo.
echo Opciones de debug:
echo   debug       - Modo debug máximo (máxima verbosidad)
echo   quiet       - Modo silencioso (mínima verbosidad)
echo   Por defecto - Equivalente a pytest -v -s (verboso, output visible)
echo.
echo Ejemplos:
echo   run_tests.bat list
echo   run_tests.bat all
echo   run_tests.bat module login
echo   run_tests.bat login --debug
echo   run_tests.bat all --quiet
echo   run_tests.bat merge
echo.
echo 💡 NOTA: Por defecto se ejecuta con máxima verbosidad (como -v -s)
echo    para ver todos los prints y debug information.
echo.
goto end

:list
echo 📋 Listando módulos disponibles...
python test_runner.py --list
goto end

:all
if "%2"=="--debug" (
    echo 🚀 Ejecutando todos los módulos [MODO DEBUG]...
    python test_runner.py --all --debug
) else if "%2"=="--quiet" (
    echo 🚀 Ejecutando todos los módulos [MODO SILENCIOSO]...
    python test_runner.py --all --quiet
) else (
    echo 🚀 Ejecutando todos los módulos [MODO NORMAL - verboso]...
    python test_runner.py --all
)
goto end

:merge
echo 🔗 Combinando reportes XML...
python test_runner.py --merge
goto end

:module
if "%2"=="" (
    echo ❌ Error: Debes especificar el nombre del módulo
    echo Uso: run_tests.bat module ^<nombre^> [--debug^|--quiet]
    echo Usa 'run_tests.bat list' para ver módulos disponibles
    goto end
)
if "%3"=="--debug" (
    echo 🚀 Ejecutando módulo: %2 [MODO DEBUG]
    python test_runner.py --module %2 --debug
) else if "%3"=="--quiet" (
    echo 🚀 Ejecutando módulo: %2 [MODO SILENCIOSO]
    python test_runner.py --module %2 --quiet
) else (
    echo 🚀 Ejecutando módulo: %2 [MODO NORMAL - verboso]
    python test_runner.py --module %2
)
goto end

:login
if "%2"=="--debug" (
    echo 🚀 Ejecutando tests de login [MODO DEBUG]...
    python test_runner.py --module login --debug
) else if "%2"=="--quiet" (
    echo 🚀 Ejecutando tests de login [MODO SILENCIOSO]...
    python test_runner.py --module login --quiet
) else (
    echo 🚀 Ejecutando tests de login [MODO NORMAL - verboso]...
    python test_runner.py --module login
)
goto end

:navigation
if "%2"=="--debug" (
    echo 🚀 Ejecutando tests de navegación [MODO DEBUG]...
    python test_runner.py --module navigation --debug
) else if "%2"=="--quiet" (
    echo 🚀 Ejecutando tests de navegación [MODO SILENCIOSO]...
    python test_runner.py --module navigation --quiet
) else (
    echo 🚀 Ejecutando tests de navegación [MODO NORMAL - verboso]...
    python test_runner.py --module navigation
)
goto end

:debug
echo 🔧 MODO DEBUG ACTIVADO para todos los módulos...
python test_runner.py --all --debug
goto end

:quiet
echo 🔇 MODO SILENCIOSO ACTIVADO para todos los módulos...
python test_runner.py --all --quiet
goto end

:end
echo.
echo 💡 Tip: Usa '--debug' para máximo detalle o '--quiet' para menos output
pause