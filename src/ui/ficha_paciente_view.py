"""
Vista detallada de un paciente con toda su información
Layout optimizado para ver todo sin mucho scroll
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from src.database.db_utils import (
    obtener_mediciones_paciente, obtener_historial_paciente,
    obtener_pautas_paciente, actualizar_paciente, eliminar_pauta, actualizar_pauta
)
from src.utils.pdf_generator import GeneradorInformes
import os


class FichaPacienteView(ctk.CTkFrame):
    """Vista de ficha completa del paciente con layout optimizado"""
    
    def __init__(self, parent, db_session, paciente, callback_volver=None):
        super().__init__(parent, fg_color="transparent")
        
        self.db_session = db_session
        self.paciente = paciente
        self.callback_volver = callback_volver
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear interfaz
        self.crear_cabecera()
        self.crear_contenido()
    
    def crear_cabecera(self):
        """Crea la cabecera con información básica"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 15))
        header.grid_columnconfigure(1, weight=1)
        
        # Icono nutria
        icono = ctk.CTkLabel(header, text="🦦", font=ctk.CTkFont(size=56))
        icono.grid(row=0, column=0, rowspan=2, padx=(0, 25), pady=10)
        
        # Nombre
        nombre = ctk.CTkLabel(
            header,
            text=self.paciente.nombre_completo(),
            font=ctk.CTkFont(size=32, weight="bold"),
            anchor="w"
        )
        nombre.grid(row=0, column=1, sticky="w", pady=(0, 5))
        
        # Calcular edad y mostrar info
        edad_text = ""
        if self.paciente.fecha_nacimiento:
            hoy = date.today()
            edad = hoy.year - self.paciente.fecha_nacimiento.year
            if (hoy.month, hoy.day) < (self.paciente.fecha_nacimiento.month, self.paciente.fecha_nacimiento.day):
                edad -= 1
            edad_text = f" ({edad} años)"
        
        info = ctk.CTkLabel(
            header,
            text=f"{self.paciente.sexo or 'N/A'}{edad_text} | RUT: {self.paciente.rut or 'N/A'}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        info.grid(row=1, column=1, sticky="w")
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=(20, 0), sticky="e")
        
        btn_informe = ctk.CTkButton(
            btn_frame,
            text="📄 PDF",
            command=self.generar_informe_pdf,
            height=40,
            width=110,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        btn_informe.pack(side="left", padx=5)
        
        btn_editar = ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            command=self.editar_paciente,
            height=40,
            width=110,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#7B1FA2", "#4A0E78"),
            hover_color=("#6A1B9A", "#3D0A5F")
        )
        btn_editar.pack(side="left", padx=5)
        
        btn_volver = ctk.CTkButton(
            btn_frame,
            text="← Volver",
            command=self.volver,
            height=40,
            width=110,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#666666",
            hover_color="#505050"
        )
        btn_volver.pack(side="left", padx=5)
    
    def crear_contenido(self):
        """Crea el contenido principal con layout scrollable"""
        # Frame principal scrollable
        main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 30))
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # SECCIÓN 1: DATOS GENERALES (2 COLUMNAS)
        self.crear_seccion_datos_generales(main_scroll)
        
        # SECCIÓN 2: MEDICIONES
        self.crear_seccion_mediciones(main_scroll)
        
        # SECCIÓN 3: HISTORIAL CLÍNICO
        self.crear_seccion_historial(main_scroll)
        
        # SECCIÓN 4: PAUTAS NUTRICIONALES
        self.crear_seccion_pautas(main_scroll)
    
    def crear_seccion_datos_generales(self, parent):
        """Crea la sección de datos generales en 2 columnas"""
        # Título
        titulo = ctk.CTkLabel(
            parent,
            text="📊 Datos Generales",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(anchor="w", pady=(25, 18), padx=0)
        
        # Frame con 2 columnas
        datos_frame = ctk.CTkFrame(parent, fg_color="transparent")
        datos_frame.pack(fill="x", padx=0, pady=(0, 20))
        datos_frame.grid_columnconfigure(0, weight=1)
        datos_frame.grid_columnconfigure(1, weight=1)
        
        # Datos a mostrar
        datos = [
            ("👤 Nombre", self.paciente.nombre_completo()),
            ("🆔 RUT", self.paciente.rut or "N/A"),
            ("📅 Fecha de Nacimiento", str(self.paciente.fecha_nacimiento) if self.paciente.fecha_nacimiento else "N/A"),
            ("⚥ Sexo", self.paciente.sexo or "N/A"),
            ("📞 Teléfono", self.paciente.telefono or "N/A"),
            ("✉️ Email", self.paciente.email or "N/A"),
            ("🏠 Dirección", self.paciente.direccion or "N/A"),
            ("💼 Ocupación", self.paciente.ocupacion or "N/A"),
        ]
        
        # Distribuir en 2 columnas
        for idx, (label_text, valor) in enumerate(datos):
            col = idx % 2
            row = idx // 2
            self._crear_campo_compacto(datos_frame, label_text, valor, row, col)
    
    def _crear_campo_compacto(self, parent, label, valor, row, col):
        """Crea un campo compacto de información"""
        frame = ctk.CTkFrame(parent, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        frame.grid(row=row, column=col, sticky="ew", padx=15, pady=12)
        frame.grid_columnconfigure(0, weight=1)
        
        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        )
        label_widget.pack(anchor="w", padx=16, pady=(12, 5))
        
        valor_widget = ctk.CTkLabel(
            frame,
            text=str(valor),
            font=ctk.CTkFont(size=12),
            text_color=("gray30", "gray70"),
            justify="left",
            wraplength=280
        )
        valor_widget.pack(anchor="w", padx=16, pady=(5, 12), fill="x")
    
    def crear_seccion_mediciones(self, parent):
        """Crea la sección de mediciones"""
        # Título
        titulo = ctk.CTkLabel(
            parent,
            text="📏 Mediciones",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(anchor="w", pady=(25, 18), padx=0)
        
        mediciones = obtener_mediciones_paciente(self.db_session, self.paciente.id)
        
        if not mediciones:
            label = ctk.CTkLabel(parent, text="📭 Sin mediciones registradas", text_color="gray")
            label.pack(pady=20)
        else:
            # Mostrar las últimas 3 mediciones en una fila
            mediciones_recientes = sorted(mediciones, key=lambda x: x.fecha, reverse=True)[:3]
            
            med_frame = ctk.CTkFrame(parent, fg_color="transparent")
            med_frame.pack(fill="x", padx=0, pady=(0, 20))
            med_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            for idx, medicion in enumerate(mediciones_recientes):
                self.crear_card_medicion_compacta(med_frame, medicion, idx)
    
    def crear_card_medicion_compacta(self, parent, medicion, col):
        """Crea una tarjeta compacta de medición con altura uniforme"""
        card = ctk.CTkFrame(parent, fg_color=("#f5f5f5", "#2b2b2b"), corner_radius=10)
        card.grid(row=0, column=col, sticky="nsew", padx=8)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)  # El contenido se expande
        
        # Fecha
        fecha_label = ctk.CTkLabel(
            card,
            text=f"📅 {medicion.fecha.strftime('%d/%m/%Y')}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        )
        fecha_label.pack(anchor="w", padx=12, pady=(12, 10))
        
        # Frame para los datos (se expande uniformemente)
        datos_frame = ctk.CTkFrame(card, fg_color="transparent")
        datos_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        
        # Datos principales (siempre se muestran)
        datos_med = [
            f"⚖️ {medicion.peso} kg" if medicion.peso else "⚖️ N/A",
            f"📏 {medicion.altura} cm" if medicion.altura else "📏 N/A",
            f"🎯 {medicion.imc:.2f}" if medicion.imc else "🎯 N/A",
            f"🦵 Cintura: {medicion.perimetro_cintura} cm" if medicion.perimetro_cintura else "🦵 Cintura: N/A",
            f"🍖 Grasa: {medicion.porcentaje_grasa}%" if medicion.porcentaje_grasa else "🍖 Grasa: N/A",
        ]
        
        for dato in datos_med:
            label = ctk.CTkLabel(datos_frame, text=dato, font=ctk.CTkFont(size=11))
            label.pack(anchor="w", pady=2)
        
        # Botón para más (siempre en la parte inferior)
        btn_mas = ctk.CTkButton(
            card,
            text="Ver todas →",
            command=lambda: messagebox.showinfo("Mediciones", "Todas las mediciones próximamente"),
            height=30,
            font=ctk.CTkFont(size=9),
            fg_color=("#9C27B0", "#6A1B9A")
        )
        btn_mas.pack(fill="x", padx=12, pady=(0, 10))
    
    def crear_seccion_historial(self, parent):
        """Crea la sección de historial clínico"""
        # Título
        titulo = ctk.CTkLabel(
            parent,
            text="🏥 Historial Clínico",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(anchor="w", pady=(25, 18), padx=0)
        
        historial = obtener_historial_paciente(self.db_session, self.paciente.id)
        
        if not historial:
            label = ctk.CTkLabel(parent, text="📭 Sin historial clínico", text_color="gray")
            label.pack(pady=20)
        else:
            # Mostrar el historial más reciente
            historial_reciente = sorted(historial, key=lambda x: x.fecha, reverse=True)[0]
            
            card = ctk.CTkFrame(parent, fg_color=("#f5f5f5", "#2b2b2b"), corner_radius=10)
            card.pack(fill="x", padx=0, pady=(0, 20))
            card.grid_columnconfigure(1, weight=1)
            
            # Fecha
            fecha_label = ctk.CTkLabel(
                card,
                text=f"📅 {historial_reciente.fecha.strftime('%d/%m/%Y')}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#9C27B0", "#E1BEE7")
            )
            fecha_label.pack(anchor="w", padx=15, pady=(12, 10))
            
            # Datos en grid 2x2
            datos_hist = [
                ("🦠 Patologías", historial_reciente.patologias or "N/A"),
                ("⚠️ Alergias", historial_reciente.alergias or "N/A"),
                ("🎯 Objetivo", historial_reciente.objetivo_principal or "N/A"),
                ("🏃 Actividad Física", historial_reciente.actividad_fisica or "N/A"),
            ]
            
            hist_grid = ctk.CTkFrame(card, fg_color="transparent")
            hist_grid.pack(fill="x", padx=15, pady=(0, 12))
            hist_grid.grid_columnconfigure((0, 1), weight=1)
            
            for idx, (label_text, valor) in enumerate(datos_hist):
                row = idx // 2
                col = idx % 2
                self._crear_campo_historial(hist_grid, label_text, valor, row, col)
    
    def _crear_campo_historial(self, parent, label, valor, row, col):
        """Crea un campo de historial compacto"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        
        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        )
        label_widget.pack(anchor="w", padx=0, pady=(0, 3))
        
        valor_widget = ctk.CTkLabel(
            frame,
            text=str(valor),
            font=ctk.CTkFont(size=9),
            text_color=("gray30", "gray70"),
            justify="left",
            wraplength=220
        )
        valor_widget.pack(anchor="w", padx=0)
    
    def crear_seccion_pautas(self, parent):
        """Crea la sección de pautas nutricionales"""
        # Título con botón de gestión
        titulo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(25, 18), padx=0)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="📋 Pautas Nutricionales",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(side="left", anchor="w")
        
        # Botón gestionar pautas
        btn_gestionar = ctk.CTkButton(
            titulo_frame,
            text="⚙️ Gestionar Pautas",
            command=self.gestionar_pautas,
            width=150,
            height=30,
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        btn_gestionar.pack(side="right", padx=5)
        
        pautas = obtener_pautas_paciente(self.db_session, self.paciente.id)
        
        if not pautas:
            label = ctk.CTkLabel(parent, text="📭 Sin pautas nutricionales", text_color="gray")
            label.pack(pady=20)
        else:
            # Mostrar la pauta más reciente
            pauta_reciente = sorted(pautas, key=lambda x: x.fecha_inicio, reverse=True)[0]
            
            card = ctk.CTkFrame(parent, fg_color=("#f5f5f5", "#2b2b2b"), corner_radius=10)
            card.pack(fill="x", padx=0, pady=(0, 20))
            card.grid_columnconfigure((1, 3), weight=1)
            
            # Fecha
            fecha_label = ctk.CTkLabel(
                card,
                text=f"📅 {pauta_reciente.fecha_inicio.strftime('%d/%m/%Y')}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#9C27B0", "#E1BEE7")
            )
            fecha_label.pack(anchor="w", padx=15, pady=(12, 10))
            
            # Datos de macronutrientes en 2x2
            datos_pauta = [
                ("🔥 Calorías", f"{int(pauta_reciente.calorias_objetivo)} kcal" if pauta_reciente.calorias_objetivo else "N/A"),
                ("🥩 Proteínas", f"{pauta_reciente.proteinas:.1f}g" if pauta_reciente.proteinas else "N/A"),
                ("🍞 Carbohidratos", f"{pauta_reciente.carbohidratos:.1f}g" if pauta_reciente.carbohidratos else "N/A"),
                ("🥑 Grasas", f"{pauta_reciente.grasas:.1f}g" if pauta_reciente.grasas else "N/A"),
            ]
            
            pauta_grid = ctk.CTkFrame(card, fg_color="transparent")
            pauta_grid.pack(fill="x", padx=15, pady=(0, 10))
            pauta_grid.grid_columnconfigure((0, 1), weight=1)
            
            for idx, (label_text, valor) in enumerate(datos_pauta):
                row = idx // 2
                col = idx % 2
                self._crear_campo_pauta(pauta_grid, label_text, valor, row, col)
            
            # Indicaciones y observaciones
            if pauta_reciente.descripcion or pauta_reciente.indicaciones:
                desc_frame = ctk.CTkFrame(card, fg_color="transparent")
                desc_frame.pack(fill="x", padx=15, pady=(0, 12))

                if pauta_reciente.descripcion:
                    desc_label = ctk.CTkLabel(
                        desc_frame,
                        text="📝 Indicaciones",
                        font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=("#9C27B0", "#E1BEE7")
                    )
                    desc_label.pack(anchor="w", pady=(0, 3))

                    desc_value = ctk.CTkLabel(
                        desc_frame,
                        text=pauta_reciente.descripcion,
                        font=ctk.CTkFont(size=9),
                        text_color=("gray30", "gray70"),
                        justify="left",
                        wraplength=500
                    )
                    desc_value.pack(anchor="w", fill="x")

                if pauta_reciente.indicaciones:
                    obs_label = ctk.CTkLabel(
                        desc_frame,
                        text="🗒️ Observaciones",
                        font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=("#9C27B0", "#E1BEE7")
                    )
                    obs_label.pack(anchor="w", pady=(8, 3))

                    obs_value = ctk.CTkLabel(
                        desc_frame,
                        text=pauta_reciente.indicaciones,
                        font=ctk.CTkFont(size=9),
                        text_color=("gray30", "gray70"),
                        justify="left",
                        wraplength=500
                    )
                    obs_value.pack(anchor="w", fill="x")
    
    def _crear_campo_pauta(self, parent, label, valor, row, col):
        """Crea un campo de pauta compacto"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        
        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("#9C27B0", "#E1BEE7")
        )
        label_widget.pack(anchor="w", padx=0, pady=(0, 3))
        
        valor_widget = ctk.CTkLabel(
            frame,
            text=str(valor),
            font=ctk.CTkFont(size=9),
            text_color=("gray30", "gray70")
        )
        valor_widget.pack(anchor="w", padx=0)
    
    def gestionar_pautas(self):
        """Abre ventana para gestionar todas las pautas del paciente"""
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Gestionar Pautas - {self.paciente.nombre_completo()}")
        ventana.geometry("900x600")
        ventana.grab_set()
        
        # Frame principal con scroll
        scroll_frame = ctk.CTkScrollableFrame(ventana)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            scroll_frame,
            text="📋 Todas las Pautas Nutricionales",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Obtener todas las pautas
        pautas = obtener_pautas_paciente(self.db_session, self.paciente.id)
        
        if not pautas:
            label = ctk.CTkLabel(
                scroll_frame,
                text="📭 No hay pautas registradas",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            label.pack(pady=40)
        else:
            # Mostrar cada pauta
            for idx, pauta in enumerate(pautas, 1):
                self._crear_tarjeta_pauta(scroll_frame, pauta, idx, ventana)
    
    def _crear_tarjeta_pauta(self, parent, pauta, numero, ventana_padre):
        """Crea una tarjeta con información de pauta y botones editar/eliminar"""
        card = ctk.CTkFrame(parent, fg_color=("#f5f5f5", "#2b2b2b"), corner_radius=10)
        card.pack(fill="x", pady=(0, 15))
        
        # Encabezado con número y fecha
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))
        
        titulo_pauta = ctk.CTkLabel(
            header,
            text=f"Pauta #{numero} - {pauta.titulo if hasattr(pauta, 'titulo') and pauta.titulo else 'Sin título'}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_pauta.pack(side="left", anchor="w")
        
        fecha = ctk.CTkLabel(
            header,
            text=f"📅 {pauta.fecha_inicio.strftime('%d/%m/%Y')} - {pauta.fecha_fin.strftime('%d/%m/%Y') if pauta.fecha_fin else 'Sin fin'}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        fecha.pack(side="right")
        
        # Macros en una fila
        macros_frame = ctk.CTkFrame(card, fg_color="transparent")
        macros_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        datos = [
            f"🔥 {int(pauta.calorias_objetivo) if pauta.calorias_objetivo else 0} kcal",
            f"🥩 {pauta.proteinas if pauta.proteinas else 0}g",
            f"🍞 {pauta.carbohidratos if pauta.carbohidratos else 0}g",
            f"🥑 {pauta.grasas if pauta.grasas else 0}g"
        ]
        
        for dato in datos:
            label = ctk.CTkLabel(
                macros_frame,
                text=dato,
                font=ctk.CTkFont(size=11),
                text_color=("#9C27B0", "#E1BEE7")
            )
            label.pack(side="left", padx=(0, 20))
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        btn_editar = ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            command=lambda p=pauta: self._editar_pauta(p, ventana_padre),
            width=120,
            height=32,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1976D2", "#1565C0")
        )
        btn_editar.pack(side="left", padx=(0, 10))
        
        btn_eliminar = ctk.CTkButton(
            btn_frame,
            text="🗑️ Eliminar",
            command=lambda p=pauta: self._eliminar_pauta(p, ventana_padre),
            width=120,
            height=32,
            fg_color=("#f44336", "#d32f2f"),
            hover_color=("#d32f2f", "#c62828")
        )
        btn_eliminar.pack(side="left")
    
    def _editar_pauta(self, pauta, ventana_padre):
        """Abre diálogo para editar una pauta"""
        ventana = ctk.CTkToplevel(ventana_padre)
        ventana.title(f"Editar Pauta")
        ventana.geometry("500x600")
        ventana.grab_set()
        
        scroll = ctk.CTkScrollableFrame(ventana)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            scroll,
            text="Editar Pauta Nutricional",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 20))
        
        # Campos de edición
        campos = {}
        
        # Título de la pauta
        ctk.CTkLabel(scroll, text="Título:").pack(anchor="w", pady=(5, 0))
        campos['titulo'] = ctk.CTkEntry(scroll, width=400)
        campos['titulo'].insert(0, pauta.titulo if hasattr(pauta, 'titulo') and pauta.titulo else "")
        campos['titulo'].pack(pady=(0, 10))
        
        # Calorías
        ctk.CTkLabel(scroll, text="Calorías objetivo:").pack(anchor="w", pady=(5, 0))
        campos['calorias_objetivo'] = ctk.CTkEntry(scroll, width=400)
        campos['calorias_objetivo'].insert(0, str(pauta.calorias_objetivo) if pauta.calorias_objetivo else "")
        campos['calorias_objetivo'].pack(pady=(0, 10))
        
        # Proteínas
        ctk.CTkLabel(scroll, text="Proteínas (g):").pack(anchor="w", pady=(5, 0))
        campos['proteinas'] = ctk.CTkEntry(scroll, width=400)
        campos['proteinas'].insert(0, str(pauta.proteinas) if pauta.proteinas else "")
        campos['proteinas'].pack(pady=(0, 10))
        
        # Carbohidratos
        ctk.CTkLabel(scroll, text="Carbohidratos (g):").pack(anchor="w", pady=(5, 0))
        campos['carbohidratos'] = ctk.CTkEntry(scroll, width=400)
        campos['carbohidratos'].insert(0, str(pauta.carbohidratos) if pauta.carbohidratos else "")
        campos['carbohidratos'].pack(pady=(0, 10))
        
        # Grasas
        ctk.CTkLabel(scroll, text="Grasas (g):").pack(anchor="w", pady=(5, 0))
        campos['grasas'] = ctk.CTkEntry(scroll, width=400)
        campos['grasas'].insert(0, str(pauta.grasas) if pauta.grasas else "")
        campos['grasas'].pack(pady=(0, 10))
        
        # Descripción
        ctk.CTkLabel(scroll, text="Descripción:").pack(anchor="w", pady=(5, 0))
        campos['descripcion'] = ctk.CTkTextbox(scroll, width=400, height=80)
        if pauta.descripcion:
            campos['descripcion'].insert("1.0", pauta.descripcion)
        campos['descripcion'].pack(pady=(0, 10))
        
        # Indicaciones
        ctk.CTkLabel(scroll, text="Indicaciones:").pack(anchor="w", pady=(5, 0))
        campos['indicaciones'] = ctk.CTkTextbox(scroll, width=400, height=80)
        if pauta.indicaciones:
            campos['indicaciones'].insert("1.0", pauta.indicaciones)
        campos['indicaciones'].pack(pady=(0, 20))
        
        # Botones
        def guardar():
            try:
                datos_actualizados = {
                    'titulo': campos['titulo'].get(),
                    'calorias_objetivo': float(campos['calorias_objetivo'].get()) if campos['calorias_objetivo'].get() else None,
                    'proteinas': float(campos['proteinas'].get()) if campos['proteinas'].get() else None,
                    'carbohidratos': float(campos['carbohidratos'].get()) if campos['carbohidratos'].get() else None,
                    'grasas': float(campos['grasas'].get()) if campos['grasas'].get() else None,
                    'descripcion': campos['descripcion'].get("1.0", "end-1c"),
                    'indicaciones': campos['indicaciones'].get("1.0", "end-1c")
                }
                
                actualizar_pauta(self.db_session, pauta.id, **datos_actualizados)
                messagebox.showinfo("Éxito", "Pauta actualizada correctamente")
                ventana.destroy()
                ventana_padre.destroy()
                self.actualizar_vista()
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            command=guardar,
            width=150,
            fg_color=("#4CAF50", "#45a049"),
            hover_color=("#45a049", "#3d8b40")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=ventana.destroy,
            width=150,
            fg_color="#666666",
            hover_color="#505050"
        ).pack(side="left", padx=5)
    
    def _eliminar_pauta(self, pauta, ventana_padre):
        """Elimina una pauta tras confirmación"""
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar esta pauta?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                eliminar_pauta(self.db_session, pauta.id)
                messagebox.showinfo("Éxito", "Pauta eliminada correctamente")
                ventana_padre.destroy()
                self.actualizar_vista()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def actualizar_vista(self):
        """Recarga la vista del paciente"""
        # Destruir el contenido actual y recrearlo
        for widget in self.winfo_children():
            widget.destroy()
        self.__init__(self.master, self.db_session, self.paciente, self.callback_volver)
    
    def editar_paciente(self):
        """Abre el diálogo para editar el paciente"""
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self)
        edit_window.title(f"Editar - {self.paciente.nombre_completo()}")
        edit_window.geometry("600x700")
        edit_window.grab_set()
        
        # Frame scrollable
        frame_scroll = ctk.CTkScrollableFrame(edit_window)
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        frame_scroll.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_scroll,
            text="✏️ Editar Información del Paciente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Campos
        campos = {}
        
        # Nombre
        ctk.CTkLabel(frame_scroll, text="Nombre", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        nombre_entry = ctk.CTkEntry(frame_scroll, placeholder_text=self.paciente.nombre)
        nombre_entry.insert(0, self.paciente.nombre)
        nombre_entry.pack(fill="x", pady=(5, 15))
        campos['nombre'] = nombre_entry
        
        # Apellidos
        ctk.CTkLabel(frame_scroll, text="Apellidos", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        apellidos_entry = ctk.CTkEntry(frame_scroll, placeholder_text=self.paciente.apellidos)
        apellidos_entry.insert(0, self.paciente.apellidos)
        apellidos_entry.pack(fill="x", pady=(5, 15))
        campos['apellidos'] = apellidos_entry
        
        # RUT
        ctk.CTkLabel(frame_scroll, text="RUT", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        rut_entry = ctk.CTkEntry(frame_scroll, placeholder_text="RUT Chileno")
        if self.paciente.rut:
            rut_entry.insert(0, self.paciente.rut)
        rut_entry.pack(fill="x", pady=(5, 15))
        campos['rut'] = rut_entry
        
        # Teléfono
        ctk.CTkLabel(frame_scroll, text="Teléfono", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        telefono_entry = ctk.CTkEntry(frame_scroll, placeholder_text="+56 9 ...")
        if self.paciente.telefono:
            telefono_entry.insert(0, self.paciente.telefono)
        telefono_entry.pack(fill="x", pady=(5, 15))
        campos['telefono'] = telefono_entry
        
        # Email
        ctk.CTkLabel(frame_scroll, text="Email", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        email_entry = ctk.CTkEntry(frame_scroll, placeholder_text="email@example.com")
        if self.paciente.email:
            email_entry.insert(0, self.paciente.email)
        email_entry.pack(fill="x", pady=(5, 15))
        campos['email'] = email_entry
        
        # Dirección
        ctk.CTkLabel(frame_scroll, text="Dirección", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        direccion_entry = ctk.CTkEntry(frame_scroll, placeholder_text="Dirección completa")
        if self.paciente.direccion:
            direccion_entry.insert(0, self.paciente.direccion)
        direccion_entry.pack(fill="x", pady=(5, 15))
        campos['direccion'] = direccion_entry
        
        # Ocupación
        ctk.CTkLabel(frame_scroll, text="Ocupación", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 0))
        ocupacion_entry = ctk.CTkEntry(frame_scroll, placeholder_text="Ocupación")
        if self.paciente.ocupacion:
            ocupacion_entry.insert(0, self.paciente.ocupacion)
        ocupacion_entry.pack(fill="x", pady=(5, 15))
        campos['ocupacion'] = ocupacion_entry
        
        # Botones
        btn_frame = ctk.CTkFrame(frame_scroll, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        def guardar_cambios():
            datos_update = {
                'nombre': campos['nombre'].get(),
                'apellidos': campos['apellidos'].get(),
                'rut': campos['rut'].get() or None,
                'telefono': campos['telefono'].get() or None,
                'email': campos['email'].get() or None,
                'direccion': campos['direccion'].get() or None,
                'ocupacion': campos['ocupacion'].get() or None,
            }
            
            try:
                actualizar_paciente(self.db_session, self.paciente.id, **datos_update)
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        
        btn_guardar = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Cambios",
            command=guardar_cambios,
            height=40,
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        btn_guardar.pack(side="left", padx=5, fill="x", expand=True)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=edit_window.destroy,
            height=40,
            fg_color="#666666",
            hover_color="#505050"
        )
        btn_cancelar.pack(side="left", padx=5, fill="x", expand=True)
    
    def generar_informe_pdf(self):
        """Genera un informe PDF del paciente"""
        try:
            # Obtener datos del paciente
            mediciones = obtener_mediciones_paciente(self.db_session, self.paciente.id)
            historial = obtener_historial_paciente(self.db_session, self.paciente.id)
            pautas = obtener_pautas_paciente(self.db_session, self.paciente.id)
            
            # Ordenar y obtener la más reciente
            pauta = sorted(pautas, key=lambda x: x.fecha_inicio, reverse=True)[0] if pautas else None
            
            # Generar PDF
            generador = GeneradorInformes()
            ruta_pdf = generador.generar_informe_paciente(
                self.paciente, 
                mediciones, 
                historial, 
                pauta
            )
            
            if os.path.exists(ruta_pdf):
                os.startfile(ruta_pdf)
                messagebox.showinfo("Éxito", f"PDF generado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo generar el PDF")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
    
    def volver(self):
        """Vuelve a la vista anterior"""
        if self.callback_volver:
            self.callback_volver()
        else:
            self.destroy()
