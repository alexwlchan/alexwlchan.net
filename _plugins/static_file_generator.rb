module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      system('mkdir -p _site'); # We may be called before _site exists.
      site.keep_files.each { |dir|
        if !system("rsync --archive --delete _#{dir}/ _site/#{dir}/")
          raise RuntimeError, "Error running the static file rsync for #{dir}!"
        end
      }
    end
  end
end
