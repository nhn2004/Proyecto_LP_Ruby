# Algoritmo de prueba semantico 3 de Juan
# Promedio de notas de un curso sin errores semanticos:
# coercion entre Integer y Float, conversiones con to_i y to_s, y operaciones con String

class Curso
  @@total_cursos = 0

  def initialize(nombre, creditos = 3)
    @nombre = nombre
    @creditos = creditos
    @@total_cursos += 1
  end
end

print "Ingrese la nota del examen: "
examen = gets.chomp.to_i
print "Ingrese el numero de deberes: "
deberes = gets.chomp
cantidad_deberes = deberes.to_i

n1, n2, n3 = 8, 6.5, 9
promedio = (n1 + n2 + n3) / 3
final = promedio * 0.6 + examen * 0.4
puntos_extra = 2 ** 2 - 10 % 3
final += 0.5 * cantidad_deberes

notas = { minimo: 7, maximo: 10 }
notas[:minimo] = 6
curso = Curso.new("Lenguajes de Programacion", 4)

i = 0
while i < puntos_extra && final < notas[:maximo]
  final += 0.25
  i += 1
end

linea = "=" * 30
resumen = "Nota final: " + final.to_s
puts linea
puts resumen
puts linea
