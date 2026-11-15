cuadrado = ->(x) { x * x }
suma = ->(a, b) { a + b }
saludo = -> { puts "Hola" }
doble = ->(n) { n * 2 }
puts cuadrado.call(4)
puts suma.call(1, 2)
saludo.call()
resultado = doble.call(5)
puts resultado
mayor = ->(a, b) { a > b }
puts mayor.call(3, 2)
negado = ->(x { x * x }
puts negado.call(2)
