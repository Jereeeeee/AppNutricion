"""
Vista para crear un nuevo paciente
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from src.database.db_utils import crear_paciente, crear_historial_clinico, buscar_paciente_por_rut
from src.utils.rut import formatear_rut


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

        # Historial Clínico
        seccion3 = ctk.CTkLabel(
            form_frame,
            text="HISTORIAL CLÍNICO (opcional)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        seccion3.grid(row=12, column=0, columnspan=2, sticky="w", pady=(20, 15))

        # Actividad física
        ctk.CTkLabel(form_frame, text="Actividad física", font=ctk.CTkFont(size=12)).grid(
            row=13, column=0, sticky="w", padx=10, pady=(5, 0))
        self.act_fisica_combo = ctk.CTkComboBox(
            form_frame,
            values=["Sedentario", "Ligero", "Moderado", "Intenso"],
            state="readonly",
            cursor="arrow",
            height=35
        )
        self.act_fisica_combo.grid(row=14, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.act_fisica_combo.set("Sedentario")
        self.act_fisica_combo.bind("<Button-1>", lambda e: self.act_fisica_combo._open_dropdown_menu())

        # Hábito tabáquico
        ctk.CTkLabel(form_frame, text="Hábito tabáquico", font=ctk.CTkFont(size=12)).grid(
            row=13, column=1, sticky="w", padx=10, pady=(5, 0))
        self.habito_tabaquico_combo = ctk.CTkComboBox(
            form_frame,
            values=["No", "Sí"],
            state="readonly",
            cursor="arrow",
            height=35
        )
        self.habito_tabaquico_combo.grid(row=14, column=1, sticky="ew", padx=10, pady=(0, 10))
        self.habito_tabaquico_combo.set("No")
        self.habito_tabaquico_combo.bind("<Button-1>", lambda e: self.habito_tabaquico_combo._open_dropdown_menu())

        # Consumo de alcohol
        ctk.CTkLabel(form_frame, text="Consumo de alcohol", font=ctk.CTkFont(size=12)).grid(
            row=15, column=0, sticky="w", padx=10, pady=(5, 0))
        self.consumo_alcohol_combo = ctk.CTkComboBox(
            form_frame,
            values=["Nunca", "Ocasional", "Frecuente"],
            state="readonly",
            cursor="arrow",
            height=35
        )
        self.consumo_alcohol_combo.grid(row=16, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.consumo_alcohol_combo.set("Ocasional")
        self.consumo_alcohol_combo.bind("<Button-1>", lambda e: self.consumo_alcohol_combo._open_dropdown_menu())

        # Objetivo principal
        ctk.CTkLabel(form_frame, text="Objetivo principal", font=ctk.CTkFont(size=12)).grid(
            row=15, column=1, sticky="w", padx=10, pady=(5, 0))
        self.objetivo_text = ctk.CTkTextbox(form_frame, height=70)
        self.objetivo_text.grid(row=16, column=1, sticky="nsew", padx=10, pady=(0, 10))

        # Patologías
        ctk.CTkLabel(form_frame, text="Patologías", font=ctk.CTkFont(size=12)).grid(
            row=17, column=0, sticky="w", padx=10, pady=(5, 0))
        self.patologias_text = ctk.CTkTextbox(form_frame, height=60)
        self.patologias_text.grid(row=18, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Alergias
        ctk.CTkLabel(form_frame, text="Alergias", font=ctk.CTkFont(size=12)).grid(
            row=17, column=1, sticky="w", padx=10, pady=(5, 0))
        self.alergias_text = ctk.CTkTextbox(form_frame, height=60)
        self.alergias_text.grid(row=18, column=1, sticky="nsew", padx=10, pady=(0, 10))

        # Intolerancias
        ctk.CTkLabel(form_frame, text="Intolerancias", font=ctk.CTkFont(size=12)).grid(
            row=19, column=0, sticky="w", padx=10, pady=(5, 0))
        self.intolerancias_text = ctk.CTkTextbox(form_frame, height=60)
        self.intolerancias_text.grid(row=20, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Medicaciones
        ctk.CTkLabel(form_frame, text="Medicaciones", font=ctk.CTkFont(size=12)).grid(
            row=19, column=1, sticky="w", padx=10, pady=(5, 0))
        self.medicamentos_text = ctk.CTkTextbox(form_frame, height=60)
        self.medicamentos_text.grid(row=20, column=1, sticky="nsew", padx=10, pady=(0, 10))

        # Antecedentes familiares
        ctk.CTkLabel(form_frame, text="Antecedentes familiares", font=ctk.CTkFont(size=12)).grid(
            row=21, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
        self.antecedentes_text = ctk.CTkTextbox(form_frame, height=60)
        self.antecedentes_text.grid(row=22, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        
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
        
        # Formatear RUT si viene y validar duplicado
        rut_val = self.rut_entry.get().strip()
        rut_formateado = None
        if rut_val:
            rut_formateado = formatear_rut(rut_val)
            # Validar duplicado
            if buscar_paciente_por_rut(self.db_session, rut_formateado):
                messagebox.showerror("Error", "El RUT ingresado ya está registrado")
                return

        # Crear diccionario con los datos
        datos_paciente = {
            'nombre': self.nombre_entry.get().strip(),
            'apellidos': self.apellidos_entry.get().strip(),
            'rut': rut_formateado,
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

            # Recolectar historial clínico (solo si hay información)
            def _get_text(tb):
                try:
                    return tb.get("1.0", "end").strip()
                except Exception:
                    return ""

            historial_data = {
                'patologias': _get_text(self.patologias_text),
                'alergias': _get_text(self.alergias_text),
                'intolerancias': _get_text(self.intolerancias_text),
                'medicamentos': _get_text(self.medicamentos_text),
                'antecedentes_familiares': _get_text(self.antecedentes_text),
                'actividad_fisica': self.act_fisica_combo.get() if hasattr(self, 'act_fisica_combo') else None,
                'habito_tabaquico': self.habito_tabaquico_combo.get() if hasattr(self, 'habito_tabaquico_combo') else None,
                'consumo_alcohol': self.consumo_alcohol_combo.get() if hasattr(self, 'consumo_alcohol_combo') else None,
                'objetivo_principal': _get_text(self.objetivo_text),
            }

            hay_historial = any(v for v in historial_data.values())
            if hay_historial:
                crear_historial_clinico(self.db_session, paciente.id, **historial_data)

            messagebox.showinfo(
                "Éxito",
                f"Paciente {paciente.nombre_completo()} creado correctamente"
            )

            # Volver a la lista de pacientes
            if self.callback_volver:
                self.callback_volver()

        except Exception as e:
            # Recuperar la sesión ante cualquier fallo
            try:
                self.db_session.rollback()
            except Exception:
                pass
            messagebox.showerror("Error", f"Error al crear el paciente: {str(e)}")
    
    def cancelar(self):
        """Cancela la creación del paciente"""
        if self.callback_volver:
            self.callback_volver()
