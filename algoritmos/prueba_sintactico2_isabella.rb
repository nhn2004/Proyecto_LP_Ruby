#Prueba isabella sintáctico
=begin
Revisa la asistencia de un estudiante y dice si puede dar el examen
=end

asistencias = [true, true, false, true, true]
MINIMO = 70

def porcentaje(lista)
  presentes = 0
  i = 0
  while i < lista.length
    if lista[i]
      presentes += 1
    end
    i += 1
  end
  return presentes * 100 / lista.length
end
total = porcentaje(asistencias)
if total >= 90
  puts "Asistencia perfecta"
elsif total >= MINIMO
  puts "Puede dar el examen", total
else
  puts "No puede dar el examen"
end

#error sintactico a proposito falta la coma en el arreglo
faltas = [false true]
