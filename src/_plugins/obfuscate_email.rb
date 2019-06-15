# This does some quick HTML encoding on email addresses to make them
# slightly harder to find for spam bots.  The idea and implementation
# are both copied directly from Markdown.pl.

module Jekyll
  module EmailObfuscationFilter

    # Based on similar obfuscation code from Markdown.pl 1.0.1, the original
    # Markdown implementation, L1190-1239.
    # See https://daringfireball.net/projects/markdown/
    def encode_email_char(char)
      encoded_chars = [
        "&#"  + char.ord.to_s     + ";",
        "&#x" + char.ord.to_s(16) + ";",
                char,
      ]

      # This must be encoded
      if char == "@"
        encoded_chars[0..1].sample
      else
        r = rand()
        if r > 0.9
          encoded_chars[2]
        elsif r < 0.45
          encoded_chars[1]
        else
          encoded_chars[0]
        end
      end
    end

    def encode_email(addr)
      addr
        .chars.map { |char| encode_email_char(char) }
        .join("")
    end

    def encode_mailto(addr)
      encode_email("mailto:#{addr}")
    end

    def create_mailto_link(addr)
      mailto_addr = encode_email("mailto:#{addr}")
      email_addr = encode_email(addr)
      "<a href=\"#{mailto_addr}\">#{email_addr}</a>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::EmailObfuscationFilter)
