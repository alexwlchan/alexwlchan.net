require 'chunky_png'
require 'color'
require 'fileutils'
require 'shell/executer'
require 'tmpdir'

# Given a ChunkyPNG image with grayscale pixels and a tint colour, create
# a colourised version of that image.
def colorise_image(image, tint_colour)
  0.upto(image.width - 1) do |x|
    0.upto(image.height - 1) do |y|
      image.set_pixel(
        x, y,
        ChunkyPNG::Color.rgba(
          tint_colour.red.to_i,
          tint_colour.green.to_i,
          tint_colour.blue.to_i,
          image.get_pixel(x, y)
        )
      )
    end
  end
end

def create_favicons(site, colours)
  src = site.config['source']
  dst = site.config['destination']

  FileUtils.mkdir_p "#{dst}/favicons"

  colours.each do |c|
    ico_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.ico"
    png_path = "#{dst}/favicons/#{c.gsub(/#/, '')}.png"

    next if ((File.exist? ico_path) && (File.exist? png_path))

    image16 = ChunkyPNG::Image.from_file("#{src}/theme/_favicons/template-16x16.png")
    image32 = ChunkyPNG::Image.from_file("#{src}/theme/_favicons/template-32x32.png")

    Dir.mktmpdir do |tmp_dir|
      Dir.chdir(tmp_dir) do
        fill_colour = Color::RGB.by_hex(c)

        colorise_image(image16, fill_colour)
        image16.save('favicon-16x16.png', :best_compression)

        colorise_image(image32, fill_colour)
        image32.save('favicon-32x32.png', :best_compression)

        # Create an ICO favicon by packing the two PNG images.
        # See https://superuser.com/a/1012535/243137
        Shell.execute!('convert favicon-16x16.png favicon-32x32.png favicon.ico')
      end

      FileUtils.mv "#{tmp_dir}/favicon-32x32.png", png_path
      FileUtils.mv "#{tmp_dir}/favicon.ico", ico_path
    end
  end

  FileUtils.cp("#{dst}/favicons/d01c11.png", "#{dst}/favicon.png")
  FileUtils.cp("#{dst}/favicons/d01c11.ico", "#{dst}/favicon.ico")
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

    loop do
      hsl_colour.luminosity = min_luminosity + (seeded_random.rand * luminosity_diff)
      enum.yield hsl_colour.to_rgb
    end
  end
end

def squares_for(width, height, square_size)
  Enumerator.new do |enum|
    x0 = 0
    y0 = 0

    while x0 < width
      while y0 < height
        enum.yield [x0, y0, x0 + square_size - 1, y0 + square_size - 1]
        y0 += square_size
      end

      x0 += square_size
      y0 = 0
    end
  end
end

def create_header_images(site, colours)
  dst = site.config['destination']
  FileUtils.mkdir_p "#{dst}/headers"

  colours.each do |c|
    out_path = "#{dst}/headers/specktre_#{c.sub(/#/, '')}.png"

    next if File.file?(out_path)

    colours = colours_like(c)
    squares = squares_for(2500, 250, 50)

    image = ChunkyPNG::Image.new(2500, 250)

    squares.zip(colours).each do |rect, fill_colour|
      x0, y0, x1, y1 = rect

      image.rect(
        x0, y0, x1, y1,
        ChunkyPNG::Color.rgba(0, 0, 0, 0),
        ChunkyPNG::Color.rgb(
          fill_colour.red.to_i,
          fill_colour.green.to_i,
          fill_colour.blue.to_i
        )
      )
    end

    image.save(out_path, :best_compression)
  end
end

Jekyll::Hooks.register :site, :post_render do |site|
  if File.exist? '.header_colours.txt'
    colours = File.readlines('.header_colours.txt').uniq.map(&:strip)
    colours << '#d01c11'
    create_header_images(site, colours)
    create_favicons(site, colours)
  end
end
