require 'shell/executer.rb'

module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      system('mkdir -p _site'); # We may be called before _site exists.
      site.keep_files.each { |dir|
        src = File.join(site.source, "_#{dir}")
        dst = File.join(site.source, "_site", dir)
        Shell.execute!("rsync --archive --delete #{src} #{dst}")
      }
    end
  end
end
