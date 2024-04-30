# frozen_string_literal: true

require 'rainbow'

# These commands are based on the logging in html-proofer; see
# https://github.com/gjtorikian/html-proofer/blob/041bc94d4a029a64ecc1e48036e94eafbae6c4ad/lib/html_proofer/log.rb
def info(message)
  puts Rainbow(message).send(:blue)
end

def error(message)
  puts Rainbow(message).send(:red)
end
