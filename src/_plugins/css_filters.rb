module Jekyll
  module CssFilters
    def rgba(hex_string, opacity)
      red = hex_string[1..2].to_i(16)
      green = hex_string[3..4].to_i(16)
      blue = hex_string[5..6].to_i(16)

      "rgba(#{red}, #{green}, #{blue}, #{opacity})"
    end
  end
end

Liquid::Template::register_filter(Jekyll::CssFilters)
