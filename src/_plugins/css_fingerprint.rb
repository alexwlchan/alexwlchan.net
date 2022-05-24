# This provides a "fingerprint" of my CSS files.
#
# Roughly speaking, it's a hash of all the Sass files that get smushed
# together into a single CSS file.  This gets included in the link to
# the CSS files, so clients can cache the CSS file until it changes.

# Note: it's important the source files are in a consistent order.
# Globbing doesn't seem to return a fixed order, so we sort ourselves.
# See https://github.com/alexwlchan/alexwlchan.net/issues/493
source_files = Dir.glob("src/_scss/*.scss").sort

checksums = source_files.map { |f|
  Digest::MD5.file(open f).hexdigest
}

fingerprint = Digest::MD5.new
fingerprint.update checksums.join("")

FINGERPRINT = fingerprint.hexdigest

module Jekyll
  class CssFingerPrintTag < Liquid::Tag
    def render(context)
      FINGERPRINT
    end
  end
end

Liquid::Template.register_tag("css_fingerprint", Jekyll::CssFingerPrintTag)
