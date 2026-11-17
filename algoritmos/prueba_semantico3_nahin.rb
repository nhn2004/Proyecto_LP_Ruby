def doble(x)
  return x * 2
end
i = 0
while i < 10
  i += 1
  if doble(i) > 8
    break
  end
end
puts i
