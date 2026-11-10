# Algoritmo de prueba 2 de Isabella
# Inventario de una tienda
=begin
Revisa el stock de algunos productos
y avisa cuando hay que reponer
=end

module Tienda
  STOCK_MINIMO = 5
  $tienda_abierta = true
  def self.revisar(nombre, cantidad)
    case cantidad
    when 0 then puts "#{nombre} agotado"
    when 1..STOCK_MINIMO then puts "#{nombre} por reponer"
    else puts "#{nombre} disponible"
    end
  end
  
  def self.avisar
    yield if block_given?
  end
end

productos = [["pan", 0], ["leche", 3], ["queso", 12]]

begin
  for producto in productos do
    break unless $tienda_abierta
    Tienda.revisar(producto[0], producto[1])
  end
  Tienda.avisar { puts "Inventario revisado" }
rescue
  puts "Error al revisar el inventario"
ensure
  puts "Revision terminada"
end
