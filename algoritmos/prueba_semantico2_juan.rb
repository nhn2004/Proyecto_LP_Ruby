# Algoritmo de prueba semantico 2 de Juan
# Calculo de la edad y el ahorro, prueba la regla de conversion:
# un String que viene de gets se convierte con to_i o to_f antes de operar

print "Ingrese su nombre: "
nombre = gets.chomp
print "Ingrese su edad: "
edad = gets.chomp
print "Ingrese su ahorro mensual: "
ahorro = gets.chomp.to_f

meses = 12
ahorro_anual = ahorro * meses
saludo = "Hola " + nombre

# errores a proposito: falta convertir
siguiente_edad = edad + 1
mitad = edad / 2
mensaje = "Meses ahorrando: " + meses

puts saludo
puts "Ahorro anual: ", ahorro_anual
