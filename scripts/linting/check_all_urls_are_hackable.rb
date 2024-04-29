# Check that every URL is "hackable".
#
# Quoting the slightly formal language of Nielsen Norman [1]:
#
#     A usable site requires […] URLs that are "hackable" to allow users
#     to move to higher levels of the information architecture by hacking
#     off the end of the URL
#
# Let's make sure I'm doing that!
#
# This means that every "hackable" URL should either exist in the site,
# or there should be a redirect for it.

require 'pathname'

require_relative 'logging'
require_relative 'netlify_redirects'

# Given a path, return a list of all its parent directories.
#
# For example:
#
#     get_all_parent_directories("/blog/2013/01/my-post/index.html")
#      => ["/blog/2013/01/my-post",
#          "/blog/2013/01",
#          "/blog/2013",
#          "/blog"]
#
def get_all_parent_directories(path)
  dirs = []

  path = Pathname.new(path)

  while (path = path.parent)
    if path == Pathname.new('.') || path == Pathname.new('/')
      break
    end

    dirs << path.to_s
  end

  dirs
end

def check_all_urls_are_hackable(dst_dir)
  info('Checking all URLs are hackable...')

  # Get a list of which paths will return an HTML page.
  #
  # This means either:
  #
  #     - There's a Netlify redirect that takes you to another page, or
  #     - There's a folder with an index.html file that will be served
  #
  # The goal is to have two sets of URLs without trailing slashes,
  # e.g. {'/writing', '/til'}
  #
  redirects = parse_netlify_redirects("#{dst_dir}/_redirects").to_set { |r| r[:source].chomp('/') }
  folders_with_index_html = Dir.glob("#{dst_dir}/**/index.html").map { |p| File.dirname(p).gsub(dst_dir, '') }

  # Work out all the URLs that somebody could "hack" their way towards.
  #
  # e.g. if there's a file `/blog/2013/01/my-post/index.html` which will
  # be served from `/blog/2013/01/my-post`, then somebody could hack
  # their way to get to:
  #
  #     - /
  #     - /blog/
  #     - /blog/2013/
  #     - /blog/2013/01/
  #
  hackable_urls = Dir.glob("#{dst_dir}/**/*.html")
                     .reject { |p| p.start_with?("#{dst_dir}/files/") }
                     .flat_map { |p| get_all_parent_directories(p.gsub(dst_dir, '')) }
                     .to_set

  # Now go through and work out which URLs are unreachable.
  unreachable_urls = hackable_urls - (redirects + folders_with_index_html)

  return if unreachable_urls.empty?

  error('- Missing pages/redirects!')
  error('  The following URLs can be "hacked" but won’t resolve:')
  unreachable_urls.sort.each do |url|
    error("  * #{url}/")
  end
  error('  Considering adding an entry in src/_redirects')
  exit!
end

if __FILE__ == $PROGRAM_NAME
  check_all_urls_are_hackable('_site')
end
