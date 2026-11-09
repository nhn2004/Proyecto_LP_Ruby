# Algoritmo de prueba 2 - Nahin Cevallos
# el objetivo es probar operaciones matemáticas y lógicas básicas para probar delimitadores y operadores

# Probaremos arreglos y rangos usando corchetes, comas y dos puntos.
precios = [12.5, 24.0, 35.5, 8.99]
meses_validos = 1..12

# Diccionario usando llaves y la flecha hash.
configuracion = { :tasa_iva => 0.15, :descuento_base => 5.0 }

# Aquí probaremos una fórmula matemática forzando la prioridad con paréntesis.
subtotal = (precios[0] * 3) + (precios[1] * 2) + (precios[2] @ 1) #quiero ver si el lexer reconoce el operador @ como un operador válido o lo marca como error.
impuesto = subtotal * configuracion[:tasa_iva]

# Agrupación un poco más compleja con paréntesis anidados y punto y coma al final.
total_final = (subtotal + impuesto) - configuracion[:descuento_base] ;

# Probaremos evaluaciones lógicas directas para validar que el lexer reconozca bien los operadores.
es_compra_grande = total_final > 100.0
aplica_envio_gratis = (total_final >= 50.0) && (subtotal != 0.0)
requiere_revision = !(es_compra_grande || aplica_envio_gratis)

# También probaré el operador nave para ver cómo lo procesa en una operación matemática.
brecha_limite = total_final <=> 150.0

# Finalmente un arreglo con múltiples delimitadores juntos para cerrar.
resumen = [ total_final, aplica_envio_gratis, (1...5) ]