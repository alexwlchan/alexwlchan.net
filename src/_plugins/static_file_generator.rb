# This plugin copies static files from the "source" to the
# "destination" directory.  This speeds up site generation times -- it's
# an idea I got from this blog post:
# http://rentzsch.tumblr.com/post/58936832594/
#
# The directories which are copied are set with the `keep_files` setting
# in `_config.yml`.
#

module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      src = site.config["source"]
      dst = site.config["destination"]

      # We may be called before the destination directory exists
      system("mkdir -p #{dst}");

      site.keep_files.each { |dir|
        if !system("rsync --archive --delete #{src}/_#{dir}/ #{dst}/#{dir}/ --exclude=twitter/avatars")
          raise RuntimeError, "Error running the static file rsync for #{dir}!"
        end
      }
    end
  end
end
