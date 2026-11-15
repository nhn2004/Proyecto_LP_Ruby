=begin
Cuenta cuantos numeros pares e impares hay en un arreglo
=end

numeros = [3, 8, 15, 22, 7]
pares, impares = 0, 0

def es_par(n)
  return n % 2 == 0
end

i = 0
while i < numeros.length
  if es_par(numeros[i])
    pares += 1
  else
    impares += 1
  end
  i += 1
end

print "Pares: ", pares, " Impares: ", impares
