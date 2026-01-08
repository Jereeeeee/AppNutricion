import re


def limpiar_rut(rut: str) -> str:
    """Devuelve el RUT en formato limpio (solo dígitos y DV en mayúscula)."""
    if not rut:
        return ""
    s = re.sub(r"[^0-9kK]", "", str(rut))
    return s[:-1] + s[-1:].upper() if len(s) >= 2 else s.upper()


def formatear_rut(rut: str) -> str:
    """Formatea un RUT a '12.345.678-9' sin validar DV."""
    limpio = limpiar_rut(rut)
    if len(limpio) < 2:
        return limpio
    cuerpo, dv = limpio[:-1], limpio[-1]
    # Insertar puntos cada 3 dígitos desde el final
    partes = []
    while cuerpo:
        partes.insert(0, cuerpo[-3:])
        cuerpo = cuerpo[:-3]
    return f"{'.'.join(partes)}-{dv}"


def rut_equivalentes(rut_a: str, rut_b: str) -> bool:
    """Compara RUTs ignorando puntos/guiones y normalizando DV."""
    return limpiar_rut(rut_a) == limpiar_rut(rut_b)
