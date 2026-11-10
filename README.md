# Analizador Léxico para Ruby (PLY)

Proyecto de Lenguajes de Programación (Grupo 2). Analizador léxico para un subconjunto de Ruby hecho en Python con la librería PLY. Tiene una interfaz gráfica para cargar un archivo `.rb`, ver los tokens y errores que encuentra, y guardar un log de cada prueba.

## Integrantes y aportes
* **Isabella Martín** (`isabellaim`) - Variables, palabras reservadas, comentarios y error para nombres de variable inválidos.
* **Juan Munizaga** (`Jmuniz27`) - Literales, cadenas, símbolos, operadores aritméticos y de asignación.
* **Nahin Cevallos** (`nhn2004`) - Operadores lógicos y de comparación, delimitadores y manejo de errores léxicos.

En `lexer.py` cada uno tiene su sección marcada con comentarios.

## Requisitos
* Python 3
* PLY: `pip install ply`
* Tkinter para la interfaz. Normalmente ya viene con Python. En Mac con Homebrew se instala con `brew install python-tk`.

## Archivos
* `lexer.py` - reglas del analizador léxico.
* `gui.py` - interfaz gráfica.
* `algoritmos/` - algoritmos de prueba en Ruby de cada integrante.
* `logs/` - logs de las pruebas.

## Cómo usarlo
Desde la carpeta del proyecto:
```bash
python gui.py
```
1. Elija su usuario arriba a la derecha.
2. Dé clic en **Abrir .rb** y escoja un algoritmo de la carpeta `algoritmos/`.
3. Dé clic en **Analizar**.

Los tokens, errores y el log salen en las pestañas de la derecha. Si da clic en un error, el editor se va a esa línea.

## Logs
Cada análisis guarda un log con el nombre `lexico-usuario-dia-mes-año-HHhMM.txt`, por ejemplo `lexico-isabellaim-09-11-2026-19h29.txt`. Se guardan en `logs/`, dentro de una carpeta con el nombre de cada usuario.
