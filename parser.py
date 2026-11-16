import re
import ply.yacc as yacc
import lexer

tokens = lexer.tokens


# Nahin, base del parser 
def p_programa(p):
    "programa : lista_sentencias"
    # las reglas de break next y llamadas se revisan al final con todo el programa
    revisar_programa(p[1], False)
    revisar_llamadas()
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
    if p.slice[1].type == 'ID':
        revisar_variable_asignada(p[1], p.lineno(1))
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
    # guardo tambien el tipo de token para saber el tipo del valor en el semantico
    p[0] = ('literal', p[1], p.slice[1].type)

def p_expresion_suma(p):
    '''expresion_suma : expresion_suma SUMA expresion_producto
                      | expresion_suma RESTA expresion_producto'''
    revisar_operacion(p[2], p[1], p[3], p.lineno(2))
    p[0] = ('aritmetica', p[2], p[1], p[3])

def p_expresion_producto(p):
    '''expresion_producto : expresion_producto MULTIPLICACION expresion_unaria
                          | expresion_producto DIVISION expresion_unaria
                          | expresion_producto MODULO expresion_unaria'''
    revisar_operacion(p[2], p[1], p[3], p.lineno(2))
    p[0] = ('aritmetica', p[2], p[1], p[3])

# menos unario ej -5
def p_expresion_unaria(p):
    "expresion_unaria : RESTA expresion_unaria"
    revisar_unario(p[2], p.lineno(1))
    p[0] = ('unario', p[1], p[2])

# la potencia se agrupa por la derecha ej 2 ** 3 ** 2 es 2 ** 9
def p_expresion_potencia(p):
    "expresion_potencia : expresion_negacion POTENCIA expresion_unaria"
    revisar_operacion(p[2], p[1], p[3], p.lineno(2))
    p[0] = ('aritmetica', p[2], p[1], p[3])
# fin Juan


# INICIO Isa, asignacion e impresion
def p_sentencia_asignacion(p):
    "sentencia : asignacion"
    revisar_constante(p[1], p.lineno(1))
    registrar_asignacion(p[1], p.lineno(1))
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
    #por ejemplo contador += 1 usa contador asi que tuvo que asignarse antes. 
    if (p[1][0].islower() or p[1][0] == '_') and p[2] not in ('||=', '&&='):#con ||= y &&= no importa revisar asignación porque esos crean la variable si no existe
        revisar_variable_asignada(p[1], p.lineno(1))
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

# asignar en una posicion de un hash o arreglo ej config[:minimo] = 5 o notas[0] += 1
def p_asignacion_indice(p):
    '''asignacion : valor CORCHETE_IZQ expresion CORCHETE_DER IGUAL expresion
                  | valor CORCHETE_IZQ expresion CORCHETE_DER MAS_IGUAL expresion
                  | valor CORCHETE_IZQ expresion CORCHETE_DER MENOS_IGUAL expresion'''
    p[0] = ('asignacion_indice', p[5], p[1], p[3], p[6])
# fin Juan

#Inicio Isa funciones con return
def p_sentencia_funcion(p):
    "sentencia : definicion_funcion"
    p[0] = p[1]

#en nuestra implementacion la funcion siempre lleva parentesis aunque no tenga parametros
def p_definicion_funcion(p):
    '''definicion_funcion : inicio_funcion PAREN_IZQ lista_parametros PAREN_DER lista_sentencias END
                          | inicio_funcion PAREN_IZQ PAREN_DER lista_sentencias END'''
    ambitos.pop() #hago pop porque al terminar la funcion se cierra su alcance
    if len(p) == 7:
        p[0] = ('funcion', p[1], p[3], p[5])
    else:
        p[0] = ('funcion', p[1], [], p[4])

def p_inicio_funcion(p):
    "inicio_funcion : DEF ID"
    ambitos.append({})#el def crea alcance nuevo antes de leer params
    nombres_funciones.add(p[2])
    p[0] = p[2]

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA parametro
                        | parametro'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_parametro(p):
    "parametro : ID"
    registrar_variable(p[1], None, p.lineno(1))
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
    llamadas.append((p[1], len(p[0][2]), p.lineno(1)))
# Fin Isa


# Nahin, lambdas
def p_valor_lambda(p):
    '''valor : LAMBDA_FLECHA PAREN_IZQ lista_parametros PAREN_DER LLAVE_IZQ lista_sentencias LLAVE_DER
             | LAMBDA_FLECHA LLAVE_IZQ lista_sentencias LLAVE_DER'''
    if len(p) == 8:
        p[0] = ('lambda', p[3], p[6])
    else:
        p[0] = ('lambda', [], p[3])
# fin Nahin


# Juan, clases y parametros opcionales
def p_sentencia_clase(p):
    "sentencia : definicion_clase"
    p[0] = p[1]

# los metodos van con def y las propiedades son las @variables
def p_definicion_clase(p):
    '''definicion_clase : CLASS CONSTANTE lista_sentencias END
                        | CLASS CONSTANTE END'''
    p[0] = ('clase', p[2], p[3] if len(p) == 5 else [])

# variable de clase que comparten todos los objetos ej @@total = 0
def p_asignacion_variable_clase(p):
    "asignacion : VAR_CLASE IGUAL expresion"
    p[0] = ('asignacion', p[1], p[3])

# parametro con valor por defecto ej saludo = "Hola"
def p_parametro_opcional(p):
    "parametro : ID IGUAL expresion"
    registrar_variable(p[1], tipo_de(p[3]), p.lineno(1))
    p[0] = ('parametro_opcional', p[1], p[3])
# fin Juan


# Juan, base del analizador semantico
# las reglas semanticas se revisan mientras yacc va reduciendo las reglas del parser
errores_semanticos = []

# tabla de simbolos, ambitos es una pila de alcances y el primero es el del programa
# cada variable guarda su tipo y la linea donde se asigno
ambitos = [{}]
# las constantes van aparte porque se pueden usar desde cualquier alcance
constantes = {}

NUMERICOS = ('Integer', 'Float')

TIPOS_LITERAL = {
    'ENTERO': 'Integer',
    'FLOTANTE': 'Float',
    'CADENA': 'String',
    'SIMBOLO': 'Symbol',
    'TRUE': 'Boolean',
    'FALSE': 'Boolean',
    'NIL': 'NilClass',
}

# metodos que convierten a otro tipo ej edad.to_i
CONVERSIONES = {'to_i': 'Integer', 'to_f': 'Float', 'to_s': 'String'}

# el mensaje lleva la categoria de la regla ej Error semántico [Conversión, línea 4]: ...
def error_semantico(categoria, linea, mensaje):
    errores_semanticos.append(f"Error semántico [{categoria}, línea {linea}]: {mensaje}")

def registrar_variable(nombre, tipo, linea):
    if nombre[0].isupper():
        constantes[nombre] = {'tipo': tipo, 'linea': linea}
    else:
        ambitos[-1][nombre] = {'tipo': tipo, 'linea': linea}

# solo se busca en el alcance actual porque en ruby un def no ve las variables de afuera
def buscar_variable(nombre):
    if nombre[0].isupper():
        return constantes.get(nombre)
    return ambitos[-1].get(nombre)

def registrar_asignacion(nodo, linea):
    if nodo[0] == 'asignacion':
        registrar_variable(nodo[1], tipo_de(nodo[2]), linea)
    elif nodo[0] == 'asignacion_multiple':
        # primero saco todos los tipos para que x, y = y, x funcione bien
        tipos = [tipo_de(valor) for valor in nodo[2]]
        for i, nombre in enumerate(nodo[1]):
            registrar_variable(nombre, tipos[i] if i < len(tipos) else None, linea)
    elif nodo[0] == 'asignacion_compuesta':
        # ej total += 1.5 es como total = total + 1.5
        operador = nodo[1][:-1]
        tipo = tipo_de(('aritmetica', operador, ('variable', nodo[2]), nodo[3]))
        registrar_variable(nodo[2], tipo, linea)

# devuelve el tipo de un nodo y None si no se puede saber, en ese caso no se reporta error
def tipo_de(nodo):
    if not isinstance(nodo, tuple):
        return None
    clase = nodo[0]
    if clase == 'literal':
        return TIPOS_LITERAL.get(nodo[2])
    if clase == 'variable':
        simbolo = buscar_variable(nodo[1])
        return simbolo['tipo'] if simbolo else None
    if clase == 'aritmetica':
        return tipo_resultado(nodo[1], tipo_de(nodo[2]), tipo_de(nodo[3]))
    if clase == 'unario':
        tipo = tipo_de(nodo[2])
        return tipo if tipo in NUMERICOS else None
    if clase in ('comparacion', 'negacion'):
        return 'Boolean'
    if clase == 'entrada':
        return 'String'
    if clase == 'arreglo':
        return 'Array'
    if clase == 'hash':
        return 'Hash'
    if clase == 'rango':
        return 'Range'
    if clase == 'lambda':
        return 'Proc'
    if clase == 'llamada_metodo':
        metodo = nodo[2]
        if metodo in CONVERSIONES:
            return CONVERSIONES[metodo]
        if metodo in ('length', 'size', 'count'):
            return 'Integer'
        # ej gets.chomp sigue siendo String
        if metodo in ('chomp', 'strip', 'upcase', 'downcase', 'capitalize'):
            return 'String' if tipo_de(nodo[1]) == 'String' else None
    return None

def numero_de_linea(mensaje):
    encontrado = re.search(r"línea (\d+)", mensaje)
    return int(encontrado.group(1)) if encontrado else 0
# fin Juan


# Juan, reglas semanticas de operaciones y conversion
VERBOS = {
    '+': 'sumar',
    '-': 'restar',
    '*': 'multiplicar',
    '/': 'dividir',
    '%': 'sacar el módulo de',
    '**': 'elevar',
}

# tipo que da una operacion, None si la operacion no se permite
def tipo_resultado(operador, tipo_izq, tipo_der):
    if tipo_izq in NUMERICOS and tipo_der in NUMERICOS:
        # regla 4 coercion entre Integer y Float, si uno es Float el resultado es Float
        return 'Float' if 'Float' in (tipo_izq, tipo_der) else 'Integer'
    # un String o un Array solo se suma con otro igual ej "Hola " + nombre
    if operador == '+' and tipo_izq == tipo_der and tipo_izq in ('String', 'Array'):
        return tipo_izq
    # y solo se multiplica por un Integer ej "-" * 10
    if operador == '*' and tipo_izq in ('String', 'Array') and tipo_der == 'Integer':
        return tipo_izq
    return None

def revisar_operacion(operador, izq, der, linea):
    tipo_izq = tipo_de(izq)
    tipo_der = tipo_de(der)
    # si no se sabe el tipo de alguno no se reporta nada
    if tipo_izq is None or tipo_der is None:
        return
    if tipo_resultado(operador, tipo_izq, tipo_der):
        return
    # regla 4 un String con un numero necesita conversion explicita ej edad.to_i
    if 'String' in (tipo_izq, tipo_der) and (tipo_izq in NUMERICOS or tipo_der in NUMERICOS):
        cadena, numero = (izq, der) if tipo_izq == 'String' else (der, izq)
        if cadena[0] == 'variable':
            nombre = cadena[1]
            error_semantico("Conversión", linea, f"'{nombre}' es String; use {nombre}.to_i o {nombre}.to_f antes de operar.")
            return
        if numero[0] == 'variable' and operador == '+':
            nombre = numero[1]
            error_semantico("Conversión", linea, f"'{nombre}' es {tipo_de(numero)}; use {nombre}.to_s antes de concatenar.")
            return
    # regla 3 las operaciones aritmeticas solo se permiten entre numeros
    error_semantico("Operaciones permitidas", linea, f"no se puede {VERBOS[operador]} {tipo_izq} con {tipo_der}.")

# el menos unario solo se usa con numeros ej -"hola" no se permite
def revisar_unario(nodo, linea):
    tipo = tipo_de(nodo)
    if tipo is not None and tipo not in NUMERICOS:
        error_semantico("Operaciones permitidas", linea, f"no se puede aplicar el menos unario a {tipo}.")
# fin Juan

#Parte de Isabella reglas semanticas de variables y constantes
nombres_funciones = set()
def revisar_variable_asignada(nombre, linea): #var solo se puede usar si se asigno antes y en el mismo alcance
    if buscar_variable(nombre) is None and nombre not in nombres_funciones:
        error_semantico("Identificadores", linea, f"la variable '{nombre}' se usa antes de ser asignada.")

#constante no se puede reasignar (lo vamos a manejar como error)
def revisar_constante(nodo, linea):
    if nodo[0] == 'asignacion' and nodo[1][0].isupper():
        anterior = constantes.get(nodo[1])
        if anterior:
            error_semantico("Asignación de tipo", linea, f"la constante '{nodo[1]}' ya fue definida en la línea {anterior['linea']} y no puede reasignarse.")
#Fin Isa

# Nahin, break next y case en asignacion
# guardo la linea para revisar despues si esta dentro de un while
def p_sentencia_break_next(p):
    '''sentencia : BREAK
                 | NEXT'''
    p[0] = (p[1], p.lineno(1))

# ej tipo = case edad when ... end
def p_asignacion_case(p):
    "asignacion : ID IGUAL sentencia_case"
    p[0] = ('asignacion', p[1], p[3])
# fin Nahin

# Nahin, reglas semanticas de break next y llamadas a funciones
# nombre de la funcion con cuantos parametros obligatorios y en total tiene
funciones = {}
# llamadas encontradas con el nombre, cuantos argumentos tienen y la linea
llamadas = []

# recorre el arbol al final porque el cuerpo del while se reduce antes que el while
def revisar_programa(nodo, dentro_while):
    if isinstance(nodo, list):
        for hijo in nodo:
            revisar_programa(hijo, dentro_while)
        return
    if not isinstance(nodo, tuple) or not nodo:
        return
    # regla 5 break y next solo pueden ir dentro de un while
    if nodo[0] in ('break', 'next'):
        if not dentro_while:
            error_semantico("Estructuras de control", nodo[1], f"'{nodo[0]}' solo puede usarse dentro de un bucle while.")
        return
    if nodo[0] == 'while':
        dentro_while = True
    elif nodo[0] in ('funcion', 'lambda', 'clase'):
        dentro_while = False
    if nodo[0] == 'funcion':
        parametros = nodo[2]
        obligatorios = len([par for par in parametros if par[0] == 'parametro'])
        funciones[nodo[1]] = (obligatorios, len(parametros))
    for hijo in nodo[1:]:
        revisar_programa(hijo, dentro_while)

# regla 6 la funcion tiene que estar definida y recibir los argumentos que pide
def revisar_llamadas():
    for nombre, cantidad, linea in llamadas:
        if nombre not in funciones:
            error_semantico("Identificadores", linea, f"la función '{nombre}' no ha sido definida.")
            continue
        obligatorios, total = funciones[nombre]
        if cantidad < obligatorios or cantidad > total:
            esperados = obligatorios if obligatorios == total else f"entre {obligatorios} y {total}"
            error_semantico("Identificadores", linea, f"'{nombre}' espera {esperados} argumentos y recibió {cantidad}.")
# fin Nahin

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
    # se limpia la tabla de simbolos para que no queden datos del analisis anterior
    errores_semanticos.clear()
    del ambitos[1:]
    ambitos[0].clear()
    constantes.clear()
    funciones.clear()
    llamadas.clear()
    nombres_funciones.clear()
    lexer.lexer.lineno = 1
    # tracking para que p.lineno tambien de la linea de las reglas y no solo de los tokens
    resultado = parser.parse(codigo, lexer=lexer.lexer, tracking=True)
    # algunas reglas se revisan al final, por eso se ordenan por linea
    errores_semanticos.sort(key=numero_de_linea)
    return resultado, errores_sintacticos