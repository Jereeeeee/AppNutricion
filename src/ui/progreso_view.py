import customtkinter as ctk
from tkinter import Canvas
from datetime import datetime
from src.database.db_utils import obtener_todos_pacientes, obtener_mediciones_paciente


class ProgresoView(ctk.CTkFrame):
    """Vista de progreso con gráficas simples de evolución"""

    def __init__(self, parent, db_session):
        super().__init__(parent, fg_color="transparent")
        self.db_session = db_session

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_header()
        self._crear_contenido()
        self._cargar_pacientes()
        # Asegurar render inicial cuando el layout ya tiene tamaño
        self.after(200, self._render_graficas)

    def _crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="📈 Progreso del Paciente",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        self.paciente_combo = ctk.CTkComboBox(
            header,
            values=["-- Selecciona un paciente --"],
            state="readonly",
            cursor="arrow",
            width=260,
            command=lambda _val=None: self._render_graficas()
        )
        self.paciente_combo.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.paciente_combo.bind("<Button-1>", self._abrir_combo)
        self.paciente_combo.set("-- Selecciona un paciente --")

    def _crear_contenido(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        container.grid_columnconfigure((0, 1), weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.canvas_peso = Canvas(container, height=320, bg="white", highlightthickness=0)
        self.canvas_peso.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.canvas_imc = Canvas(container, height=320, bg="white", highlightthickness=0)
        self.canvas_imc.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Redibujar cuando cambia el tamaño
        self.canvas_peso.bind("<Configure>", lambda e: self._render_graficas())
        self.canvas_imc.bind("<Configure>", lambda e: self._render_graficas())

        self.label_status = ctk.CTkLabel(self, text="Selecciona un paciente para ver su progreso", text_color="gray")
        self.label_status.grid(row=2, column=0, pady=(0, 10))

    def _cargar_pacientes(self):
        """Recarga opciones del combo sin perder la selección actual."""
        seleccion_actual = self.paciente_combo.get()

        pacientes = obtener_todos_pacientes(self.db_session)
        self.map_pacientes = {}
        opciones = []

        for p in pacientes:
            if p.rut:
                label = f"{p.nombre_completo()} (RUT: {p.rut})"
            else:
                label = f"{p.nombre_completo()} (ID: {p.id})"
            self.map_pacientes[label] = p
            opciones.append(label)

        if opciones:
            self.paciente_combo.configure(values=opciones)
            # Mantener selección si sigue existiendo
            if seleccion_actual in opciones:
                self.paciente_combo.set(seleccion_actual)
            else:
                self.paciente_combo.set(opciones[0])
        else:
            placeholder = "-- No hay pacientes, agrega uno --"
            self.paciente_combo.configure(values=[placeholder])
            self.paciente_combo.set(placeholder)

        self._render_graficas()

    def _abrir_combo(self, _event=None):
        """Recarga pacientes y abre dropdown al hacer click."""
        self._cargar_pacientes()
        # Abrir después de refrescar las opciones
        self.after(10, self.paciente_combo._open_dropdown_menu)

    def _render_graficas(self):
        nombre = self.paciente_combo.get()
        paciente = self.map_pacientes.get(nombre)
        if not paciente:
            mensaje = "Agrega un paciente para ver su progreso" if nombre.startswith("-- No hay pacientes") else "Selecciona un paciente para ver su progreso"
            self._reset_canvases(mensaje)
            return

        mediciones = obtener_mediciones_paciente(self.db_session, paciente.id)
        if not mediciones:
            self._reset_canvases("El paciente no tiene mediciones registradas")
            return

        # Datos para graficar
        fechas = [m.fecha for m in mediciones][::-1]
        pesos = [m.peso for m in mediciones][::-1]
        imcs = [m.imc for m in mediciones][::-1]

        self._draw_chart(self.canvas_peso, "Peso (kg)", fechas, pesos, color="#9C27B0")
        self._draw_chart(self.canvas_imc, "IMC", fechas, imcs, color="#7B1FA2")
        self.label_status.configure(text=f"Mostrando {len(mediciones)} mediciones de {paciente.nombre_completo()}")

    def _reset_canvases(self, mensaje):
        for canvas in [self.canvas_peso, self.canvas_imc]:
            canvas.delete("all")
            canvas.create_text(
                canvas.winfo_reqwidth() // 2,
                canvas.winfo_reqheight() // 2,
                text=mensaje,
                fill="gray",
                font=("Helvetica", 11)
            )
        self.label_status.configure(text=mensaje)

    def _draw_chart(self, canvas: Canvas, titulo: str, fechas, valores, color="#9C27B0"):
        canvas.delete("all")
        w = canvas.winfo_width() or canvas.winfo_reqwidth() or 600
        h = canvas.winfo_height() or canvas.winfo_reqheight() or 320
        padding = 50
        bottom = h - 40
        top = 40
        left = 60
        right = w - 20

        # Título
        canvas.create_text(w / 2, 20, text=titulo, font=("Helvetica", 12, "bold"), fill="#333")

        # Filtrar valores válidos
        puntos = [(f, v) for f, v in zip(fechas, valores) if v is not None]
        if len(puntos) == 0:
            canvas.create_text(w / 2, h / 2, text="Sin datos para graficar", fill="gray", font=("Helvetica", 11))
            return

        xs = list(range(len(puntos)))
        ys = [p[1] for p in puntos]
        min_y, max_y = min(ys), max(ys)
        if min_y == max_y:
            min_y -= 1
            max_y += 1

        def scale_x(i):
            if len(xs) == 1:
                return (left + right) / 2
            return left + (i / (len(xs) - 1)) * (right - left)

        def scale_y(val):
            return bottom - ((val - min_y) / (max_y - min_y)) * (bottom - top)

        # Ejes
        canvas.create_line(left, top, left, bottom, fill="#555", width=1)
        canvas.create_line(left, bottom, right, bottom, fill="#555", width=1)

        # Líneas y puntos
        coords = []
        for idx, (_f, val) in enumerate(puntos):
            x = scale_x(idx)
            y = scale_y(val)
            coords.append((x, y))
        for i in range(len(coords) - 1):
            canvas.create_line(*coords[i], *coords[i + 1], fill=color, width=2)
        for (x, y) in coords:
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline=color)

        # Etiquetas de eje Y (3 marcas)
        for frac in [0, 0.5, 1]:
            val = min_y + frac * (max_y - min_y)
            y = scale_y(val)
            canvas.create_line(left - 5, y, left, y, fill="#555")
            canvas.create_text(left - 10, y, text=f"{val:.1f}", anchor="e", fill="#555", font=("Helvetica", 9))

        # Etiquetas de fechas
        for idx, (fecha, _val) in enumerate(puntos):
            x = scale_x(idx)
            try:
                label = fecha.strftime("%d/%m") if isinstance(fecha, datetime) else str(fecha)
            except Exception:
                label = str(fecha)
            canvas.create_text(x, bottom + 12, text=label, anchor="n", angle=0, fill="#555", font=("Helvetica", 9))

        # Marco
