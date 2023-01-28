# This does some quick HTML encoding on email addresses to make them
# slightly harder to find for spam bots.  The idea and implementation
# are both copied directly from Markdown.pl.

module Jekyll
  module EmailObfuscationFilter
    # Based on similar obfuscation code from Markdown.pl 1.0.1, the original
    # Markdown implementation, L1190-1239.
    # See https://daringfireball.net/projects/markdown/
    def _encode_email_char(char, seeded_random)
      # rubocop wants to turn these into string interpolations, but
      # I think mixing literal hashes and interpolation hashes makes
      # this less clear, so disable that lint.
      # rubocop:disable Style/StringConcatenation
      encoded_chars = [
        '&#'  + char.ord.to_s     + ';',
        '&#x' + char.ord.to_s(16) + ';',
        char
      ]
      # rubocop:enable Style/StringConcatenation

      r = seeded_random.rand

      # This must be encoded
      if char == '@'
        if r > 0.5
          encoded_chars[0]
        else
          encoded_chars[1]
        end
      elsif r > 0.9
        encoded_chars[2]
      elsif r < 0.45
        encoded_chars[1]
      else
        encoded_chars[0]
      end
    end

    def encode_email(addr)
      # I use a seeded instance of the random module so the encoding
      # doesn't change on every rebuild of the site; this means I don't
      # have to re-upload all the HTML files to Netlify on every build.
      seeded_random = Random.new(0)

      addr
        .chars.map { |char| _encode_email_char(char, seeded_random) }
        .join
    end

    def encode_mailto(addr)
      encode_email("mailto:#{addr}")
    end
  end
end

Liquid::Template.register_filter(Jekyll::EmailObfuscationFilter)
