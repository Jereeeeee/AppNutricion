"""
Vista para listar y gestionar pacientes
"""
import customtkinter as ctk
from tkinter import messagebox
from src.database.db_utils import obtener_todos_pacientes, eliminar_paciente


class PacientesView(ctk.CTkScrollableFrame):
    """Vista para mostrar la lista de pacientes"""
    
    def __init__(self, parent, db_session, callback_ver_paciente=None):
        super().__init__(parent)
        
        self.db_session = db_session
        self.callback_ver_paciente = callback_ver_paciente
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Gestión de Pacientes",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar paciente por nombre o DNI...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.buscar_pacientes)
        
        btn_actualizar = ctk.CTkButton(
            search_frame,
            text="🔄 Actualizar",
            command=self.cargar_pacientes,
            width=120,
            height=40
        )
        btn_actualizar.grid(row=0, column=1)
        
        # Contenedor de pacientes
        self.pacientes_container = ctk.CTkFrame(self)
        self.pacientes_container.grid(row=2, column=0, sticky="nsew")
        self.pacientes_container.grid_columnconfigure(0, weight=1)
        
        # Cargar pacientes
        self.cargar_pacientes()
    
    def cargar_pacientes(self):
        """Carga todos los pacientes de la base de datos"""
        # Limpiar contenedor
        for widget in self.pacientes_container.winfo_children():
            widget.destroy()
        
        # Obtener pacientes
        pacientes = obtener_todos_pacientes(self.db_session)
        
        if not pacientes:
            label_vacio = ctk.CTkLabel(
                self.pacientes_container,
                text="No hay pacientes registrados\n\n➕ Usa el botón 'Nuevo Paciente' para agregar uno",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            label_vacio.pack(pady=40)
            return
        
        # Crear tarjeta para cada paciente
        for i, paciente in enumerate(pacientes):
            self.crear_tarjeta_paciente(paciente, i)
    
    def crear_tarjeta_paciente(self, paciente, index):
        """Crea una tarjeta para mostrar información del paciente"""
        # Frame de la tarjeta
        card = ctk.CTkFrame(self.pacientes_container)
        card.grid(row=index, column=0, sticky="ew", pady=5, padx=5)
        card.grid_columnconfigure(1, weight=1)
        
        # Icono
        icono = ctk.CTkLabel(
            card,
            text="👤",
            font=ctk.CTkFont(size=32)
        )
        icono.grid(row=0, column=0, rowspan=2, padx=20, pady=10)
        
        # Información del paciente
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", pady=10)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Nombre
        nombre = ctk.CTkLabel(
            info_frame,
            text=paciente.nombre_completo(),
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        nombre.grid(row=0, column=0, sticky="w", columnspan=2)
        
        # DNI y otros datos
        datos = f"RUT: {paciente.rut or 'N/A'} | Tel: {paciente.telefono or 'N/A'}"
        if paciente.email:
            datos += f" | {paciente.email}"
        
        info = ctk.CTkLabel(
            info_frame,
            text=datos,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        info.grid(row=1, column=0, sticky="w", columnspan=2, pady=(5, 0))
        
        # Botones de acción
        acciones_frame = ctk.CTkFrame(card, fg_color="transparent")
        acciones_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        btn_ver = ctk.CTkButton(
            acciones_frame,
            text="👁 Ver",
            command=lambda p=paciente: self.ver_paciente(p),
            width=100,
            height=32
        )
        btn_ver.grid(row=0, column=0, padx=5)
        
        btn_editar = ctk.CTkButton(
            acciones_frame,
            text="✏ Editar",
            command=lambda p=paciente: self.editar_paciente(p),
            width=100,
            height=32
        )
        btn_editar.grid(row=0, column=1, padx=5)
        
        btn_eliminar = ctk.CTkButton(
            acciones_frame,
            text="🗑 Eliminar",
            command=lambda p=paciente: self.confirmar_eliminar(p),
            width=100,
            height=32,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        btn_eliminar.grid(row=0, column=2, padx=5)
    
    def buscar_pacientes(self, event=None):
        """Busca pacientes según el texto ingresado"""
        termino = self.search_entry.get().lower()
        
        # Limpiar contenedor
        for widget in self.pacientes_container.winfo_children():
            widget.destroy()
        
        # Obtener todos los pacientes
        pacientes = obtener_todos_pacientes(self.db_session)
        
        # Filtrar pacientes
        pacientes_filtrados = [
            p for p in pacientes
            if termino in p.nombre.lower() or
               termino in p.apellidos.lower() or
               (p.rut and termino in p.rut.lower())
        ]
        
        # Mostrar resultados
        if not pacientes_filtrados:
            label_vacio = ctk.CTkLabel(
                self.pacientes_container,
                text="No se encontraron pacientes con ese criterio",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            label_vacio.pack(pady=40)
            return
        
        for i, paciente in enumerate(pacientes_filtrados):
            self.crear_tarjeta_paciente(paciente, i)
    
    def ver_paciente(self, paciente):
        """Muestra la ficha completa del paciente"""
        if self.callback_ver_paciente:
            self.callback_ver_paciente(paciente)
        else:
            # Fallback: mostrar en la misma vista
            from src.ui.ficha_paciente_view import FichaPacienteView
            
            # Limpiar el contenedor
            for widget in self.winfo_children():
                widget.destroy()
            
            # Crear vista de ficha completa
            vista = FichaPacienteView(self, self.db_session, paciente, callback_volver=self.volver_a_lista)
            vista.pack(fill="both", expand=True, padx=0, pady=0)
    
    def editar_paciente(self, paciente):
        """Edita un paciente existente"""
        messagebox.showinfo("Editar", f"Función de edición para {paciente.nombre_completo()}")
    
    def confirmar_eliminar(self, paciente):
        """Confirma antes de eliminar un paciente"""
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar a {paciente.nombre_completo()}?\n\n"
            "Esta acción eliminará también todas las mediciones, pautas e historial asociados."
        )
        
        if respuesta:
            if eliminar_paciente(self.db_session, paciente.id):
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                self.cargar_pacientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el paciente")
    
    def volver_a_lista(self):
        """Vuelve a mostrar la lista de pacientes"""
        # Limpiar y cargar la lista nuevamente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Recrear la interfaz de lista
        self.__init__(self.master, self.db_session)
