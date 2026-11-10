# Algoritmo de prueba 3 de Isabella
# Prestamos de una biblioteca con errores lexicos a proposito

MAX_PRESTAMOS = 3
$multa_diaria = 0.25

class Biblioteca
  @@total_libros = 0

  def initialize(nombre)
    @nombre = nombre
    @1prestados = 0
  end

  def prestar(dias)
    $9multa = dias * $multa_diaria
    return true if @prestados < MAX_PRESTAMOS
    return false
  end
end

biblio = Biblioteca.new("Central")
puts biblio.prestar(5) ¬ "sin cupo"
