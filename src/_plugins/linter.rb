# frozen_string_literal: true

require 'html-proofer'
require 'json'
require 'json-schema'
require 'nokogiri'
require 'rainbow'
require 'rszr'
require 'uri'
require 'yaml'

class RunLinting < Jekyll::Command
  class << self
    def init_with_program(prog)
      prog.command(:lint) do |cmd|
        cmd.action do |_, options|
          options = configuration_from_options(options)

          src_dir = options['source']
          html_dir = options['destination']

          run_html_linting(html_dir)

          html_documents = get_html_documents(html_dir)

          check_writing_has_been_archived(src_dir)
          check_card_images(html_dir, html_documents)
          check_yaml_front_matter(src_dir)
          check_no_localhost_links(html_documents)
          check_no_html_in_titles(html_documents)
          check_all_images_are_srgb(html_dir)
          check_netlify_redirects(html_dir)
        end
      end
    end

    def run_html_linting(html_dir)
      HTMLProofer.check_directory(
        html_dir, {
          check_html: true,
          check_img_http: true,
          check_opengraph: true,
          disable_external: true,
          report_invalid_tags: true
        }
      ).run
    end

    # These commands are based on the logging in html-proofer; see
    # https://github.com/gjtorikian/html-proofer/blob/041bc94d4a029a64ecc1e48036e94eafbae6c4ad/lib/html_proofer/log.rb
    def info(message)
      puts Rainbow(message).send(:blue)
    end

    def error(message)
      puts Rainbow(message).send(:red)
    end

    # Parse all the generated HTML documents with Nokogiri.
    def get_html_documents(html_dir)
      Dir["#{html_dir}/**/*.html"]
        # Anything in the /files/ directory can be ignored, because it's
        # not part of the site, it's a static asset.
        #
        # e.g. if I've got a file that I'm using to demo a particular
        # HTML feature.
        .filter { |html_path| !html_path.include? '/files' }
        # This page is a special case for crawlers and doesn't count for
        # the purposes of linting and the like.
        .filter { |html_path| html_path != "#{html_dir}/400/index.html" }
        .map do |html_path|
          doc = Nokogiri::HTML(File.open(html_path))
          display_path = get_display_path(html_path, doc)

          {
            display_path:,
            doc:
          }
        end
    end

    # This checks that every article on /elsewhere/ has at least one copy
    # archived on my own computers.
    #
    # This means I'm not susceptible to link rot -- if one of my articles
    # is taken offline, I'll still have a copy.
    #
    # See also: https://www.stephaniemorillo.co/post/why-developers-should-archive-their-old-content

    def check_writing_has_been_archived(src_dir)
      elsewhere = YAML.load_file(
        "#{src_dir}/_data/elsewhere.yml",
        permitted_classes: [Date]
      )

      no_archive_writing = elsewhere['writing']
                           .filter { |w| !w.key? 'archived_paths' }

      return if no_archive_writing.empty?

      puts "The following writing entries in 'elsewhere' have not been archived:"
      no_archive_writing
        .each { |w| puts w['url'] }
      puts "Please run 'python3 scripts/archive_elsewhere.py'"
      exit!
    end

    # Validate the images used by my Twitter cards by checking that:
    #
    #   1. They point at images that actually exist
    #   2. I'm using a valid card type
    #   3. If the card type is "summary_large_image", the image has
    #      the 2:1 aspect ratio required by Twitter
    #
    def check_card_images(html_dir, html_documents)
      errors = Hash.new { [] }

      info('Checking social sharing card images...')

      html_documents.each do |html_doc|
        meta_tags = html_doc[:doc].xpath('//meta')

        # Get a map of meta tag (name/property => content).
        #
        # This assumes that the meta tag for a given name is never duplicated,
        # which would only happen if I'd messed up one of the templates.
        # That's not the sort of thing this linting is meant to catch, so
        # the assumption is fine.
        meta_tags_map = meta_tags
                        .reject { |mt| mt.attribute('name').nil? && mt.attribute('property').nil? }
                        .reject { |mt| mt.attribute('content').nil? }
                        .to_h do |mt|
                          name = (mt.attribute('name') || mt.attribute('property')).value
                          content = mt.attribute('content').value

                          [name, content]
                        end

        if meta_tags_map['twitter:card'] != 'summary' && meta_tags_map['twitter:card'] != 'summary_large_image'
          errors[html_doc[:display_path]] <<= "Twitter card has an invalid card type #{meta_tags_map['twitter:card']}"
        end

        ['twitter:image', 'og:image'].each do |image_name|
          # e.g. http://0.0.0.0:5757/images/profile_red_square2.jpg
          #
          # This uses the site.uri variable, which varies based on the build
          # system running at the top. Discard it.
          if meta_tags_map[image_name].nil?
            errors[html_doc[:display_path]] <<= "Could not find `#{image_name}` attribute on page"
            next
          end

          image_path = URI(meta_tags_map[image_name]).path

          local_image_path = "#{html_dir}#{image_path}"

          unless File.exist? local_image_path
            errors[html_doc[:display_path]] <<= "Card points to a missing image: #{local_image_path}"
          end

          # If it's a 'summary_large_image' card, check the aspect ratio is 2:1.
          #
          # Anything else will be cropped by Twitter's algorithm, which may
          # pick a bad crop.
          #
          # See https://alexwlchan.net/2022/02/two-twitter-cards/
          #
          next unless meta_tags_map['twitter:card'] == 'summary_large_image'

          next unless File.exist? local_image_path

          image = Rszr::Image.load(local_image_path)
          errors[html_doc[:display_path]] <<= 'Card image does not have a 2:1 aspect ratio' if image.width != image.height * 2
        end
      end

      report_errors(errors)
    end

    # Validate the YAML front matter by checking that:
    #
    #   1. I'm not using undocumented fields
    #   2. Fields have appropriate values
    #
    def check_yaml_front_matter(src_dir)
      errors = Hash.new { [] }

      info('Checking YAML front matter...')

      schema = JSON.parse(File.read('front-matter.json'))

      Dir["#{src_dir}/**/*.md"].each do |md_path|
        # Skip some Markdown files in the source directory that aren't
        # posts on the site and so don't need validating.
        next if md_path.end_with?('theme/_favicons/README.md')

        # This page is a special case for crawlers and doesn't count for
        # the purposes of linting and the like.
        next if md_path == "#{src_dir}/400.md"

        # The YAML loader will try to be "smart" (e.g. reading dates as
        # proper Ruby date types), which is unhelpful for json-schema checking.
        #
        # Make sure everything is JSON-esque (i.e. strings/numbers/bools)
        # before passing to the json-schema gem.
        front_matter = YAML.load(
          File.read(md_path).split("\n---\n")[0],
          permitted_classes: [Date, Time]
        )
        front_matter = JSON.parse(JSON.dump(front_matter))

        md_errors = JSON::Validator.fully_validate(schema, front_matter)

        errors[md_path] = md_errors unless md_errors.empty?

        # This is to test some rules that can't easily be expressed
        # in a JSON schema definition.
        is_in_post_directory = (
          md_path.start_with?('src/_posts/') or
          md_path.start_with?('src/_drafts/')
        )

        errors[md_path] <<= "layout should be 'post'" if is_in_post_directory && front_matter['layout'] != 'post'

        errors[md_path] <<= "layout should be 'page'" if !is_in_post_directory && front_matter['layout'] != 'page'
      end

      report_errors(errors)
    end

    def localhost_link?(anchor_tag)
      !anchor_tag.attribute('href').nil? &&
        anchor_tag.attribute('href').value.start_with?('http') &&
        anchor_tag.attribute('href').value.include?('localhost:5757')
    end

    # Check I haven't used localhost URLs anywhere (in links or images)
    #
    # This is an error I've occasionally made while doing local development;
    # I'll use my ;furl snippet to get the front URL, and forget to remove
    # the localhost development prefix.
    def check_no_localhost_links(html_documents)
      errors = Hash.new { [] }

      info('Checking there aren’t any localhost links...')

      html_documents.each do |html_doc|
        localhost_links = html_doc[:doc].xpath('//a')
                                        .select { |a| localhost_link?(a) }
                                        .map { |a| a.attribute('href').value }

        unless localhost_links.empty?
          errors[html_doc[:display_path]] <<= "There are links to localhost: #{localhost_links.join('; ')}"
        end
      end

      report_errors(errors)
    end

    # Check I haven't got HTML in titles; this can break the formatting
    # of Google and social media previews.
    def check_no_html_in_titles(html_documents)
      errors = Hash.new { [] }

      info('Checking there isn’t any HTML in titles...')

      html_documents.each do |html_doc|
        # Look for HTML in the '<title>' element in the '<head>'.
        #
        # We can't just look for angle brackets, because at least one post
        # does have HTML-looking stuff in its title
        # (Remembering if a <details> element was opened).
        #
        # What we want to check is if there's any unescaped HTML that
        # needs removing.
        title = html_doc[:doc].xpath('//head/title').children

        if title.children.length > 1
          errors[html_doc[:display_path]] <<= "Title contains HTML: #{title}"
        end
      end

      report_errors(errors)
    end

    # Check every image uses an sRGB colour profile.
    #
    # This ensures images should display with consistent colour on all browsers
    # and devices; my iMac in particular uses a Display P3 colour profile for
    # screenshots and images which looks washed out on non-Apple displays.
    def check_all_images_are_srgb(dst_dir)
      errors = Hash.new { [] }

      info('Checking image colour profiles...')

      safe_colour_profiles = Set['sRGB']

      exiftool_output = `exiftool -quiet -quiet -printFormat '$directory/$filename : $profileDescription' #{dst_dir}/images/**`

      exiftool_output
        .split("\n")
        .sort
        .map do |line|
          path, profile = line.split(':')
          path = path.strip!
          profile = profile.strip!

          unless safe_colour_profiles.include? profile
            errors[path] <<= "Image has an unrecognised colour profile: #{profile}"
          end
        end

      report_errors(errors)
    end

    def parse_netlify_redirects(path)
      File.readlines(path).each_with_index
          .filter { |line, _i| !line.start_with? '#' }
          .filter { |line, _i| !line.strip.empty? }
          .map do |line, i|
            {
              line:,
              lineno: i + 1,
              source: line.strip.split[0],
              target: line.strip.split[1]
            }
          end
    end

    # Check my Netlify redirects point to real pages.
    #
    # This ensures that any redirects I create are working.  It doesn't mean
    # I can't forget to create a redirect, but it does mean I won't create
    # a redirect that points to another broken page.
    def check_netlify_redirects(dst_dir)
      info('Checking Netlify redirect rules...')

      bad_lines = []

      parse_netlify_redirects("#{dst_dir}/_redirects").each do |redirect|
        # A couple of special cases that I don't worry about.
        next if redirect[:source] == '/ideas-for-inclusive-events/*'
        next if redirect[:target].start_with? 'https://social.alexwlchan.net/'

        # ignore URL fragments when linting, the important thing is that
        # pages don't 404
        target = redirect[:target].split('#')[0]

        lineno = redirect[:lineno]
        line = redirect[:line]

        expected_file =
          if target.end_with? '/'
            "#{dst_dir}#{target}/index.html"
          else
            "#{dst_dir}/#{target}"
          end
        bad_lines << [lineno, line.strip] unless File.exist? expected_file
      end

      return if bad_lines.empty?

      error('- src/_redirects')
      error('  The following lines are redirecting to broken resources:')
      bad_lines.each do |ln|
        lineno, line = ln
        error("  * L#{lineno}:\t#{line}")
      end
      exit!
    end

    def report_errors(errors)
      # This is meant to look similar to the output from HTMLProofer --
      # errors are grouped by filename, so they can be easily traced
      # back to the problem file.
      return if errors.empty?

      errors.each do |display_path, messages|
        error("- #{display_path}")
        messages.each do |m|
          error("  *  #{m}")
        end
      end
      exit!
    end

    def get_display_path(html_path, doc)
      # Look up the Markdown file that was used to create this file.
      #
      # This means the error report can link to the source file, not
      # the rendered HTML file.
      #
      # Note that we may fail to retrieve this value if for some reason
      # the `<meta>` tag hasn't been written properly, in which case
      # we show the HTML path instead.
      md_path = doc.xpath("//meta[@name='page-source-path']").attribute('content')

      if md_path == '' || md_path.nil?
        html_path
      else
        "src/#{md_path}"
      end
    end
  end
end
