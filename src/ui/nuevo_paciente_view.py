"""
Vista para crear un nuevo paciente
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from src.database.db_utils import crear_paciente


class NuevoPacienteView(ctk.CTkScrollableFrame):
    """Vista para crear un nuevo paciente"""
    
    def __init__(self, parent, db_session, callback_volver=None):
        super().__init__(parent)
        
        self.db_session = db_session
        self.callback_volver = callback_volver
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo_frame = ctk.CTkFrame(self, fg_color="transparent")
        titulo_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="➕ Nuevo Paciente",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Formulario
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        form_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Datos personales
        seccion1 = ctk.CTkLabel(
            form_frame,
            text="DATOS PERSONALES",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        seccion1.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 15))
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre *", font=ctk.CTkFont(size=12)).grid(
            row=1, column=0, sticky="w", padx=10, pady=(5, 0))
        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Juan", height=35)
        self.nombre_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Apellidos
        ctk.CTkLabel(form_frame, text="Apellidos *", font=ctk.CTkFont(size=12)).grid(
            row=1, column=1, sticky="w", padx=10, pady=(5, 0))
        self.apellidos_entry = ctk.CTkEntry(form_frame, placeholder_text="Pérez García", height=35)
        self.apellidos_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=(0, 10))
        
        # DNI
        ctk.CTkLabel(form_frame, text="RUT Chileno", font=ctk.CTkFont(size=12)).grid(
            row=3, column=0, sticky="w", padx=10, pady=(5, 0))
        self.rut_entry = ctk.CTkEntry(form_frame, placeholder_text="12.345.678-9", height=35)
        self.rut_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Fecha de nacimiento
        ctk.CTkLabel(form_frame, text="Fecha de Nacimiento (DD/MM/AAAA)", 
                    font=ctk.CTkFont(size=12)).grid(
            row=3, column=1, sticky="w", padx=10, pady=(5, 0))
        self.fecha_nac_entry = ctk.CTkEntry(form_frame, placeholder_text="15/03/1990", height=35)
        self.fecha_nac_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=(0, 10))
        
        # Sexo
        ctk.CTkLabel(form_frame, text="Sexo", font=ctk.CTkFont(size=12)).grid(
            row=5, column=0, sticky="w", padx=10, pady=(5, 0))
        self.sexo_combo = ctk.CTkComboBox(
            form_frame,
            values=["Masculino", "Femenino"],
            state="readonly",
            cursor="arrow",
            height=35
        )
        self.sexo_combo.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.sexo_combo.set("Masculino")
        self.sexo_combo.bind("<Button-1>", lambda e: self.sexo_combo._open_dropdown_menu())
        
        # Ocupación
        ctk.CTkLabel(form_frame, text="Ocupación", font=ctk.CTkFont(size=12)).grid(
            row=5, column=1, sticky="w", padx=10, pady=(5, 0))
        self.ocupacion_entry = ctk.CTkEntry(form_frame, placeholder_text="Profesión", height=35)
        self.ocupacion_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=(0, 10))
        
        # Datos de contacto
        seccion2 = ctk.CTkLabel(
            form_frame,
            text="DATOS DE CONTACTO",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        seccion2.grid(row=7, column=0, columnspan=2, sticky="w", pady=(20, 15))
        
        # Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono", font=ctk.CTkFont(size=12)).grid(
            row=8, column=0, sticky="w", padx=10, pady=(5, 0))
        self.telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="+34 600 123 456", height=35)
        self.telefono_entry.grid(row=9, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Email
        ctk.CTkLabel(form_frame, text="Email", font=ctk.CTkFont(size=12)).grid(
            row=8, column=1, sticky="w", padx=10, pady=(5, 0))
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="ejemplo@email.com", height=35)
        self.email_entry.grid(row=9, column=1, sticky="ew", padx=10, pady=(0, 10))
        
        # Dirección
        ctk.CTkLabel(form_frame, text="Dirección", font=ctk.CTkFont(size=12)).grid(
            row=10, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
        self.direccion_entry = ctk.CTkEntry(form_frame, placeholder_text="Calle, Número, Ciudad", height=35)
        self.direccion_entry.grid(row=11, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        # Botones
        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.grid(row=2, column=0, pady=30)
        
        btn_guardar = ctk.CTkButton(
            botones_frame,
            text="💾 Guardar Paciente",
            command=self.guardar_paciente,
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        btn_guardar.grid(row=0, column=0, padx=10)
        
        btn_cancelar = ctk.CTkButton(
            botones_frame,
            text="❌ Cancelar",
            command=self.cancelar,
            width=150,
            height=45,
            font=ctk.CTkFont(size=16),
            fg_color="gray",
            hover_color="#505050"
        )
        btn_cancelar.grid(row=0, column=1, padx=10)
    
    def guardar_paciente(self):
        """Guarda el nuevo paciente en la base de datos"""
        # Validar campos obligatorios
        if not self.nombre_entry.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if not self.apellidos_entry.get().strip():
            messagebox.showerror("Error", "Los apellidos son obligatorios")
            return
        
        # Procesar fecha de nacimiento
        fecha_nacimiento = None
        if self.fecha_nac_entry.get().strip():
            try:
                fecha_nacimiento = datetime.strptime(
                    self.fecha_nac_entry.get().strip(),
                    "%d/%m/%Y"
                ).date()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Use DD/MM/AAAA")
                return
        
        # Crear diccionario con los datos
        datos_paciente = {
            'nombre': self.nombre_entry.get().strip(),
            'apellidos': self.apellidos_entry.get().strip(),
            'rut': self.rut_entry.get().strip() or None,
            'fecha_nacimiento': fecha_nacimiento,
            'sexo': self.sexo_combo.get(),
            'telefono': self.telefono_entry.get().strip() or None,
            'email': self.email_entry.get().strip() or None,
            'direccion': self.direccion_entry.get().strip() or None,
            'ocupacion': self.ocupacion_entry.get().strip() or None,
        }
        
        try:
            # Crear paciente
            paciente = crear_paciente(self.db_session, **datos_paciente)
            messagebox.showinfo(
                "Éxito",
                f"Paciente {paciente.nombre_completo()} creado correctamente"
            )
            
            # Volver a la lista de pacientes
            if self.callback_volver:
                self.callback_volver()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el paciente: {str(e)}")
    
    def cancelar(self):
        """Cancela la creación del paciente"""
        if self.callback_volver:
            self.callback_volver()
