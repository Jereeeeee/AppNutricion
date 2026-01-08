#!/usr/bin/env python
"""Script de configuración inicial"""
import os
import sys

# Cambiar al directorio de la app
os.chdir(r"c:\Users\jeremy.contreras\Desktop\AppNutricion")

# Mostrar el directorio actual
print(f"Directorio: {os.getcwd()}")

# Verificar si la DB existe
db_path = "data/nutricion.db"
if os.path.exists(db_path):
    print(f"✅ Base de datos existe: {db_path}")
    size = os.path.getsize(db_path)
    print(f"   Tamaño: {size} bytes")
else:
    print(f"❌ Base de datos NO existe: {db_path}")
    # Crear directorio si no existe
    os.makedirs("data", exist_ok=True)

# Intentar importar modelos
try:
    from src.database.models import Paciente
    print("✅ Modelos importados correctamente")
except Exception as e:
    print(f"❌ Error importando modelos: {e}")
    sys.exit(1)

# Intentar insertar datos
try:
    print("\n🔄 Insertando datos de ejemplo...")
    import insertar_datos_ejemplo
    insertar_datos_ejemplo.insertar_datos_ejemplo()
    print("✅ Datos insertados correctamente")
except Exception as e:
    print(f"❌ Error insertando datos: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Verificar que los datos se insertaron
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    paciente = session.query(Paciente).first()
    if paciente:
        print(f"\n✅ Paciente encontrado: {paciente.nombre_completo()}")
        print(f"   RUT: {paciente.rut}")
    else:
        print("\n⚠️ No hay pacientes en la base de datos")
    
    session.close()
except Exception as e:
    print(f"❌ Error verificando datos: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Setup completado")
