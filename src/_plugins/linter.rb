require "html-proofer"
require "json"
require "json-schema"
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
          check_card_images(options["destination"])
          check_yaml_front_matter(options["source"])
          check_no_localhost_links(options["destination"])
          check_all_images_are_srgb(options["destination"])
          check_netlify_redirects(options["destination"])
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
      elsewhere = YAML.load_file(
        "#{src_dir}/_data/elsewhere.yml",
        permitted_classes: [Date]
      )

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
    def check_card_images(html_dir)
      errors = Hash.new { [] }

      info("Checking social sharing card images...")

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
        display_path = get_display_path(doc)

        meta_tags = doc.xpath("//meta")

        # Get a map of meta tag (name/property => content).
        #
        # This assumes that the meta tag for a given name is never duplicated,
        # which would only happen if I'd messed up one of the templates.
        # That's not the sort of thing this linting is meant to catch, so
        # the assumption is fine.
        meta_tags_map = meta_tags
          .reject { |mt| mt.attribute('name').nil? && mt.attribute('property').nil? }
          .reject { |mt| mt.attribute('content').nil? }
          .map { |mt|
            name = (mt.attribute('name') || mt.attribute('property')).value
            content = mt.attribute('content').value

            [name, content]
          }
          .to_h

        if meta_tags_map['twitter:card'] != 'summary' && meta_tags_map['twitter:card'] != 'summary_large_image'
          errors[display_path] <<= "Twitter card has an invalid card type #{meta_tags_map['twitter:card']}"
        end

        for image_name in ['twitter:image', 'og:image']
          # e.g. http://0.0.0.0:5757/images/profile_red_square2.jpg
          #
          # This uses the site.uri variable, which varies based on the build
          # system running at the top. Discard it.
          if meta_tags_map[image_name].nil?
            errors[display_path] <<= "Could not find `#{image_name}` attribute on page"
            next
          end

          image_path = URI(meta_tags_map[image_name]).path

          local_image_path = "#{html_dir}#{image_path}"

          if !File.exist? local_image_path
            errors[display_path] <<= "Card points to a missing image: #{local_image_path}"
          end

          # If it's a 'summary_large_image' card, check the aspect ratio is 2:1.
          #
          # Anything else will be cropped by Twitter's algorithm, which may
          # pick a bad crop.
          #
          # See https://alexwlchan.net/2022/02/two-twitter-cards/
          #
          if meta_tags_map['twitter:card'] == 'summary_large_image'
            if File.exist? local_image_path
              image = Rszr::Image.load(local_image_path)
              if image.width != image.height * 2
                errors[display_path] <<= "Card image does not have a 2:1 aspect ratio"
              end
            end
          end
        end
      }

      report_errors(errors)
    end

    # Validate the YAML front matter by checking that:
    #
    #   1. I'm not using undocumented fields
    #   2. Fields have appropriate values
    #
    def check_yaml_front_matter(src_dir)
      errors = Hash.new { [] }

      info("Checking YAML front matter...")

      schema = JSON.parse(File.open("front-matter.json").read)

      Dir["#{src_dir}/**/*.md"].each { |md_path|

        # Skip some Markdown files in the source directory that aren't
        # posts on the site and so don't need validating.
        if md_path.end_with?("theme/_favicons/README.md")
          next
        end

        # The YAML loader will try to be "smart" (e.g. reading dates as
        # proper Ruby date types), which is unhelpful for json-schema checking.
        #
        # Make sure everything is JSON-esque (i.e. strings/numbers/bools)
        # before passing to the json-schema gem.
        front_matter = YAML.load(
          File.open(md_path).read.split("\n---\n")[0],
          permitted_classes: [Date, Time]
        )
        front_matter = JSON.parse(JSON.dump(front_matter))

        md_errors = JSON::Validator.fully_validate(schema, front_matter)

        if !md_errors.empty?
          errors[md_path] = md_errors
        end

        # This is to test some rules that can't easily be expressed
        # in a JSON schema definition.
        is_in_post_directory = (
          md_path.start_with?("src/_posts/") or
          md_path.start_with?("src/_drafts/")
        )

        if is_in_post_directory and front_matter["layout"] != "post"
          errors[md_path] <<= "layout should be 'post'"
        end

        if !is_in_post_directory and front_matter["layout"] != "page"
          errors[md_path] <<= "layout should be 'page'"
        end
      }

      report_errors(errors)
    end

    # Check I haven't used localhost URLs anywhere (in links or images)
    #
    # This is an error I've occasionally made while doing local development;
    # I'll use my ;furl snippet to get the front URL, and forget to remove
    # the localhost development prefix.
    def check_no_localhost_links(html_dir)
      errors = Hash.new { [] }

      info("Checking there aren’t any localhost links...")

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
        display_path = get_display_path(doc)

        localhost_links = doc.xpath("//a")
          .select { |a|
            a.attribute('href') != nil &&
            a.attribute("href").value.start_with?("http") &&
            a.attribute('href').value.include?("localhost:5757")
          }
          .map { |a| a.attribute('href').value }

        if !localhost_links.empty?
          errors[display_path] <<= "There are links to localhost: #{localhost_links.join("; ")}"
        end
      }

      report_errors(errors)
    end

    # Check every image uses an sRGB colour profile.
    #
    # This ensures images should display with consistent colour on all browsers
    # and devices; my iMac in particular uses a Display P3 colour profile for
    # screenshots and images which looks washed out on non-Apple displays.
    def check_all_images_are_srgb(dst_dir)
      errors = Hash.new { [] }

      info("Checking image colour profiles...")

      safe_colour_profiles = Set["sRGB"]

      exiftool_output = `exiftool -quiet -quiet -printFormat '$directory/$filename : $profileDescription' #{dst_dir}/images/**`

      image_profiles = exiftool_output
        .split("\n")
        .sort
        .map { |line|
          path, profile = line.split(":")
          path = path.strip!
          profile = profile.strip!
          [path, profile]
        }
        .map { |path, profile|
          if !safe_colour_profiles.include? profile
            errors[path] <<= "Image has an unrecognised colour profile: #{profile}"
          end
        }

      report_errors(errors)
    end

    # Check my Netlify redirects point to real pages.
    #
    # This ensures that any redirects I create are working.  It doesn't mean
    # I can't forget to create a redirect, but it does mean I won't create
    # a redirect that points to another broken page.
    def check_netlify_redirects(dst_dir)
      info("Checking Netlify redirect rules...")

      bad_lines = []

      File.readlines("#{dst_dir}/_redirects")
        .each_with_index { |line, i|
          lineno = i + 1

          if line.start_with? "#" or line.strip.empty?
            next
          end

          # This is a bit of a special case that I don't worry about.
          if line.start_with? "/ideas-for-inclusive-events/"
            next
          end

          target = line.strip.split()[1]

          # Another special case
          if target == "/#contact"
            next
          end

          if target.end_with? "/"
            if !File.exist? "#{dst_dir}#{target}/index.html"
              bad_lines << [lineno, line.strip]
            end
          else
            if !File.exist? "#{dst_dir}#{target}"
              bad_lines << [lineno, line.strip]
            end
          end
        }

      if !bad_lines.empty?
        error("- src/_redirects")
        error("  The following lines are redirecting to broken resources:")
        bad_lines.each { |ln|
          lineno, line = ln
          error("  * L#{lineno}:\t#{line}")
        }
        exit!
      end
    end

    def report_errors(errors)
      # This is meant to look similar to the output from HTMLProofer --
      # errors are grouped by filename, so they can be easily traced
      # back to the problem file.
      if !errors.empty?
        errors.each { |display_path, messages|
          error("- #{display_path}")
          messages.each { |m|
            error("  *  #{m}")
          }
        }
        exit!
      end
    end

    def get_display_path(doc)
      # Look up the Markdown file that was used to create this file.
      #
      # This means the error report can link to the source file, not
      # the rendered HTML file.
      #
      # Note that we may fail to retrieve this value if for some reason
      # the `<meta>` tag hasn't been written properly, in which case
      # we show the HTML path instead.
      md_path = doc.xpath("//meta[@name='page-source-path']").attribute('content')

      md_path == "" ? html_path : "src/#{md_path}"
    end
  end
end
