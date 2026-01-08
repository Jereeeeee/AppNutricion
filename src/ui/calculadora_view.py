"""
Vista de calculadora nutricional
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from src.utils.calculadora import (
    calcular_imc, clasificar_imc, calcular_tmb_harris_benedict,
    calcular_calorias_objetivo, calcular_macronutrientes, calcular_agua_recomendada
)
from src.database.db_utils import (
    obtener_todos_pacientes, crear_medicion, crear_pauta
)


class CalculadoraView(ctk.CTkFrame):
    """Vista de calculadora nutricional con opción de guardar datos"""
    
    def __init__(self, parent, db_session=None):
        super().__init__(parent, fg_color="transparent")
        
        self.db_session = db_session
        self.datos_calculados = None
        self.pacientes_lista = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Encabezado con título
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            header,
            text="🔢 Calculadora Nutricional",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(side="left")
        
        # Contenedor principal con dos columnas
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_container.grid_columnconfigure((0, 1), weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Columna izquierda: Datos de entrada
        input_frame = ctk.CTkScrollableFrame(main_container, fg_color=("white", "#1a1a1a"))
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        input_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            input_frame,
            text="📋 Datos del Paciente",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 15), padx=15)
        
        # Peso
        ctk.CTkLabel(input_frame, text="Peso (kg)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.peso_entry = ctk.CTkEntry(input_frame, placeholder_text="70", height=35, font=ctk.CTkFont(size=12))
        self.peso_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Altura
        ctk.CTkLabel(input_frame, text="Altura (cm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.altura_entry = ctk.CTkEntry(input_frame, placeholder_text="170", height=35, font=ctk.CTkFont(size=12))
        self.altura_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Edad
        ctk.CTkLabel(input_frame, text="Edad (años)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.edad_entry = ctk.CTkEntry(input_frame, placeholder_text="30", height=35, font=ctk.CTkFont(size=12))
        self.edad_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Helper para abrir dropdown al hacer click en cualquier lado
        def _click_open(cb):
            cb.bind("<Button-1>", lambda e: cb._open_dropdown_menu())

        # Sexo
        ctk.CTkLabel(input_frame, text="Sexo", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.sexo_combo = ctk.CTkComboBox(
            input_frame,
            values=["Masculino", "Femenino"],
            state="readonly",
            cursor="arrow",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.sexo_combo.pack(pady=(0, 10), fill="x", padx=15)
        self.sexo_combo.set("Masculino")
        _click_open(self.sexo_combo)
        
        # Nivel de actividad
        ctk.CTkLabel(input_frame, text="Nivel de Actividad", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.actividad_combo = ctk.CTkComboBox(
            input_frame,
            values=["Sedentario", "Ligero", "Moderado", "Activo", "Muy Activo"],
            state="readonly",
            cursor="arrow",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.actividad_combo.pack(pady=(0, 10), fill="x", padx=15)
        self.actividad_combo.set("Moderado")
        _click_open(self.actividad_combo)
        
        # Objetivo
        ctk.CTkLabel(input_frame, text="Objetivo", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.objetivo_combo = ctk.CTkComboBox(
            input_frame,
            values=["Pérdida de peso", "Mantenimiento", "Ganancia de peso"],
            state="readonly",
            cursor="arrow",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.objetivo_combo.pack(pady=(0, 10), fill="x", padx=15)
        self.objetivo_combo.set("Mantenimiento")
        _click_open(self.objetivo_combo)
        
        # Distribución de macros
        ctk.CTkLabel(input_frame, text="Distribución de Macros", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.macros_combo = ctk.CTkComboBox(
            input_frame,
            values=["Balanceada", "Alta Proteína", "Baja en Carbohidratos"],
            state="readonly",
            cursor="arrow",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.macros_combo.pack(pady=(0, 10), fill="x", padx=15)
        self.macros_combo.set("Balanceada")
        _click_open(self.macros_combo)
        
        # Selector de paciente
        ctk.CTkLabel(input_frame, text="Asociar a Paciente", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.paciente_combo = ctk.CTkComboBox(
            input_frame,
            values=["-- Sin paciente --"],
            state="readonly",
            cursor="arrow",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.paciente_combo.pack(pady=(0, 15), fill="x", padx=15)
        self.paciente_combo.set("-- Sin paciente --")
        _click_open(self.paciente_combo)
        self.cargar_pacientes()
        
        # Botones
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            btn_frame,
            text="🔍 Calcular",
            command=self.calcular,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#9C27B0", "#6A1B9A")
        ).grid(row=0, column=0, padx=(0, 7), sticky="ew")
        
        self.btn_guardar = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Datos",
            command=self.guardar_datos,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#7B1FA2", "#4A0E78"),
            state="disabled"
        )
        self.btn_guardar.grid(row=0, column=1, padx=(7, 0), sticky="ew")
        
        # Columna derecha: Resultados
        self.resultados_frame = ctk.CTkFrame(main_container, fg_color=("white", "#1a1a1a"), corner_radius=8)
        self.resultados_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        self.resultados_frame.grid_columnconfigure(0, weight=1)
        self.resultados_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            self.resultados_frame,
            text="📊 Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=15, sticky="ew")
        
        self.resultado_text = ctk.CTkTextbox(
            self.resultados_frame,
            font=ctk.CTkFont(size=12),
            text_color=("black", "white"),
            corner_radius=4
        )
        self.resultado_text.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="nsew")
        self.resultado_text.configure(state="disabled")
        
        self.mostrar_mensaje_inicial()
    
    def mostrar_mensaje_inicial(self):
        """Muestra un mensaje inicial en el área de resultados"""
        mensaje = """Bienvenido a la Calculadora Nutricional

Complete los datos del paciente en el formulario
de la izquierda y presione el botón "Calcular"
para obtener:

• Índice de Masa Corporal (IMC)
• Tasa Metabólica Basal (TMB)
• Calorías objetivo diarias
• Distribución de macronutrientes
• Recomendación de ingesta de agua

Los cálculos se basan en fórmulas científicas
reconocidas internacionalmente."""
        
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", "end")
        self.resultado_text.insert("1.0", mensaje)
        self.resultado_text.configure(state="disabled")
    
    def calcular(self):
        """Realiza todos los cálculos nutricionales"""
        try:
            # Validar y obtener datos
            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())
            edad = int(self.edad_entry.get())
            sexo = self.sexo_combo.get()
            
            # Mapear nivel de actividad a formato esperado
            actividad_map = {
                "Sedentario": "sedentario",
                "Ligero": "ligero",
                "Moderado": "moderado",
                "Activo": "activo",
                "Muy Activo": "muy_activo"
            }
            nivel_act = actividad_map.get(self.actividad_combo.get(), "moderado")
            
            objetivo = self.objetivo_combo.get()
            
            # Mapear distribución de macros a formato esperado
            macros_map = {
                "Balanceada": "balanceada",
                "Alta Proteína": "alta_proteina",
                "Baja en Carbohidratos": "baja_carbohidratos"
            }
            dist_macros = macros_map.get(self.macros_combo.get(), "balanceada")
            
            # Calcular IMC
            imc = calcular_imc(peso, altura)
            clasificacion_imc = clasificar_imc(imc)
            
            # Calcular TMB
            tmb = calcular_tmb_harris_benedict(peso, altura, edad, sexo)
            
            # Mapear objetivo
            objetivo_map = {
                "Pérdida de peso": "perdida",
                "Mantenimiento": "mantenimiento",
                "Ganancia de peso": "ganancia"
            }
            objetivo_calc = objetivo_map.get(objetivo, "mantenimiento")
            
            # Calcular calorías objetivo
            calorias = calcular_calorias_objetivo(tmb, nivel_act, objetivo_calc)
            
            # Calcular macronutrientes
            macros = calcular_macronutrientes(calorias, dist_macros)
            
            # Calcular agua
            agua = calcular_agua_recomendada(peso)
            
            # Mostrar resultados
            resultado = f"""═══════════════════════════════════════
        RESULTADOS DEL CÁLCULO
═══════════════════════════════════════

📊 COMPOSICIÓN CORPORAL
────────────────────────────────────
• Peso: {peso} kg
• Altura: {altura} cm
• IMC: {imc:.2f}
• Clasificación: {clasificacion_imc}

⚡ METABOLISMO
────────────────────────────────────
• TMB (Metabolismo Basal): {int(tmb)} kcal/día
• Nivel de actividad: {self.actividad_combo.get()}
• Objetivo: {objetivo}

🎯 CALORÍAS DIARIAS
────────────────────────────────────
• Calorías objetivo: {int(calorias)} kcal/día

🥗 MACRONUTRIENTES
────────────────────────────────────
Distribución: {self.macros_combo.get()}

• Proteínas: {macros['proteinas']:.1f} g/día
  ({int(macros['proteinas'] * 4)} kcal - {int((macros['proteinas'] * 4 / calorias) * 100)}%)

• Carbohidratos: {macros['carbohidratos']:.1f} g/día
  ({int(macros['carbohidratos'] * 4)} kcal - {int((macros['carbohidratos'] * 4 / calorias) * 100)}%)

• Grasas: {macros['grasas']:.1f} g/día
  ({int(macros['grasas'] * 9)} kcal - {int((macros['grasas'] * 9 / calorias) * 100)}%)

💧 HIDRATACIÓN
────────────────────────────────────
• Agua recomendada: {agua:.1f} litros/día

═══════════════════════════════════════
Estos valores son orientativos y deben
ser ajustados según necesidades individuales.
═══════════════════════════════════════"""
            
            # Limpiar y escribir resultados
            self.resultado_text.configure(state="normal")
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", resultado)
            self.resultado_text.configure(state="disabled")
            
            # Guardar datos calculados para usarlos después
            self.datos_calculados = {
                'peso': peso,
                'altura': altura,
                'edad': edad,
                'sexo': sexo,
                'imc': imc,
                'tmb': tmb,
                'calorias': calorias,
                'proteinas': macros['proteinas'],
                'carbohidratos': macros['carbohidratos'],
                'grasas': macros['grasas'],
                'agua': agua,
                'objetivo': objetivo
            }
            
            # Habilitar botón de guardar si hay paciente seleccionado
            if self.paciente_combo.get() != "-- Sin paciente --":
                self.btn_guardar.configure(state="normal")
            
        except ValueError as e:
            messagebox.showerror(
                "Error de validación",
                "Por favor, ingrese valores numéricos válidos en todos los campos.\nVerifique: Peso, Altura y Edad."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def cargar_pacientes(self):
        """Carga la lista de pacientes disponibles"""
        if not self.db_session:
            return
        
        try:
            pacientes = obtener_todos_pacientes(self.db_session)
            paciente_names = [f"{p.nombre_completo()} (RUT: {p.rut})" for p in pacientes]
            
            if paciente_names:
                valores = ["-- Sin paciente --"] + paciente_names
                self.paciente_combo.configure(values=valores)
            
            # Guardar referencia de pacientes para luego usarla
            self.pacientes_lista = pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
    
    def guardar_datos(self):
        """Guarda los datos calculados en el paciente seleccionado"""
        if not self.datos_calculados:
            messagebox.showwarning("Advertencia", "Primero debe calcular los datos")
            return
        
        if self.paciente_combo.get() == "-- Sin paciente --":
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente")
            return
        
        if not self.db_session:
            messagebox.showerror("Error", "No hay sesión de base de datos")
            return
        
        try:
            # Obtener el paciente seleccionado
            nombre_seleccionado = self.paciente_combo.get()
            paciente = None
            
            for p in self.pacientes_lista:
                if f"{p.nombre_completo()} (RUT: {p.rut})" == nombre_seleccionado:
                    paciente = p
                    break
            
            if not paciente:
                messagebox.showerror("Error", "No se encontró el paciente")
                return
            
            # Actualizar datos del paciente
            try:
                paciente.sexo = self.datos_calculados['sexo']
                self.db_session.commit()
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar paciente: {str(e)}")
                return
            
            # Crear medición
            try:
                crear_medicion(
                    self.db_session,
                    paciente_id=paciente.id,
                    fecha=date.today(),
                    peso=float(self.datos_calculados['peso']),
                    altura=float(self.datos_calculados['altura']),
                    imc=float(self.datos_calculados['imc'])
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear medición: {str(e)}")
                return
            
            # Crear pauta nutricional
            try:
                crear_pauta(
                    self.db_session,
                    paciente_id=paciente.id,
                    fecha_inicio=date.today(),
                    calorias_objetivo=int(round(self.datos_calculados['calorias'])),
                    proteinas=float(self.datos_calculados['proteinas']),
                    carbohidratos=float(self.datos_calculados['carbohidratos']),
                    grasas=float(self.datos_calculados['grasas'])
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear pauta: {str(e)}")
                return
            
            messagebox.showinfo(
                "Éxito",
                f"Datos guardados correctamente para {paciente.nombre_completo()}\n\n" +
                "✅ Paciente actualizado\n" +
                "✅ Nueva medición registrada\n" +
                "✅ Nueva pauta nutricional asignada"
            )
            
            # Desactivar botón después de guardar
            self.btn_guardar.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {str(e)}\n\nDetalles: {type(e).__name__}")

