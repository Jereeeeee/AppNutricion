"""
Vista para otras mediciones antropométricas
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from src.database.db_utils import obtener_todos_pacientes, obtener_ultima_medicion


class OtrasMedicionesView(ctk.CTkFrame):
    """Vista para registrar mediciones antropométricas adicionales"""
    
    def __init__(self, parent, db_session=None):
        super().__init__(parent, fg_color="transparent")
        
        self.db_session = db_session
        self.pacientes_lista = []
        self.paciente_seleccionado = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Encabezado con título
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        titulo = ctk.CTkLabel(
            header,
            text="📐 Otras Mediciones Antropométricas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(side="left")
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Frame scrollable con formulario
        form_frame = ctk.CTkScrollableFrame(main_container, fg_color=("white", "#1a1a1a"))
        form_frame.grid(row=0, column=0, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Selector de paciente
        ctk.CTkLabel(
            form_frame,
            text="📋 Seleccione un Paciente",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 15), padx=15)
        
        self.paciente_combo = ctk.CTkComboBox(
            form_frame,
            values=["-- Seleccione un paciente --"],
            state="readonly",
            height=35,
            font=ctk.CTkFont(size=12),
            command=self.cargar_medicion_paciente
        )
        self.paciente_combo.pack(pady=(0, 20), fill="x", padx=15)
        self.paciente_combo.set("-- Seleccione un paciente --")
        self.paciente_combo.bind("<Button-1>", lambda e: self.paciente_combo._open_dropdown_menu())
        self.cargar_pacientes()
        
        # Sección: Perímetros
        ctk.CTkLabel(
            form_frame,
            text="📏 Perímetros (cm)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        ).pack(pady=(10, 10), padx=15, anchor="w")
        
        # Perímetro Cintura
        ctk.CTkLabel(form_frame, text="Cintura (cm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.cintura_entry = ctk.CTkEntry(form_frame, placeholder_text="80.0", height=35, font=ctk.CTkFont(size=12))
        self.cintura_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Perímetro Cadera
        ctk.CTkLabel(form_frame, text="Cadera (cm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.cadera_entry = ctk.CTkEntry(form_frame, placeholder_text="95.0", height=35, font=ctk.CTkFont(size=12))
        self.cadera_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Perímetro Brazo
        ctk.CTkLabel(form_frame, text="Brazo (cm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.brazo_entry = ctk.CTkEntry(form_frame, placeholder_text="30.0", height=35, font=ctk.CTkFont(size=12))
        self.brazo_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Sección: Pliegues Cutáneos
        ctk.CTkLabel(
            form_frame,
            text="📊 Pliegues Cutáneos (mm)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        ).pack(pady=(20, 10), padx=15, anchor="w")
        
        # Pliegue Tricipital
        ctk.CTkLabel(form_frame, text="Tricipital (mm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.tricipital_entry = ctk.CTkEntry(form_frame, placeholder_text="15.0", height=35, font=ctk.CTkFont(size=12))
        self.tricipital_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Pliegue Subescapular
        ctk.CTkLabel(form_frame, text="Subescapular (mm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.subescapular_entry = ctk.CTkEntry(form_frame, placeholder_text="12.0", height=35, font=ctk.CTkFont(size=12))
        self.subescapular_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Pliegue Abdominal
        ctk.CTkLabel(form_frame, text="Abdominal (mm)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.abdominal_entry = ctk.CTkEntry(form_frame, placeholder_text="20.0", height=35, font=ctk.CTkFont(size=12))
        self.abdominal_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Sección: Composición Corporal
        ctk.CTkLabel(
            form_frame,
            text="🎯 Composición Corporal",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        ).pack(pady=(20, 10), padx=15, anchor="w")
        
        # Porcentaje de Grasa
        ctk.CTkLabel(form_frame, text="Porcentaje de Grasa (%)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.grasa_entry = ctk.CTkEntry(form_frame, placeholder_text="20.0", height=35, font=ctk.CTkFont(size=12))
        self.grasa_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Masa Muscular
        ctk.CTkLabel(form_frame, text="Masa Muscular (kg)", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)
        self.muscular_entry = ctk.CTkEntry(form_frame, placeholder_text="35.0", height=35, font=ctk.CTkFont(size=12))
        self.muscular_entry.pack(pady=(0, 10), fill="x", padx=15)
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(20, 15))
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Actualizar Mediciones",
            command=self.actualizar_mediciones,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#9C27B0", "#6A1B9A")
        ).grid(row=0, column=0, padx=(0, 7), sticky="ew")
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpiar Formulario",
            command=self.limpiar_formulario,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#7B1FA2", "#4A0E78")
        ).grid(row=0, column=1, padx=(7, 0), sticky="ew")
    
    def cargar_pacientes(self):
        """Carga la lista de pacientes disponibles"""
        if not self.db_session:
            return
        
        try:
            pacientes = obtener_todos_pacientes(self.db_session)
            paciente_names = [f"{p.nombre_completo()} (RUT: {p.rut})" for p in pacientes]
            
            if paciente_names:
                valores = ["-- Seleccione un paciente --"] + paciente_names
                self.paciente_combo.configure(values=valores)
            
            self.pacientes_lista = pacientes
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")
    
    def cargar_medicion_paciente(self, seleccion):
        """Carga la última medición del paciente seleccionado"""
        if seleccion == "-- Seleccione un paciente --":
            self.limpiar_formulario()
            return
        
        try:
            # Encontrar el paciente
            for p in self.pacientes_lista:
                if f"{p.nombre_completo()} (RUT: {p.rut})" == seleccion:
                    self.paciente_seleccionado = p
                    break
            
            if not self.paciente_seleccionado:
                return
            
            # Obtener última medición
            medicion = obtener_ultima_medicion(self.db_session, self.paciente_seleccionado.id)
            
            if medicion:
                # Cargar datos en el formulario
                if medicion.perimetro_cintura:
                    self.cintura_entry.delete(0, "end")
                    self.cintura_entry.insert(0, str(medicion.perimetro_cintura))
                
                if medicion.perimetro_cadera:
                    self.cadera_entry.delete(0, "end")
                    self.cadera_entry.insert(0, str(medicion.perimetro_cadera))
                
                if medicion.perimetro_brazo:
                    self.brazo_entry.delete(0, "end")
                    self.brazo_entry.insert(0, str(medicion.perimetro_brazo))
                
                if medicion.pliegue_tricipital:
                    self.tricipital_entry.delete(0, "end")
                    self.tricipital_entry.insert(0, str(medicion.pliegue_tricipital))
                
                if medicion.pliegue_subescapular:
                    self.subescapular_entry.delete(0, "end")
                    self.subescapular_entry.insert(0, str(medicion.pliegue_subescapular))
                
                if medicion.pliegue_abdominal:
                    self.abdominal_entry.delete(0, "end")
                    self.abdominal_entry.insert(0, str(medicion.pliegue_abdominal))
                
                if medicion.porcentaje_grasa:
                    self.grasa_entry.delete(0, "end")
                    self.grasa_entry.insert(0, str(medicion.porcentaje_grasa))
                
                if medicion.masa_muscular:
                    self.muscular_entry.delete(0, "end")
                    self.muscular_entry.insert(0, str(medicion.masa_muscular))
                
                messagebox.showinfo("Información", f"Se cargaron los datos de la medición del {medicion.fecha}")
            else:
                self.limpiar_formulario()
                messagebox.showinfo("Información", "Este paciente no tiene mediciones previas. Puede ingresar nuevos datos.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar medición: {str(e)}")
    
    def actualizar_mediciones(self):
        """Actualiza las mediciones del paciente seleccionado"""
        if not self.paciente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente")
            return
        
        if not self.db_session:
            messagebox.showerror("Error", "No hay sesión de base de datos")
            return
        
        try:
            # Obtener o crear medición
            medicion = obtener_ultima_medicion(self.db_session, self.paciente_seleccionado.id)
            
            if not medicion:
                messagebox.showwarning("Advertencia", "Este paciente no tiene una medición base. Por favor, use primero la Calculadora Nutricional para crear los datos básicos.")
                return
            
            # Actualizar campos opcionales
            if self.cintura_entry.get().strip():
                medicion.perimetro_cintura = float(self.cintura_entry.get())
            
            if self.cadera_entry.get().strip():
                medicion.perimetro_cadera = float(self.cadera_entry.get())
            
            if self.brazo_entry.get().strip():
                medicion.perimetro_brazo = float(self.brazo_entry.get())
            
            if self.tricipital_entry.get().strip():
                medicion.pliegue_tricipital = float(self.tricipital_entry.get())
            
            if self.subescapular_entry.get().strip():
                medicion.pliegue_subescapular = float(self.subescapular_entry.get())
            
            if self.abdominal_entry.get().strip():
                medicion.pliegue_abdominal = float(self.abdominal_entry.get())
            
            if self.grasa_entry.get().strip():
                medicion.porcentaje_grasa = float(self.grasa_entry.get())
            
            if self.muscular_entry.get().strip():
                medicion.masa_muscular = float(self.muscular_entry.get())
            
            # Guardar cambios
            self.db_session.commit()
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Mediciones actualizadas correctamente para {self.paciente_seleccionado.nombre_completo()}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
        except Exception as e:
            self.db_session.rollback()
            messagebox.showerror("Error", f"Error al actualizar mediciones: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.cintura_entry.delete(0, "end")
        self.cadera_entry.delete(0, "end")
        self.brazo_entry.delete(0, "end")
        self.tricipital_entry.delete(0, "end")
        self.subescapular_entry.delete(0, "end")
        self.abdominal_entry.delete(0, "end")
        self.grasa_entry.delete(0, "end")
        self.muscular_entry.delete(0, "end")
