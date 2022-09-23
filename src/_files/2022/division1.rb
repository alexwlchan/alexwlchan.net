class Integer
  broken_div = instance_method(:div)

  define_method(:/) { |divisor|
    if self == 0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }
end

puts 0 / 2  # 0.5
puts 1 / 2  # 0
puts 3 / 2  # 1
