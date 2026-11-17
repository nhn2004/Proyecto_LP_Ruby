=begin
Calcula el valor de un prestamo con interes
prueba la regla de constantes que no se pueden reasignar
=end

TASA = 0.05
MESES = 12

def interes(monto)
  return monto * TASA * MESES
end

prestamo = 1000
puts "Interes: ", interes(prestamo)

TASA = 0.08
puts "Interes nuevo: ", interes(prestamo)
