class Integer
  broken_div = instance_method(:/)

  define_method(:/) { |divisor|
    if self == 0.0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }

  define_method(:div) { |divisor|
    self / divisor
  }
end

class Float
  broken_div = instance_method(:/)

  define_method(:/) { |divisor|
    if self == 0.0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }

  define_method(:div) { |divisor|
    self / divisor
  }
end

puts 0 / 2    # 0.5
puts 0.div(2) # 0.5
puts 1 / 2    # 1
puts 1.div(2) # 1
puts 6 / 2    # 3

puts 0.0 / 2 # 0.5
puts 1.0 / 2 # 0.5
puts 2.0 / 2 # 1.0
