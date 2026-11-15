=begin
Guarda las notas de una estudiante en un arreglo y saca el promedio y dice si aprobo
=end

NOTA_MIN = 7
nombre = "Ana"
notas = [8.5, 6, 9.75, 7]

def promedio(notas)
  suma = 0
  i = 0
  while i < notas.length
    suma += notas[i]
    i += 1
  end
  return suma / notas.length.to_f
end
def clasificar(prom)
  if prom >= 9
    return "Excelente"
  elsif prom >= NOTA_MIN
    return "Aprobado"
  else
    return "Reprobado"
  end
end

print "Ingrese una nota extra: "
extra = gets.chomp.to_f
if extra >= 0 && extra <= 10
  notas = notas + [extra]
end
prom = promedio(notas)
puts "Estudiante: " + nombre, "Promedio: #{prom}"
puts "Resultado: " + clasificar(prom)