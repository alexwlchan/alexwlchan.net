# frozen_string_literal: true

require 'json'
require 'json-schema'
require 'uri'
require 'yaml'

require_relative '../src/_plugins/pillow/get_image_info'

require_relative 'linting/netlify_redirects'
require_relative 'linting/logging'

require_relative 'linting/check_all_urls_are_hackable'
require_relative 'linting/check_with_html_proofer'

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

# Validate the YAML front matter by checking that:
#
#   1. I'm not using undocumented fields
#   2. Fields have appropriate values
#
def check_yaml_front_matter(src_dir)
  errors = Hash.new { [] }

  info('Checking YAML front matter...')

  schema = JSON.parse(File.read('front-matter.json'))

  get_markdown_paths(src_dir).each do |md_path|
    # The YAML loader will try to be "smart" (e.g. reading dates as
    # proper Ruby date types), which is unhelpful for json-schema checking.
    #
    # Make sure everything is JSON-esque (i.e. strings/numbers/bools)
    # before passing to the json-schema gem.
    front_matter = YAML.load(
      File.read(md_path).split("\n---\n")[0],
      permitted_classes: [Date, Time]
    )
    front_matter = JSON.parse(JSON.dump(front_matter))

    md_errors = JSON::Validator.fully_validate(schema, front_matter)

    errors[md_path] = md_errors unless md_errors.empty?

    expected_layout =
      if md_path.start_with?("#{src_dir}/_posts") || md_path.start_with?("#{src_dir}/_drafts")
        'post'
      elsif md_path.start_with?('src/_til')
        'til'
      else
        'page'
      end

    if front_matter['layout'] != expected_layout
      errors[md_path] <<= "layout should be '#{expected_layout}'; got #{front_matter['layout']}"
    end
  end

  report_errors(errors)
end

# Check my Netlify redirects point to real pages.
#
# This ensures that any redirects I create are working.  It doesn't mean
# I can't forget to create a redirect, but it does mean I won't create
# a redirect that points to another broken page.
def check_netlify_redirects(dst_dir)
  info('Checking Netlify redirect rules...')

  bad_lines = []

  parse_netlify_redirects("#{dst_dir}/_redirects").each do |redirect|
    # A couple of special cases that I don't worry about.
    next if redirect[:source] == '/ideas-for-inclusive-events/*'
    next if redirect[:target].start_with? 'https://social.alexwlchan.net/'

    # ignore URL fragments when linting, the important thing is that
    # pages don't 404
    target = redirect[:target].split('#')[0].split('?')[0]

    expected_file =
      if target.end_with? '/'
        "#{dst_dir}#{target}/index.html"
      else
        "#{dst_dir}/#{target}"
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

def report_errors(errors)
  # This is meant to look similar to the output from HTMLProofer --
  # errors are grouped by filename, so they can be easily traced
  # back to the problem file.
  return if errors.empty?

  errors.each do |display_path, messages|
    error("- #{display_path}")
    messages.each do |m|
      error("  *  #{m}")
    end
  end
  exit!
end

html_dir = '_site'
src_dir = 'src'

check_with_html_proofer(html_dir)

check_writing_has_been_archived(src_dir)
check_yaml_front_matter(src_dir)
check_netlify_redirects(html_dir)
check_all_urls_are_hackable(html_dir)
