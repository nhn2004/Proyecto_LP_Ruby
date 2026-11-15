# Analizador Léxico y Sintáctico para Ruby (PLY)

Proyecto de Lenguajes de Programación (Grupo 2). Analizador léxico y sintáctico para un subconjunto de Ruby hecho en Python con la librería PLY. Tiene una interfaz gráfica para cargar un archivo `.rb`, ver los tokens y errores que encuentra, y guardar un log de cada prueba.

## Integrantes y aportes

### Analizador léxico (`lexer.py`)
* **Isabella Martín** (`isabellaim`) - Variables, palabras reservadas, comentarios y error para nombres de variable inválidos.
* **Juan Munizaga** (`Jmuniz27`) - Literales, cadenas, símbolos, operadores aritméticos y de asignación.
* **Nahin Cevallos** (`nhn2004`) - Operadores lógicos y de comparación, delimitadores y manejo de errores léxicos.

### Analizador sintáctico (`parser.py`)
* **Isabella Martín** (`isabellaim`) - Asignación simple y compuesta (`+=`, `-=`, etc.), impresión con `puts` y `print`, `if / elsif / else`, arreglos y acceso por índice, funciones con `return` y llamadas a funciones.
* **Juan Munizaga** (`Jmuniz27`) - Expresiones aritméticas, `while`, asignación múltiple, hashes, clases y parámetros opcionales.
* **Nahin Cevallos** (`nhn2004`) - Base del parser, condiciones con `&&`, `||`, `and`, `or` y `not`, entrada con `gets`, llamadas con punto, `case / when`, rangos, lambdas y manejo de errores sintácticos.

En los dos archivos cada uno tiene su sección marcada con comentarios.

## Requisitos
* Python 3
* PLY: `pip install ply`
* Tkinter para la interfaz. Normalmente ya viene con Python. En Mac con Homebrew se instala con `brew install python-tk`.

## Archivos
* `lexer.py` - reglas del analizador léxico.
* `parser.py` - reglas del analizador sintáctico.
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

Primero se hace el análisis léxico. Si no hay errores léxicos, se hace también el sintáctico. Los tokens, errores y el log salen en las pestañas de la derecha. Si da clic en un error, el editor se va a esa línea.

## Logs
Cada análisis guarda un log léxico con el nombre `lexico-usuario-añomesdia-HHhMM.txt`, por ejemplo `lexico-isabellaim-20261109-19h29.txt`. Si pasa al análisis sintáctico, guarda además un log `sintactico-usuario-añomesdia-HHhMM.txt`, por ejemplo `sintactico-isabellaim-20261114-20h33.txt`. Se guardan en `logs/`, dentro de una carpeta con el nombre de cada usuario.
