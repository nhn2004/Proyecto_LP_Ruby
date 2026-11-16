# Algoritmo de prueba semantico 1 de Juan
# Factura de una tienda, prueba la regla de operaciones permitidas:
# solo se opera entre numeros, un String solo se suma con String y se multiplica por Integer

IVA = 0.15
productos = { "cuaderno" => 2.5, "lapiz" => 0.75 }
cantidad = 4
precio = 2.5

subtotal = cantidad * precio
impuesto = subtotal * IVA
total = subtotal + impuesto
separador = "-" * 20

puts separador
puts "Factura de la tienda"
print "Productos: ", productos

# errores a proposito
etiqueta = "Total: " + 20
descuento = 3 * "%"
envio = true + 1.5
saldo = -"pendiente"

puts separador
