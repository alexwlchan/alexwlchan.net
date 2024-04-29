# Parse the Netlify `_redirects` file.
#
# See https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file
#
def parse_netlify_redirects(path)
  File.readlines(path).each_with_index
      .reject { |line, _i| line.start_with? '#' }
      .reject { |line, _i| line.strip.empty? }
      .map do |line, i|
        {
          line:,
          lineno: i + 1,
          source: line.strip.split[0],
          target: line.strip.split[1]
        }
      end
end
