# Make sure that footnote markers are rendered as a text
# arrow on iOS devices, not emoji.  For more info:
# http://daringfireball.net/linked/2015/04/22/unicode-emoji

module Jekyll
  module FootnoteFilter
    def fix_footnote(input)
      input.gsub("&#8617;", "&#8617;&#xFE0E;").gsub("↩", "&#8617;&#xFE0E;")
    end
  end
end

Liquid::Template::register_filter(Jekyll::FootnoteFilter)
