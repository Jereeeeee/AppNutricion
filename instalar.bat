@echo off
echo ========================================
echo    App Nutricion - Instalador
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor, instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)
echo.

echo [2/3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo.

echo [3/3] Insertando datos de ejemplo...
python insertar_datos_ejemplo.py
echo.

echo ========================================
echo    Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion, usa:
echo     ejecutar.bat
echo.
echo O directamente:
echo     python main.py
echo.
pause
