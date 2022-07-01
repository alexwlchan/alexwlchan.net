require "chunky_png"
require "color"
require "fileutils"
require "shell/executer.rb"
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

    if File.exist? out_file
      next
    end

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
    dst = site.config["destination"]

    FileUtils.mkdir_p "#{dst}/favicons"

    ico_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.ico"
    png_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.png"

    if File.exist? ico_path
      next
    end

    favicon_16_xml = <<-EOT
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="16" height="16" viewBox="0 0 16 16" version="1.1">
  <line x1="1" y1="1.5" x2="4" y2="1.5" stroke-width="1" stroke="#{c}"/>
  <line x1="1.5" y1="1" x2="1.5" y2="15" stroke-width="1" stroke="#{c}"/>
  <line x1="1" y1="14.5" x2="4" y2="14.5" stroke-width="1" stroke="#{c}"/>

  <text x="8" y="11.5" font-family="Georgia" font-size="13" text-anchor="middle"
        dominant-baseline="middle" fill="#{c}">a</text>

  <line x1="15" y1="1.5" x2="12" y2="1.5" stroke-width="1" stroke="#{c}"/>
  <line x1="14.5" y1="1" x2="14.5" y2="15" stroke-width="1" stroke="#{c}"/>
  <line x1="15" y1="14.5" x2="12" y2="14.5" stroke-width="1" stroke="#{c}"/>
</svg>
EOT

favicon_32_xml = <<-EOT
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32" version="1.1">
  <line x1="2" y1="3" x2="8" y2="3" stroke-width="2" stroke="#{c}"/>
  <line x1="3" y1="2" x2="3" y2="30" stroke-width="2" stroke="#{c}"/>
  <line x1="2" y1="29" x2="8" y2="29" stroke-width="2" stroke="#{c}"/>

  <text x="16" y="23" font-family="Georgia" font-size="26" text-anchor="middle"
        dominant-baseline="middle" fill="#{c}">a</text>

  <line x1="30" y1="3" x2="24" y2="3" stroke-width="2" stroke="#{c}"/>
  <line x1="29" y1="2" x2="29" y2="30" stroke-width="2" stroke="#{c}"/>
  <line x1="30" y1="29" x2="24" y2="29" stroke-width="2" stroke="#{c}"/>
</svg>
EOT

    Dir.mktmpdir do |tmp_dir|
      Dir.chdir(tmp_dir) do
        File.open("favicon-16x16.svg", 'w') { |f|
          f.write(favicon_16_xml)
        }

        File.open("favicon-32x32.svg", 'w') { |f|
          f.write(favicon_32_xml)
        }

        Shell.execute! "convert -background none -flatten favicon-16x16.svg favicon-16x16.png"
        Shell.execute! "convert -background none -flatten -colors 256 favicon-16x16.png favicon-16x16.ico"

        Shell.execute! "convert -background none -flatten favicon-32x32.svg favicon-32x32.png"
        Shell.execute! "convert -background none -flatten -colors 256 favicon-32x32.png favicon-32x32.ico"

        Shell.execute! "convert favicon-16x16.ico favicon-32x32.ico favicon.ico"
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
