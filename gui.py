import os
import re
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox

CARPETA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CARPETA)
import lexer

USUARIOS = ["isabellaim", "Jmuniz27", "nhn2004"]

def analizar_codigo(codigo):
    # llama al lexer y devuelve copias de la lista de tokens y de errores
    tokens, errores = lexer.tokenizar(codigo)
    return list(tokens), list(errores)

def linea_de_error(mensaje):
    # num de línea de un mensaje de error
    match = re.search(r"línea (\d+)", mensaje)
    if match:
        return int(match.group(1))
    return None

def armar_log(usuario, archivo, tokens, errores):
    ahora = datetime.now()
    nombre = f"lexico-{usuario}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    texto = f"Archivo de log: {nombre}\n"
    texto += f"Estudiante: {usuario}\n"
    texto += f"Fecha de ejecución: {ahora.strftime('%d-%m-%Y %H:%M')}\n"
    texto += f"Archivo analizado: {archivo}\n\n"
    texto += "*********** TOKENS VÁLIDOS *********** \n"
    if tokens:
        for tok in tokens:
            texto += f"[{tok.lineno}] {tok.type}: {tok.value}\n"
    else:
        texto += "No se encontraron tokens válidos.\n"
    texto += "\n*********** ERRORES ***********\n"
    if errores:
        for err in errores:
            texto += f"{err}\n"
    else:
        texto += "No se encontraron errores léxicos.\n"
    return nombre, texto


def guardar_log(nombre, texto):
    # los logs de la interfaz van en su propia subcarpeta
    carpeta_logs = os.path.join(CARPETA, "logs", "interfaz")
    os.makedirs(carpeta_logs, exist_ok=True)
    ruta = os.path.join(carpeta_logs, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta

FONDO = "white"
FONDO_NUMEROS = "#f5f5f5"
BORDE = "#d6d6d6"
TEXTO_SUAVE = "#8a8a8a"
TEXTO = "#333333"
OSCURO = "#222222"
FUENTE_CODIGO = ("Menlo", 10)
FUENTE_PANEL = ("Helvetica", 10)
ROJO = "#c62828"
ROJO_FONDO = "#ffd9d9"


class AnalizadorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico Ruby - Grupo 2")
        self.geometry("1100x650")
        self.configure(bg=FONDO)
        self.archivo_actual = None
        self._estilos()
        self._encabezado()
        self._cuerpo()
        self._barra_estado()

    def _estilos(self):
        # mismo estilo para botones y caja de usuario
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        forma = dict(background="white", fieldbackground="white", bordercolor=BORDE, lightcolor="white", darkcolor="white", focuscolor="white", relief="solid", borderwidth=1, padding=(10, 4), foreground=TEXTO)
        estilo.configure("TButton", width=0, **forma)
        estilo.map("TButton", background=[("active", FONDO_NUMEROS)], bordercolor=[("focus", BORDE)])

        # Analizar en oscuro porque es el botón principal
        estilo.configure("Principal.TButton", background=OSCURO, foreground="white", bordercolor=OSCURO, lightcolor=OSCURO, darkcolor=OSCURO, focuscolor=OSCURO)
        estilo.map("Principal.TButton", background=[("active", "black")], bordercolor=[("focus", OSCURO)])

        estilo.configure("TCombobox", arrowcolor=TEXTO_SUAVE, **forma)
        estilo.configure("TCombobox", padding=(10, 5))
        estilo.map("TCombobox", fieldbackground=[("readonly", "white")], bordercolor=[("focus", BORDE)], lightcolor=[("focus", "white")], selectbackground=[("readonly", "white")], selectforeground=[("readonly", TEXTO)])

        # pestañas planas
        estilo.configure("TNotebook", background="white", borderwidth=0, bordercolor="white", lightcolor="white", darkcolor="white", tabmargins=(0, 0, 0, 0))
        estilo.configure("TNotebook.Tab", background=FONDO_NUMEROS, foreground=TEXTO_SUAVE, bordercolor=BORDE, lightcolor=FONDO_NUMEROS, darkcolor=FONDO_NUMEROS, focuscolor=FONDO_NUMEROS, padding=(12, 4), font=FUENTE_PANEL)
        estilo.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", OSCURO)], lightcolor=[("selected", "white")], focuscolor=[("selected", "white")], expand=[("selected", (0, 0, 0, 0))])

        # tablas
        estilo.configure("Treeview", background="white", fieldbackground="white", foreground=TEXTO, font=FUENTE_CODIGO, rowheight=19, borderwidth=0, bordercolor="white", lightcolor="white", darkcolor="white")
        estilo.map("Treeview", bordercolor=[("focus", "white")], lightcolor=[("focus", "white")])
        estilo.configure("Treeview.Heading", background=FONDO_NUMEROS, foreground=TEXTO_SUAVE, relief="flat", borderwidth=0, bordercolor=FONDO_NUMEROS, lightcolor=FONDO_NUMEROS, darkcolor=FONDO_NUMEROS, padding=(8, 4), font=("Helvetica", 9, "bold"))
        estilo.map("Treeview.Heading", background=[("active", FONDO_NUMEROS)])

    def _encabezado(self):
        tk.Label(self, text="Analizador Léxico Ruby - Grupo 2", bg=FONDO, anchor="center", font=("Helvetica", 16, "bold")).pack(fill="x", pady=(14, 0))

        barra = tk.Frame(self, padx=14, pady=10, bg=FONDO)
        barra.pack(fill="x")
        ttk.Button(barra, text="Abrir .rb", command=self.abrir_archivo).pack(side="left")
        ttk.Button(barra, text="Analizar", style="Principal.TButton", command=self.analizar).pack(side="left", padx=6)
        ttk.Button(barra, text="Limpiar", command=self.limpiar).pack(side="left")

        self.usuario = tk.StringVar(value=USUARIOS[0])
        ttk.Combobox(barra, textvariable=self.usuario, values=USUARIOS, state="readonly", width=12).pack(side="right")
        tk.Label(barra, text="Usuario:", bg=FONDO).pack(side="right", padx=(0, 6))

    def _tarjeta(self, columna, titulo):
        tarjeta = tk.Frame(self.cuerpo, bg=FONDO)
        tarjeta.grid(row=0, column=columna, sticky="nsew", padx=(0, 7) if columna == 0 else (7, 0))
        etiqueta = tk.Label(tarjeta, text=titulo, bg=FONDO, fg=TEXTO_SUAVE, anchor="w")
        etiqueta.pack(fill="x", pady=(0, 4))
        borde = tk.Frame(tarjeta, bg="white", highlightthickness=1, highlightbackground=BORDE)
        borde.pack(fill="both", expand=True)
        return etiqueta, borde

    def _cuerpo(self):
        # dos columnas del mismo ancho
        self.cuerpo = tk.Frame(self, bg=FONDO, padx=14)
        self.cuerpo.pack(fill="both", expand=True)
        self.cuerpo.columnconfigure(0, weight=1, uniform="lados")
        self.cuerpo.columnconfigure(1, weight=1, uniform="lados")
        self.cuerpo.rowconfigure(0, weight=1)
        # lado izquierdo con el código
        self.lbl_archivo, marco = self._tarjeta(0, "CÓDIGO")
        self.numeros = tk.Text(marco, width=4, state="disabled", takefocus=0, bd=0, highlightthickness=0, bg=FONDO_NUMEROS, fg=TEXTO_SUAVE, padx=6, font=FUENTE_CODIGO)
        self.numeros.pack(side="left", fill="y")
        scroll = tk.Scrollbar(marco, command=self._scroll_ambos)
        scroll.pack(side="right", fill="y")
        # solo lectura porque el código entra con click en "Abrir .rb"
        self.editor = tk.Text(marco, wrap="none", bd=0, highlightthickness=0, padx=8, state="disabled", font=FUENTE_CODIGO, fg=TEXTO, yscrollcommand=lambda *a: self._sync(scroll, *a))
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.tag_configure("linea_error", background="#fff3b0")
        # error seleccionado en la pestaña Errores
        self.editor.tag_configure("error_elegido", background=ROJO_FONDO)
        self.numeros.tag_configure("error_elegido", foreground=ROJO, font=(FUENTE_CODIGO[0], FUENTE_CODIGO[1], "bold"))
        self.editor.bind("<<Modified>>", self._al_modificar)

        # lo que se muestra cuando no hay archivo
        self.guia = tk.Label(self.editor, bg="white", fg=TEXTO_SUAVE, justify="center", font=FUENTE_PANEL, text="Usa \"Abrir .rb\" para cargar un algoritmo")
        self._al_modificar()

        # lado derecho con los resultados (Juan, commit 3)
        _, der = self._tarjeta(1, "RESULTADOS")
        self.pestanas = ttk.Notebook(der)
        self.pestanas.pack(fill="both", expand=True)
        # columna ancho y si se estira
        self.tabla_tokens = self._tabla([("#", 50, False), ("Token", 170, False), ("Lexema", 200, True), ("Línea", 60, False)])
        self.tabla_errores = self._tabla([("Línea", 60, False), ("Mensaje", 400, True)])
        self.texto_log = tk.Text(self.pestanas, wrap="none", state="disabled", bd=0, highlightthickness=0, padx=8, pady=6, font=FUENTE_CODIGO, fg=TEXTO)
        self.pestanas.add(self.tabla_tokens, text="Tokens")
        self.pestanas.add(self.tabla_errores, text="Errores")
        self.pestanas.add(self.texto_log, text="Log")
        self.tabla_errores.bind("<<TreeviewSelect>>", self._ir_a_error)

    def _tabla(self, columnas):
        nombres = [c[0] for c in columnas]
        tabla = ttk.Treeview(self.pestanas, columns=nombres, show="headings")
        for nombre, ancho, estira in columnas:
            tabla.heading(nombre, text=nombre, anchor="w")
            tabla.column(nombre, width=ancho, minwidth=40, stretch=estira, anchor="w")
        return tabla

    def _barra_estado(self):
        self.estado = tk.StringVar(value="")
        tk.Label(self, textvariable=self.estado, anchor="w", padx=14, pady=8, bg=FONDO, fg=TEXTO_SUAVE).pack(fill="x")

    def _sync(self, scroll, primero, ultimo):
        scroll.set(primero, ultimo)
        self.numeros.yview_moveto(primero)

    def _scroll_ambos(self, *args):
        self.editor.yview(*args)
        self.numeros.yview(*args)

    def _al_modificar(self, evento=None):
        # sin esto el evento se repite sin parar
        if evento is not None and not self.editor.edit_modified():
            return
        self.editor.edit_modified(False)
        total = int(self.editor.index("end-1c").split(".")[0])
        self.numeros.config(state="normal")
        self.numeros.delete("1.0", "end")
        for i in range(1, total + 1):
            if i > 1:
                self.numeros.insert("end", "\n")
            self.numeros.insert("end", str(i))
        self.numeros.config(state="disabled")
        self.numeros.yview_moveto(self.editor.yview()[0])
        self.editor.tag_remove("linea_error", "1.0", "end")
        if self.editor.get("1.0", "end-1c"):
            self.guia.place_forget()
        else:
            self.guia.place(relx=0.5, rely=0.45, anchor="center")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            initialdir=os.path.join(CARPETA, "algoritmos"),
            filetypes=[("Ruby", "*.rb"), ("Todos", "*.*")])
        if not ruta:
            return
        with open(ruta, encoding="utf-8") as f:
            contenido = f.read()
        self._poner_codigo(contenido)
        self.archivo_actual = ruta
        self.lbl_archivo.config(text=f"CÓDIGO: {os.path.relpath(ruta, CARPETA)}")

    def _poner_codigo(self, contenido):
        # se activa un momento para poder cambiar el texto
        self.editor.config(state="normal")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", contenido)
        self.editor.config(state="disabled")

    def limpiar(self):
        self._poner_codigo("")
        self.archivo_actual = None
        self.lbl_archivo.config(text="CÓDIGO")
        self._llenar_resultados([], [])
        self._mostrar_log("")
        self.estado.set("")

    def analizar(self):
        if not self.archivo_actual:
            messagebox.showinfo("Aviso", "Primero abre un archivo .rb.")
            return

        codigo = self.editor.get("1.0", "end-1c")
        tokens, errores = analizar_codigo(codigo)
        self._llenar_resultados(tokens, errores)

        archivo = os.path.relpath(self.archivo_actual, CARPETA)
        nombre, texto = armar_log(self.usuario.get(), archivo, tokens, errores)
        guardar_log(nombre, texto)

        self._mostrar_log(texto)
        self.estado.set(f"Log guardado: logs/interfaz/{nombre}")

    def _mostrar_log(self, texto):
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.insert("1.0", texto)
        self.texto_log.config(state="disabled")

    def _llenar_resultados(self, tokens, errores):
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self.tabla_errores.delete(*self.tabla_errores.get_children())

        for i, tok in enumerate(tokens, start=1):
            self.tabla_tokens.insert("", "end", values=(i, tok.type, tok.value, tok.lineno))

        self.editor.tag_remove("linea_error", "1.0", "end")
        self.editor.tag_remove("error_elegido", "1.0", "end")
        self.numeros.tag_remove("error_elegido", "1.0", "end")

        for err in errores:
            linea = linea_de_error(err)
            self.tabla_errores.insert("", "end", values=(linea, err))
            if linea:
                self.editor.tag_add("linea_error", f"{linea}.0", f"{linea}.end")

    def _ir_a_error(self, evento=None):
        seleccion = self.tabla_errores.selection()
        if not seleccion:
            return
        linea = self.tabla_errores.item(seleccion[0], "values")[0]
        self.editor.tag_remove("error_elegido", "1.0", "end")
        self.numeros.tag_remove("error_elegido", "1.0", "end")
        if linea:
            self.editor.tag_add("error_elegido", f"{linea}.0", f"{linea}.end")
            self.editor.tag_raise("error_elegido")  # rojo encima del amarillo
            self.numeros.tag_add("error_elegido", f"{linea}.0", f"{linea}.end")
            self.numeros.see(f"{linea}.0")
            self.editor.see(f"{linea}.0")
            self.editor.mark_set("insert", f"{linea}.0")
            self.editor.focus_set()


if __name__ == "__main__":
    AnalizadorGUI().mainloop()
