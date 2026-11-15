puts "Ingresa tu nombre"
nombre = gets.chomp
puts "Ingresa tu edad"
edad = gets.chomp.to_i
puts "Ingresa tu nota"
nota = gets.chomp.to_f
asistencia = 0.85
requiere_permiso = false
aprobado = nota >= 7 && asistencia > 0.7
puede_entrar = edad >= 18 || !requiere_permiso
mayor = edad > 17
igual = edad == 18
distinto = nombre != "Ana"
vacio = false
activo = true
valido = not vacio and activo
if aprobado and puede_entrar
  puts "Bienvenido ", nombre
else
  puts "Acceso denegado"
end
