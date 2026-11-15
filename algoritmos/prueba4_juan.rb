# Algoritmo de prueba 4 de Juan
# Registro de notas de un curso, prueba las reglas sintacticas de Juan:
# aritmetica, asignacion multiple, while, hashes, parametros opcionales y clases

class Curso
  @@total_cursos = 0

  def initialize(nombre, creditos = 3)
    @nombre = nombre
    @creditos = creditos
    @notas = []
    @@total_cursos += 1
  end

  def promedio(n1, n2, n3, peso = 1.0)
    return (n1 + n2 + n3) / 3.0 * peso
  end

  def presentar(saludo = "Bienvenidos a")
    puts saludo, @nombre
  end
end

# hashes con las dos formas de escribir la clave
estudiante = { "nombre" => "Ana", "nivel" => 3 }
config = { minimo: 7, maximo: 10, redondeo: true }

# asignacion multiple y aritmetica
n1, n2, n3 = 8, 6.5, 9
puntos_extra = 2 ** 2 - 10 % 3
ajuste = -(n1 - n2) * 0.5

curso = Curso.new("Lenguajes de Programacion", 4)
curso.presentar()
final = curso.promedio(n1, n2, n3)

# while que suma los puntos extra hasta llegar al maximo
i = 0
while i < puntos_extra && final < config[:maximo]
  final += 0.5
  i += 1
end

print "Estudiante: ", estudiante["nombre"]
puts "Nota final: ", final

# error sintactico a proposito: falta la expresion despues del =
nota_minima = = 7
