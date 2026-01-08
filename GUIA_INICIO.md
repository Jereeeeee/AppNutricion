# 🥗 App Nutrición - Guía de Inicio Rápido

## 📋 Requisitos Previos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

## 🚀 Instalación y Configuración

### 1. Instalar las dependencias

Abre una terminal (PowerShell o CMD) en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará todas las bibliotecas necesarias:
- CustomTkinter (interfaz gráfica moderna)
- SQLAlchemy (base de datos)
- ReportLab (generación de PDFs)
- Pandas (manejo de datos)

### 2. Verificar la instalación

Asegúrate de que todas las dependencias se instalaron correctamente:

```bash
python -c "import customtkinter; import sqlalchemy; import reportlab; print('✅ Todas las dependencias instaladas')"
```

## 🎯 Primera Ejecución

### Opción A: Iniciar con datos de ejemplo (Recomendado para prueba)

1. Ejecuta el script de datos de ejemplo:
```bash
python insertar_datos_ejemplo.py
```

2. Inicia la aplicación:
```bash
python main.py
```

### Opción B: Iniciar con base de datos vacía

Simplemente ejecuta:
```bash
python main.py
```

## 📱 Uso de la Aplicación

### Pantalla Principal

Al iniciar la aplicación verás:
- **Panel lateral izquierdo**: Menú de navegación con todas las secciones
- **Panel central**: Contenido de la sección seleccionada
- **Estadísticas**: Número de pacientes registrados y accesos rápidos

### Funcionalidades Principales

#### 1. 👥 Gestión de Pacientes

**Crear nuevo paciente:**
1. Click en "➕ Nuevo Paciente" en el menú lateral
2. Rellena el formulario con los datos del paciente
3. Click en "💾 Guardar Paciente"

**Ver pacientes:**
1. Click en "👥 Pacientes"
2. Usa la barra de búsqueda para filtrar
3. Click en "👁 Ver" para ver la ficha completa

**Eliminar paciente:**
1. En la lista de pacientes, click en "🗑 Eliminar"
2. Confirma la eliminación (esto eliminará también mediciones, historial y pautas)

#### 2. 📏 Mediciones Antropométricas

Desde la ficha de un paciente:
1. Ve a la pestaña "📏 Mediciones"
2. Click en "➕ Nueva Medición"
3. Ingresa peso, altura, perímetros, etc.
4. El IMC se calcula automáticamente

#### 3. 📋 Pautas Nutricionales

**Crear pauta:**
1. Desde la ficha del paciente, pestaña "📋 Pautas"
2. Click en "➕ Nueva Pauta"
3. Completa la información nutricional
4. Detalla las comidas del día
5. Agrega indicaciones especiales

#### 4. 📄 Generación de Informes PDF

**Informe completo:**
1. Ve a "📄 Informes"
2. Selecciona un paciente
3. Click en "Generar Informe Completo"
4. El PDF se abrirá automáticamente

**Informe de evolución:**
1. Mismo proceso pero con "Generar Informe de Evolución"
2. Requiere que el paciente tenga mediciones registradas

Los informes se guardan en la carpeta `informes/`

#### 5. 🔢 Calculadora Nutricional

Una herramienta útil para cálculos rápidos:
1. Click en "🔢 Calculadora"
2. Ingresa datos: peso, altura, edad, sexo
3. Selecciona nivel de actividad y objetivo
4. Click en "🔍 Calcular"

Obtendrás:
- IMC y clasificación
- TMB (Tasa Metabólica Basal)
- Calorías objetivo diarias
- Distribución de macronutrientes (proteínas, carbohidratos, grasas)
- Recomendación de agua

## 📁 Estructura de Archivos

```
AppNutricion/
├── data/                    # Base de datos SQLite
│   └── nutricion.db
├── informes/                # PDFs generados
├── src/
│   ├── database/           # Modelos y utilidades de BD
│   ├── ui/                 # Interfaces gráficas
│   └── utils/              # Utilidades y generadores
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── insertar_datos_ejemplo.py
```

## 🔧 Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### La aplicación no inicia
1. Verifica la versión de Python:
   ```bash
   python --version
   ```
   Debe ser 3.8 o superior

2. Reinstala las dependencias:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

### Los informes PDF no se generan
- Asegúrate de que la carpeta `informes/` existe
- Verifica que ReportLab está instalado correctamente
- Comprueba los permisos de escritura en el directorio

## 💡 Consejos de Uso

1. **Backup regular**: Haz copias de seguridad de `data/nutricion.db`
2. **Datos completos**: Cuanto más completa sea la información, mejores serán los informes
3. **Seguimiento**: Registra mediciones periódicamente para ver la evolución
4. **Personalización**: Adapta las pautas a cada paciente según sus necesidades
5. **Impresión**: Los PDFs están optimizados para impresión en tamaño A4

## 🎨 Personalización

### Cambiar el tema de color
En `src/ui/ventana_principal.py`, línea 19:
```python
ctk.set_default_color_theme("green")  # Opciones: blue, green, dark-blue
```

### Cambiar el modo (claro/oscuro)
En `src/ui/ventana_principal.py`, línea 18:
```python
ctk.set_appearance_mode("light")  # Opciones: light, dark, system
```

## 📞 Soporte

Para cualquier duda o problema:
- Revisa esta guía
- Consulta el archivo README.md
- Verifica que todas las dependencias están instaladas

## 🚀 Próximas Funcionalidades

Ideas para expandir la aplicación:
- Gráficas de evolución integradas
- Exportación a Excel
- Base de datos de alimentos
- Cálculo automático de recetas
- Recordatorios y citas
- Multi-usuario con login

¡Disfruta usando App Nutrición! 🥗✨
