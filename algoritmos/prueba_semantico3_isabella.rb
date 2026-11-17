#Cuenta cuantas notas son mayores al promedio
MINIMO = 7
notas = [8, 6.5, 9, 7]

def promedio(lista)
  suma = 0
  i = 0
  while i < lista.length
    suma += lista[i]
    i += 1
  end
  return suma / lista.length
end
prom = promedio(notas)
mayores = 0
i = 0
while i < notas.length
  if notas[i] > prom
    mayores += 1
  end
  i += 1
end
if prom >= MINIMO
  puts "Aprobado con ", prom
else
  puts "Reprobado con ", prom
end
puts "Notas sobre el promedio: ", mayores