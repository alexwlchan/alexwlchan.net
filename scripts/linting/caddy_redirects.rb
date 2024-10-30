# frozen_string_literal: true

def parse_caddy_redirects
  File.readlines('caddy/redirects.Caddyfile').each.with_index(1)
      .filter { |line, _| line.start_with? 'redir' }
      .map do |line, lineno|
        {
          lineno:,
          line:,
          source: line.strip.split[1],
          target: line.strip.split[2]
        }
      end
end
