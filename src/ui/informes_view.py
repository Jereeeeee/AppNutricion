"""
Vista para generar informes
"""
import customtkinter as ctk
from tkinter import messagebox
from src.database.db_utils import obtener_todos_pacientes, obtener_mediciones_paciente
from src.utils.pdf_generator import GeneradorInformes
import os


class InformesView(ctk.CTkScrollableFrame):
    """Vista para generar informes"""
    
    def __init__(self, parent, db_session):
        super().__init__(parent)
        
        self.db_session = db_session
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📄 Generación de Informes",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 30), sticky="w")
        
        # Selector de paciente
        selector_frame = ctk.CTkFrame(self)
        selector_frame.grid(row=1, column=0, sticky="ew", pady=20, padx=20)
        selector_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            selector_frame,
            text="Seleccionar Paciente:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Obtener lista de pacientes
        pacientes = obtener_todos_pacientes(self.db_session)
        self.pacientes_dict = {p.nombre_completo(): p for p in pacientes}
        nombres_pacientes = list(self.pacientes_dict.keys())
        
        if not nombres_pacientes:
            nombres_pacientes = ["No hay pacientes registrados"]
        
        self.paciente_combo = ctk.CTkComboBox(
            selector_frame,
            values=nombres_pacientes,
            width=400,
            height=35,
            state="readonly",
            cursor="arrow"
        )
        self.paciente_combo.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        # Abrir dropdown al click en cualquier parte del campo
        self.paciente_combo.bind("<Button-1>", lambda e: self.paciente_combo._open_dropdown_menu())
        
        if nombres_pacientes and nombres_pacientes[0] != "No hay pacientes registrados":
            self.paciente_combo.set(nombres_pacientes[0])
        
        # Tipos de informes
        informes_frame = ctk.CTkFrame(self)
        informes_frame.grid(row=2, column=0, sticky="ew", pady=20)
        informes_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(
            informes_frame,
            text="Tipos de Informes Disponibles",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 15))
        
        # Informe completo
        card1 = ctk.CTkFrame(informes_frame)
        card1.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            card1,
            text="📋 Informe Completo",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            card1,
            text="Incluye datos personales, mediciones,\nhistorial clínico y pauta nutricional actual",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15))
        
        ctk.CTkButton(
            card1,
            text="Generar Informe Completo",
            command=self.generar_informe_completo,
            height=40
        ).pack(pady=(0, 20), padx=20)
        
        # Informe de evolución
        card2 = ctk.CTkFrame(informes_frame)
        card2.grid(row=1, column=1, padx=15, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            card2,
            text="📊 Informe de Evolución",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            card2,
            text="Muestra la evolución del paciente\na través del tiempo con gráficas",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 15))
        
        ctk.CTkButton(
            card2,
            text="Generar Informe de Evolución",
            command=self.generar_informe_evolucion,
            height=40
        ).pack(pady=(0, 20), padx=20)
        
        # Información adicional
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=3, column=0, sticky="ew", pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Los informes se guardarán en formato PDF en la carpeta 'informes'",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=15)
    
    def generar_informe_completo(self):
        """Genera un informe completo del paciente seleccionado"""
        nombre_seleccionado = self.paciente_combo.get()
        
        if nombre_seleccionado == "No hay pacientes registrados":
            messagebox.showwarning("Advertencia", "No hay pacientes registrados")
            return
        
        paciente = self.pacientes_dict.get(nombre_seleccionado)
        
        if not paciente:
            messagebox.showerror("Error", "Seleccione un paciente válido")
            return
        
        try:
            from src.database.db_utils import (
                obtener_mediciones_paciente,
                obtener_historial_paciente,
                obtener_pautas_paciente
            )
            
            generador = GeneradorInformes()
            mediciones = obtener_mediciones_paciente(self.db_session, paciente.id)
            historial = obtener_historial_paciente(self.db_session, paciente.id)
            pautas = obtener_pautas_paciente(self.db_session, paciente.id)
            
            pauta_activa = pautas[0] if pautas else None
            
            ruta = generador.generar_informe_paciente(
                paciente,
                mediciones,
                historial,
                pauta_activa
            )
            
            messagebox.showinfo(
                "Éxito",
                f"Informe completo generado correctamente:\n{ruta}"
            )
            
            # Abrir el archivo
            os.startfile(ruta)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el informe: {str(e)}")
    
    def generar_informe_evolucion(self):
        """Genera un informe de evolución del paciente seleccionado"""
        nombre_seleccionado = self.paciente_combo.get()
        
        if nombre_seleccionado == "No hay pacientes registrados":
            messagebox.showwarning("Advertencia", "No hay pacientes registrados")
            return
        
        paciente = self.pacientes_dict.get(nombre_seleccionado)
        
        if not paciente:
            messagebox.showerror("Error", "Seleccione un paciente válido")
            return
        
        try:
            generador = GeneradorInformes()
            mediciones = obtener_mediciones_paciente(self.db_session, paciente.id)
            
            if not mediciones:
                messagebox.showwarning(
                    "Advertencia",
                    "El paciente no tiene mediciones registradas"
                )
                return
            
            ruta = generador.generar_informe_evolucion(paciente, mediciones)
            
            messagebox.showinfo(
                "Éxito",
                f"Informe de evolución generado correctamente:\n{ruta}"
            )
            
            # Abrir el archivo
            os.startfile(ruta)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el informe: {str(e)}")
