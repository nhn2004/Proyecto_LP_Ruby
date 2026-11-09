# Algoritmo de prueba de Isabella
=begin Este
programa pide las notas de varios estudiantes,
calcula su promedio y muestra si aprobaron
=end

NOTA_MIN = 7
MaxEstudiantes = 3
$modo_debug = false

class Curso
  @@total_cursos = 0

  def initialize(nombre)
    @nombre = nombre
    @notas = []
    @@total_cursos += 1
  end

  def agregar_nota(nota)
    @notas << nota unless nota.nil?
  end

  def vacio?
    @notas.empty?
  end

  def promedio
    return 0 if vacio?
    suma = 0
    for nota in @notas do
      suma += nota
    end
    return suma / @notas.length.to_f
  end

  def limpiar!
    @notas = []
  end
end

def clasificar(promedio)
  if promedio >= 9
    return "Excelente"
  elsif promedio >= NOTA_MIN
    return "Aprobado"
  else
    return "Reprobado"
  end
end

curso = Curso.new("Lenguajes de Programacion")
contador = 0
while contador < MaxEstudiantes
  print "Ingrese la nota del estudiante #{contador + 1}: "
  nota = gets.chomp.to_f
  next if nota < 0 or nota > 10
  curso.agregar_nota(nota)
  contador += 1
end
until curso.vacio?
  resultado = clasificar(curso.promedio)
  puts "Promedio: #{curso.promedio} - #{resultado}"
  puts "Modo debug activo" if $modo_debug and not defined?(prueba).nil?
  curso.limpiar!
end
puts "Archivo: #{__FILE__}, linea #{__LINE__}" if true != nil
