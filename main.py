"""
App Nutrición - Sistema de Gestión Nutricional
Aplicación de escritorio para nutricionistas

Punto de entrada principal de la aplicación
"""
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.ui import VentanaPrincipal


def main():
    """Función principal que inicia la aplicación"""
    
    # Crear directorios necesarios
    os.makedirs('data', exist_ok=True)
    os.makedirs('informes', exist_ok=True)
    
    # Inicializar base de datos
    db = Database('data/nutricion.db')
    session = db.get_session()
    
    # Crear y ejecutar la aplicación
    app = VentanaPrincipal(session)
    
    # Centrar la ventana en la pantalla
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar loop de la aplicación
    try:
        app.mainloop()
    finally:
        # Cerrar la sesión de base de datos al salir
        db.close()


if __name__ == "__main__":
    main()
