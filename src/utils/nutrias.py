"""
Nutrias caminando - Decoración para la app chilena
Las nutrias son nativas de Chile y ¡son adorables!
"""

def get_nutrias_animadas():
    """Retorna una animación de nutrias caminando"""
    frames = [
        "🦦 🦦 🦦 🦦 🦦",
        " 🦦 🦦 🦦 🦦 🦦",
        "🦦 🦦 🦦 🦦 🦦 ",
        " 🦦 🦦 🦦 🦦 🦦",
    ]
    return frames


def get_nutria_random():
    """Retorna una nutria aleatoria"""
    return "🦦"


def get_encabezado_nutria():
    """Retorna un encabezado bonito con nutrias"""
    return """
╔═══════════════════════════════════╗
║   🦦 APP NUTRICIÓN CHILE 🦦      ║
║   Para nutricionistas en ascenso  ║
╚═══════════════════════════════════╝
"""


def get_pie_nutrias():
    """Retorna un pie de página con nutrias"""
    return "🦦 🦦 🦦 Hecho con ❤️ para Chile 🦦 🦦 🦦"


# Diferentes posiciones de nutrias caminando
NUTRIAS_CAMINANDO = {
    "inicio": "🦦 ← nutrias chilenas explorando",
    "medio": "← nutrias en acción →",
    "fin": "nutrias alimentándose →",
}
