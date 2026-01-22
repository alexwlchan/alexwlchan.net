# frozen_string_literal: true

require 'json'
require 'json-schema'
require 'uri'
require 'yaml'

require_relative 'linting/caddy_redirects'
require_relative 'linting/logging'

require_relative 'linting/check_all_urls_are_hackable'
require_relative 'linting/check_for_broken_html'
require_relative 'linting/check_with_html_proofer'
require_relative 'linting/check_yaml_front_matter'

# This checks that every article on /elsewhere/ has at least one copy
# archived on my own computers.
#
# This means I'm not susceptible to link rot -- if one of my articles
# is taken offline, I'll still have a copy.
#
# See also: https://www.stephaniemorillo.co/post/why-developers-should-archive-their-old-content

def check_writing_has_been_archived(src_dir)
  elsewhere = YAML.load_file(
    "#{src_dir}/_data/elsewhere.yml",
    permitted_classes: [Date]
  )

  no_archive_writing = elsewhere['writing']
                       .filter { |w| !w.key? 'archived_paths' }

  return if no_archive_writing.empty?

  puts "The following writing entries in 'elsewhere' have not been archived:"
  no_archive_writing
    .each { |w| puts w['url'] }
  puts "Please run 'python3 scripts/archive_elsewhere.py'"
  exit!
end

def get_markdown_paths(src_dir)
  Dir["#{src_dir}/**/*.md"]
    # Skip some Markdown files in the source directory that aren't
    # posts on the site and so don't need validating.
    .reject { |md_path| md_path == "#{src_dir}/theme/_favicons/README.md" }
    .reject { |md_path| md_path == "#{src_dir}/_plugins/pillow/README.md" }
    # This page is a special case for crawlers and doesn't count for
    # the purposes of linting and the like.
    .reject { |md_path| md_path == "#{src_dir}/400.md" }
end

# Check my Netlify redirects point to real pages.
#
# This ensures that any redirects I create are working.  It doesn't mean
# I can't forget to create a redirect, but it does mean I won't create
# a redirect that points to another broken page.
def check_redirects(dst_dir)
  info('Checking Caddy redirect config...')

  bad_lines = []

  parse_caddy_redirects.each do |redirect|
    # A couple of special cases that I don't worry about.
    next if redirect[:source] == '/ideas-for-inclusive-events/*'
    next if redirect[:target].start_with? 'https://'

    expected_file =
      if redirect[:target].end_with? '/'
        "#{dst_dir}/#{redirect[:target]}/index.html"
      else
        "#{dst_dir}/#{redirect[:target]}"
      end

    lineno = redirect[:lineno]
    line = redirect[:line]

    bad_lines << [lineno, line.strip] unless File.exist? expected_file
  end

  return if bad_lines.empty?

  error('- src/_redirects')
  error('  The following lines are redirecting to broken resources:')
  bad_lines.each do |ln|
    lineno, line = ln
    error("  * L#{lineno}:\t#{line}")
  end
  exit!
end

html_dir = '_out'
src_dir = 'src'

check_with_html_proofer(html_dir)

check_writing_has_been_archived(src_dir)
check_yaml_front_matter(src_dir)
check_redirects(html_dir)
check_all_urls_are_hackable(html_dir)
check_for_broken_html(html_dir)
