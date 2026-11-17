import os
import re
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkfont

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


def armar_log_lexico(usuario, archivo, tokens, errores):
    ahora = datetime.now()
    nombre = f"lexico-{usuario}-{ahora.strftime('%Y%m%d-%Hh%M')}.txt"
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

def armar_log_sintactico(usuario, archivo, errores_sint):
    ahora = datetime.now()
    nombre = f"sintactico-{usuario}-{ahora.strftime('%Y%m%d-%Hh%M')}.txt"
    texto = f"Archivo de log: {nombre}\n"
    texto += f"Estudiante: {usuario}\n"
    texto += f"Fecha de ejecución: {ahora.strftime('%d-%m-%Y %H:%M')}\n"
    texto += f"Archivo analizado: {archivo}\n\n"
    texto += "*********** ERRORES SINTÁCTICOS ***********\n"
    if errores_sint:
        for err in errores_sint:
            texto += f"{err}\n"
    else:
        texto += "No se encontraron errores sintácticos.\n"
    return nombre, texto

def armar_log_semantico(usuario, archivo, errores_sem):
    ahora = datetime.now()
    nombre = f"semantico-{usuario}-{ahora.strftime('%Y%m%d-%Hh%M')}.txt"
    texto = f"Archivo de log: {nombre}\n"
    texto += f"Estudiante: {usuario}\n"
    texto += f"Fecha de ejecución: {ahora.strftime('%d-%m-%Y %H:%M')}\n"
    texto += f"Archivo analizado: {archivo}\n\n"
    texto += "*********** ERRORES SEMÁNTICOS ***********\n"
    if errores_sem:
        for err in errores_sem:
            texto += f"{err}\n"
    else:
        texto += "No se encontraron errores semánticos.\n"
    return nombre, texto


def guardar_log(usuario, nombre, texto):
    # La ruta crea la subcarpeta con el nombre del usuario de forma dinámica
    carpeta_logs = os.path.join(CARPETA, "logs", usuario)
    os.makedirs(carpeta_logs, exist_ok=True)
    ruta = os.path.join(carpeta_logs, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta




if sys.platform == "darwin":
    FUENTE, FUENTE_MONO = "Avenir Next", "Menlo"
elif sys.platform == "win32":
    FUENTE, FUENTE_MONO = "Segoe UI", "Consolas"
else:
    FUENTE, FUENTE_MONO = "Helvetica", "Courier"

FONDO = "#eef2f8"
TARJETA = "white"
SOMBRA = "#dfe5ef"
BORDE = "#e5e9f1"
TEXTO_SUAVE = "#8c95ab"
TEXTO = "#2b3452"
OSCURO = "#1f2740"
AZUL = "#4a6cd4"
AZUL_OSCURO = "#3b5bc0"
AZUL_SUAVE = "#eef2fd"
FUENTE_CODIGO = (FUENTE_MONO, 10)
FUENTE_PANEL = (FUENTE, 10)
ROJO = "#d64545"
ROJO_FONDO = "#fde3e3"
VERDE = "#3a9a5f"
ROJO_TEXTO = "#b83232"
VERDE_TEXTO = "#2b7a4b"

COLORES_TOKEN = {
    "reservada": "#4a6cd4",
    "cadena": "#3a9a5f",
    "numero": "#d08a1e",
    "especial": "#c2457a",
    "comentario": "#a3abbd",
}

COLOR_ETAPA = {"ok": VERDE, "error": ROJO, None: "#cdd3df"}

def categoria_token(tipo):
    if tipo in lexer.palabras_reservadas.values():
        return "reservada"
    if tipo in ("CADENA", "SIMBOLO"):
        return "cadena"
    if tipo in ("ENTERO", "FLOTANTE"):
        return "numero"
    if tipo in ("CONSTANTE", "VAR_INSTANCIA", "VAR_GLOBAL", "VAR_CLASE"):
        return "especial"
    return None

def rectangulo_redondo(lienzo, x1, y1, x2, y2, radio, **opciones):
    puntos = [x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio, x2, y2 - radio, x2, y2,
              x2 - radio, y2, x1 + radio, y2, x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1]
    return lienzo.create_polygon(puntos, smooth=True, **opciones)


class Tarjeta(tk.Canvas):
    def __init__(self, padre, radio=16, margen=14, ajustar_alto=False):
        super().__init__(padre, bg=FONDO, highlightthickness=0, bd=0, height=1)
        self.radio = radio
        self.margen = margen
        self.ajustar_alto = ajustar_alto
        self.interior = tk.Frame(self, bg=TARJETA)
        self.ventana = self.create_window(0, 0, window=self.interior, anchor="nw")
        self.bind("<Configure>", self._dibujar)
        if ajustar_alto:
            self.interior.bind("<Configure>", lambda e: self.config(height=self.interior.winfo_reqheight() + 2 * (4 + self.margen) + 2))

    def _dibujar(self, evento):
        self.delete("fondo")
        ancho, alto = evento.width, evento.height
        rectangulo_redondo(self, 4, 8, ancho - 4, alto - 2, self.radio, fill=SOMBRA, outline="", tags="fondo")
        rectangulo_redondo(self, 4, 4, ancho - 4, alto - 6, self.radio, fill=TARJETA, outline="", tags="fondo")
        self.tag_lower("fondo")
        m = 4 + self.margen
        self.coords(self.ventana, m, m)
        if self.ajustar_alto:
            self.itemconfig(self.ventana, width=max(ancho - 2 * m, 1))
        else:
            self.itemconfig(self.ventana, width=max(ancho - 2 * m, 1), height=max(alto - 6 - 2 * m + 4, 1))


class BotonRedondo(tk.Canvas):
    def __init__(self, padre, texto, command, principal=False):
        self.fuente = (FUENTE, 10)
        self.ancho = tkfont.Font(font=self.fuente).measure(texto) + 36
        self.alto = 34
        super().__init__(padre, width=self.ancho, height=self.alto, bg=padre["bg"], highlightthickness=0, bd=0, cursor="hand2")
        self.texto = texto
        self.command = command
        if principal:
            self.colores = (AZUL, AZUL_OSCURO, "white", "")
        else:
            self.colores = (TARJETA, AZUL_SUAVE, TEXTO, BORDE)
        self._dibujar(self.colores[0])
        self.bind("<Enter>", lambda e: self._dibujar(self.colores[1]))
        self.bind("<Leave>", lambda e: self._dibujar(self.colores[0]))
        self.bind("<ButtonRelease-1>", lambda e: self.command())

    def _dibujar(self, relleno):
        self.delete("all")
        rectangulo_redondo(self, 1, 1, self.ancho - 1, self.alto - 1, 11, fill=relleno, outline=self.colores[3])
        self.create_text(self.ancho / 2, self.alto / 2, text=self.texto, fill=self.colores[2], font=self.fuente)


class Pestanas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=TARJETA)
        self.barra = tk.Frame(self, bg=TARJETA)
        self.barra.pack(fill="x")
        tk.Frame(self, bg=BORDE, height=1).pack(fill="x")
        self.paginas = []
        self.botones = []
        self.actual = None

    def add(self, pagina, text):
        indice = len(self.paginas)
        caja = tk.Frame(self.barra, bg=TARJETA)
        caja.pack(side="left", padx=(0, 22))
        etiqueta = tk.Label(caja, text=text, bg=TARJETA, font=(FUENTE, 10), cursor="hand2")
        etiqueta.pack(pady=(0, 6))
        linea = tk.Frame(caja, height=2, bg=TARJETA)
        linea.pack(fill="x")
        etiqueta.bind("<Button-1>", lambda e: self.select(indice))
        self.paginas.append(pagina)
        self.botones.append((etiqueta, linea))
        if self.actual is None:
            self.select(0)
        else:
            self.select(self.actual)

    def select(self, indice):
        for i, (etiqueta, linea) in enumerate(self.botones):
            elegida = i == indice
            etiqueta.config(fg=AZUL if elegida else TEXTO_SUAVE)
            linea.config(bg=AZUL if elegida else TARJETA)
        if self.actual is not None:
            self.paginas[self.actual].pack_forget()
        self.paginas[indice].pack(fill="both", expand=True, pady=(10, 0))
        self.actual = indice


class BarraDelgada(tk.Canvas):
    def __init__(self, padre, orient="vertical", command=None):
        self.vertical = orient == "vertical"
        grosor = 10
        super().__init__(padre, bg=TARJETA, highlightthickness=0, bd=0, width=grosor if self.vertical else 1, height=1 if self.vertical else grosor)
        self.command = command
        self.inicio, self.fin = 0.0, 1.0
        self.color = "#d6dbe5"
        self.desfase = None
        self.bind("<Configure>", lambda e: self._dibujar())
        self.bind("<Enter>", lambda e: self._cambiar_color("#aab2c3"))
        self.bind("<Leave>", lambda e: self._cambiar_color("#d6dbe5"))
        self.bind("<ButtonPress-1>", self._presionar)
        self.bind("<B1-Motion>", self._arrastrar)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, "desfase", None))

    def set(self, inicio, fin):
        self.inicio, self.fin = float(inicio), float(fin)
        self._dibujar()

    def _largo(self):
        return max(self.winfo_height() if self.vertical else self.winfo_width(), 1)

    def _cambiar_color(self, color):
        self.color = color
        self._dibujar()

    def _dibujar(self):
        self.delete("all")
        if self.fin - self.inicio >= 1:
            return
        largo = self._largo()
        a = max(self.inicio * largo, 5)
        b = min(max(self.fin * largo, a + 20), largo - 5)
        if self.vertical:
            self.create_line(5, a, 5, b, width=6, fill=self.color, capstyle="round")
        else:
            self.create_line(a, 5, b, 5, width=6, fill=self.color, capstyle="round")

    def _posicion(self, evento):
        return (evento.y if self.vertical else evento.x) / self._largo()

    def _presionar(self, evento):
        pos = self._posicion(evento)
        if self.inicio <= pos <= self.fin:
            self.desfase = pos - self.inicio
        else:
            self.desfase = (self.fin - self.inicio) / 2
            self._arrastrar(evento)

    def _arrastrar(self, evento):
        if self.command and self.desfase is not None:
            self.command("moveto", self._posicion(evento) - self.desfase)


class AnalizadorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico, Sintáctico y Semántico Ruby - Grupo 2")
        self.geometry("1180x720")
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
        estilo.configure("TCombobox", background=TARJETA, fieldbackground=TARJETA, bordercolor=BORDE, lightcolor=TARJETA, darkcolor=TARJETA, focuscolor=TARJETA, arrowcolor=TEXTO_SUAVE, foreground=TEXTO, padding=(10, 6), relief="solid", borderwidth=1)
        estilo.map("TCombobox", fieldbackground=[("readonly", TARJETA)], bordercolor=[("focus", BORDE)], lightcolor=[("focus", TARJETA)], selectbackground=[("readonly", TARJETA)], selectforeground=[("readonly", TEXTO)])
        self.option_add("*TCombobox*Listbox.font", FUENTE_PANEL)
        self.option_add("*TCombobox*Listbox.selectBackground", AZUL_SUAVE)
        self.option_add("*TCombobox*Listbox.selectForeground", TEXTO)

        # tablas
        estilo.configure("Treeview", background=TARJETA, fieldbackground=TARJETA, foreground=TEXTO, font=FUENTE_CODIGO, rowheight=24, borderwidth=0, bordercolor=TARJETA, lightcolor=TARJETA, darkcolor=TARJETA)
        estilo.map("Treeview", background=[("selected", AZUL_SUAVE)], foreground=[("selected", OSCURO)], bordercolor=[("focus", TARJETA)], lightcolor=[("focus", TARJETA)])
        estilo.configure("Treeview.Heading", background=TARJETA, foreground=TEXTO_SUAVE, relief="flat", borderwidth=0, bordercolor=TARJETA, lightcolor=TARJETA, darkcolor=TARJETA, padding=(8, 2, 8, 8), font=(FUENTE, 9))
        estilo.map("Treeview.Heading", background=[("active", TARJETA)])

    def _encabezado(self):
        tarjeta = Tarjeta(self, margen=16, ajustar_alto=True)
        tarjeta.pack(fill="x", padx=24, pady=(20, 0))
        barra = tarjeta.interior
        textos = tk.Frame(barra, bg=TARJETA)
        textos.pack(side="left", padx=(6, 0))
        tk.Label(textos, text="Analizador Léxico, Sintáctico y Semántico Ruby", bg=TARJETA, fg=OSCURO, font=(FUENTE, 15, "bold")).pack(anchor="w")
        tk.Label(textos, text="Grupo 2: Martín, Munizaga, Cevallos", bg=TARJETA, fg=TEXTO_SUAVE, font=(FUENTE, 10)).pack(anchor="w", pady=(2, 0))

        # Analizar resaltado porque es el botón principal
        BotonRedondo(barra, "Analizar", self.analizar, principal=True).pack(side="right", padx=(0, 6))
        BotonRedondo(barra, "Limpiar", self.limpiar).pack(side="right", padx=8)
        BotonRedondo(barra, "Abrir .rb", self.abrir_archivo).pack(side="right")
        self.usuario = tk.StringVar(value=USUARIOS[0])
        ttk.Combobox(barra, textvariable=self.usuario, values=USUARIOS, state="readonly", width=11, font=FUENTE_PANEL).pack(side="right", padx=(0, 16))
        tk.Label(barra, text="Usuario", bg=TARJETA, fg=TEXTO_SUAVE, font=FUENTE_PANEL).pack(side="right", padx=(0, 8))

        etapas = tk.Frame(self, bg=FONDO, padx=34)
        etapas.pack(fill="x", pady=(10, 0))
        self.etapas = []
        for nombre in ("Léxico", "Sintáctico", "Semántico"):
            punto = tk.Label(etapas, text="●", bg=FONDO, font=(FUENTE, 14))
            punto.pack(side="left")
            etiqueta = tk.Label(etapas, text=nombre, bg=FONDO, font=(FUENTE, 10))
            etiqueta.pack(side="left", padx=(4, 20))
            self.etapas.append((punto, etiqueta))
        self._marcar_etapas([])

    def _tarjeta(self, columna, titulo):
        tarjeta = Tarjeta(self.cuerpo)
        tarjeta.grid(row=0, column=columna, sticky="nsew", padx=(0, 8) if columna == 0 else (8, 0))
        etiqueta = tk.Label(tarjeta.interior, text=titulo, bg=TARJETA, fg=TEXTO_SUAVE, anchor="w", font=(FUENTE, 9))
        etiqueta.pack(fill="x", pady=(0, 10))
        borde = tk.Frame(tarjeta.interior, bg=TARJETA)
        borde.pack(fill="both", expand=True)
        return etiqueta, borde

    def _cuerpo(self):
        # dos columnas del mismo ancho
        self.cuerpo = tk.Frame(self, bg=FONDO, padx=24)
        self.cuerpo.pack(fill="both", expand=True, pady=(6, 0))
        self.cuerpo.columnconfigure(0, weight=1, uniform="lados")
        self.cuerpo.columnconfigure(1, weight=1, uniform="lados")
        self.cuerpo.rowconfigure(0, weight=1)
        # lado izquierdo con el código
        self.lbl_archivo, marco = self._tarjeta(0, "CÓDIGO")
        scroll_x = BarraDelgada(marco, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        self.numeros = tk.Text(marco, width=4, state="disabled", takefocus=0, bd=0, highlightthickness=0, bg=TARJETA, fg="#b7bfcf", padx=4, font=FUENTE_CODIGO, spacing1=2, spacing3=2)
        self.numeros.pack(side="left", fill="y")
        scroll = BarraDelgada(marco, command=self._scroll_ambos)
        scroll.pack(side="right", fill="y")
        # solo lectura porque el código entra con click en "Abrir .rb"
        self.editor = tk.Text(marco, wrap="none", bd=0, highlightthickness=0, padx=10, state="disabled", font=FUENTE_CODIGO, fg=TEXTO, spacing1=2, spacing3=2, yscrollcommand=lambda *a: self._sync(scroll, *a))
        self.editor.pack(side="left", fill="both", expand=True)
        self.editor.config(xscrollcommand=scroll_x.set)
        scroll_x.command = self.editor.xview
        for categoria, color in COLORES_TOKEN.items():
            self.editor.tag_configure(categoria, foreground=color)
        self.editor.tag_configure("comentario", font=(FUENTE_MONO, 10, "italic"))
        self.editor.tag_configure("linea_error", background="#fff4cc")
        # error seleccionado en la pestaña Errores
        self.editor.tag_configure("error_elegido", background=ROJO_FONDO)
        self.numeros.tag_configure("error_elegido", foreground=ROJO, font=(FUENTE_MONO, 10, "bold"))
        self.editor.bind("<<Modified>>", self._al_modificar)

        # lo que se muestra cuando no hay archivo
        self.guia = tk.Label(self.editor, bg=TARJETA, fg=TEXTO_SUAVE, justify="center", font=FUENTE_PANEL, text="Usa \"Abrir .rb\" para cargar un algoritmo")
        self._al_modificar()

        # lado derecho con los resultados (Juan, commit 3)
        _, der = self._tarjeta(1, "RESULTADOS")
        # pestañas planas
        self.pestanas = Pestanas(der)
        self.pestanas.pack(fill="both", expand=True)
        # columna ancho y si se estira
        caja_tokens, self.tabla_tokens = self._tabla([("#", 50, False), ("Token", 170, False), ("Lexema", 200, True), ("Línea", 60, False)])
        caja_errores, self.tabla_errores = self._tabla([("Línea", 60, False), ("Mensaje", 400, False)])
        for categoria, color in COLORES_TOKEN.items():
            self.tabla_tokens.tag_configure(categoria, foreground=color)
        self.tabla_errores.tag_configure("error", foreground=ROJO)

        caja_log = tk.Frame(self.pestanas, bg=TARJETA)
        self.texto_log = tk.Text(caja_log, wrap="none", state="disabled", bd=0, highlightthickness=0, padx=8, pady=4, font=FUENTE_CODIGO, fg=TEXTO, spacing1=2, spacing3=2)
        self._agregar_scroll(caja_log, self.texto_log, horizontal=True)
        self.texto_log.tag_configure("error", foreground=ROJO)
        self.texto_log.tag_configure("bien", foreground=VERDE)

        self.pestanas.add(caja_tokens, text="Tokens")
        self.pestanas.add(caja_errores, text="Errores")
        self.pestanas.add(caja_log, text="Log")
        self.tabla_errores.bind("<<TreeviewSelect>>", self._ir_a_error)

    def _agregar_scroll(self, caja, widget, horizontal=False):
        scroll_y = BarraDelgada(caja, command=widget.yview)
        widget.configure(yscrollcommand=scroll_y.set)
        if horizontal:
            scroll_x = BarraDelgada(caja, orient="horizontal", command=widget.xview)
            widget.configure(xscrollcommand=scroll_x.set)
            scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        widget.pack(side="left", fill="both", expand=True)

    def _tabla(self, columnas):
        caja = tk.Frame(self.pestanas, bg=TARJETA)
        nombres = [c[0] for c in columnas]
        tabla = ttk.Treeview(caja, columns=nombres, show="headings")
        for nombre, ancho, estira in columnas:
            tabla.heading(nombre, text=nombre, anchor="w")
            tabla.column(nombre, width=ancho, minwidth=40, stretch=estira, anchor="w")
        self._agregar_scroll(caja, tabla, horizontal=True)
        return caja, tabla

    def _marcar_etapas(self, estados):
        for i, (punto, etiqueta) in enumerate(self.etapas):
            estado = estados[i] if i < len(estados) else None
            punto.config(fg=COLOR_ETAPA[estado])
            etiqueta.config(fg=ROJO_TEXTO if estado == "error" else VERDE_TEXTO if estado == "ok" else TEXTO_SUAVE)

    def _colorear_codigo(self):
        for categoria in COLORES_TOKEN:
            self.editor.tag_remove(categoria, "1.0", "end")
        codigo = self.editor.get("1.0", "end-1c")
        tokens, _ = analizar_codigo(codigo)
        cadenas = []
        for tok in tokens:
            categoria = categoria_token(tok.type)
            if categoria:
                inicio, fin = tok.lexpos, tok.lexpos + len(str(tok.value))
                self.editor.tag_add(categoria, f"1.0+{inicio}c", f"1.0+{fin}c")
                if categoria == "cadena":
                    cadenas.append((inicio, fin))
        for encontrado in re.finditer(r"=begin(.|\n)*?=end|#[^\n]*", codigo):
            if any(a <= encontrado.start() < b for a, b in cadenas):
                continue
            self.editor.tag_add("comentario", f"1.0+{encontrado.start()}c", f"1.0+{encontrado.end()}c")

    def _barra_estado(self):
        tarjeta = Tarjeta(self, margen=10, ajustar_alto=True)
        tarjeta.pack(fill="x", padx=24, pady=(4, 18))
        barra = tarjeta.interior
        self.punto_estado = tk.Label(barra, text="●", bg=TARJETA, font=(FUENTE, 9))
        self.punto_estado.pack(side="left", padx=(6, 8))
        self.lbl_estado = tk.Label(barra, bg=TARJETA, font=(FUENTE, 10), anchor="w")
        self.lbl_estado.pack(side="left")
        self.lbl_ruta = tk.Label(barra, bg=TARJETA, fg=TEXTO_SUAVE, font=(FUENTE, 9), anchor="w")
        self.lbl_ruta.pack(side="left", padx=(12, 0))
        self.hay_errores = None
        self.estado = tk.StringVar(value="")
        self.estado.trace_add("write", lambda *a: self._mostrar_estado())
        self._mostrar_estado()

    def _poner_estado(self, texto, hay_errores):
        self.hay_errores = hay_errores
        self.estado.set(texto)

    def _mostrar_estado(self):
        texto = self.estado.get()
        if not texto:
            self.hay_errores = None
            self.punto_estado.config(fg="#cdd3df")
            self.lbl_estado.config(text="Abra un algoritmo y dé clic en Analizar", fg=TEXTO_SUAVE)
            self.lbl_ruta.config(text="")
            return
        resultado, _, ruta = texto.partition(". Log guardado: ")
        color = ROJO_TEXTO if self.hay_errores else VERDE_TEXTO
        self.punto_estado.config(fg=ROJO if self.hay_errores else VERDE)
        self.lbl_estado.config(text=resultado, fg=color)
        self.lbl_ruta.config(text=f"Log guardado en {ruta}" if ruta else "")

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
        self._colorear_codigo()
        self.archivo_actual = ruta
        self.lbl_archivo.config(text=f"CÓDIGO: {os.path.relpath(ruta, CARPETA)}")
        self._marcar_etapas([])
        self.estado.set("")

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
        self._marcar_etapas([])
        self.estado.set("")

    def analizar(self):
        if not self.archivo_actual:
            messagebox.showinfo("Aviso", "Primero abre un archivo .rb.")
            return

        codigo = self.editor.get("1.0", "end-1c")
        usuario_actual = self.usuario.get()
        archivo = os.path.relpath(self.archivo_actual, CARPETA)

        # PASO 1: Ejecutar el Análisis Léxico
        tokens, errores_lex = analizar_codigo(codigo)

        # Generar y guardar el log léxico
        nombre_lex, texto_lex = armar_log_lexico(usuario_actual, archivo, tokens, errores_lex)
        guardar_log(usuario_actual, nombre_lex, texto_lex)

        # Si hay errores léxicos, los mostramos en la UI y detenemos el flujo
        if errores_lex:
            self._llenar_resultados(tokens, errores_lex)
            self._mostrar_log(texto_lex)
            self._marcar_etapas(["error"])
            self._poner_estado(f"Detenido por errores léxicos. Log guardado: logs/{usuario_actual}/{nombre_lex}", True)
            return

        # PASO 2: Si el léxico pasó limpio, ejecutamos el Análisis Sintáctico (Parser)
        import parser
        _, errores_sint = parser.parsear(codigo)

        # Llenamos los resultados en la UI (esto poblará la tabla de errores y marcará las líneas en amarillo)
        self._llenar_resultados(tokens, errores_sint)

        # Generar y guardar el log sintáctico
        nombre_sint, texto_sint = armar_log_sintactico(usuario_actual, archivo, errores_sint)
        guardar_log(usuario_actual, nombre_sint, texto_sint)

        # Si hay errores sintácticos se muestra el log sintáctico y no se sigue
        if errores_sint:
            self._mostrar_log(texto_sint)
            self._marcar_etapas(["ok", "error"])
            self._poner_estado(f"Detenido por errores sintácticos. Log guardado: logs/{usuario_actual}/{nombre_sint}", True)
            return

        # PASO 3: Análisis semántico, sus errores se guardan mientras corre el parser
        errores_sem = list(parser.errores_semanticos)
        self._llenar_resultados(tokens, errores_sem)

        nombre_sem, texto_sem = armar_log_semantico(usuario_actual, archivo, errores_sem)
        guardar_log(usuario_actual, nombre_sem, texto_sem)

        self._mostrar_log(texto_sem)
        if errores_sem:
            self._marcar_etapas(["ok", "ok", "error"])
            self._poner_estado(f"Análisis completo con errores semánticos. Log guardado: logs/{usuario_actual}/{nombre_sem}", True)
        else:
            self._marcar_etapas(["ok", "ok", "ok"])
            self._poner_estado(f"Análisis completo sin errores. Log guardado: logs/{usuario_actual}/{nombre_sem}", False)



    def _mostrar_log(self, texto):
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.insert("1.0", texto)
        for i, linea in enumerate(texto.splitlines(), start=1):
            if linea.startswith("Error"):
                self.texto_log.tag_add("error", f"{i}.0", f"{i}.end")
            elif linea.startswith("No se encontraron"):
                self.texto_log.tag_add("bien", f"{i}.0", f"{i}.end")
        self.texto_log.config(state="disabled")

    def _llenar_resultados(self, tokens, errores):
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self.tabla_errores.delete(*self.tabla_errores.get_children())

        for i, tok in enumerate(tokens, start=1):
            categoria = categoria_token(tok.type)
            self.tabla_tokens.insert("", "end", values=(i, tok.type, tok.value, tok.lineno), tags=(categoria,) if categoria else ())

        self.editor.tag_remove("linea_error", "1.0", "end")
        self.editor.tag_remove("error_elegido", "1.0", "end")
        self.numeros.tag_remove("error_elegido", "1.0", "end")

        for err in errores:
            linea = linea_de_error(err)
            self.tabla_errores.insert("", "end", values=(linea, err), tags=("error",))
            if linea:
                self.editor.tag_add("linea_error", f"{linea}.0", f"{linea}.end")
        medida = tkfont.Font(font=FUENTE_CODIGO)
        ancho = max([medida.measure(err) + 30 for err in errores] + [400])
        self.tabla_errores.column("Mensaje", width=ancho)

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
