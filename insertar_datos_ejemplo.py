"""
Script para insertar datos de ejemplo en la base de datos
Útil para probar la aplicación
"""
from datetime import datetime, date, timedelta
from src.database import Database
from src.database.db_utils import (
    crear_paciente, crear_medicion, crear_historial_clinico, crear_pauta
)


def insertar_datos_ejemplo():
    """Inserta datos de ejemplo en la base de datos"""
    
    # Inicializar base de datos
    db = Database('data/nutricion.db')
    session = db.get_session()
    
    print("🔄 Insertando datos de ejemplo...")
    
    # Paciente 1: María González
    paciente1 = crear_paciente(
        session,
        nombre="María",
        apellidos="González López",
        rut="12.345.678-9",
        fecha_nacimiento=date(1985, 5, 15),
        sexo="Femenino",
        telefono="+56 9 1234 5678",
        email="maria.gonzalez@email.com",
        direccion="Avenida Principal 123, Santiago",
        ocupacion="Profesora"
    )
    print(f"✅ Paciente creado: {paciente1.nombre_completo()}")
    
    # Mediciones para María
    crear_medicion(
        session,
        paciente_id=paciente1.id,
        fecha=date.today() - timedelta(days=90),
        peso=72.5,
        altura=165,
        perimetro_cintura=85,
        perimetro_cadera=98,
        porcentaje_grasa=32.5
    )
    
    crear_medicion(
        session,
        paciente_id=paciente1.id,
        fecha=date.today() - timedelta(days=60),
        peso=70.2,
        altura=165,
        perimetro_cintura=82,
        perimetro_cadera=96,
        porcentaje_grasa=30.8
    )
    
    crear_medicion(
        session,
        paciente_id=paciente1.id,
        fecha=date.today() - timedelta(days=30),
        peso=68.5,
        altura=165,
        perimetro_cintura=80,
        perimetro_cadera=95,
        porcentaje_grasa=29.2
    )
    
    print("✅ Mediciones creadas para María")
    
    # Historial clínico
    crear_historial_clinico(
        session,
        paciente_id=paciente1.id,
        patologias="Hipotiroidismo controlado",
        alergias="Frutos secos",
        intolerancias="Lactosa",
        medicamentos="Levotiroxina 50mcg",
        actividad_fisica="Moderado",
        objetivo_principal="Pérdida de peso y mejora de composición corporal"
    )
    print("✅ Historial clínico creado para María")
    
    # Pauta nutricional
    crear_pauta(
        session,
        paciente_id=paciente1.id,
        fecha_inicio=date.today() - timedelta(days=30),
        fecha_fin=date.today() + timedelta(days=60),
        calorias_objetivo=1600,
        proteinas=120,
        carbohidratos=150,
        grasas=55,
        titulo="Plan de Pérdida de Peso",
        descripcion="Plan personalizado para pérdida de peso gradual",
        desayuno="• Tostadas integrales (2 rebanadas)\n• Jamón de pavo (60g)\n• Aguacate (1/4)\n• Café con bebida vegetal",
        media_manana="• Yogur vegetal natural (1 unidad)\n• Arándanos (50g)\n• Almendras (15g)",
        almuerzo="• Ensalada verde variada\n• Pechuga de pollo a la plancha (150g)\n• Arroz integral (60g peso crudo)\n• Aceite de oliva (1 cucharada)",
        merienda="• Batido de proteínas con fruta\n• Plátano (1 unidad pequeña)",
        cena="• Salmón al horno (120g)\n• Verduras asadas (berenjena, calabacín, pimiento)\n• Patata cocida (100g)\n• Aceite de oliva (1 cucharada)",
        indicaciones="• Beber mínimo 2 litros de agua al día\n• Evitar frutos secos por alergia\n• Usar bebidas vegetales sin lactosa\n• Realizar ejercicio moderado 3-4 veces por semana\n• No saltarse comidas\n• Respetar horarios de comida"
    )
    print("✅ Pauta nutricional creada para María")
    
    # Paciente 2: Carlos Rodríguez
    paciente2 = crear_paciente(
        session,
        nombre="Carlos",
        apellidos="Rodríguez Pérez",
        rut="87.654.321-0",
        fecha_nacimiento=date(1992, 8, 22),
        sexo="Masculino",
        telefono="+56 9 8765 4321",
        email="carlos.rodriguez@email.com",
        direccion="Paseo Central 45, Valparaíso",
        ocupacion="Ingeniero"
    )
    print(f"✅ Paciente creado: {paciente2.nombre_completo()}")
    
    # Mediciones para Carlos
    crear_medicion(
        session,
        paciente_id=paciente2.id,
        fecha=date.today() - timedelta(days=45),
        peso=78.0,
        altura=178,
        perimetro_cintura=88,
        perimetro_cadera=95,
        porcentaje_grasa=18.5
    )
    
    crear_medicion(
        session,
        paciente_id=paciente2.id,
        fecha=date.today() - timedelta(days=15),
        peso=80.5,
        altura=178,
        perimetro_cintura=89,
        perimetro_cadera=96,
        porcentaje_grasa=17.8,
        masa_muscular=66.2
    )
    print("✅ Mediciones creadas para Carlos")
    
    # Historial clínico
    crear_historial_clinico(
        session,
        paciente_id=paciente2.id,
        patologias="Ninguna",
        alergias="Ninguna",
        intolerancias="Ninguna",
        medicamentos="Ninguno",
        actividad_fisica="Activo",
        habito_tabaquico="No fumador",
        consumo_alcohol="Ocasional",
        objetivo_principal="Ganancia de masa muscular"
    )
    print("✅ Historial clínico creado para Carlos")
    
    # Pauta nutricional
    crear_pauta(
        session,
        paciente_id=paciente2.id,
        fecha_inicio=date.today() - timedelta(days=15),
        fecha_fin=date.today() + timedelta(days=75),
        calorias_objetivo=2800,
        proteinas=175,
        carbohidratos=350,
        grasas=85,
        num_comidas=6,
        titulo="Plan de Ganancia Muscular",
        descripcion="Plan hipercalórico para incremento de masa muscular",
        desayuno="• Avena (80g)\n• Claras de huevo (4 unidades)\n• Plátano (1 grande)\n• Mantequilla de cacahuete (20g)\n• Café",
        media_manana="• Batido de proteína whey (30g)\n• Avena (40g)\n• Frutos rojos (100g)",
        almuerzo="• Arroz basmati (100g peso crudo)\n• Pechuga de pollo (200g)\n• Brócoli y zanahoria al vapor\n• Aceite de oliva (1 cucharada)\n• Ensalada",
        merienda="• Pan integral (80g)\n• Atún al natural (1 lata)\n• Tomate y lechuga\n• Frutas variadas",
        cena="• Pasta integral (90g peso crudo)\n• Ternera magra (180g)\n• Verduras salteadas\n• Aceite de oliva (1 cucharada)",
        indicaciones="• Beber 3-4 litros de agua al día\n• Entrenar con pesas 4-5 veces por semana\n• Descansar 7-8 horas diarias\n• Tomar batido post-entreno\n• No realizar cardio excesivo\n• Aumentar progresivamente las cargas\n• Revisar progreso cada 2 semanas"
    )
    print("✅ Pauta nutricional creada para Carlos")
    
    # Paciente 3: Ana Martínez (sin mediciones ni pautas)
    paciente3 = crear_paciente(
        session,
        nombre="Ana",
        apellidos="Martínez Sánchez",
        rut="45.678.912-3",
        fecha_nacimiento=date(1998, 12, 10),
        sexo="Femenino",
        telefono="+56 9 5123 7890",
        email="ana.martinez@email.com",
        ocupacion="Estudiante"
    )
    print(f"✅ Paciente creado: {paciente3.nombre_completo()}")
    
    print("\n✨ ¡Datos de ejemplo insertados correctamente!")
    print(f"📊 Total pacientes: 3")
    print("🏃 Puedes ejecutar la aplicación con: python main.py")
    
    db.close()


if __name__ == "__main__":
    insertar_datos_ejemplo()
