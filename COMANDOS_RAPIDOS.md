# 🥗 App Nutrición - Comandos Rápidos

## 🎯 Instalación y Primer Uso

### Windows (Recomendado)
```bash
# Opción 1: Usar el instalador automático
instalar.bat

# Opción 2: Manual
pip install -r requirements.txt
python insertar_datos_ejemplo.py
```

## ▶️ Ejecutar la Aplicación

### Windows
```bash
# Opción 1: Usar el ejecutor
ejecutar.bat

# Opción 2: Directamente
python main.py
```

## 📦 Gestión de Dependencias

### Instalar todas las dependencias
```bash
pip install -r requirements.txt
```

### Actualizar dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Verificar instalación
```bash
python -c "import customtkinter, sqlalchemy, reportlab; print('✅ OK')"
```

## 🗄️ Base de Datos

### Insertar datos de prueba
```bash
python insertar_datos_ejemplo.py
```

### Resetear base de datos
```bash
# Eliminar archivo de BD
del data\nutricion.db

# Volver a crear con datos de ejemplo
python insertar_datos_ejemplo.py
```

### Ubicación de la base de datos
```
data/nutricion.db
```

## 📄 Informes

### Ubicación de PDFs generados
```
informes/
```

### Abrir carpeta de informes
```bash
explorer informes
```

## 🔧 Solución Rápida de Problemas

### Error: ModuleNotFoundError
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: Base de datos bloqueada
```bash
# Cerrar todas las instancias de la aplicación
# Luego reiniciar
python main.py
```

### La aplicación no se ve correctamente
```bash
# Actualizar CustomTkinter
pip install --upgrade customtkinter
```

## 📋 Atajos de la Aplicación

| Sección | Función Principal |
|---------|-------------------|
| 🏠 Inicio | Vista general y estadísticas |
| 👥 Pacientes | Lista y gestión de pacientes |
| ➕ Nuevo Paciente | Crear paciente nuevo |
| 📋 Pautas | Gestión de planes nutricionales |
| 📄 Informes | Generar PDFs |
| 🔢 Calculadora | Cálculos nutricionales |

## 💾 Backup

### Hacer copia de seguridad
```bash
# Copiar la base de datos
copy data\nutricion.db data\backup_nutricion_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db
```

### Restaurar desde backup
```bash
copy data\backup_nutricion_YYYYMMDD.db data\nutricion.db
```

## 🎨 Personalización

### Cambiar tema a oscuro
Editar `src/ui/ventana_principal.py` línea 18:
```python
ctk.set_appearance_mode("dark")
```

### Cambiar color principal
Editar `src/ui/ventana_principal.py` línea 19:
```python
ctk.set_default_color_theme("blue")  # blue, green, dark-blue
```

## 📊 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Punto de entrada de la aplicación |
| `requirements.txt` | Lista de dependencias |
| `data/nutricion.db` | Base de datos (¡hacer backup!) |
| `src/database/models.py` | Modelos de datos |
| `src/ui/ventana_principal.py` | Ventana principal |
| `src/utils/pdf_generator.py` | Generación de PDFs |

## 🚀 Desarrollo

### Estructura del proyecto
```
AppNutricion/
├── main.py              # Inicio de la app
├── src/
│   ├── database/        # Modelos y BD
│   ├── ui/             # Interfaces
│   └── utils/          # Utilidades
├── data/               # Base de datos
└── informes/           # PDFs generados
```

### Añadir nueva funcionalidad
1. Crear módulo en `src/`
2. Importar en el archivo correspondiente
3. Actualizar la interfaz si es necesario

## 📞 Ayuda

- **Guía completa**: Ver `GUIA_INICIO.md`
- **Documentación**: Ver `README.md`
- **Problemas comunes**: Ver sección de solución de problemas arriba

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos creada
- [ ] Aplicación ejecuta correctamente
- [ ] PDFs se generan correctamente

---
**Última actualización**: Enero 2026
