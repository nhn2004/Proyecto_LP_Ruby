"""Analizador sintactico (parser) con PLY yacc para Ruby - Grupo 2"""

import ply.yacc as yacc
import lexer

tokens = lexer.tokens


# Nahin, base del parser 
def p_programa(p):
    '''programa : lista_sentencias'''
    p[0] = ('programa', p[1])

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_sentencia_expresion(p):
    '''sentencia : expresion'''
    p[0] = p[1]

# niveles de las expresiones de menor a mayor prioridad segun la documentacion de Ruby
# por ahora cada nivel solo pasa al siguiente y cada integrante agrega sus operadores en su nivel
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
    '''valor : PAREN_IZQ expresion PAREN_DER'''
    p[0] = p[2]

def p_empty(p):
    '''empty :'''
    p[0] = []



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
