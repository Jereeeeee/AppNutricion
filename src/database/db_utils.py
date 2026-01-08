"""
Funciones de utilidad para la base de datos
"""
from .models import Database, Paciente, Medicion, HistorialClinico, Pauta
from datetime import datetime, date


def crear_paciente(session, **kwargs):
    """Crea un nuevo paciente en la base de datos"""
    paciente = Paciente(**kwargs)
    session.add(paciente)
    session.commit()
    return paciente


def obtener_todos_pacientes(session):
    """Obtiene todos los pacientes"""
    return session.query(Paciente).order_by(Paciente.apellidos).all()


def buscar_paciente_por_dni(session, dni):
    """Busca un paciente por DNI"""
    return session.query(Paciente).filter_by(dni=dni).first()


def actualizar_paciente(session, paciente_id, **kwargs):
    """Actualiza los datos de un paciente"""
    paciente = session.query(Paciente).filter_by(id=paciente_id).first()
    if paciente:
        for key, value in kwargs.items():
            if hasattr(paciente, key):
                setattr(paciente, key, value)
        session.commit()
    return paciente


def eliminar_paciente(session, paciente_id):
    """Elimina un paciente y todos sus registros relacionados"""
    paciente = session.query(Paciente).filter_by(id=paciente_id).first()
    if paciente:
        session.delete(paciente)
        session.commit()
        return True
    return False


def crear_medicion(session, paciente_id, **kwargs):
    """Crea una nueva medición para un paciente"""
    medicion = Medicion(paciente_id=paciente_id, **kwargs)
    medicion.calcular_imc()
    session.add(medicion)
    session.commit()
    return medicion


def obtener_mediciones_paciente(session, paciente_id):
    """Obtiene todas las mediciones de un paciente"""
    return session.query(Medicion).filter_by(paciente_id=paciente_id).order_by(Medicion.fecha.desc()).all()


def obtener_ultima_medicion(session, paciente_id):
    """Obtiene la última medición de un paciente"""
    return session.query(Medicion).filter_by(paciente_id=paciente_id).order_by(Medicion.fecha.desc()).first()


def crear_historial_clinico(session, paciente_id, **kwargs):
    """Crea un registro de historial clínico"""
    historial = HistorialClinico(paciente_id=paciente_id, **kwargs)
    session.add(historial)
    session.commit()
    return historial


def obtener_historial_paciente(session, paciente_id):
    """Obtiene el historial clínico de un paciente"""
    return session.query(HistorialClinico).filter_by(paciente_id=paciente_id).order_by(HistorialClinico.fecha.desc()).all()


def crear_pauta(session, paciente_id, **kwargs):
    """Crea una nueva pauta nutricional"""
    pauta = Pauta(paciente_id=paciente_id, **kwargs)
    session.add(pauta)
    session.commit()
    return pauta


def obtener_pautas_paciente(session, paciente_id):
    """Obtiene todas las pautas de un paciente"""
    return session.query(Pauta).filter_by(paciente_id=paciente_id).order_by(Pauta.fecha_creacion.desc()).all()


def obtener_pauta_activa(session, paciente_id):
    """Obtiene la pauta activa actual de un paciente"""
    hoy = date.today()
    return session.query(Pauta).filter(
        Pauta.paciente_id == paciente_id,
        Pauta.fecha_inicio <= hoy,
        Pauta.fecha_fin >= hoy
    ).first()
