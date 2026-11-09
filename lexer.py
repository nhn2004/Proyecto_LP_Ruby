import ply.lex as lex

# Contribución Isabella
# Responsabilidades: variables, palabras reservadas y comentarios
palabras_reservadas = {
    'if': 'IF',
    'elsif': 'ELSIF',
    'else': 'ELSE',
    'unless': 'UNLESS',
    'then': 'THEN',
    'case': 'CASE',
    'when': 'WHEN',
    'in': 'IN',
    'while': 'WHILE',
    'until': 'UNTIL',
    'for': 'FOR',
    'do': 'DO',
    'break': 'BREAK',
    'next': 'NEXT',
    'redo': 'REDO',
    'retry': 'RETRY',
    'def': 'DEF',
    'return': 'RETURN',
    'yield': 'YIELD',
    'class': 'CLASS',
    'module': 'MODULE',
    'self': 'SELF',
    'super': 'SUPER',
    'begin': 'BEGIN',
    'rescue': 'RESCUE',
    'ensure': 'ENSURE',
    'end': 'END',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE',
    'nil': 'NIL',
    'alias': 'ALIAS',
    'undef': 'UNDEF',
    'defined?': 'DEFINED',
    'BEGIN': 'BEGIN_BLOCK',
    'END': 'END_BLOCK',
    '__FILE__': 'FILE',
    '__LINE__': 'LINE',
    '__ENCODING__': 'ENCODING'
}


# JUAN
# Responsabilidades: literales numéricos, cadenas y operadores aritméticos.

def t_NUMERO_TEMPORAL(t):
    r'\d+(\.\d+)?'
    t.type = 'NUMERO_TEMPORAL'
    return t

def t_CADENA_TEMPORAL(t):
    r'(".*?")|(\'.*?\')'
    t.type = 'CADENA_TEMPORAL'
    return t


# Nahin Cevallos
# Responsabilidades: Operadores lógicos, comparación, delimitadores y manejo de errores.


tokens_nahin = (
    'IGUAL_CASO', 'IGUAL_IGUAL', 'DISTINTO', 'NAVE',
    'MENOR_IGUAL', 'MAYOR_IGUAL', 'MENOR', 'MAYOR',
    'AND_LOGICO', 'OR_LOGICO', 'NOT_LOGICO',
    'RANGO_EXCLUSIVO', 'RANGO_INCLUSIVO', 'DOBLE_DOS_PUNTOS',
    'FLECHA_HASH', 'LAMBDA_FLECHA',
    'PAREN_IZQ', 'PAREN_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'COMA', 'PUNTO_COMA', 'PUNTO', 'DOS_PUNTOS'
)

t_IGUAL_CASO = r'==='
t_IGUAL_IGUAL = r'=='
t_DISTINTO = r'!='
t_NAVE = r'<=>'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MENOR = r'<'
t_MAYOR = r'>'

t_AND_LOGICO = r'&&'
t_OR_LOGICO = r'\|\|'
t_NOT_LOGICO = r'!'

t_RANGO_EXCLUSIVO = r'\.\.\.'
t_RANGO_INCLUSIVO = r'\.\.'
t_DOBLE_DOS_PUNTOS = r'::'
t_FLECHA_HASH = r'=>'
t_LAMBDA_FLECHA = r'->'

t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_COMA = r','
t_PUNTO_COMA = r';'
t_PUNTO = r'\.'
t_DOS_PUNTOS = r':'

def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'
errores_lexicos = []

def t_error(t):
    msj = f"Error léxico [línea {t.lexer.lineno}]: carácter no reconocido '{t.value[0]}'"
    errores_lexicos.append(msj)
    t.lexer.skip(1)

# fin

tokens = tuple(list(tokens_nahin) + ['ID_TEMPORAL', 'NUMERO_TEMPORAL', 'CADENA_TEMPORAL'])

lexer = lex.lex()

# Función puente para que otros archivos usen el lexer
def tokenizar(codigo):
    global errores_lexicos
    errores_lexicos.clear()
    lexer.lineno = 1
    lexer.input(codigo)
    
    tokens_generados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_generados.append(tok)
        
    return tokens_generados, errores_lexicos