"""
Ventana principal de la aplicación
"""
import customtkinter as ctk
from datetime import datetime


class VentanaPrincipal(ctk.CTk):
    """Ventana principal de la aplicación de nutrición"""
    
    def __init__(self, db_session):
        super().__init__()
        
        self.db_session = db_session
        
        # Configuración de la ventana en pantalla completa
        self.title("App Nutrición - Gestión Profesional")
        self.state('zoomed')  # Pantalla completa en Windows
        
        # Configurar tema - Morado hermoso para Chile 🦦
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")  # Usaremos azul como base y lo personalizaremos
        
        # Configurar grid para ocupar todo el espacio
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(800, 600)
        
        # Crear componentes
        self.crear_menu_lateral()
        self.crear_contenedor_principal()
        
        # Mostrar pantalla de inicio
        self.mostrar_inicio()
    
    def crear_menu_lateral(self):
        """Crea el menú lateral de navegación"""
        self.menu_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=("#E1BEE7", "#7B1FA2"))
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_rowconfigure(9, weight=1)
        
        # Logo/Título con nutrias chilenas
        self.titulo_label = ctk.CTkLabel(
            self.menu_frame,
            text="🦦 App Nutrición 🦦",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#7B1FA2", "white")
        )
        self.titulo_label.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        # Botones de navegación
        self.btn_inicio = ctk.CTkButton(
            self.menu_frame,
            text="🏠 Inicio",
            command=self.mostrar_inicio,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_pacientes = ctk.CTkButton(
            self.menu_frame,
            text="👥 Pacientes",
            command=self.mostrar_pacientes,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_pacientes.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_nuevo_paciente = ctk.CTkButton(
            self.menu_frame,
            text="➕ Nuevo Paciente",
            command=self.mostrar_nuevo_paciente,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_nuevo_paciente.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_pautas = ctk.CTkButton(
            self.menu_frame,
            text="📋 Pautas",
            command=self.mostrar_pautas,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_pautas.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_informes = ctk.CTkButton(
            self.menu_frame,
            text="📄 Informes",
            command=self.mostrar_informes,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_informes.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_calculadora = ctk.CTkButton(
            self.menu_frame,
            text="🔢 Calculadora",
            command=self.mostrar_calculadora,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_calculadora.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_otras_mediciones = ctk.CTkButton(
            self.menu_frame,
            text="📐 Otras Mediciones",
            command=self.mostrar_otras_mediciones,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_otras_mediciones.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.btn_progreso = ctk.CTkButton(
            self.menu_frame,
            text="📈 Progreso",
            command=self.mostrar_progreso,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        self.btn_progreso.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        
        # Información en la parte inferior
        self.info_label = ctk.CTkLabel(
            self.menu_frame,
            text=f"🦦 App Nutrición\nChile © 2026",
            font=ctk.CTkFont(size=10),
            text_color=("#5E0B8A", "white")
        )
        self.info_label.grid(row=10, column=0, padx=20, pady=20)
    
    def crear_contenedor_principal(self):
        """Crea el contenedor principal donde se mostrarán las diferentes vistas"""
        self.contenedor_principal = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.contenedor_principal.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.contenedor_principal.grid_columnconfigure(0, weight=1)
        self.contenedor_principal.grid_rowconfigure(0, weight=1)
    
    def limpiar_contenedor(self):
        """Limpia el contenedor principal"""
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()
    
    def mostrar_inicio(self):
        """Muestra la pantalla de inicio"""
        self.limpiar_contenedor()
        
        # Frame de bienvenida
        frame_inicio = ctk.CTkFrame(self.contenedor_principal)
        frame_inicio.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame_inicio.grid_columnconfigure(0, weight=1)
        
        # Título de bienvenida
        titulo = ctk.CTkLabel(
            frame_inicio,
            text="Bienvenida Karlita la Mejor Nutricionista 🦦",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(40, 20))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_inicio,
            text="Sistema profesional de gestión nutricional para mi Princesa ❤️",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitulo.grid(row=1, column=0, pady=(0, 40))

        # Texto didáctico
        ctk.CTkLabel(
            frame_inicio,
            text="Explora pacientes, registra mediciones y genera informes. Usa el menú lateral para navegar.",
            font=ctk.CTkFont(size=14),
            text_color="#5E0B8A"
        ).grid(row=2, column=0, pady=(0, 30))
        
        # Estadísticas rápidas
        stats_frame = ctk.CTkFrame(frame_inicio)
        stats_frame.grid(row=3, column=0, pady=20, padx=40, sticky="ew")
        stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Obtener estadísticas de la base de datos
        from src.database.db_utils import obtener_todos_pacientes
        pacientes = obtener_todos_pacientes(self.db_session)
        num_pacientes = len(pacientes)
        
        # Tarjeta de pacientes
        card1 = ctk.CTkFrame(stats_frame, fg_color=("#E1BEE7", "#7B1FA2"))
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card1,
            text=str(num_pacientes),
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card1,
            text="Pacientes Registrados",
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(pady=(0, 20))
        
        # Tarjeta de fecha
        card2 = ctk.CTkFrame(stats_frame, fg_color=("#2196F3", "#1976D2"))
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            card2,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card2,
            text="Fecha Actual",
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(pady=(0, 20))
        
    
    def mostrar_pacientes(self):
        """Muestra la lista de pacientes"""
        self.limpiar_contenedor()
        
        from src.ui.pacientes_view import PacientesView
        vista = PacientesView(
            self.contenedor_principal, 
            self.db_session,
            callback_ver_paciente=self.mostrar_ficha_paciente
        )
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_ficha_paciente(self, paciente):
        """Muestra la ficha completa de un paciente"""
        self.limpiar_contenedor()
        
        from src.ui.ficha_paciente_view import FichaPacienteView
        vista = FichaPacienteView(
            self.contenedor_principal,
            self.db_session,
            paciente,
            callback_volver=self.mostrar_pacientes
        )
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_nuevo_paciente(self):
        """Muestra el formulario para crear un nuevo paciente"""
        self.limpiar_contenedor()
        
        from src.ui.nuevo_paciente_view import NuevoPacienteView
        vista = NuevoPacienteView(self.contenedor_principal, self.db_session, self.mostrar_pacientes)
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_pautas(self):
        """Muestra las pautas nutricionales"""
        self.limpiar_contenedor()
        
        from src.ui.pautas_view import PautasView
        vista = PautasView(self.contenedor_principal, self.db_session)
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_informes(self):
        """Muestra la sección de informes"""
        self.limpiar_contenedor()
        
        from src.ui.informes_view import InformesView
        vista = InformesView(self.contenedor_principal, self.db_session)
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_calculadora(self):
        """Muestra la calculadora nutricional"""
        self.limpiar_contenedor()
        
        from src.ui.calculadora_view import CalculadoraView
        vista = CalculadoraView(self.contenedor_principal, self.db_session)
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_progreso(self):
        """Muestra la vista de progreso con gráficas"""
        self.limpiar_contenedor()
        
        from src.ui.progreso_view import ProgresoView
        vista = ProgresoView(self.contenedor_principal, self.db_session)
        vista.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_otras_mediciones(self):
        """Muestra el formulario de otras mediciones"""
        self.limpiar_contenedor()
        
        from src.ui.otras_mediciones_view import OtrasMedicionesView
        vista = OtrasMedicionesView(self.contenedor_principal, self.db_session)
        vista.grid(row=0, column=0, sticky="nsew")
