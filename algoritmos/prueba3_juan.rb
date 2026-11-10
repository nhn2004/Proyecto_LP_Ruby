# Algoritmo de prueba 3 de Juan
# Calculadora de pagos de una compra, prueba los literales y todos
# los operadores aritmeticos y de asignacion

# literales numericos
cuotas = 12
monto = 1_500
recargo = 0.035
limite = 2.5e4
codigo_tienda = 0xFF
permisos = 0b0110

# cadenas y simbolos
cliente = 'Maria Perez'
nota = "Cliente \"frecuente\" con #{cuotas} cuotas"
estado = :pendiente
metodo = :tarjeta?

# operadores aritmeticos
interes = monto * recargo
total = monto + interes - 50
pago_mensual = total / cuotas
residuo = monto % cuotas
crecimiento = (1 + recargo) ** cuotas

# asignacion multiple y compuesta
pagado, saldo = 0, total
pagado += pago_mensual
saldo -= pago_mensual
saldo *= 1
saldo /= 1
residuo %= 5
crecimiento **= 2
descuento ||= 0
aprobado = true
aprobado &&= saldo < limite

puts "Cliente: " + cliente
puts nota
puts "Estado: #{estado}, metodo #{metodo}"
puts "Saldo pendiente: #{saldo.round(2)}"
