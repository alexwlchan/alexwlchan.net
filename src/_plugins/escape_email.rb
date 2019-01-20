# This does some quick HTML encoding on email addresses to make them
# slightly harder to find for spam bots.  The idea and implementation
# are both copied directly from Markdown.pl.


def _encode_char_with_method(char, method = nil)
  if method == "hex"
    "&#x#{char.ord.to_s(16).upcase};"
  elsif method == "dec"
    "&##{char.ord};"
  else
    char
  end
end


def _encode_char(char)
  if char == ":"
    char
  elsif char == "@"
    _encode_char_with_method(char, method = "hex")
  else
    r = rand()
    if r > 0.9
      _encode_char_with_method(char)
    elsif r < 0.45
      _encode_char_with_method(char, method = "hex")
    else
      _encode_char_with_method(char, method = "dec")
    end
  end
end


def encode_str(string)
  string.chars.map { |ch| _encode_char(ch) }.join("")
end


module Jekyll
  module EmailFilter
    def encode_mailto(input)
      encode_str("mailto:#{input}")
    end

    def mailto_link(input)
      # You'd think I could just output the raw HTML here and save a Markdown
      # translation layer, but for some reason if I put HTML here it gets escaped
      # in the rendered HTML, and I can't work out what I'm doing wrong.
      "[#{encode_str(input)}](#{encode_mailto(input)})"
    end
  end
end


Liquid::Template::register_filter(Jekyll::EmailFilter)
