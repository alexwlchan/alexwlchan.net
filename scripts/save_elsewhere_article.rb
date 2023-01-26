#!/usr/bin/env ruby
# Saves a new article to my "elsewhere" page [1].  This is a list of
# all the writing I've done that isn't on alexwlchan.net
#
# This script will:
#
#    - ask me about the article
#    - save the metadata to the YAML file that builds that page
#    - prompt me to save my own copies of the article
#
# The latter is important because I don't want to rely on external sites
# to be the sole copy of my writing [2].  This is also checked by the plugin
# that renders the elsewhere page, but it's good to have a prompt when
# I initially save the article.
#
# [1]: https://alexwlchan.net/elsewhere/
# [2]: https://www.stephaniemorillo.co/post/why-developers-should-archive-their-old-content

require 'fileutils'
require 'set'
require 'yaml'

require 'unidecode'

ELSEWHERE_YML_PATH = 'src/_data/elsewhere.yml'
ARCHIVE_DIR = '/Volumes/Media (Sapphire)/backups/alexwlchan.net/elsewhere'

def ask_question(question)
  puts question
  print '> '
  gets.delete "\n"
end

def ask_for_metadata
  title = ask_question "What's the title of the article?"
  url = ask_question "What's the URL?"

  publication = if url.start_with? 'https://www.lastweekinaws.com/blog/'
                  'Last Week in AWS'
                elsif url.start_with? 'https://stacks.wellcomecollection.org/'
                  'Wellcome Collection development blog'
                else
                  ask_question 'Where was it published?'
                end

  date = ask_question 'When was it published?'

  {
    'title' => title,
    'url' => url,
    'publication' => publication,
    'date' => date
  }
end

def slugify(url)
  # Convert Unicode string into blog slug.
  #
  # Based on http://www.leancrew.com/all-this/2014/10/asciifying/
  u = url.gsub(%r{[–—/:;,.]}, '-') # replace separating punctuation
  a = u.to_ascii.downcase         # best ASCII substitutions, lowercased
  a = a.gsub(/[^a-z0-9 -]/, '')   # delete any other characters
  a = a.sub(' ', '-')             # spaces to hyphens
  a.gsub(/-+/, '-')               # condense repeated hyphens
end

def archive_dir_for(url)
  slug = slugify(
    url
      .sub('https://', '')
      .sub('www.', '')
      .sub('lastweekinaws.com/blog/', 'lastweekinaws/')
  ).chomp('-')

  File.join(ARCHIVE_DIR, slug)
end

metadata = ask_for_metadata

archive_dir = archive_dir_for(metadata['url'])
FileUtils.mkdir_p archive_dir

puts "Archive directory: #{archive_dir}"
puts 'Have you saved archive copies?'
gets

metadata['archived_paths'] = Dir.glob(archive_dir + '/*')

elsewhere = YAML.load(File.read(ELSEWHERE_YML_PATH))
elsewhere['writing'] << metadata
File.write(ELSEWHERE_YML_PATH, elsewhere.to_yaml)

# This will trigger a rebuild of /elsewhere/ if I'm running a local dev
# server, so I'll see my changes reflected on the site.
FileUtils.touch('src/elsewhere.md')
