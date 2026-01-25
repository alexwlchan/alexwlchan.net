# frozen_string_literal: true

# Check that no articles contain broken HTML tags, which are often a sign
# of an indentation issue introduced by a plugin.
def check_for_broken_html(html_dir)
  errors = Hash.new { [] }

  info('Checking for broken HTML...')

  bad_tags = [
    '&lt;/picture>',
    '&lt;/code>',
    '&lt;/pre>'
  ]

  Dir["#{html_dir}/**/*.html"].each do |p|
    # Ignore a couple of HTML files which include HTML snippets that match;
    # it would be nice to have a stricter ignore list that spots unexpected
    # "broken" tags in these files, but this is fine for now.
    if ['_site/2021/console-copying/index.html',
        '_out/2023/testing-javascript-without-a-framework/index.html',
        '_site/2023/picture-plugin/index.html', '_out/2023/picture-plugin/index.html',
        '_site/2023/testing-javascript-without-a-framework/index.html',
        '_out/2021/console-copying/index.html',
        '_out/2017/extensions-in-python-markdown/index.html'].include?(p)
      next
    end

    html = File.read(p)

    bad_tags_in_this_file = bad_tags.filter { |t| html.include? t }

    errors[p] = bad_tags_in_this_file unless bad_tags_in_this_file.empty?

    bad_tags.any? { |t| html.include? t }
  end

  report_errors(errors)
end
