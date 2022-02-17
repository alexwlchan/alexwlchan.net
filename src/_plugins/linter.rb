require "html-proofer"
require "nokogiri"
require "uri"
require "yaml"


class RunLinting < Jekyll::Command
  class << self
    def init_with_program(prog)
      prog.command(:lint) do |cmd|
        cmd.action do |_, options|
          options = configuration_from_options(options)

          check_writing_has_been_archived(options["source"])
          run_html_linting(options["destination"])
          check_social_card_images(options["destination"])
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

    # This checks that all my Twitter/OpenGraph cards point at images
    # that actually exists.
    def check_social_card_images(html_dir)
      has_errors = false

      Dir["#{html_dir}/**/*.html"].each { |html_path|

        # Anything in the /files/ directory can be ignored, because it's
        # not part of the site, it's a static asset.
        if html_path.include? "/files/"
          next
        end

        doc = Nokogiri::HTML(File.open(html_path))

        twitter_cards = doc.xpath("//meta[@name='twitter:image']")

        if twitter_cards.length != 1
          puts "#{html_path} is missing a Twitter card"
          has_errors = true
        end

        twitter_cards.each { |twitter_meta|
          uri = URI(twitter_meta.attribute('content'))
          if !File.exist? "#{html_dir}#{uri.path}"
            puts "#{html_path} has a Twitter card pointing to a missing image"
            has_errors = true
          end
        }

        opengraph_cards = doc.xpath("//meta[@property='og:image']")

        if opengraph_cards.length != 1
          puts "#{html_path} is missing an OpenGraph card"
          has_errors = true
        end

        opengraph_cards.each { |og_meta|
          uri = URI(og_meta.attribute('content'))
          if !File.exist? "#{html_dir}#{uri.path}"
            puts "#{html_path} has a OpenGraph card pointing to a missing image"
            has_errors = true
          end
        }
      }

      if has_errors
        exit!
      end
    end
  end
end
