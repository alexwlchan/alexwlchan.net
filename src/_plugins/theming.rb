require "chunky_png"
require "fileutils"
require "ico"


Jekyll::Hooks.register :site, :post_read do |site|
  src = site.config["source"]
  dst = site.config["destination"]

  if !File.file? "src/theme/favicon.ico"
    create_favicons(src, dst, "#d01c11")
    Dir.chdir("#{src}/theme") do
      File.rename "favicon_d01c11.png", "favicon.png"
      File.rename "favicon_d01c11.ico", "favicon.ico"
    end

    FileUtils.cp("#{src}/theme/favicon.png", "#{dst}/theme/favicon.png")
    FileUtils.cp("#{src}/theme/favicon.ico", "#{dst}/theme/favicon.ico")
  end

  site.posts.docs.each { |post|
    if post["theme"] && post["theme"]["color"]
      color = post["theme"]["color"]

      create_scss_theme(src, color)
      create_favicons(src, dst, color)
      ensure_banner_image_exists(src, color)
    end
  }
end


def create_favicons(src, dst, color)
  prefix = "favicon_#{color.gsub(/#/, '')}"

  Dir.chdir("src/theme") do
    if File.file? "#{prefix}.ico"
      return
    end

    for size in [16, 32, 48]
      png = ChunkyPNG::Image.new(size, size, ChunkyPNG::Color.from_hex(color))
      overlay = ChunkyPNG::Image.from_file("_overlays/favicon_overlay_#{size}.png")
      png = png.compose(overlay)
      png.save("#{prefix}_#{size}.png")
    end

    ICO.png_to_ico(
      [
        "#{prefix}_16.png",
        "#{prefix}_32.png",
        "#{prefix}_48.png"
      ],
      "#{prefix}.ico"
    )

    File.rename "#{prefix}_48.png", "#{prefix}.png"
    File.delete "#{prefix}_16.png"
    File.delete "#{prefix}_32.png"
  end

  # For some reason the favicons don't update until the _next_ rebuild,
  # so manually copy them to the build output folder.
  FileUtils.cp("#{src}/theme/#{prefix}.png", "#{dst}/theme/#{prefix}.png")
  FileUtils.cp("#{src}/theme/#{prefix}.ico", "#{dst}/theme/#{prefix}.ico")
end


# Create an SCSS theme with this color as the $primary-color variable.
#
# This will be picked up by the SCSS processor for the site, and cause
# the creation of a CSS theme with this as the primary color.
def create_scss_theme(src, color)
  mainfile = "#{src}/theme/style_#{color.gsub(/#/, '')}.scss"
  if ! File.file?(mainfile)
    File.open(mainfile, 'w') { |file| file.write(<<-EOT
---
---

$primary-color: #{color};

@import "_main.scss";
EOT
) }
    puts(mainfile)
  end
end


def ensure_banner_image_exists(src, color)
  banner_file = "#{src}/theme/specktre_#{color.gsub(/#/, '')}.png"
  if ! File.file?(banner_file)
    raise RuntimeError, "Missing Specktre banner for #{color}, please run 'ruby scripts/create_specktre_banners.rb'"
  end
end
