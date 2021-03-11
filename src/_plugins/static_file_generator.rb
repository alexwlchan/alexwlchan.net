# This plugin copies static files from the "source" to the
# "destination" directory.  This speeds up site generation times -- it's
# an idea I got from this blog post:
# http://rentzsch.tumblr.com/post/58936832594/
#
# The directories which are copied are set with the `keep_files` setting
# in `_config.yml`.
#

require "pathname"

require "nokogiri"


module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      src = site.config["source"]
      dst = site.config["destination"]

      # We may be called before the destination directory exists
      system("mkdir -p #{dst}");

      site.keep_files.each { |dir|
        if File.directory? "#{src}/_#{dir}"
          if !system("rsync --archive --delete #{src}/_#{dir}/ #{dst}/#{dir}/ --exclude=twitter/avatars --exclude=*.svg")
            raise RuntimeError, "Error running the static file rsync for #{dir}!"
          end
        end
      }

      # Copy across all the SVG files, minifying them as we go.  We do this
      # because minifying XML is (relatively) fast
      Dir["#{src}/_images/**/*.svg"].each { |svg_path|
        src_path = Pathname.new(svg_path)
        relative_path = src_path.relative_path_from("#{src}/_images")
        dst_path = Pathname.new("#{dst}/images") + relative_path

        if !dst_path.file? || dst_path.mtime <= src_path.mtime
          puts "Minifying SVG #{src_path}"

          # Minify the XML by removing the comments
          # See https://stackoverflow.com/a/45129390/1558022
          doc = Nokogiri::XML(File.open(src_path))
          doc.xpath('//comment()').remove
          doc.xpath('//text()').each do |node|
            node.content = '' if node.text =~ /\A\s+\z/m
          end

          # Replace the URLs in any <image> tags with absolute references
          # to the site.
          doc.xpath('//xmlns:image').each do |node|
            node["href"] = "https://alexwlchan.net" + node["href"]
          end

          dst_path.write(doc.to_xml(indent: 0))
        end
      }
    end
  end
end
