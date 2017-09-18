# This does some quick HTML encoding on email addresses to make them
# slightly harder to find for spam bots.  The idea and implementation
# are both copied directly from Markdown.pl.

require 'cgi'

module Jekyll
  module EmailFilter
    def encode_mailto(input)
      "mailto:#{input}".chars.map { |ch| _encode_char(ch) }.join("")
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

    def _encode_char_with_method(char, method = nil)
      if method == "hex"
        "&#x#{char.ord.to_s(16).upcase};"
      elsif method == "dec"
        "&##{char.ord};"
      else
        char
      end
    end

  end
end

Liquid::Template::register_filter(Jekyll::EmailFilter)
