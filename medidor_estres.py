import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import csv
from datetime import datetime

# ============================================================
# PREGUNTAS DE LA ESCALA ECEA
# ============================================================
PREGUNTAS = [
    "1. Cuando me preguntan en clase",
    "2. Si tengo que hablar en voz alta en clase",
    "3. Al hacer una exposición o hablar en público",
    "4. Al hablar de los exámenes",
    "5. Cuando tengo exámenes",
    "6. Mientras preparo los exámenes",
    "7. Cuando se acercan las fechas de los exámenes",
    "8. Cuando no me queda claro cómo estudiar una materia",
    "9. Cuando no tengo claro qué exigen en las distintas materias",
    "10. Cuando el profesor no plantea de forma clara qué tenemos que hacer",
    "11. Por el excesivo número de asignaturas del plan de estudios",
    "12. Por el escaso tiempo que tengo para estudiar adecuadamente",
    "13. Por el cumplimiento de plazos o fechas de las tareas",
    "14. Por la excesiva carga de trabajo que debo atender",
    "15. Por el excesivo número de horas de clase diarias",
    "16. Por no saber si mi ritmo de aprendizaje es el adecuado",
    "17. Por los conflictos con profesores o compañeros",
    "18. Por la excesiva competitividad en clase",
    "19. Por la falta de apoyo de los compañeros",
    "20. Por la ausencia de un buen ambiente en clase",
]

CAUSAS_ACADEMICAS = [
    "¿Sientes que la carga de tareas es excesiva?",
    "¿Los exámenes te generan mucha presión?",
    "¿Los proyectos académicos te abruman?",
    "¿Las calificaciones te preocupan demasiado?",
    "¿Sientes que el tiempo para estudiar es insuficiente?",
]

CAUSAS_PERSONALES = [
    "¿Tienes problemas familiares que te afectan?",
    "¿La falta de sueño afecta tu rendimiento?",
    "¿Sientes que te falta organización personal?",
]

CAUSAS_SOCIALES = [
    "¿Tienes conflictos con compañeros o profesores?",
    "¿Tus relaciones interpersonales te generan estrés?",
    "¿Sientes presión social en el ambiente escolar?",
    "¿El ambiente escolar te parece negativo?",
]

RECOMENDACIONES = {
    "bajo": [
        "¡Bien! Tu nivel de estrés es bajo. Sigue así.",
        "Mantén hábitos saludables: duerme bien, aliméntate bien y haz ejercicio.",
        "Continúa organizando tu tiempo con listas de tareas.",
        "Practica técnicas de relajación preventivas.",
    ],
    "moderado": {
        "academico": [
            "Usa técnicas de organización y estudio: Pomodoro, mapas conceptuales, resúmenes.",
            "Planifica tus tareas semanalmente con prioridades.",
            "Divide los proyectos grandes en tareas pequeñas.",
            "Pide asesoría académica si no entiendes algún tema.",
        ],
        "personal": [
            "Establece horarios fijos de descanso y sueño.",
            "Haz actividad física al menos 30 minutos al día.",
            "Practica mindfulness o respiración profunda.",
            "Evita la cafeína en exceso y mantén una dieta balanceada.",
        ],
        "social": [
            "Comunícate asertivamente con compañeros y profesores.",
            "Busca apoyo en amigos, familia o grupos de estudio.",
            "Participa en actividades sociales saludables.",
            "Si lo necesitas, acude a orientación psicológica.",
        ],
    },
    "alto": {
        "academico": [
            "URGENTE: Busca apoyo académico inmediato (tutorías, asesorías).",
            "Reduce la carga académica si es posible (habla con coordinación).",
            "Establece un plan de estudio realista y con apoyo de un mentor.",
        ],
        "personal": [
            "URGENTE: Acude a servicios de apoyo psicológico o counseling.",
            "Prioriza tu salud: duerme, aliméntate bien y descansa.",
            "Habla con alguien de confianza sobre cómo te sientes.",
            "Considera técnicas de manejo de ansiedad con un profesional.",
        ],
        "social": [
            "URGENTE: Busca orientación psicológica o tutoría especializada.",
            "Habla con tu familia o personas cercanas sobre tu situación.",
            "Evita el aislamiento; participa en grupos de apoyo.",
            "Contacta a servicios estudiantiles de tu universidad.",
        ],
    },
}

# ============================================================
# UBICACIÓN DEL ARCHIVO DE RESULTADOS
# ============================================================
ARCHIVO_RESULTADOS = os.path.join(
    os.path.expanduser("~"), "Documents", "resultados_estres.json"
)


# ============================================================
# APLICACIÓN
# ============================================================
class MedidorEstres:
    def __init__(self, root):
        self.root = root
        self.root.title("Medidor de Estrés Académico - ECEA")
        self.root.geometry("750x600")
        self.root.configure(bg="#f0f4f8")

        self.respuestas = []
        self.indice = 0
        self.nivel = ""
        self.causas_seleccionadas = {"academico": False, "personal": False, "social": False}
        self.preguntas_causas = []
        self.indice_causa = 0
        self.respuestas_causas = []

        self.crear_pantalla_bienvenida()

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ========================================================
    # PANTALLA DE BIENVENIDA
    # ========================================================
    def crear_pantalla_bienvenida(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True)

        tk.Label(frame, text="MEDIDOR DE ESTRÉS ACADÉMICO",
                 font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#1a365d").pack(pady=20)
        tk.Label(frame, text="Escala de Estresores Académicos (ECEA)",
                 font=("Arial", 13), bg="#f0f4f8", fg="#2c5282").pack(pady=5)
        tk.Label(frame, text="20 ítems | Escala Likert 1-5",
                 font=("Arial", 11), bg="#f0f4f8", fg="#4a5568").pack(pady=5)

        instrucciones = (
            "Instrucciones:\n\n"
            "A continuación encontrarás una serie de enunciados relacionados con\n"
            "situaciones que pueden generarte estrés académico.\n\n"
            "Indica en qué medida te ponen nervioso o te inquietan,\n"
            "usando la siguiente escala:\n\n"
            "1 = Nunca / Muy poco\n"
            "2 = Casi nunca / Poco\n"
            "3 = A veces / Moderado\n"
            "4 = Casi siempre / Bastante\n"
            "5 = Siempre / Mucho"
        )
        tk.Label(frame, text=instrucciones, font=("Arial", 11),
                 bg="#f0f4f8", fg="#2d3748", justify="left").pack(pady=15)

        tk.Button(frame, text="Comenzar", font=("Arial", 14, "bold"),
                  bg="#3182ce", fg="white", padx=30, pady=10,
                  command=self.iniciar_preguntas).pack(pady=5)

        tk.Button(frame, text="Ver historial", font=("Arial", 11),
                  bg="#718096", fg="white", padx=20, pady=6,
                  command=self.ver_historial).pack(pady=5)

    # ========================================================
    # PREGUNTAS PRINCIPALES
    # ========================================================
    def iniciar_preguntas(self):
        self.respuestas = []
        self.indice = 0
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        progreso = tk.Frame(frame, bg="#e2e8f0", height=10)
        progreso.pack(fill="x", pady=(0, 20))
        barra = tk.Frame(progreso, bg="#3182ce", height=10)
        barra.place(x=0, y=0, relwidth=self.indice/len(PREGUNTAS), relheight=1)

        tk.Label(frame, text=f"Pregunta {self.indice + 1} de {len(PREGUNTAS)}",
                 font=("Arial", 12), bg="#f0f4f8", fg="#4a5568").pack(pady=5)

        tk.Label(frame, text=PREGUNTAS[self.indice],
                 font=("Arial", 14, "bold"), bg="#f0f4f8", fg="#1a365d",
                 wraplength=600, justify="center").pack(pady=20)

        self.variable = tk.IntVar(value=0)

        opciones = [
            (1, "1 = Nunca / Muy poco"),
            (2, "2 = Casi nunca / Poco"),
            (3, "3 = A veces / Moderado"),
            (4, "4 = Casi siempre / Bastante"),
            (5, "5 = Siempre / Mucho"),
        ]

        for valor, texto in opciones:
            tk.Radiobutton(frame, text=texto, variable=self.variable,
                           value=valor, font=("Arial", 12),
                           bg="#f0f4f8", fg="#2d3748", selectcolor="#bee3f8",
                           anchor="w").pack(fill="x", padx=100, pady=3)

        tk.Button(frame, text="Siguiente", font=("Arial", 12, "bold"),
                  bg="#3182ce", fg="white", padx=20, pady=8,
                  command=self.siguiente_pregunta).pack(pady=20)

    def siguiente_pregunta(self):
        if self.variable.get() == 0:
            messagebox.showwarning("Atención", "Por favor selecciona una opción.")
            return

        self.respuestas.append(self.variable.get())
        self.indice += 1

        if self.indice < len(PREGUNTAS):
            self.mostrar_pregunta()
        else:
            self.calcular_nivel()

    def calcular_nivel(self):
        total = sum(self.respuestas)
        minimo = len(PREGUNTAS) * 1
        maximo = len(PREGUNTAS) * 5
        porcentaje = (total - minimo) / (maximo - minimo) * 100

        if porcentaje < 33:
            self.nivel = "bajo"
        elif porcentaje < 66:
            self.nivel = "moderado"
        else:
            self.nivel = "alto"

        self.mostrar_resultado(total, porcentaje)

    def mostrar_resultado(self, total, porcentaje):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        colores = {"bajo": "#38a169", "moderado": "#d69e2e", "alto": "#e53e3e"}
        color = colores[self.nivel]

        tk.Label(frame, text="RESULTADO", font=("Arial", 18, "bold"),
                 bg="#f0f4f8", fg="#1a365d").pack(pady=10)

        tk.Label(frame, text=f"Puntuación total: {total} / {len(PREGUNTAS)*5}",
                 font=("Arial", 14), bg="#f0f4f8", fg="#2d3748").pack(pady=5)

        tk.Label(frame, text=f"Porcentaje: {porcentaje:.1f}%",
                 font=("Arial", 14), bg="#f0f4f8", fg="#2d3748").pack(pady=5)

        tk.Label(frame, text=f"Nivel de estrés: {self.nivel.upper()}",
                 font=("Arial", 16, "bold"), bg="#f0f4f8", fg=color).pack(pady=15)

        if self.nivel == "bajo":
            tk.Label(frame, text="Se generarán recomendaciones preventivas.",
                     font=("Arial", 12), bg="#f0f4f8", fg="#2d3748").pack(pady=10)
            tk.Button(frame, text="Ver recomendaciones", font=("Arial", 12, "bold"),
                      bg="#38a169", fg="white", padx=20, pady=8,
                      command=self.mostrar_recomendaciones).pack(pady=20)
        else:
            tk.Label(frame, text="Se aplicarán preguntas sobre posibles causas.",
                     font=("Arial", 12), bg="#f0f4f8", fg="#2d3748").pack(pady=10)
            tk.Button(frame, text="Continuar", font=("Arial", 12, "bold"),
                      bg=color, fg="white", padx=20, pady=8,
                      command=self.iniciar_causas).pack(pady=20)

    # ========================================================
    # CAUSAS
    # ========================================================
    def iniciar_causas(self):
        self.preguntas_causas = []
        for p in CAUSAS_ACADEMICAS:
            self.preguntas_causas.append(("academico", p))
        for p in CAUSAS_PERSONALES:
            self.preguntas_causas.append(("personal", p))
        for p in CAUSAS_SOCIALES:
            self.preguntas_causas.append(("social", p))

        self.indice_causa = 0
        self.respuestas_causas = []
        self.mostrar_causa()

    def mostrar_causa(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        categoria, pregunta = self.preguntas_causas[self.indice_causa]

        tk.Label(frame, text=f"Causa {self.indice_causa + 1} de {len(self.preguntas_causas)}",
                 font=("Arial", 12), bg="#f0f4f8", fg="#4a5568").pack(pady=5)

        tk.Label(frame, text=f"Categoría: {categoria.capitalize()}",
                 font=("Arial", 11, "italic"), bg="#f0f4f8", fg="#718096").pack(pady=5)

        tk.Label(frame, text=pregunta, font=("Arial", 14, "bold"),
                 bg="#f0f4f8", fg="#1a365d", wraplength=600, justify="center").pack(pady=20)

        self.variable_causa = tk.IntVar(value=-1)
        for valor, texto in [(1, "Sí"), (0, "No")]:
            tk.Radiobutton(frame, text=texto, variable=self.variable_causa,
                           value=valor, font=("Arial", 12),
                           bg="#f0f4f8", fg="#2d3748", selectcolor="#bee3f8").pack(pady=5)

        tk.Button(frame, text="Siguiente", font=("Arial", 12, "bold"),
                  bg="#3182ce", fg="white", padx=20, pady=8,
                  command=self.siguiente_causa).pack(pady=20)

    def siguiente_causa(self):
        if self.variable_causa.get() == -1:
            messagebox.showwarning("Atención", "Selecciona Sí o No.")
            return

        categoria, _ = self.preguntas_causas[self.indice_causa]
        if self.variable_causa.get() == 1:
            self.causas_seleccionadas[categoria] = True
            self.respuestas_causas.append(categoria)

        self.indice_causa += 1
        if self.indice_causa < len(self.preguntas_causas):
            self.mostrar_causa()
        else:
            self.mostrar_recomendaciones()

    # ========================================================
    # RECOMENDACIONES
    # ========================================================
    def mostrar_recomendaciones(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(frame, text="RECOMENDACIONES PERSONALIZADAS",
                 font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#1a365d").pack(pady=15)

        texto = tk.Text(frame, wrap="word", font=("Arial", 11),
                        bg="white", fg="#2d3748", padx=15, pady=15, height=20)
        texto.pack(fill="both", expand=True)

        if self.nivel == "bajo":
            texto.insert("end", "Nivel BAJO - Recomendaciones preventivas:\n\n")
            for r in RECOMENDACIONES["bajo"]:
                texto.insert("end", f"• {r}\n\n")
        else:
            texto.insert("end", f"Nivel {self.nivel.upper()} - Recomendaciones:\n\n")
            for cat in ["academico", "personal", "social"]:
                if self.causas_seleccionadas.get(cat, False):
                    texto.insert("end", f"--- Área {cat.upper()} ---\n\n")
                    for r in RECOMENDACIONES[self.nivel][cat]:
                        texto.insert("end", f"• {r}\n\n")

            if not any(self.causas_seleccionadas.values()):
                texto.insert("end", "No se identificaron causas específicas. "
                                    "Se recomienda seguimiento general.\n\n")
                for cat in ["academico", "personal", "social"]:
                    for r in RECOMENDACIONES[self.nivel][cat]:
                        texto.insert("end", f"• {r}\n\n")

        texto.configure(state="disabled")

        tk.Button(frame, text="Registrar y finalizar", font=("Arial", 12, "bold"),
                  bg="#3182ce", fg="white", padx=20, pady=8,
                  command=self.registrar_resultado).pack(pady=15)

    # ========================================================
    # REGISTRAR RESULTADO
    # ========================================================
    def registrar_resultado(self):
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": self.nivel,
            "puntuacion_total": sum(self.respuestas),
            "respuestas": self.respuestas,
            "causas": {k: v for k, v in self.causas_seleccionadas.items() if v},
        }

        historial = self.leer_historial()
        historial.append(registro)

        if self.guardar_historial(historial):
            messagebox.showinfo(
                "Registro",
                f"Resultado registrado correctamente.\n\n"
                f"Guardado en:\n{ARCHIVO_RESULTADOS}"
            )
            self.crear_pantalla_bienvenida()

    # ========================================================
    # HISTORIAL
    # ========================================================
    def leer_historial(self):
        if os.path.exists(ARCHIVO_RESULTADOS):
            try:
                with open(ARCHIVO_RESULTADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_historial(self, historial):
        try:
            carpeta = os.path.dirname(ARCHIVO_RESULTADOS)
            if carpeta and not os.path.exists(carpeta):
                os.makedirs(carpeta, exist_ok=True)

            with open(ARCHIVO_RESULTADOS, "w", encoding="utf-8") as f:
                json.dump(historial, f, ensure_ascii=False, indent=2)
            return True
        except PermissionError:
            messagebox.showerror(
                "Error de permisos",
                f"No se pudo guardar el archivo:\n{ARCHIVO_RESULTADOS}\n\n"
                f"Verifica que el archivo NO esté abierto en otro programa."
            )
            return False
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            return False

    def ver_historial(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(frame, text="HISTORIAL DE RESULTADOS",
                 font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1a365d").pack(pady=10)

        tk.Label(frame, text=f"Ubicación: {ARCHIVO_RESULTADOS}",
                 font=("Arial", 9, "italic"), bg="#f0f4f8", fg="#718096").pack(pady=5)

        historial = self.leer_historial()

        if not historial:
            tk.Label(frame, text="No hay resultados registrados aún.",
                     font=("Arial", 12), bg="#f0f4f8", fg="#718096").pack(pady=30)
            tk.Button(frame, text="Volver al inicio", font=("Arial", 12, "bold"),
                      bg="#3182ce", fg="white", padx=20, pady=8,
                      command=self.crear_pantalla_bienvenida).pack(pady=20)
            return

        contenedor = tk.Frame(frame, bg="#f0f4f8")
        contenedor.pack(fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(contenedor)
        scrollbar.pack(side="right", fill="y")

        columnas = ("#", "Fecha", "Nivel", "Puntuación")
        tree = ttk.Treeview(contenedor, columns=columnas, show="headings",
                            yscrollcommand=scrollbar.set, height=12)
        scrollbar.config(command=tree.yview)

        tree.heading("#", text="#")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Nivel", text="Nivel")
        tree.heading("Puntuación", text="Puntuación")

        tree.column("#", width=40, anchor="center")
        tree.column("Fecha", width=180, anchor="center")
        tree.column("Nivel", width=120, anchor="center")
        tree.column("Puntuación", width=120, anchor="center")

        for i, reg in enumerate(historial, start=1):
            tree.insert("", "end", iid=str(i-1),
                        values=(i, reg.get("fecha", ""),
                                reg.get("nivel", "").upper(),
                                reg.get("puntuacion_total", "")))

        tree.pack(fill="both", expand=True)

        botones = tk.Frame(frame, bg="#f0f4f8")
        botones.pack(pady=10)

        tk.Button(botones, text="Ver detalle", font=("Arial", 11, "bold"),
                  bg="#3182ce", fg="white", padx=15, pady=6,
                  command=lambda: self.ver_detalle(tree, historial)).pack(side="left", padx=5)

        tk.Button(botones, text="Exportar a CSV", font=("Arial", 11, "bold"),
                  bg="#38a169", fg="white", padx=15, pady=6,
                  command=lambda: self.exportar_csv(historial)).pack(side="left", padx=5)

        tk.Button(botones, text="Borrar historial", font=("Arial", 11, "bold"),
                  bg="#e53e3e", fg="white", padx=15, pady=6,
                  command=self.borrar_historial).pack(side="left", padx=5)

        tk.Button(botones, text="Volver al inicio", font=("Arial", 11),
                  bg="#718096", fg="white", padx=15, pady=6,
                  command=self.crear_pantalla_bienvenida).pack(side="left", padx=5)

    def ver_detalle(self, tree, historial):
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para ver el detalle.")
            return

        idx = int(seleccion[0])
        registro = historial[idx]

        ventana = tk.Toplevel(self.root)
        ventana.title(f"Detalle del registro #{idx + 1}")
        ventana.geometry("600x500")
        ventana.configure(bg="#f0f4f8")

        tk.Label(ventana, text=f"REGISTRO #{idx + 1}",
                 font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#1a365d").pack(pady=10)

        info = (
            f"Fecha: {registro.get('fecha', '')}\n"
            f"Nivel: {registro.get('nivel', '').upper()}\n"
            f"Puntuación total: {registro.get('puntuacion_total', '')}\n"
            f"Causas identificadas: "
            f"{', '.join(registro.get('causas', {}).keys()) or 'Ninguna'}"
        )
        tk.Label(ventana, text=info, font=("Arial", 12),
                 bg="#f0f4f8", fg="#2d3748", justify="left").pack(pady=10)

        tk.Label(ventana, text=f"Respuestas a los {len(PREGUNTAS)} ítems:",
                 font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#1a365d").pack(pady=5)

        texto = tk.Text(ventana, wrap="word", font=("Arial", 11),
                        bg="white", fg="#2d3748", padx=10, pady=10)
        texto.pack(fill="both", expand=True, padx=20, pady=10)

        respuestas = registro.get("respuestas", [])
        for i, r in enumerate(respuestas, start=1):
            texto.insert("end", f"{i}. {PREGUNTAS[i-1]} -> {r}\n")

        texto.configure(state="disabled")

        tk.Button(ventana, text="Cerrar", font=("Arial", 11, "bold"),
                  bg="#718096", fg="white", padx=20, pady=6,
                  command=ventana.destroy).pack(pady=10)

    def exportar_csv(self, historial):
        if not historial:
            messagebox.showwarning("Atención", "No hay registros para exportar.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            initialfile="resultados_estres.csv"
        )
        if not archivo:
            return

        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["#", "Fecha", "Nivel", "Puntuación total", "Causas"])
            for i, reg in enumerate(historial, start=1):
                writer.writerow([
                    i,
                    reg.get("fecha", ""),
                    reg.get("nivel", "").upper(),
                    reg.get("puntuacion_total", ""),
                    ", ".join(reg.get("causas", {}).keys()) or "Ninguna"
                ])

        messagebox.showinfo("Exportar", f"Archivo exportado correctamente:\n{archivo}")

    def borrar_historial(self):
        if not os.path.exists(ARCHIVO_RESULTADOS):
            messagebox.showinfo("Historial", "No hay historial para borrar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que quieres borrar TODO el historial?\n"
            "Esta acción no se puede deshacer."
        )
        if confirmar:
            try:
                os.remove(ARCHIVO_RESULTADOS)
                messagebox.showinfo("Historial", "Historial borrado correctamente.")
                self.ver_historial()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo borrar el historial:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedidorEstres(root)
    root.mainloop()
