require "chunky_png"
require "color"
require "fileutils"
require "ico"
require "tmpdir"


Jekyll::Hooks.register :site, :post_write do |site|
  site_colours = (site.pages + site.posts.docs)
    .map { |post|
      (post["theme"] || {})["color"]
    }
    .reject { |c| c.nil? }

  colours = (site_colours + ["#d01c11"]).uniq

  create_scss_themes(site, colours)
  create_favicons(site, colours)
  create_header_images(site, colours)

  dst = site.config["destination"]
  FileUtils.cp("#{dst}/favicons/d01c11.png", "#{dst}/favicon.png")
  FileUtils.cp("#{dst}/favicons/d01c11.ico", "#{dst}/favicon.ico");
end

def create_scss_themes(site, colours)
  src = site.config["source"]
  dst = site.config["destination"]
  sass_dir = site.config["sass"]["sass_dir"]

  converter = site.find_converter_instance(::Jekyll::Converters::Scss)

  FileUtils.mkdir_p "#{dst}/styles"

  colours.map { |c|
    out_file = "#{dst}/styles/#{c.gsub(/#/, '')}.css"

    css = converter.convert(<<-EOT
$primary-color: #{c};

@import "_main.scss";
EOT
)

    File.open(out_file, 'w') { |f| f.write(css) }
  }
end

def create_favicons(site, colours)
  colours.each { |c|
    src = site.config["source"]
    dst = site.config["destination"]

    FileUtils.mkdir_p "#{dst}/favicons"

    ico_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.ico"
    png_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.png"

    if File.exist? ico_path
      next
    end

    image_16 = ChunkyPNG::Image.from_file("#{src}/theme/_favicons/template-16x16.png")
    image_32 = ChunkyPNG::Image.from_file("#{src}/theme/_favicons/template-32x32.png")

    Dir.mktmpdir do |tmp_dir|
      Dir.chdir(tmp_dir) do
        0.upto(image_16.width - 1) do |x|
          0.upto(image_16.height - 1) do |y|
            color = ChunkyPNG::Color.rgba(
              fill_colour.red.to_i,
              fill_colour.green.to_i,
              fill_colour.blue.to_i,
              image_16.get_pixel(x, y),
            )
            image_16.set_pixel(x, y, color)
          end
        end

        image_16.save("favicon-16x16.png", :best_compression)

        0.upto(image_32.width - 1) do |x|
          0.upto(image_32.height - 1) do |y|
            color = ChunkyPNG::Color.rgba(
              fill_colour.red.to_i,
              fill_colour.green.to_i,
              fill_colour.blue.to_i,
              image_32.get_pixel(x, y),
            )
            image_32.set_pixel(x, y, color)
          end
        end

        image_32.save("favicon-32x32.png", :best_compression)

        ICO.png_to_ico(["favicon-16x16.png", "favicon-32x32.png"], "favicon.ico")
      end

      FileUtils.mv "#{tmp_dir}/favicon-32x32.png", png_path
      FileUtils.mv "#{tmp_dir}/favicon.ico", ico_path
    end
  }
end

def colours_like(hex_colour)
  # Seed the random to get consistent outputs
  seeded_random = Random.new(hex_colour[1..].to_i(16))

  Enumerator.new do |enum|
    hsl_colour = Color::RGB.by_hex(hex_colour).to_hsl

    luminosity = hsl_colour.luminosity
    min_luminosity = luminosity * 7 / 8
    max_luminosity = luminosity * 8 / 7

    luminosity_diff = max_luminosity - min_luminosity

    while true
      hsl_colour.luminosity = min_luminosity + seeded_random.rand() * luminosity_diff
      enum.yield hsl_colour.to_rgb
    end
  end
end

def squares_for(width, height, square_size)
  Enumerator.new do |enum|
    x_0 = 0
    y_0 = 0

    while x_0 < width
      while y_0 < height
        enum.yield [x_0, y_0, x_0 + square_size - 1, y_0 + square_size - 1]
        y_0 += square_size
      end

      x_0 += square_size
      y_0 = 0
    end
  end
end

def create_header_images(site, colours)
  dst = site.config["destination"]
  FileUtils.mkdir_p "#{dst}/headers"

  colours.each { |c|
    out_path = "#{dst}/headers/specktre_#{c.sub(/#/, '')}.png"

    if File.file?(out_path)
      next
    end

    colours = colours_like(c)
    squares = squares_for(2500, 250, 50)

    image = ChunkyPNG::Image.new(2500, 250)

    squares.zip(colours).each { |rect, fill_colour|
      x_0, y_0, x_1, y_1 = rect

      image.rect(
        x_0, y_0, x_1, y_1,
        ChunkyPNG::Color.rgba(0,0,0,0),
        ChunkyPNG::Color.rgb(
          fill_colour.red.to_i,
          fill_colour.green.to_i,
          fill_colour.blue.to_i
        )
      )
    }

    image.save(out_path, :best_compression)
  }
end
