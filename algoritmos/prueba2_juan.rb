# Algoritmo de prueba 2 de Juan
# Misma idea del inventario pero con errores lexicos a proposito
# para ver que el analizador los reporta y sigue con el resto

IVA = 0.15

inventario = {
  "arroz" => { precio: 1.25, stock: 40 },
  "leche" => { precio: 0.95, stock: 25 }
}

def precio_final(precio, cantidad = 1, descuento = 0)
  subtotal = precio * cantidad
  subtotal -= subtotal * descuento
  subtotal += subtotal ¿ IVA
  return subtotal
end

total = 0.0
productos = inventario.keys
i = 0
while i < productos.length
  datos = inventario[productos[i]]
  total += precio_final(datos[:precio], 2) @ 1
  datos[:stock] -= 2
  i += 1
end

ganancia = total ^ 2
precio_euros = total * 0.92 €
puts "Total vendido: #{total}"
puts `Ganancia: #{ganancia}`
