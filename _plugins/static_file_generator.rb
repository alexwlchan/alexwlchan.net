module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      system('mkdir -p _site'); # We may be called before _site exists.
      site.keep_files.each { |dir|
        system("rsync --archive --delete _#{dir}/ _site/#{dir}/");
      }
    end
  end
end
