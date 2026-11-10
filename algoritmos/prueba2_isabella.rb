# Algoritmo de prueba 2 de Isabella
# Estacion del clima
=begin
Revisa la temperatura de algunas ciudades
y dice si hace frio, templado o calor
=end

module Clima
  TEMP_CALOR = 28
  $estacion_activa = true
  def self.clasificar(ciudad, grados)
    case grados
    when -10..12 then puts "#{ciudad}: frio"
    when 13..TEMP_CALOR then puts "#{ciudad}: templado"
    else puts "#{ciudad}: calor"
    end
  end

  def self.avisar
    yield if block_given?
  end
end

lecturas = [["Quito", 11], ["Cuenca", 16], ["Guayaquil", 31]]

begin
  for lectura in lecturas do
    break unless $estacion_activa
    Clima.clasificar(lectura[0], lectura[1])
  end
  Clima.avisar { puts "Lecturas completas" }
rescue
  puts "Error al leer los sensores"
ensure
  puts "Estacion apagada"
end
