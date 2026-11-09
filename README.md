# Analizador Léxico para Ruby (PLY)

Primer avance del proyecto de Lenguajes de Programación (ESPOL). Implementación de un analizador léxico para un subconjunto del lenguaje Ruby utilizando Python y la librería PLY.

## Integrantes y Aportes
* **Isabella Martín** (`isabellaim`) - Variables, palabras reservadas y comentarios.
* **Juan Munizaga** (`Jmuniz27`) - Literales, cadenas, símbolos, operadores aritméticos y de asignación.
* **Nahin Cevallos** (`nhn2004`) - Operadores lógicos, operadores de comparación, delimitadores y manejo de errores léxicos.

## Requisitos
* Python 3.x
* PLY (`pip install ply`)

## Estructura del Repositorio
* `lexer.py`: Código principal del analizador.
* `/algoritmos`: Archivos de prueba `.rb` separados por integrante.
* `/logs`: Archivos `.txt` con los resultados de los análisis.

## Ejecución
Para ejecutar el analizador:
```bash
python lexer.py
