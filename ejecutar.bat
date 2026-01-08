@echo off
echo ========================================
echo    Iniciando App Nutricion...
echo ========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: La aplicacion se cerro inesperadamente
    echo.
    echo Si es la primera vez, ejecuta: instalar.bat
    echo.
    pause
)
