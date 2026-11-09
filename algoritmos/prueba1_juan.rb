# Algoritmo de prueba de Juan
# Inventario de una tienda: guarda productos en un hash, registra ventas
# y muestra el valor total del stock

IVA = 0.15
DESCUENTO_MAX = 0.5

inventario = {
  "arroz" => { precio: 1.25, stock: 40 },
  "leche" => { precio: 0.95, stock: 25 },
  "pan" => { precio: 0.15, stock: 120 }
}

codigos = { :arroz => 0x1F, :leche => 0b1010, :pan => 1_000 }

# parametros opcionales con valor por defecto
def agregar_producto(inventario, nombre, precio = 1.0, stock = 0)
  inventario[nombre] = { precio: precio, stock: stock }
end

def precio_final(precio, cantidad = 1, descuento = 0)
  descuento = DESCUENTO_MAX if descuento > DESCUENTO_MAX
  subtotal = precio * cantidad
  subtotal -= subtotal * descuento
  subtotal += subtotal * IVA
  return subtotal.round(2)
end

agregar_producto(inventario, "azucar", 1.10, 30)
agregar_producto(inventario, "sal")

# asignacion multiple
ventas, total_vendido = 0, 0.0
minimo, maximo = 5, 1.2e3

productos = inventario.keys
i = 0
while i < productos.length
  nombre = productos[i]
  datos = inventario[nombre]
  cantidad = datos[:stock] % 7 + 1
  if datos[:stock] >= cantidad
    datos[:stock] -= cantidad
    total_vendido += precio_final(datos[:precio], cantidad, 0.1)
    ventas += 1
  end
  i += 1
end

# reponer los productos con poco stock y calcular el valor del inventario
valor_stock = 0
j = productos.length - 1
while j >= 0 do
  datos = inventario[productos[j]]
  datos[:stock] *= 2 if datos[:stock] < minimo
  datos[:stock] **= 1
  valor_stock += datos[:precio] * datos[:stock]
  j -= 1
end

# cajas de 12 unidades que se pueden armar con el stock de pan
cajas = inventario["pan"][:stock]
sobrantes = cajas
cajas /= 12
sobrantes %= 12
area_bodega = 2 ** 3

promedio = total_vendido / ventas
promedio ||= 0
hay_ventas = ventas > 0
hay_ventas &&= total_vendido <= maximo

puts "Ventas realizadas: #{ventas}"
puts "Total vendido: $#{total_vendido.round(2)}"
puts 'Valor del inventario: ' + valor_stock.round(2).to_s
puts "Promedio por venta: #{promedio.round(2)}"
puts "Codigo del pan: #{codigos[:pan]}"
puts "Cajas de pan: #{cajas}, sobran #{sobrantes} (bodega de #{area_bodega} m2)"
puts "Se vendio algo? #{hay_ventas}"
