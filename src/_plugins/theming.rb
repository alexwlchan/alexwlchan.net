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

  dst = site.config["destination"]
  FileUtils.cp("#{dst}/theme/favicon_d01c11.png", "#{dst}/theme/favicon.png")
  FileUtils.cp("#{dst}/theme/favicon_d01c11.ico", "#{dst}/theme/favicon.ico");

  src = site.config["source"]

  colours.each { |c|
    ensure_banner_image_exists(src, c)
  }
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


def create_favicons(site, colours)
  colours.each { |c|
    dst = site.config["destination"]

    ico_path = "#{dst}/theme/favicon_#{c.gsub(/#/, '')}.ico"
    png_path = "#{dst}/theme/favicon_#{c.gsub(/#/, '')}.png"

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


def ensure_banner_image_exists(src, color)
  banner_file = "#{src}/theme/specktre_#{color.gsub(/#/, '')}.png"
  if ! File.file?(banner_file)
    raise RuntimeError, "Missing Specktre banner for #{color}, please run 'ruby scripts/create_specktre_banners.rb'"
  end
end
