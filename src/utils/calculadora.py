"""
Utilidades para cálculos nutricionales
"""


def calcular_imc(peso, altura_cm):
    """
    Calcula el Índice de Masa Corporal
    Args:
        peso: Peso en kg
        altura_cm: Altura en cm
    Returns:
        IMC redondeado a 2 decimales
    """
    if not peso or not altura_cm or altura_cm == 0:
        return None
    altura_m = altura_cm / 100
    return round(peso / (altura_m ** 2), 2)


def clasificar_imc(imc):
    """
    Clasifica el IMC según estándares de la OMS
    """
    if imc is None:
        return "No calculado"
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidad grado I"
    elif imc < 40:
        return "Obesidad grado II"
    else:
        return "Obesidad grado III"


def calcular_tmb_harris_benedict(peso, altura_cm, edad, sexo):
    """
    Calcula la Tasa Metabólica Basal usando la fórmula de Harris-Benedict
    Args:
        peso: Peso en kg
        altura_cm: Altura en cm
        edad: Edad en años
        sexo: 'Masculino' o 'Femenino'
    Returns:
        TMB en kcal/día
    """
    if sexo.lower() in ['masculino', 'hombre', 'm']:
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)
    
    return round(tmb, 0)


def calcular_calorias_objetivo(tmb, nivel_actividad, objetivo='mantenimiento'):
    """
    Calcula las calorías objetivo según nivel de actividad y objetivo
    Args:
        tmb: Tasa Metabólica Basal
        nivel_actividad: sedentario, ligero, moderado, activo, muy_activo
        objetivo: perdida, mantenimiento, ganancia
    Returns:
        Calorías objetivo diarias
    """
    # Factores de actividad
    factores = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'activo': 1.725,
        'muy_activo': 1.9
    }
    
    factor = factores.get(nivel_actividad.lower(), 1.2)
    calorias_mantenimiento = tmb * factor
    
    # Ajustar según objetivo
    if objetivo.lower() in ['perdida', 'pérdida', 'adelgazar']:
        calorias = calorias_mantenimiento - 500  # Déficit de 500 kcal
    elif objetivo.lower() in ['ganancia', 'aumentar', 'volumen']:
        calorias = calorias_mantenimiento + 300  # Superávit de 300 kcal
    else:
        calorias = calorias_mantenimiento
    
    return round(calorias, 0)


def calcular_macronutrientes(calorias_objetivo, distribucion='balanceada'):
    """
    Calcula la distribución de macronutrientes
    Args:
        calorias_objetivo: Calorías objetivo diarias
        distribucion: balanceada, alta_proteina, baja_carbohidratos
    Returns:
        Dict con gramos de proteínas, carbohidratos y grasas
    """
    distribuciones = {
        'balanceada': {'proteinas': 0.30, 'carbohidratos': 0.40, 'grasas': 0.30},
        'alta_proteina': {'proteinas': 0.35, 'carbohidratos': 0.35, 'grasas': 0.30},
        'baja_carbohidratos': {'proteinas': 0.30, 'carbohidratos': 0.20, 'grasas': 0.50},
    }
    
    dist = distribuciones.get(distribucion, distribuciones['balanceada'])
    
    # Calorías por gramo: Proteínas=4, Carbohidratos=4, Grasas=9
    proteinas = round((calorias_objetivo * dist['proteinas']) / 4, 1)
    carbohidratos = round((calorias_objetivo * dist['carbohidratos']) / 4, 1)
    grasas = round((calorias_objetivo * dist['grasas']) / 9, 1)
    
    return {
        'proteinas': proteinas,
        'carbohidratos': carbohidratos,
        'grasas': grasas
    }


def calcular_agua_recomendada(peso):
    """
    Calcula la cantidad de agua recomendada en litros
    Regla: 35ml por kg de peso corporal
    """
    return round((peso * 35) / 1000, 1)


def calcular_porcentaje_grasa_navy(perimetro_cintura, perimetro_cuello, altura, sexo, perimetro_cadera=None):
    """
    Calcula el porcentaje de grasa corporal usando el método de la Marina de EE.UU.
    """
    import math
    
    if sexo.lower() in ['masculino', 'hombre', 'm']:
        if perimetro_cintura and perimetro_cuello and altura:
            valor = 86.010 * math.log10(perimetro_cintura - perimetro_cuello) - 70.041 * math.log10(altura) + 36.76
            return round(valor, 1)
    else:  # Femenino
        if perimetro_cintura and perimetro_cuello and altura and perimetro_cadera:
            valor = 163.205 * math.log10(perimetro_cintura + perimetro_cadera - perimetro_cuello) - 97.684 * math.log10(altura) - 78.387
            return round(valor, 1)
    
    return None
