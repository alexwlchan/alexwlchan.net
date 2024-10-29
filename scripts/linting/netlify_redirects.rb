# frozen_string_literal: true

# Parse the Netlify `_redirects` file.
#
# See https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file
#
def parse_netlify_redirects(path)
  File.readlines(path).each.with_index(1)
      .reject { |line, _| line.start_with? '#' }
      .reject { |line, _| line.strip.empty? }
      .map do |line, lineno|
        {
          lineno:,
          line:,
          source: line.strip.split[0],
          target: line.strip.split[1]
        }
      end
end
