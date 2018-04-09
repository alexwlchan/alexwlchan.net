module Jekyll
  class StaticFileGenerator < Generator
    def generate(site)
      src = site.config["source"]
      dst = site.config["destination"]

      # We may be called before the destination directory exists
      system("mkdir -p #{dst}");

      site.keep_files.each { |dir|
        if !system("rsync --archive --delete #{src}/_#{dir}/ #{dst}/#{dir}/")
          raise RuntimeError, "Error running the static file rsync for #{dir}!"
        end
      }
    end
  end
end
