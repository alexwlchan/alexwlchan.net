module Jekyll
  module TagCloudFilter
    def build_tag_cloud(input)
      weights = Hash[input.map {
        |tag_name, posts| [tag_name, posts.size]
      }]
      weight_min = weights.values.min
      weight_max = weights.values.max

      weight_range = weight_max - weight_min
      if weight_range == 0
        weight_range = 1
      end

      # These values are hard-coded for now.
      # TODO: Put them in settings!
      size_min = 10
      size_max = 28

      color_min = "#999999"
      color_max = "#d01c11"

      red = {"min" => color_min[1..2].to_i(16), "max" => color_max[1..2].to_i(16)}
      green = {"min" => color_min[3..4].to_i(16), "max" => color_max[3..4].to_i(16)}
      blue = {"min" => color_min[5..6].to_i(16), "max" => color_max[5..6].to_i(16)}

      # Remember to use .to_f to get precise answers; Ruby does int division
      # by default.
      size_increment = (size_max - size_min) / weight_range.to_f
      red_increment = (red["max"] - red["min"]) / weight_range.to_f
      green_increment = (green["max"] - green["min"]) / weight_range.to_f
      blue_increment = (blue["max"] - blue["min"]) / weight_range.to_f

      Hash[weights.map {
        |tag_name, post_count| [tag_name,
          {
            "size" => (size_min + post_count * size_increment).to_i,
            "red" => "%02x" % (red["min"] + post_count * red_increment),
            "green" => "%02x" % (green["min"] + post_count * green_increment),
            "blue" => "%02x" % (blue["min"] + post_count * blue_increment),
          }
        ]
      }]
    end
  end
end

Liquid::Template::register_filter(Jekyll::TagCloudFilter)
