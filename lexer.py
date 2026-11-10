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
    '__ENCODING__': 'ENCODING',
    'puts': 'PUTS',   
    'print': 'PRINT',
    'gets': 'GETS'
}

tokens_isabella = ('ID', 'CONSTANTE', 'VAR_CLASE', 'VAR_INSTANCIA', 'VAR_GLOBAL')

def t_ID(t):
    #primer caracter debe ser letra minuscula o guion bajo y después cualquier combinación de letras, dígitos o guiones bajos y opcional al final ? o !
    r'[a-z_]\w*[?!]?'
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    else:
        t.type = 'ID'
    return t

def t_CONSTANTE(t):
    # primer caracter es mayuscula y el resto pueden ser letras, dígitos o guiones bajos
    r'[A-Z]\w*'
    if t.value not in palabras_reservadas:
        t.type = 'CONSTANTE'
    else:
        t.type = palabras_reservadas[t.value]
    return t

def t_VAR_CLASE(t):
    # primer caracter @@ y luego letra o guion bajo y demas letras, digitos o guiones bajos.
    r'@@[_a-zA-Z]\w*'
    t.type = 'VAR_CLASE'
    return t

def t_VAR_INSTANCIA(t):
    #un @ y luego letra o guion bajo y despues demas letras, digitos o guiones bajos
    r'@[_a-zA-Z]\w*'
    t.type = 'VAR_INSTANCIA'
    return t

def t_VAR_GLOBAL(t):
    # primero $ y luego letra o guion bajo y despues letras, digitos o guiones bajos
    r'\$[_a-zA-Z]\w*'
    t.type = 'VAR_GLOBAL'
    return t

def t_VARIABLE_INVALIDA(t):
    # @ @@ o $ seguido de un numero no es un nombre valido en Ruby
    r'(@@|@|\$)[0-9]\w*'
    errores_lexicos.append(f"Error léxico [línea {t.lexer.lineno}]: nombre de variable inválido '{t.value}', no puede empezar con un número")

def t_COMENTARIO(t):
    # un comentario inicia con # y puede ir cualquier caracter excepto un salto de línea
    r'\#[^\n]*'

def t_COMENTARIO_MULTILINEA(t):
    # inicia con =begin y termina con =end y puede ir cualquier caracter entre ellos y lo hice para que sea lo menos codicioso posible para que tome el primer =end que encuentre (con *?)   
    r'=begin(.|\n)*?=end'
    t.lexer.lineno += t.value.count('\n')

# JUAN
# Responsabilidades: literales numericos, cadenas, simbolos y operadores aritmeticos y de asignacion

tokens_juan = (
    'FLOTANTE', 'ENTERO', 'CADENA', 'SIMBOLO',
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'MODULO', 'POTENCIA',
    'IGUAL', 'MAS_IGUAL', 'MENOS_IGUAL', 'POR_IGUAL', 'DIVIDIDO_IGUAL',
    'MODULO_IGUAL', 'POTENCIA_IGUAL', 'OR_IGUAL', 'AND_IGUAL'
)

def t_FLOTANTE(t):
    # numeros con punto decimal y exponente opcional ej 3.14 o 1.2e3
    # va antes de ENTERO para que no lo corte en el punto
    r'\d[\d_]*\.\d[\d_]*([eE][+-]?\d+)?'
    return t

def t_ENTERO(t):
    # hexadecimal (0x1F), binario (0b1010) o decimal que puede tener _ (1_000_000)
    r'0[xX][0-9a-fA-F]+|0[bB][01]+|\d[\d_]*'
    return t

def t_CADENA(t):
    # cadena con comillas dobles o simples, se aceptan escapes como \" adentro
    r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''
    t.lexer.lineno += t.value.count('\n')
    return t

def t_SIMBOLO(t):
    # dos puntos seguido del nombre ej :nombre, no choca con :: porque despues del : tiene que venir letra
    r':[a-zA-Z_]\w*[?!]?'
    return t

# operadores aritmeticos
t_POTENCIA = r'\*\*'
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'

# operadores de asignacion
# ply ordena estos por largo de la expresion asi que **= va antes que ** y ||= antes que ||
t_POTENCIA_IGUAL = r'\*\*='
t_MAS_IGUAL = r'\+='
t_MENOS_IGUAL = r'-='
t_POR_IGUAL = r'\*='
t_DIVIDIDO_IGUAL = r'/='
t_MODULO_IGUAL = r'%='
t_OR_IGUAL = r'\|\|='
t_AND_IGUAL = r'&&='
t_IGUAL = r'='


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

# Aqui queremos definir los tokens que tienen más de un caracter y que pueden ser confundidos con otros tokens más cortos. Para que '===' sea reconocido antes que '==' y '==' en ese orden especifico como definimos las funciones.
def t_IGUAL_CASO(t):
    r'==='
    return t

def t_IGUAL_IGUAL(t):
    r'=='
    return t

def t_NAVE(t):
    r'<=>'
    return t

def t_MENOR_IGUAL(t):
    r'<='
    return t

def t_MAYOR_IGUAL(t):
    r'>='
    return t

# Lo mismo con los rangos.
def t_RANGO_EXCLUSIVO(t):
    r'\.\.\.'
    return t

def t_RANGO_INCLUSIVO(t):
    r'\.\.'
    return t

def t_LAMBDA_FLECHA(t):
    r'->'
    return t

def t_DOBLE_DOS_PUNTOS(t):
    r'::'
    return t

t_DISTINTO = r'!='
t_MENOR = r'<'
t_MAYOR = r'>'
t_AND_LOGICO = r'&&'
t_OR_LOGICO = r'\|\|'
t_NOT_LOGICO = r'!'
t_FLECHA_HASH = r'=>'

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

# Para el manejo de errores, contar el salto de linea  ver en que linea estamos y agregarlo a la lista de errores lexicos.
def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'
errores_lexicos = []

def t_error(t):
    caracter = t.value[0]
    if caracter.isspace():
        t.lexer.skip(1)
        return
        
    msj = f"Error léxico [línea {t.lexer.lineno}]: carácter no reconocido '{caracter}'"
    errores_lexicos.append(msj)
    t.lexer.skip(1)

# fin

tokens = tuple(list(tokens_nahin) + list(palabras_reservadas.values()) + list(tokens_isabella) + list(tokens_juan))

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