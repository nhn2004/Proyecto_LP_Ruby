import ply.yacc as yacc
import lexer

tokens = lexer.tokens


# Nahin, base del parser 
def p_programa(p):
    "programa : lista_sentencias"
    p[0] = ('programa', p[1])

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_sentencia_expresion(p):
    "sentencia : expresion"
    p[0] = p[1]

# niveles de las expresiones de menor a mayor prioridad segun la documentacion de Ruby
def p_niveles_expresion(p):
    '''expresion : expresion_not
       expresion_not : expresion_rango
       expresion_rango : expresion_o
       expresion_o : expresion_y
       expresion_y : expresion_igualdad
       expresion_igualdad : expresion_comparacion
       expresion_comparacion : expresion_suma
       expresion_suma : expresion_producto
       expresion_producto : expresion_unaria
       expresion_unaria : expresion_potencia
       expresion_potencia : expresion_negacion
       expresion_negacion : valor'''
    p[0] = p[1]

def p_valor_variable(p):
    '''valor : ID
             | CONSTANTE
             | VAR_INSTANCIA
             | VAR_GLOBAL
             | VAR_CLASE
             | SELF'''
    p[0] = ('variable', p[1])

def p_valor_parentesis(p):
    "valor : PAREN_IZQ expresion PAREN_DER"
    p[0] = p[2]

def p_empty(p):
    "empty :"
    p[0] = []



# Juan, expresiones aritmeticas
def p_valor_literal(p):
    '''valor : ENTERO
             | FLOTANTE
             | CADENA
             | SIMBOLO
             | TRUE
             | FALSE
             | NIL'''
    p[0] = ('literal', p[1])

def p_expresion_suma(p):
    '''expresion_suma : expresion_suma SUMA expresion_producto
                      | expresion_suma RESTA expresion_producto'''
    p[0] = ('aritmetica', p[2], p[1], p[3])

def p_expresion_producto(p):
    '''expresion_producto : expresion_producto MULTIPLICACION expresion_unaria
                          | expresion_producto DIVISION expresion_unaria
                          | expresion_producto MODULO expresion_unaria'''
    p[0] = ('aritmetica', p[2], p[1], p[3])

# menos unario ej -5
def p_expresion_unaria(p):
    "expresion_unaria : RESTA expresion_unaria"
    p[0] = ('unario', p[1], p[2])

# la potencia se agrupa por la derecha ej 2 ** 3 ** 2 es 2 ** 9
def p_expresion_potencia(p):
    "expresion_potencia : expresion_negacion POTENCIA expresion_unaria"
    p[0] = ('aritmetica', p[2], p[1], p[3])
# fin Juan


# INICIO Isa, asignacion e impresion
def p_sentencia_asignacion(p):
    "sentencia : asignacion"
    p[0] = p[1]

#aqui no guardo el = porque siempre es el mismo
def p_asignacion_simple(p):
    "asignacion : ID IGUAL expresion"
    p[0] = ('asignacion', p[1], p[3])

# ej contador += 1 y aqui si guardo el operador para saber cual fue
def p_asignacion_compuesta(p):
    '''asignacion : variable_compuesta MAS_IGUAL expresion
                  | variable_compuesta MENOS_IGUAL expresion
                  | variable_compuesta POR_IGUAL expresion
                  | variable_compuesta DIVIDIDO_IGUAL expresion
                  | variable_compuesta MODULO_IGUAL expresion
                  | variable_compuesta POTENCIA_IGUAL expresion
                  | variable_compuesta OR_IGUAL expresion
                  | variable_compuesta AND_IGUAL expresion'''
    p[0] = ('asignacion_compuesta', p[2], p[1], p[3])

# Variables que pueden ir antes de por ejemplo += o -=
def p_variable_compuesta(p):
    '''variable_compuesta : ID
                          | VAR_INSTANCIA
                          | VAR_GLOBAL
                          | VAR_CLASE'''
    p[0] = p[1]

def p_sentencia_impresion(p):
    "sentencia : impresion"
    p[0] = p[1]

def p_impresion(p):
    '''impresion : PUTS lista_expresiones
                 | PRINT lista_expresiones'''
    p[0] = ('impresion', p[1], p[2])

#la usan luego puts, los arreglos y los argumentos de las funciones
def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]
# FIN Isa

# Nahin, condiciones y entrada de datos
def p_expresion_comparacion(p):
    '''expresion_comparacion : expresion_suma MENOR expresion_suma
                             | expresion_suma MAYOR expresion_suma
                             | expresion_suma MENOR_IGUAL expresion_suma
                             | expresion_suma MAYOR_IGUAL expresion_suma'''
    p[0] = ('comparacion', p[2], p[1], p[3])

def p_expresion_igualdad(p):
    '''expresion_igualdad : expresion_comparacion IGUAL_IGUAL expresion_comparacion
                          | expresion_comparacion DISTINTO expresion_comparacion
                          | expresion_comparacion IGUAL_CASO expresion_comparacion
                          | expresion_comparacion NAVE expresion_comparacion'''
    p[0] = ('comparacion', p[2], p[1], p[3])

# && tiene mas prioridad que ||
def p_expresion_y(p):
    "expresion_y : expresion_y AND_LOGICO expresion_igualdad"
    p[0] = ('logica', p[2], p[1], p[3])

def p_expresion_o(p):
    "expresion_o : expresion_o OR_LOGICO expresion_y"
    p[0] = ('logica', p[2], p[1], p[3])

# ! tiene la prioridad mas alta y not la mas baja
def p_expresion_negacion(p):
    "expresion_negacion : NOT_LOGICO expresion_negacion"
    p[0] = ('negacion', p[1], p[2])

def p_expresion_not(p):
    "expresion_not : NOT expresion_not"
    p[0] = ('negacion', p[1], p[2])

# and y or son las de menor prioridad
def p_expresion_and_or(p):
    '''expresion : expresion AND expresion_not
                 | expresion OR expresion_not'''
    p[0] = ('logica', p[2], p[1], p[3])

def p_valor_gets(p):
    "valor : GETS"
    p[0] = ('entrada', p[1])

# llamadas con punto que se pueden encadenar ej gets.chomp.to_i o Curso.new("LP")
def p_valor_llamada_punto(p):
    '''valor : valor PUNTO ID
             | valor PUNTO ID PAREN_IZQ PAREN_DER
             | valor PUNTO ID PAREN_IZQ lista_expresiones PAREN_DER'''
    argumentos = p[5] if len(p) == 7 else []
    p[0] = ('llamada_metodo', p[1], p[3], argumentos)
# fin Nahin

# Juan, while y asignacion multiple
def p_sentencia_while(p):
    "sentencia : sentencia_while"
    p[0] = p[1]

# el do es opcional como en ruby ej while i < 5 do
def p_sentencia_while_cuerpo(p):
    '''sentencia_while : WHILE expresion DO lista_sentencias END
                       | WHILE expresion lista_sentencias END'''
    cuerpo = p[4] if len(p) == 6 else p[3]
    p[0] = ('while', p[2], cuerpo)

# ej a, b = 1, 2
def p_asignacion_multiple(p):
    "asignacion : lista_variables IGUAL lista_expresiones"
    p[0] = ('asignacion_multiple', p[1], p[3])

# empieza con dos variables para que no choque con la asignacion simple
def p_lista_variables(p):
    '''lista_variables : lista_variables COMA ID
                       | ID COMA ID'''
    p[0] = p[1] + [p[3]] if isinstance(p[1], list) else [p[1], p[3]]
# fin Juan

# Inicio Isa, if elsif else y arreglos
def p_sentencia_if(p):
    "sentencia : sentencia_if"
    p[0] = p[1]

#elsif y else pueden no estar pero el end siempre si esta
def p_sentencia_if_cuerpo(p):
    "sentencia_if : cabecera_if lista_sentencias lista_elsif else_opcional END"
    p[0] = ('if', p[1], p[2], p[3], p[4])

#then opcional
def p_cabecera_if(p):
    '''cabecera_if : IF expresion THEN
                   | IF expresion'''
    p[0] = p[2]

# Puede haber varios elsif
def p_lista_elsif(p):
    '''lista_elsif : lista_elsif ELSIF expresion lista_sentencias
                   | empty'''
    if len(p) == 5:
        p[0] = p[1] + [('elsif', p[3], p[4])]
    else:
        p[0] = []

def p_else_opcional(p):
    '''else_opcional : ELSE lista_sentencias
                     | empty'''
    if len(p) == 3:
        p[0] = ('else', p[2])
    else:
        p[0] = []

def p_valor_arreglo(p):
    '''valor : CORCHETE_IZQ lista_expresiones CORCHETE_DER
             | CORCHETE_IZQ CORCHETE_DER'''
    if len(p) == 4:
        p[0] = ('arreglo', p[2])
    else:
        p[0] = ('arreglo', [])

# ejemplos numeros[0] y matriz[0][1]
def p_valor_acceso_arreglo(p):
    "valor : valor CORCHETE_IZQ expresion CORCHETE_DER"
    p[0] = ('acceso', p[1], p[3])
# Fin Isa


# Nahin, case when rangos y asignacion especial
def p_sentencia_case(p):
    "sentencia : sentencia_case"
    p[0] = p[1]

def p_sentencia_case_cuerpo(p):
    "sentencia_case : CASE expresion lista_when else_opcional END"
    p[0] = ('case', p[2], p[3], p[4])

def p_lista_when(p):
    '''lista_when : lista_when bloque_when
                  | bloque_when'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_bloque_when(p):
    '''bloque_when : WHEN lista_expresiones THEN lista_sentencias
                   | WHEN lista_expresiones lista_sentencias'''
    cuerpo = p[4] if len(p) == 5 else p[3]
    p[0] = ('when', p[2], cuerpo)

def p_expresion_rango(p):
    '''expresion_rango : expresion_o RANGO_INCLUSIVO expresion_o
                       | expresion_o RANGO_EXCLUSIVO expresion_o'''
    p[0] = ('rango', p[2], p[1], p[3])

def p_asignacion_especial(p):
    '''asignacion : CONSTANTE IGUAL expresion
                  | VAR_INSTANCIA IGUAL expresion
                  | VAR_GLOBAL IGUAL expresion'''
    p[0] = ('asignacion', p[1], p[3])
# fin Nahin


# Juan, hashes
def p_valor_hash(p):
    '''valor : LLAVE_IZQ lista_pares LLAVE_DER
             | LLAVE_IZQ LLAVE_DER'''
    p[0] = ('hash', p[2] if len(p) == 4 else [])

def p_lista_pares(p):
    '''lista_pares : lista_pares COMA par
                   | par'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

# acepta "clave" => valor y tambien clave: valor
def p_par(p):
    '''par : expresion FLECHA_HASH expresion
           | ID DOS_PUNTOS expresion'''
    p[0] = ('par', p[1], p[3])
# fin Juan

#Inicio Isa funciones con return
def p_sentencia_funcion(p):
    "sentencia : definicion_funcion"
    p[0] = p[1]

#en nuestra implementacion la funcion siempre lleva parentesis aunque no tenga parametros
def p_definicion_funcion(p):
    '''definicion_funcion : DEF ID PAREN_IZQ lista_parametros PAREN_DER lista_sentencias END
                          | DEF ID PAREN_IZQ PAREN_DER lista_sentencias END'''
    if len(p) == 8:
        p[0] = ('funcion', p[2], p[4], p[6])
    else:
        p[0] = ('funcion', p[2], [], p[5])

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA parametro
                        | parametro'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parametro(p):
    "parametro : ID"
    p[0] = ('parametro', p[1])

#un ejemplo puede ser return base * altura
def p_sentencia_return(p):
    "sentencia : RETURN expresion"
    p[0] = ('return', p[2])

# Llamada a funciones con argumentos y sin
def p_valor_llamada_funcion(p):
    '''valor : ID PAREN_IZQ lista_expresiones PAREN_DER
             | ID PAREN_IZQ PAREN_DER'''
    if len(p) == 5:
        p[0] = ('llamada', p[1], p[3])
    else:
        p[0] = ('llamada', p[1], [])
# Fin Isa


# Nahin, Manejo de errores sintácticos
errores_sintacticos = []

def p_error(p):
    if p:
        msj = f"Error sintáctico [línea {p.lineno}]: token inesperado '{p.value}' (tipo: {p.type})"
    else:
        msj = "Error sintáctico: fin de archivo inesperado (posible falta de 'end')"
    errores_sintacticos.append(msj)

# debug y write_tables en False para que no se creen parser.out ni parsetab.py
parser = yacc.yacc(debug=False, write_tables=False)

def parsear(codigo):
    errores_sintacticos.clear()
    lexer.lexer.lineno = 1
    resultado = parser.parse(codigo, lexer=lexer.lexer)
    return resultado, errores_sintacticos