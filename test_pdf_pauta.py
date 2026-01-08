"""
Script de prueba para generar un PDF con pauta de 7 días
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.database.db_utils import obtener_todos_pacientes, obtener_mediciones_paciente, obtener_historial_paciente
from src.utils.pdf_generator import GeneradorInformes

def main():
    # Conectar a la BD
    db = Database('data/nutricion.db')
    session = db.get_session()
    
    # Obtener primer paciente
    pacientes = obtener_todos_pacientes(session)
    
    if not pacientes:
        print("❌ No hay pacientes en la base de datos")
        return
    
    paciente = pacientes[0]
    print(f"✅ Generando PDF para: {paciente.nombre_completo()}")
    
    # Obtener datos
    mediciones = obtener_mediciones_paciente(session, paciente.id)
    historial = obtener_historial_paciente(session, paciente.id)
    
    # Generar PDF SIN pauta (para forzar el ejemplo de 7 días)
    generador = GeneradorInformes()
    ruta_pdf = generador.generar_informe_paciente(
        paciente, 
        mediciones, 
        historial, 
        pauta=None  # Forzamos None para ver la pauta de ejemplo
    )
    
    print(f"✅ PDF generado: {ruta_pdf}")
    print(f"\n📍 La pauta de 7 días aparece después de:")
    print("   1. Datos del paciente")
    print("   2. Mediciones antropométricas (si hay)")
    print("   3. Historial clínico (si hay)")
    print("   4. [NUEVA PÁGINA] PAUTA DE EJEMPLO (AUTOGENERADA)")
    print("      - Calorías y macros calculados")
    print("      - Plan semanal de ejemplo (7 días)")
    print("        • Día 1, Día 2, ... Día 7")
    print("        • Cada día con: Desayuno, Media Mañana, Almuerzo, Merienda, Cena")
    
    # Abrir el PDF
    os.startfile(ruta_pdf)

if __name__ == '__main__':
    main()
