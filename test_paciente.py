#!/usr/bin/env python
"""Prueba de datos del paciente"""

from src.database.models import Paciente
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/nutricion.db')
Session = sessionmaker(bind=engine)
session = Session()

# Obtener primer paciente
paciente = session.query(Paciente).first()
if paciente:
    print(f'✅ Paciente: {paciente.nombre_completo()}')
    print(f'   RUT: {paciente.rut}')
    print(f'   Sexo: {paciente.sexo}')
    print(f'   Email: {paciente.email}')
    print(f'   Teléfono: {paciente.telefono}')
    print(f'   Dirección: {paciente.direccion}')
    print(f'   Ocupación: {paciente.ocupacion}')
else:
    print('❌ No hay pacientes en la base de datos')

session.close()
