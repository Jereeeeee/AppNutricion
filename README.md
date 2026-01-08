# App Nutrición Chile 🦦

Aplicación de escritorio para la gestión profesional de pacientes y generación de pautas nutricionales e informes.

**Diseñada especialmente para nutricionistas en ascenso en Chile** 🇨🇱

## Características

- 📋 **Gestión de Pacientes**: Registro completo de datos personales, mediciones antropométricas e historial clínico
- 📝 **Pautas Nutricionales**: Generación de planes alimenticios personalizados
- 📄 **Informes PDF**: Creación de informes profesionales en PDF
- 💾 **Base de Datos Local**: Almacenamiento seguro de toda la información
- 🎨 **Interfaz Moderna**: Diseño intuitivo y profesional

## Instalación

1. Asegúrate de tener Python 3.8 o superior instalado
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación con:
```bash
python main.py
```

## Estructura del Proyecto

```
AppNutricion/
├── src/
│   ├── database/       # Modelos y gestión de base de datos
│   ├── ui/            # Interfaces gráficas
│   └── utils/         # Utilidades y generadores
├── assets/            # Recursos gráficos
├── data/             # Base de datos local
├── requirements.txt  # Dependencias
└── main.py          # Punto de entrada
```

## Desarrollado con

- Python 3.x
- CustomTkinter (Interfaz moderna)
- SQLAlchemy (Base de datos)
- ReportLab (Generación de PDF)
