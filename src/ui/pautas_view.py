"""Vista para generar pautas nutricionales desde datos ya registrados"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from src.database.db_utils import (
    obtener_todos_pacientes,
    obtener_ultima_medicion,
    crear_pauta
)
from src.utils.calculadora import (
    calcular_tmb_harris_benedict,
    calcular_calorias_objetivo,
    calcular_macronutrientes
)


class PautasView(ctk.CTkScrollableFrame):
    """Vista para gestionar y generar pautas nutricionales"""

    def __init__(self, parent, db_session):
        super().__init__(parent)

        self.db_session = db_session
        self.grid_columnconfigure(0, weight=1)

        # Cargar pacientes
        self.pacientes = obtener_todos_pacientes(self.db_session)
        self.map_nombre_paciente = {
            f"{p.apellidos}, {p.nombre}": p for p in self.pacientes
        }

        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📋 Generar Pauta Nutricional",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 20), sticky="w")

        desc = ctk.CTkLabel(
            self,
            text="Genera una pauta automática usando los datos ya registrados del paciente (última medición, sexo, fecha de nacimiento)",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        desc.grid(row=1, column=0, pady=(0, 15), sticky="w")

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=2, column=0, sticky="ew", pady=10)
        form.grid_columnconfigure((0, 1), weight=1)

        # Helper para abrir dropdown al click en cualquier parte
        def _click_open(cb):
            cb.bind("<Button-1>", lambda e: cb._open_dropdown_menu())

        # Paciente
        ctk.CTkLabel(form, text="Paciente", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=(5, 2))
        opciones_pacientes = list(self.map_nombre_paciente.keys()) or ["Sin pacientes"]
        self.cmb_paciente = ctk.CTkComboBox(form, values=opciones_pacientes, state="readonly")
        if opciones_pacientes:
            self.cmb_paciente.set(opciones_pacientes[0])
        self.cmb_paciente.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 10))
        self.cmb_paciente.configure(cursor="arrow")
        _click_open(self.cmb_paciente)

        # Parámetros de cálculo
        ctk.CTkLabel(form, text="Nivel de actividad", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, sticky="w", padx=5, pady=(5, 2))
        self.cmb_actividad = ctk.CTkComboBox(form, state="readonly", values=["sedentario", "ligero", "moderado", "activo", "muy_activo"])
        self.cmb_actividad.set("moderado")
        self.cmb_actividad.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 10))
        self.cmb_actividad.configure(cursor="arrow")
        _click_open(self.cmb_actividad)

        ctk.CTkLabel(form, text="Objetivo", font=ctk.CTkFont(weight="bold")).grid(row=2, column=1, sticky="w", padx=5, pady=(5, 2))
        self.cmb_objetivo = ctk.CTkComboBox(form, state="readonly", values=["mantenimiento", "perdida", "ganancia"])
        self.cmb_objetivo.set("mantenimiento")
        self.cmb_objetivo.grid(row=3, column=1, sticky="ew", padx=5, pady=(0, 10))
        self.cmb_objetivo.configure(cursor="arrow")
        _click_open(self.cmb_objetivo)

        ctk.CTkLabel(form, text="Distribución de macros", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, sticky="w", padx=5, pady=(5, 2))
        self.cmb_macros = ctk.CTkComboBox(form, state="readonly", values=["balanceada", "alta_proteina", "baja_carbohidratos"])
        self.cmb_macros.set("balanceada")
        self.cmb_macros.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 12))
        self.cmb_macros.configure(cursor="arrow")
        _click_open(self.cmb_macros)

        # Botón generar
        btn_generar = ctk.CTkButton(
            form,
            text="➕ Generar Pauta Automática",
            command=self.generar_pauta,
            height=46,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        )
        btn_generar.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 5))

        # Nota
        nota = ctk.CTkLabel(
            self,
            text="La pauta usa: última medición (peso/altura), sexo y edad (fecha de nacimiento) del paciente. Si falta algún dato se pedirá completarlo antes.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        nota.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def generar_pauta(self):
        """Genera y guarda una pauta usando datos ya registrados"""
        try:
            nombre_sel = self.cmb_paciente.get()
            paciente = self.map_nombre_paciente.get(nombre_sel)
            if not paciente:
                messagebox.showerror("Error", "Selecciona un paciente válido")
                return

            # Validaciones mínimas
            if not paciente.sexo:
                messagebox.showerror("Falta dato", "El paciente no tiene sexo registrado. Edítalo antes de generar la pauta.")
                return
            if not paciente.fecha_nacimiento:
                messagebox.showerror("Falta dato", "El paciente no tiene fecha de nacimiento. Edítalo antes de generar la pauta.")
                return

            ultima_med = obtener_ultima_medicion(self.db_session, paciente.id)
            if not ultima_med:
                messagebox.showerror("Sin mediciones", "Este paciente no tiene mediciones. Registra una con la calculadora primero.")
                return
            if not ultima_med.peso or not ultima_med.altura:
                messagebox.showerror("Falta dato", "La última medición no tiene peso o altura. Registra nuevamente la medición.")
                return

            # Calcular edad
            hoy = date.today()
            edad = hoy.year - paciente.fecha_nacimiento.year - ((hoy.month, hoy.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))
            if edad <= 0:
                messagebox.showerror("Dato inválido", "La fecha de nacimiento no es válida para calcular la edad.")
                return

            # Calcular calorías y macros
            tmb = calcular_tmb_harris_benedict(ultima_med.peso, ultima_med.altura, edad, paciente.sexo)
            calorias = calcular_calorias_objetivo(tmb, self.cmb_actividad.get(), self.cmb_objetivo.get())
            macros = calcular_macronutrientes(calorias, self.cmb_macros.get())

            self._mostrar_previsualizacion(paciente, calorias, macros)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la pauta: {str(e)}")

    def _mostrar_previsualizacion(self, paciente, calorias, macros):
        """Muestra diálogo para revisar y editar la pauta antes de guardarla"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Previsualizar Pauta")
        dialog.geometry("720x780")
        dialog.minsize(700, 720)
        dialog.grab_set()

        dialog.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            dialog,
            text=f"Pauta para {paciente.nombre_completo()}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")

        form = ctk.CTkFrame(dialog, fg_color="transparent")
        form.grid(row=1, column=0, sticky="nsew", padx=20)
        form.grid_columnconfigure(0, weight=1)

        def add_field(row, label_text, value):
            ctk.CTkLabel(form, text=label_text, font=ctk.CTkFont(weight="bold"))\
                .grid(row=row, column=0, sticky="w", pady=(6, 0))
            entry = ctk.CTkEntry(form)
            entry.insert(0, value)
            entry.grid(row=row+1, column=0, sticky="ew", pady=(0, 8))
            return entry

        # Campos editables
        entry_titulo = add_field(0, "Título", f"Pauta automática {date.today().strftime('%d/%m/%Y')}")
        entry_calorias = add_field(2, "Calorías objetivo (kcal)", str(int(calorias)))
        entry_prot = add_field(4, "Proteínas (g)", f"{macros['proteinas']}")
        entry_carb = add_field(6, "Carbohidratos (g)", f"{macros['carbohidratos']}")
        entry_grasas = add_field(8, "Grasas (g)", f"{macros['grasas']}")
        entry_desc = add_field(10, "Indicaciones (plan)", f"Actividad: {self.cmb_actividad.get()} | Objetivo: {self.cmb_objetivo.get()} | Distribución: {self.cmb_macros.get()}")

        # Observaciones en textarea
        ctk.CTkLabel(form, text="Observaciones", font=ctk.CTkFont(weight="bold"))\
            .grid(row=12, column=0, sticky="w", pady=(6, 0))
        txt_obs = ctk.CTkTextbox(form, height=80)
        txt_obs.grid(row=13, column=0, sticky="ew", pady=(0, 8))

        # Botones
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        def guardar():
            try:
                crear_pauta(
                    self.db_session,
                    paciente.id,
                    calorias_objetivo=int(float(entry_calorias.get() or 0)),
                    proteinas=float(entry_prot.get() or 0),
                    carbohidratos=float(entry_carb.get() or 0),
                    grasas=float(entry_grasas.get() or 0),
                    fecha_inicio=date.today(),
                    titulo=entry_titulo.get().strip() or "Pauta automática",
                    descripcion=entry_desc.get().strip(),  # indicaciones o plan
                    indicaciones=txt_obs.get("1.0", "end").strip()  # observaciones
                )
                messagebox.showinfo("Éxito", "Pauta generada y guardada correctamente. Revisa la ficha del paciente.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la pauta: {str(e)}")

        ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Pauta",
            command=guardar,
            height=40,
            fg_color=("#9C27B0", "#6A1B9A"),
            hover_color=("#7B1FA2", "#5E0B8A")
        ).grid(row=0, column=0, padx=5, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=dialog.destroy,
            height=40,
            fg_color="#666666",
            hover_color="#505050"
        ).grid(row=0, column=1, padx=5, sticky="ew")
