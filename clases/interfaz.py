import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from clases.arbol_decision import ArbolDecision
from clases.gestor_archivos import GestorArchivos


class InterfazArbol(ctk.CTk):
    """Interfaz grafica principal del juego."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Arbol Adivino")
        self.geometry("820x560")
        self.resizable(False, False)

        self.ruta_base = os.path.dirname(os.path.dirname(__file__))
        self.ruta_datos = os.path.join(self.ruta_base, "datos")
        self.ruta_por_defecto = os.path.join(self.ruta_datos, "comidas.json")

        self.gestor = GestorArchivos(self.ruta_por_defecto)
        self.arbol = self.cargar_arbol_inicial()

        self.frame_actual = None
        self.lbl_archivo = None

        self.mostrar_inicio()

    def cargar_arbol_inicial(self):
        try:
            return self.gestor.cargar_arbol(self.ruta_por_defecto)
        except Exception:
            return ArbolDecision()

    def limpiar_ventana(self):
        if self.frame_actual:
            self.frame_actual.destroy()

        # Se reemplaza el frame para cambiar de pantalla sin abrir otra ventana.
        self.frame_actual = ctk.CTkFrame(self, corner_radius=12)
        self.frame_actual.pack(fill="both", expand=True, padx=24, pady=24)

    def obtener_nombre_archivo_actual(self):
        nombre = os.path.basename(self.gestor.ruta_actual)
        return os.path.splitext(nombre)[0]

    def crear_titulo(self, texto, subtitulo=None):
        ctk.CTkLabel(
            self.frame_actual,
            text=texto,
            font=("Arial", 30, "bold"),
        ).pack(pady=(28, 8))

        if subtitulo:
            ctk.CTkLabel(
                self.frame_actual,
                text=subtitulo,
                font=("Arial", 14),
                text_color="#444444",
                wraplength=640,
            ).pack(pady=(0, 22))

    def mostrar_inicio(self):
        self.limpiar_ventana()
        self.crear_titulo(
            "Arbol Adivino",
            "Piensa en una comida. La aplicacion intentara adivinarla usando preguntas de Si o No."
        )

        self.lbl_archivo = ctk.CTkLabel(
            self.frame_actual,
            text=f"Archivo actual: {self.obtener_nombre_archivo_actual()}",
            font=("Arial", 13),
            text_color="#555555",
        )
        self.lbl_archivo.pack(pady=(0, 18))

        contenedor = ctk.CTkFrame(self.frame_actual, fg_color="transparent")
        contenedor.pack(pady=8)

        self.crear_boton(contenedor, "Iniciar partida", self.iniciar_partida)
        self.crear_boton(contenedor, "Cargar arbol desde archivo", self.cargar_arbol)
        self.crear_boton(contenedor, "Guardar arbol actual", self.guardar_arbol_manual)
        self.crear_boton(contenedor, "Salir", self.destroy, color="#555555")

        ctk.CTkLabel(
            self.frame_actual,
            text="Si el sistema falla, aprendera una nueva respuesta y guardara el arbol automaticamente.",
            font=("Arial", 12),
            text_color="#666666",
        ).pack(side="bottom", pady=18)

    def crear_boton(self, padre, texto, comando, color="#1f6aa5"):
        ctk.CTkButton(
            padre,
            text=texto,
            width=260,
            height=42,
            fg_color=color,
            command=comando,
            font=("Arial", 14, "bold"),
        ).pack(pady=7)

    def cargar_arbol(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar arbol",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if not ruta:
            return

        try:
            self.arbol = self.gestor.cargar_arbol(ruta)
            self.arbol.reiniciar()
            messagebox.showinfo("Arbol cargado", "El arbol se cargo correctamente.")
            self.mostrar_inicio()
        except Exception as error:
            messagebox.showerror(
                "Error al cargar",
                f"No se pudo cargar el archivo.\n\n{error}\n\nSe continuara con un arbol por defecto."
            )
            self.arbol = ArbolDecision()
            self.arbol.reiniciar()

    def guardar_arbol_manual(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar arbol",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")]
        )

        if not ruta:
            return

        try:
            self.gestor.guardar_arbol(self.arbol, ruta)
            messagebox.showinfo("Guardado", "El arbol se guardo correctamente.")
            self.mostrar_inicio()
        except Exception as error:
            messagebox.showerror("Error al guardar", f"No se pudo guardar el arbol.\n\n{error}")

    def iniciar_partida(self):
        self.arbol.reiniciar()
        self.mostrar_nodo_actual()

    def mostrar_nodo_actual(self):
        self.limpiar_ventana()

        if self.arbol.actual_es_pregunta():
            self.crear_titulo("Pregunta actual")
            ctk.CTkLabel(
                self.frame_actual,
                text=self.arbol.obtener_texto_actual(),
                font=("Arial", 22, "bold"),
                wraplength=650,
            ).pack(pady=30)

            fila = ctk.CTkFrame(self.frame_actual, fg_color="transparent")
            fila.pack(pady=10)
            self.crear_boton(fila, "Si", lambda: self.responder_pregunta(True), color="#1c7c54")
            self.crear_boton(fila, "No", lambda: self.responder_pregunta(False), color="#9b2c2c")
        else:
            self.mostrar_adivinanza()

        self.crear_boton(self.frame_actual, "Volver al inicio", self.mostrar_inicio, color="#555555")

    def responder_pregunta(self, respuesta_si):
        self.arbol.responder(respuesta_si)
        self.mostrar_nodo_actual()

    def mostrar_adivinanza(self):
        self.crear_titulo("Creo que ya se la respuesta")
        respuesta = self.arbol.obtener_texto_actual()

        ctk.CTkLabel(
            self.frame_actual,
            text=f"¿Estabas pensando en {respuesta}?",
            font=("Arial", 22, "bold"),
            wraplength=650,
        ).pack(pady=30)

        fila = ctk.CTkFrame(self.frame_actual, fg_color="transparent")
        fila.pack(pady=10)
        self.crear_boton(fila, "Si, correcto", self.mostrar_victoria, color="#1c7c54")
        self.crear_boton(fila, "No, aprende", self.mostrar_formulario_aprendizaje, color="#9b2c2c")

    def mostrar_victoria(self):
        self.limpiar_ventana()
        self.crear_titulo("¡Adivine!", "El arbol encontro la respuesta correcta.")
        self.crear_boton(self.frame_actual, "Nueva partida", self.iniciar_partida)
        self.crear_boton(self.frame_actual, "Volver al inicio", self.mostrar_inicio, color="#555555")

    def mostrar_formulario_aprendizaje(self):
        self.limpiar_ventana()
        respuesta_anterior = self.arbol.obtener_texto_actual()

        self.crear_titulo(
            "Ayudame a aprender",
            f"Yo pense que era: {respuesta_anterior}. Ingresa la informacion correcta."
        )

        self.txt_respuesta = self.crear_entrada("¿En que estabas pensando?")
        self.txt_pregunta = self.crear_entrada("Pregunta para diferenciar ambas respuestas")

        ctk.CTkLabel(
            self.frame_actual,
            text="Para tu respuesta correcta, ¿la respuesta a esa pregunta seria Si o No?",
            font=("Arial", 13),
            text_color="#444444",
        ).pack(pady=(12, 4))

        self.valor_respuesta = ctk.StringVar(value="")
        fila = ctk.CTkFrame(self.frame_actual, fg_color="transparent")
        fila.pack(pady=8)
        ctk.CTkRadioButton(fila, text="Si", variable=self.valor_respuesta, value="si").pack(side="left", padx=20)
        ctk.CTkRadioButton(fila, text="No", variable=self.valor_respuesta, value="no").pack(side="left", padx=20)

        self.crear_boton(self.frame_actual, "Guardar aprendizaje", self.guardar_aprendizaje, color="#1c7c54")
        self.crear_boton(self.frame_actual, "Cancelar", self.mostrar_inicio, color="#555555")

    def crear_entrada(self, etiqueta):
        ctk.CTkLabel(
            self.frame_actual,
            text=etiqueta,
            font=("Arial", 13, "bold"),
        ).pack(pady=(8, 2))

        entrada = ctk.CTkEntry(self.frame_actual, width=520, height=38)
        entrada.pack(pady=(0, 8))
        return entrada

    def guardar_aprendizaje(self):
        respuesta = self.txt_respuesta.get().strip()
        pregunta = self.txt_pregunta.get().strip()
        valor = self.valor_respuesta.get()

        # Validaciones simples para que el arbol no guarde datos vacios.
        if not respuesta:
            messagebox.showwarning("Dato faltante", "Debes escribir la respuesta correcta.")
            return

        if not pregunta:
            messagebox.showwarning("Dato faltante", "Debes escribir una pregunta para diferenciar.")
            return

        if valor not in ("si", "no"):
            messagebox.showwarning("Dato faltante", "Debes indicar si para la nueva respuesta seria Si o No.")
            return

        self.arbol.aprender(respuesta, pregunta, valor == "si")

        try:
            self.gestor.guardar_arbol(self.arbol)
            messagebox.showinfo("Aprendizaje guardado", "El arbol aprendio y se guardo automaticamente.")
        except Exception as error:
            messagebox.showerror("Error al guardar", f"El arbol aprendio, pero no pudo guardarse.\n\n{error}")

        self.mostrar_inicio()
