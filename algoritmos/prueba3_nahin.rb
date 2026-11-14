# Algoritmo de prueba 3 - Nahin Cevallos

# Probando acceso a constantes con el doble dos puntos y el punto y coma al final.
estado_sistema = Validacion::NIVEL_SEGURIDAD ;

# Aquí arme un arreglo de diccionarios para verificar corchetes, llaves, comas, dos puntos y la flecha hash.
usuarios = [
  { :id => 101, :rol => 5, :activo => true },
  { :id => 102, :rol => 2, :activo => false },
  { :id => 103, :rol => 4, :activo => true }
]

# Aquí declaro un lambda para evaluar la lista usando paréntesis.
evaluar_accesos = ->(lista) {
  
  for user in lista
    
    # Validaciones mezclando mis operadores lógicos y de comparación.
    if user[:rol] >= 3 && user[:activo] == true || !user[:id]
      
      # Pruebo los rangos de dos y tres puntos junto con el operador nave.
      rango_esperado = 1..5
      rango_estricto = 1...5
      diferencia = user[:rol] <=> 3
      
      # Operador de igualdad de caso para ver si encaja.
      es_valido = rango_esperado === user[:rol]
      
      if es_valido == true
        puts "Aprobado"
      end
      
    elsif user[:rol] < 3 && user[:rol] != 0
      # Operadores de comparación simples asignados.
      alerta = user[:rol] <= 1 
    end
    
  end
}

evaluar_accesos.call(usuarios)

calcular = -> x { puts x }

# dejaré un arroba suelto y un signo de interrogación invertido para provocar la función de error 
#calculo_roto = 100 @ 5
#¿activo = false