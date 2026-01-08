"""
Script de diagnóstico para verificar generación de PDF
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.database.db_utils import obtener_todos_pacientes, obtener_mediciones_paciente, obtener_historial_paciente, obtener_pautas_paciente
from src.utils.pdf_generator import GeneradorInformes

def main():
    db = Database('data/nutricion.db')
    session = db.get_session()
    
    pacientes = obtener_todos_pacientes(session)
    
    if not pacientes:
        print("❌ No hay pacientes")
        return
    
    paciente = pacientes[0]
    print(f"📋 Paciente: {paciente.nombre_completo()}")
    
    mediciones = obtener_mediciones_paciente(session, paciente.id)
    historial = obtener_historial_paciente(session, paciente.id)
    pautas = obtener_pautas_paciente(session, paciente.id)
    
    print(f"📊 Mediciones: {len(mediciones)}")
    print(f"🏥 Historial: {len(historial)}")
    print(f"📝 Pautas guardadas: {len(pautas)}")
    
    pauta_activa = pautas[0] if pautas else None
    
    if pauta_activa:
        print(f"⚠️  Hay una pauta guardada: {pauta_activa.titulo}")
        print(f"   Por eso NO se genera la pauta de 7 días automática")
    else:
        print(f"✅ NO hay pauta guardada")
        print(f"   Se generará PAUTA NUTRICIONAL automática de 7 días")
    
    print(f"\n🔄 Generando PDF...")
    generador = GeneradorInformes()
    ruta_pdf = generador.generar_informe_paciente(
        paciente, 
        mediciones, 
        historial, 
        pauta_activa
    )
    
    print(f"✅ PDF generado: {ruta_pdf}")
    
    # Abrir
    os.startfile(ruta_pdf)

if __name__ == '__main__':
    main()
