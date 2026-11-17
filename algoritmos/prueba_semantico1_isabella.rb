=begin
Saca el total de una compra
prueba la regla de variables usadas antes de ser asignadas
=end

precios = [2.5, 4, 1.25]

def sumar(lista)
  i = 0
  while i < lista.length
    suma += lista[i]
    i += 1
  end
  return suma
end

total = sumar(precios)
puts "Total: ", total, descuento
