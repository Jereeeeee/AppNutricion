"""
Modelos de base de datos para la aplicación de nutrición
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class Paciente(Base):
    """Modelo para almacenar información de pacientes"""
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    rut = Column(String(20), unique=True)  # RUT Chileno: Ej. 12.345.678-9
    fecha_nacimiento = Column(Date)
    sexo = Column(String(10))  # Masculino/Femenino
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    ocupacion = Column(String(100))
    fecha_registro = Column(DateTime, default=datetime.now)
    
    # Relaciones
    mediciones = relationship("Medicion", back_populates="paciente", cascade="all, delete-orphan")
    pautas = relationship("Pauta", back_populates="paciente", cascade="all, delete-orphan")
    historial = relationship("HistorialClinico", back_populates="paciente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Paciente {self.nombre} {self.apellidos}>"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"


class Medicion(Base):
    """Modelo para mediciones antropométricas"""
    __tablename__ = 'mediciones'
    
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    fecha = Column(Date, nullable=False, default=datetime.now().date())
    
    # Medidas corporales
    peso = Column(Float)  # kg
    altura = Column(Float)  # cm
    imc = Column(Float)  # Calculado automáticamente
    
    # Perímetros (cm)
    perimetro_cintura = Column(Float)
    perimetro_cadera = Column(Float)
    perimetro_brazo = Column(Float)
    
    # Pliegues cutáneos (mm)
    pliegue_tricipital = Column(Float)
    pliegue_subescapular = Column(Float)
    pliegue_abdominal = Column(Float)
    
    # Composición corporal
    porcentaje_grasa = Column(Float)
    masa_muscular = Column(Float)
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="mediciones")
    
    def __repr__(self):
        return f"<Medicion {self.fecha} - Peso: {self.peso}kg>"
    
    def calcular_imc(self):
        """Calcula el IMC automáticamente"""
        if self.peso and self.altura:
            altura_metros = self.altura / 100
            self.imc = round(self.peso / (altura_metros ** 2), 2)
        return self.imc


class HistorialClinico(Base):
    """Modelo para historial clínico del paciente"""
    __tablename__ = 'historial_clinico'
    
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    
    # Información clínica
    patologias = Column(Text)  # Enfermedades actuales
    alergias = Column(Text)  # Alergias alimentarias
    intolerancias = Column(Text)  # Intolerancias
    medicamentos = Column(Text)  # Medicación actual
    antecedentes_familiares = Column(Text)
    
    # Hábitos
    actividad_fisica = Column(String(50))  # Sedentario, Ligero, Moderado, Intenso
    habito_tabaquico = Column(String(50))
    consumo_alcohol = Column(String(50))
    
    # Objetivos
    objetivo_principal = Column(Text)
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="historial")
    
    def __repr__(self):
        return f"<HistorialClinico {self.fecha}>"


class Pauta(Base):
    """Modelo para pautas nutricionales"""
    __tablename__ = 'pautas'
    
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    
    # Información nutricional
    calorias_objetivo = Column(Integer)
    proteinas = Column(Float)  # gramos
    carbohidratos = Column(Float)  # gramos
    grasas = Column(Float)  # gramos
    
    # Número de comidas
    num_comidas = Column(Integer, default=5)
    
    # Detalles de la pauta
    titulo = Column(String(200))
    descripcion = Column(Text)
    indicaciones = Column(Text)
    
    # Comidas (JSON o texto estructurado)
    desayuno = Column(Text)
    media_manana = Column(Text)
    almuerzo = Column(Text)
    merienda = Column(Text)
    cena = Column(Text)
    
    # Relaciones
    paciente = relationship("Paciente", back_populates="pautas")
    
    def __repr__(self):
        return f"<Pauta {self.titulo} - {self.fecha_creacion}>"


class Database:
    """Clase para gestionar la base de datos"""
    
    def __init__(self, db_path='data/nutricion.db'):
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Crear engine y sesión
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_session(self):
        """Retorna la sesión de la base de datos"""
        return self.session
    
    def close(self):
        """Cierra la conexión"""
        self.session.close()
