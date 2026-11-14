"""Analizador Sintáctico (Parser) con PLY yacc para Ruby - Grupo 2"""

import ply.yacc as yacc
import lexer

tokens = lexer.tokens



# Aporte Nahin, Base del parser
def p_programa(p):
    '''programa : lista_sentencias
                | empty'''
    p[0] = ('programa', p[1])

def p_lista_sentencias_multi(p):
    '''lista_sentencias : lista_sentencias sentencia'''
    p[0] = p[1] + [p[2]]

def p_lista_sentencias_single(p):
    '''lista_sentencias : sentencia'''
    p[0] = [p[1]]

def p_sentencia(p):
    '''sentencia : expresion'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = []


# Estructura de control: if, while, case/when 
def p_estructura_control_case(p):
    '''estructura_control_case : CASE expresion lista_when else_opt END'''
    p[0] = ('case', p[2], p[3], p[4])

def p_lista_when(p):
    '''lista_when : lista_when bloque_when
                  | bloque_when'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_bloque_when(p):
    '''bloque_when : WHEN lista_expresiones THEN lista_sentencias
                   | WHEN lista_expresiones lista_sentencias'''
    if len(p) == 5:
        p[0] = ('when', p[2], p[4])
    else:
        p[0] = ('when', p[2], p[3])

def p_else_opt(p):
    '''else_opt : ELSE lista_sentencias
                | empty'''
    p[0] = ('else', p[2]) if len(p) == 3 else []


# Regla para definir una función lambda con la flecha ->
def p_funcion_lambda(p):
    '''funcion_lambda : LAMBDA_FLECHA PAREN_IZQ parametros_lambda_opt PAREN_DER LLAVE_IZQ lista_sentencias LLAVE_DER
                      | LAMBDA_FLECHA LLAVE_IZQ lista_sentencias LLAVE_DER'''
    if len(p) == 8:
        p[0] = ('lambda', p[3], p[6])
    else:
        p[0] = ('lambda', [], p[3])

def p_parametros_lambda_opt(p):
    '''parametros_lambda_opt : lista_parametros_lambda
                             | empty'''
    p[0] = p[1]

def p_lista_parametros_lambda(p):
    '''lista_parametros_lambda : lista_parametros_lambda COMA ID
                               | ID'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


# Rangos inclusivos y exclusivos
def p_rango_expresion(p):
    '''rango_expresion : aritmetica RANGO_INCLUSIVO aritmetica
                       | aritmetica RANGO_EXCLUSIVO aritmetica
                       | aritmetica'''
    if len(p) == 4:
        p[0] = ('rango', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# Expresiones lógicas y comparaciones
def p_expresion(p):
    '''expresion : expresion OR_LOGICO expresion_and
                 | expresion OR expresion_and
                 | expresion_and'''
    p[0] = ('logica', p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_expresion_and(p):
    '''expresion_and : expresion_and AND_LOGICO expresion_comp
                     | expresion_and AND expresion_comp
                     | expresion_comp'''
    p[0] = ('logica', p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_expresion_comp(p):
    '''expresion_comp : rango_expresion IGUAL_IGUAL rango_expresion
                      | rango_expresion DISTINTO rango_expresion
                      | rango_expresion MENOR rango_expresion
                      | rango_expresion MAYOR rango_expresion
                      | rango_expresion MENOR_IGUAL rango_expresion
                      | rango_expresion MAYOR_IGUAL rango_expresion
                      | rango_expresion IGUAL_CASO rango_expresion
                      | rango_expresion NAVE rango_expresion
                      | rango_expresion'''
    p[0] = ('comparacion', p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


# Expresiones aritméticas y unarias
def p_aritmetica(p):
    '''aritmetica : unario'''
    p[0] = p[1]

def p_unario(p):
    '''unario : NOT_LOGICO unario
              | NOT unario
              | postfijo'''
    if len(p) == 3:
        p[0] = ('unario', p[1], p[2])
    else:
        p[0] = p[1]


def p_postfijo(p):
    '''postfijo : postfijo PUNTO nombre_metodo PAREN_IZQ argumentos_opt PAREN_DER
                | postfijo PUNTO nombre_metodo
                | primario'''
    if len(p) == 7:
        p[0] = ('llamada', p[1], p[3], p[5])
    elif len(p) == 4:
        p[0] = ('llamada', p[1], p[3], [])
    else:
        p[0] = p[1]

def p_nombre_metodo(p):
    '''nombre_metodo : ID
                     | CONSTANTE'''
    p[0] = p[1]

if 'CHOMP' in tokens:
    p_nombre_metodo.__doc__ += '\n                     | CHOMP'

def p_argumentos_opt(p):
    '''argumentos_opt : lista_expresiones
                      | empty'''
    p[0] = p[1]


def p_primario(p):
    '''primario : ENTERO
                | FLOTANTE
                | CADENA
                | SIMBOLO
                | TRUE
                | FALSE
                | NIL
                | ID
                | CONSTANTE
                | VAR_INSTANCIA
                | VAR_CLASE
                | VAR_GLOBAL
                | GETS
                | estructura_control_case
                | funcion_lambda
                | PAREN_IZQ expresion PAREN_DER'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]



# Manejo de errores sintácticos
errores_sintacticos = []

def p_error(p):
    if p:
        msj = f"Error sintáctico [línea {p.lineno}]: token inesperado '{p.value}' (tipo: {p.type})"
    else:
        msj = (f"Error sintáctico [línea {lexer.lexer.lineno}]: "
               "fin de archivo inesperado (posible falta de 'end' o '}')")
    errores_sintacticos.append(msj)


class LexerSinComentarios:
    """Envuelve al lexer y salta los comentarios, que no tienen regla sintáctica."""
    def __init__(self, base):
        self.base = base

    def input(self, codigo):
        self.base.input(codigo)

    def token(self):
        tok = self.base.token()
        while tok and tok.type in ("COMENTARIO", "COMENTARIO_MULTILINEA"):
            tok = self.base.token()
        return tok


parser = yacc.yacc(debug=False, write_tables=False)

def parsear(codigo):
    """Devuelve (arbol, errores). Los errores son cadenas con el formato
    'Error sintáctico [línea N]: ...', igual que los del léxico."""
    errores_sintacticos.clear()
    lexer.lexer.lineno = 1
    resultado = parser.parse(codigo, lexer=LexerSinComentarios(lexer.lexer))
    return resultado, list(errores_sintacticos)
