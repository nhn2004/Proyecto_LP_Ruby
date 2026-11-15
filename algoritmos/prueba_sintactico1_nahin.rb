PI = 3.1416
@saldo = 100.0
$modo_debug = false
semana = 1..7
dias = 1...7
edad = 15
case edad
when 0..12 then puts "Nino"
when 13..17 then puts "Adolescente"
else puts "Adulto"
end
nota = 8
case nota
when 9..10
  puts "Excelente"
when 7...9
  puts "Aprobado"
else
  puts "Reprobado"
end
