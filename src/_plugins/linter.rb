require "html-proofer"
require "nokogiri"
require "rainbow"
require "rszr"
require "uri"
require "yaml"


class RunLinting < Jekyll::Command
  class << self
    def init_with_program(prog)
      prog.command(:lint) do |cmd|
        cmd.action do |_, options|
          options = configuration_from_options(options)

          run_html_linting(options["destination"])
          check_writing_has_been_archived(options["source"])
          check_twitter_card_images(options["destination"])
        end
      end
    end

    def run_html_linting(html_dir)
      HTMLProofer.check_directory(
        html_dir, opts = {
          :check_html => true,
          :check_img_http => true,
          :check_opengraph => true,
          :disable_external => true,
          :report_invalid_tags => true,
          :alt_ignore => [
            "/theme/file_javascript_2x.png",
            "/theme/file_python_2x.png",
            "/theme/file_zip_2x.png",
          ],
        }).run
    end

    # These commands are based on the logging in html-proofer; see
    # https://github.com/gjtorikian/html-proofer/blob/041bc94d4a029a64ecc1e48036e94eafbae6c4ad/lib/html_proofer/log.rb
    def info(message)
      puts Rainbow(message).send(:blue)
    end

    def error(message)
      puts Rainbow(message).send(:red)
    end

    # This checks that every article on /elsewhere/ has at least one copy
    # archived on my own computers.
    #
    # This means I'm not susceptible to link rot -- if one of my articles
    # is taken offline, I'll still have a copy.
    #
    # See also: https://www.stephaniemorillo.co/post/why-developers-should-archive-their-old-content

    #
    def check_writing_has_been_archived(src_dir)
      elsewhere = YAML.load_file("#{src_dir}/_data/elsewhere.yml")

      no_archive_writing = elsewhere["writing"]
        .filter { |w| !w.has_key? "archived_paths" }

      if !no_archive_writing.empty?
        puts "The following writing entries in 'elsewhere' have not been archived:"
        no_archive_writing
          .each { |w| puts w["url"] }
        puts "Please run 'python3 scripts/archive_elsewhere.py'"
        exit!
      end
    end

    # Validate the images used by my Twitter cards by checking that:
    #
    #   1. They point at images that actually exist
    #   2. I'm using a valid card type
    #   3. If the card type is "summary_large_image", the image has
    #      the 2:1 aspect ratio required by Twitter
    #
    def check_twitter_card_images(html_dir)
      errors = Hash.new { [] }

      info("Checking Twitter card metadata...")

      Dir["#{html_dir}/**/*.html"].each { |html_path|

        # Anything in the /files/ directory can be ignored, because it's
        # not part of the site, it's a static asset.
        #
        # e.g. if I've got a file that I'm using to demo a particular
        # HTML feature.
        if html_path.include? "/files/"
          next
        end

        doc = Nokogiri::HTML(File.open(html_path))
        meta_tags = doc.xpath("//meta")

        # Look up the Markdown file that was used to create this file.
        #
        # This means the error report can link to the source file, not
        # the rendered HTML file.
        md_path = doc.xpath("//meta[@name='page-source-path']").attribute('content')

        # Get a map of Twitter cards (name => content).
        #
        # This assumes that the meta tag for a given name is never duplicated,
        # which would only happen if I'd messed up one of the templates.
        # That's not the sort of thing this linting is meant to catch, so
        # the assumption is fine.
        twitter_cards = meta_tags
          .select { |mt|
            mt.attribute('name') != nil && mt.attribute('name').value.start_with?('twitter:')
          }
          .map { |mt| [mt.attribute('name').value, mt.attribute('content').value] }
          .to_h

        # e.g. http://0.0.0.0:5757/images/profile_red_square2.jpg
        #
        # This uses the site.uri variable, which varies based on the build
        # system running at the top. Discard it.
        image_path = URI(twitter_cards['twitter:image']).path

        local_image_path = "#{html_dir}#{image_path}"

        if !File.exist? local_image_path
          errors[md_path] <<= "Twitter card points to a missing image"
        end

        if twitter_cards['twitter:card'] != 'summary' && twitter_cards['twitter:card'] != 'summary_large_image'
          errors[md_path] <<= "Twitter card has an invalid card type #{twitter_cards['twitter:card']}"
        end

        # If it's a 'summary_large_image' card, check the aspect ratio is 2:1.
        #
        # Anything else will be cropped by Twitter's algorithm, which may
        # pick a bad crop.
        #
        # See https://alexwlchan.net/2022/02/two-twitter-cards/
        #
        if twitter_cards['twitter:card'] == 'summary_large_image'
          if File.exist? local_image_path
            image = Rszr::Image.load(local_image_path)
            if image.width != image.height * 2
              errors[md_path] <<= "summary_large_image Twitter card does not have a 2:1 aspect ratio"
            end
          end
        end

        # I could likewise inspect the OpenGraph metadata here, but it's all
        # pulled from the template using the same values as Twitter.
        #
        # If an image doesn't exist on the Twitter card, it won't exist on
        # the OpenGraph card either, and vice versa.
      }

      # This is meant to look similar to the output from HTMLProofer --
      # errors are grouped by filename, so they can be easily traced
      # back to the problem file.
      if !errors.empty?
        errors.each { |path, messages|
          error("- #{path}")
          messages.each { |m|
            error("  *  #{m}")
          }
        }
        exit!
      end
    end
  end
end
