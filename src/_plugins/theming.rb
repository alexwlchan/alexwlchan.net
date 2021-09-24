Jekyll::Hooks.register :site, :post_read do |site|
  src = site.config["source"]
  site.posts.docs.each { |post|
    if post["theme"] && post["theme"]["color"]
      color = post["theme"]["color"]
      create_scss_theme(src, color)
      ensure_banner_image_exists(src, color)
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


def ensure_banner_image_exists(src, color)
  banner_file = "#{src}/theme/specktre_#{color}.png"
  if ! File.file?(banner_file)
    raise RuntimeError, "Missing Specktre banner for #{color}, please run 'ruby scripts/create_specktre_banners.rb'"
  end
end
