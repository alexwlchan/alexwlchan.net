# This plugin copies static files from the "source" to the
# "destination" directory.  This speeds up site generation times -- it's
# an idea I got from this blog post:
# http://rentzsch.tumblr.com/post/58936832594/
#
# The directories which are copied are set with the `keep_files` setting
# in `_config.yml`.
#

require 'open3'

module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      src = site.config['source']
      dst = site.config['destination']

      # We may be called before the destination directory exists
      system("mkdir -p #{dst}")

      site.keep_files.each do |dir|
        next unless File.directory? "#{src}/_#{dir}"

        _, status = Open3.capture2('rsync', '--archive', "#{src}/_#{dir}/", "#{dst}/#{dir}/",
                                   '--exclude=social_embeds/avatars',
                                   '--exclude=social_embeds/twemoji',
                                   '--exclude=icons',
                                   '--exclude=*.svg')
        raise 'Unable to run static file rsync' unless status.success?
      end
    end
  end
end
