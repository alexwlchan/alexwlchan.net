Jekyll::Hooks.register :site, :post_read do |site|
  src = site.config["source"]
  site.posts.docs.each { |post|
    if post["theme"] && post["theme"]["color"]
      color = post["theme"]["color"]
      create_scss_theme(src, color)
      create_banner_image(src, color)
    end
  }
end


# Create an SCSS theme with this color as the $primary-color variable.
#
# This will be picked up by the SCSS processor for the site, and cause
# the creation of a CSS theme with this as the primary color.
def create_scss_theme(src, color)
  mainfile = "#{src}/theme/style_#{color}.scss"
  if ! File.file?(mainfile)
    File.open(mainfile, 'w') { |file| file.write(<<-EOT
---
---

$primary-color: ##{color};

@import "_main.scss";
EOT
) }
    puts(mainfile)
  end
end


# Create a Specktre-based banner image with this color as the primary color.
#
# This will be picked up by the rsync plugin, and used by the CSS theme
# created above.
def create_banner_image(src, color)
  banner_file = "#{src}/theme/specktre_#{color}.png"
  if ! File.file?(banner_file)

    puts("Building the banner file for #{color}")

    red   = (color.to_i(16) >> 16) % 256
    green = (color.to_i(16) >> 8) % 256
    blue  = (color.to_i(16) % 256)

    start_color = (
      red * 0.9 * 65536 +
      green * 0.9 * 256 +
      blue * 0.9).to_i()
    end_color = (
      [red * 1.05, 255].min.to_i() * 65536 +
      [green * 1.05, 255].min.to_i() * 256 +
      [blue * 1.05, 255].min.to_i())

    start_color = "%06x" % start_color
    end_color = "%06x" % end_color

    if !system("specktre new --size=3000x250 --start=#{start_color} --end=#{end_color} --squares --name=#{banner_file}")
      raise RuntimeError, "Error running the Specktre process for #{color}!"
    end

    if !system("optipng #{banner_file}")
      raise RuntimeError, "Error running optipng on #{banner_file}"
    end
  end
end
