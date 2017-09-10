module Jekyll
    class StaticFileGenerator < Generator
        def generate(site)
            system('mkdir -p _site'); # We may be called before _site exists.
            system('rsync --archive --delete _images/ _site/images/');
            system('rsync --archive --delete _videos/ _site/videos/');
        end
    end
end
