# Analizador Léxico, Sintáctico y Semántico para Ruby (PLY)

Proyecto de Lenguajes de Programación del Grupo 2. Es un analizador léxico, sintáctico y semántico para un subconjunto de Ruby, escrito en Python con la librería PLY. Incluye una interfaz gráfica en la que se carga un archivo `.rb`, se revisan los tokens y los errores encontrados y se guarda un log de cada prueba.

## Integrantes y aportes

Cada integrante tiene su sección marcada con comentarios en `lexer.py` y en `parser.py`.

### Analizador léxico (`lexer.py`)
* Isabella Martín (`isabellaim`): variables, palabras reservadas, comentarios y error para nombres de variable inválidos.
* Juan Munizaga (`Jmuniz27`): literales, cadenas, símbolos y operadores aritméticos y de asignación.
* Nahin Cevallos (`nhn2004`): operadores lógicos y de comparación, delimitadores y manejo de errores léxicos.

### Analizador sintáctico (`parser.py`)
* Isabella Martín (`isabellaim`): asignación simple y compuesta (`+=`, `-=`, etc.), impresión con `puts` y `print`, `if / elsif / else`, arreglos con acceso por índice, funciones con `return` y llamadas a funciones.
* Juan Munizaga (`Jmuniz27`): expresiones aritméticas, `while`, asignación múltiple, hashes, asignación a una posición de un arreglo o hash (`notas[0] = 5`), clases y parámetros opcionales.
* Nahin Cevallos (`nhn2004`): base del parser, condiciones con `&&`, `||`, `and`, `or` y `not`, entrada con `gets`, llamadas con punto, asignación de constantes y de variables `@` y `$`, `case / when` (también dentro de una asignación), rangos, lambdas, `break`, `next` y manejo de errores sintácticos.

### Analizador semántico (`parser.py`)
Las reglas semánticas se verifican mientras el parser reconoce cada regla gramatical. Para ello se usa una tabla de símbolos que guarda el tipo y la línea de cada variable y constante. Cada error indica su categoría y su línea, por ejemplo: `Error semántico [Identificadores, línea 1]: la variable 'total' se usa antes de ser asignada.`

* Isabella Martín (`isabellaim`): una variable solo puede usarse si fue asignada antes en el mismo alcance. Cada `def` tiene su propio alcance, así que no ve las variables de afuera y sus variables no se ven fuera de él. Además, una constante no puede reasignarse.
* Juan Munizaga (`Jmuniz27`): base del analizador semántico (tabla de símbolos y tipos). Las operaciones aritméticas solo se permiten entre números (`Integer` y `Float`); un `String` solo puede sumarse con otro `String` o multiplicarse por un `Integer`, y el signo negativo (`-x`) solo se aplica a números. Para operar una cadena con un número hay que convertirla con `to_i`, `to_f` o `to_s`. Un `Integer` y un `Float` sí pueden operarse sin conversión, y el resultado es `Float`.
* Nahin Cevallos (`nhn2004`): `break` y `next` solo pueden usarse dentro de un `while`. Una función solo puede llamarse si fue definida y con una cantidad de argumentos que coincida con sus parámetros obligatorios y opcionales.

## Requisitos
* Python 3
* PLY: `pip install ply`
* Tkinter para la interfaz. Suele venir incluido con Python; en Mac con Homebrew se instala con `brew install python-tk`.

## Archivos
* `lexer.py`: reglas del analizador léxico.
* `parser.py`: reglas del analizador sintáctico y del semántico.
* `gui.py`: interfaz gráfica.
* `algoritmos/`: algoritmos de prueba en Ruby de cada integrante. Los de `pruebaN` corresponden al avance léxico, los de `prueba_sintacticoN` (y `prueba4_juan.rb`) al sintáctico y los de `prueba_semanticoN` al semántico.
* `logs/`: logs de las pruebas, en una carpeta por usuario.
* `Propuesta Grupo2 Ruby.pdf`: propuesta del proyecto, con las reglas de cada integrante y el diseño de la interfaz.
* `Informe Final Grupo2 Ruby.pdf`: informe final, con los resultados de las pruebas, las conclusiones y las recomendaciones de cada integrante.

## Cómo usarlo
Desde la carpeta del proyecto ejecute:
```bash
python gui.py
```
En Mac o Linux puede ser `python3 gui.py`.

1. Elija su usuario en la parte superior derecha.
2. Dé clic en **Abrir .rb** y seleccione un algoritmo de la carpeta `algoritmos/`.
3. Dé clic en **Analizar**.

El análisis se hace en orden. Primero se ejecuta el léxico; si no encuentra errores, se ejecuta el sintáctico, y si este tampoco los encuentra, se ejecuta el semántico. Debajo del encabezado, cada etapa aparece en verde si pasó sin errores, en rojo si encontró errores y en gris si no llegó a ejecutarse. En la parte inferior se muestra el resultado del análisis y la ruta del log guardado.

En el panel de código, los tokens se colorean según su tipo (palabras reservadas, cadenas, números, constantes y variables especiales, y comentarios), con los mismos colores que en la pestaña Tokens. Las líneas con errores se marcan en amarillo. Al dar clic en un error de la pestaña Errores, el editor va a esa línea y la resalta en rojo.

## Logs
Cada análisis guarda un log léxico con el nombre `lexico-usuario-añomesdia-HHhMM.txt`, por ejemplo `lexico-isabellaim-20261109-19h29.txt`. Si el análisis llega a la etapa sintáctica, guarda además `sintactico-usuario-añomesdia-HHhMM.txt`, por ejemplo `sintactico-isabellaim-20261114-20h33.txt`. Si llega a la etapa semántica, guarda también `semantico-usuario-añomesdia-HHhMM.txt`, por ejemplo `semantico-isabellaim-20261116-21h49.txt`. Los logs se guardan en `logs/`, dentro de la carpeta de cada usuario.
