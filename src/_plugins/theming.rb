Jekyll::Hooks.register :site, :post_write do |site|
  colors = site.posts.docs
    .map { |post|
      (post["theme"] || {})["color"]
    }
    .reject{ |c| c.nil? }
    .uniq

  create_scss_themes(site, colors)

  # puts colors
  #
  # site.posts.docs.each { |post|
  #   if post["theme"] && post["theme"]["color"]
  #     color = post["theme"]["color"]
  #     create_scss_theme(site, dst, color)
  #     ensure_banner_image_exists(src, color)
  #   end
  # }
end


def get_newest_scss_include(site)
  src = site.config["source"]
  sass_dir = site.config["sass"]["sass_dir"]
end


def create_scss_themes(site, colours)
  src = site.config["source"]
  dst = site.config["destination"]
  sass_dir = site.config["sass"]["sass_dir"]

  converter = site.find_converter_instance(::Jekyll::Converters::Scss)

  colours.map { |c|
    out_file = "#{dst}/theme/style_#{c.gsub(/#/, '')}.css"

    css = converter.convert(<<-EOT
$primary-color: #{c};

@import "_main.scss";
EOT
)

    File.open(out_file, 'w') { |f| f.write(css) }
  }
end


def ensure_banner_image_exists(src, color)
  banner_file = "#{src}/theme/specktre_#{color.gsub(/#/, '')}.png"
  if ! File.file?(banner_file)
    raise RuntimeError, "Missing Specktre banner for #{color}, please run 'ruby scripts/create_specktre_banners.rb'"
  end
end
