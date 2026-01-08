"""
Inicialización del paquete de utilidades
"""
from .pdf_generator import GeneradorInformes
from .calculadora import *

__all__ = [
    'GeneradorInformes',
    'calcular_imc',
    'clasificar_imc',
    'calcular_tmb_harris_benedict',
    'calcular_calorias_objetivo',
    'calcular_macronutrientes',
]
