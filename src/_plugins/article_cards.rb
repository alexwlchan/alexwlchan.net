# frozen_string_literal: true

# Creates the images used in the cards, which appear on the site-wide index
# and in social media previews.
#
# == How to name cards ==
#
# Each post with a card should be named in one of two ways:
#
#     src/_images/cards/#{year}/#{post_slug}.#{ext}
#
#     src/_images/cards/#{year}/#{post_slug}.index.#{ext}
#     src/_images/cards/#{year}/#{post_slug}.social.#{ext}
#
# For example:
#
#     src/_images/cards/2020/a-sprinkling-of-azure.jpg
#
#     src/_images/cards/2022/circle-party.social.jpg
#     src/_images/cards/2022/circle-party.index.png
#
# Depending on whether the same image should be used in both places, or if
# they have different cards.
#
# Card images should always have a 2:1 ratio.
#
# == What this plugin does ==
#
#   - It creates an appropriately resized version for social media.
#   - It uses the {% picture %} plugin to create appropriately sized versions
#     for the site-wide index.
#
# This plugin means I can put the highest resolution card images in the
# `src` directory, but the site doesn't pay a perf penalty.

require 'abbrev'

require_relative 'pillow/convert_image'
require_relative 'pillow/get_image_info'
require_relative 'utils/markdownify_oneline'
require_relative 'utils/pictures'

Jekyll::Hooks.register :site, :post_read do |site|
  site.posts.docs.each do |post|
    year = post.date.year
    slug = post.data['slug']

    matching_images = Dir["src/_images/cards/#{year}/#{slug}.*"]

    # If there are no cards, then both the social and index card should
    # use the default image.  Note that the social cards behave slightly
    # different in this case, so we defer the default to the template.
    next if matching_images.empty?

    # Now work out which image is which the card for social media, which is
    # the card for the site-wide index (which may be different).
    if matching_images.length == 2
      index_card = matching_images.find { |p| p.include? '.index.' }
      social_card = matching_images.find { |p| p.include? '.social.' }
    else
      index_card = social_card = matching_images[0]
    end

    # Make sure we save a copy of the social card at the right size; this
    # won't be sent with srcset or similar.
    convert_image({
                    'in_path' => social_card,
                    'out_path' => social_card.gsub('src/_images', '_site/images'),
                    'target_width' => 800
                  })

    # Fetch the card colours to use on the index card.
    post_colors = post.data.fetch('colors', {})
    color_lt = post_colors.fetch('index_light', post_colors.fetch('css_light', nil))
    color_dk = post_colors.fetch('index_dark', post_colors.fetch('css_dark', nil))

    title = apply_markdownify_oneline(site, post.data['title'])
    if post.data['summary'].nil?
      summary = nil
    else
      summary = apply_markdownify_oneline(site, post.data['summary'])
    end

    # Now we attach enough data to the post that the downstream components
    # can render the necessary HTML.
    post.data['card'] = {
      'attribution' => post.data['card_attribution'],
      'year' => year,
      'social' => File.basename(social_card),
      'index' => File.basename(index_card),

      'color_lt' => color_lt,
      'color_dk' => color_dk,
      'title' => title,
      'summary' => summary,
    }
  end

  posts_with_cards = site.posts.docs.reject { |p| p.data['card'].nil? }

  # Now work out unique abbrevations for the names of each card.
  #
  # Because these filenames will be used a lot on the global index page,
  # we don't want them to be longer than necessary.
  #
  # We construct minimal prefixes that uniquely identify each card name,
  # e.g. "digital-decluttering.jpg" might become "di", which is much shorter!

  # A list of card names e.g. "2025/cool-to-care.jpg", "2024/in-reading.png"
  index_names = posts_with_cards.map do |p|
    year = p.data['card']['year']
    index = p.data['card']['index']
    "#{year}/#{index}"
  end

  # A map from full card name to unique prefix,
  # e.g. "2025/cool-to-care.jpg" => "2025/c"
  index_prefixes = Abbrev.abbrev(index_names)
                         .group_by { |_, v| v }
                         .transform_values { |v| v.flatten.min_by(&:length) }

  # Add the prefix to each card object, without the year.
  posts_with_cards.each do |p|
    year = p.data['card']['year']
    index = p.data['card']['index']
    key = "#{year}/#{index}"

    p.data['card']['index_prefix'] = index_prefixes[key].gsub("#{year}/", '')
  end
end

module Jekyll
  class CardImageTag < Liquid::Tag
    def render(context)
      article = context['article']
      card = article['card']

      if card.nil?
        <<~HTML
          <img
            src="/images/default-card.png"
            alt=""
            loading="lazy"
            data-proofer-ignore
          />
        HTML
      else

        # What widths do I want to create cards at?
        widths = [
          302, 302 * 2,  # 3-up column => ~302px wide
          365, 365 * 2,  # 2-up column => ~365px wide
          405, 405 * 2 # 1-up column => ~405px wide
        ]

        sizes_attribute = '(max-width: 450px) 405px, 405px'

        year = article['date'].year

        source_path = "src/_images/cards/#{year}/#{card['index']}"
        dst_prefix = "_site/c/#{year - 2000}/#{File.basename(card['index_prefix'], '.*')}"

        image = get_single_image_info(source_path)
        im_format = get_format(source_path, image)

        if image['width'] != image['height'] * 2
          raise "Card #{card['index']} doesn’t have a 2:1 aspect ratio"
        end

        sources = prepare_images(source_path, dst_prefix, im_format, widths)

        default_image = sources[im_format]
                        .map { |im| im.split[0] }
                        .find { |path| path.include? '_365' }

        light_html = create_source_elements(
          sources, im_format, {
            desired_formats: [im_format, ImageFormat::AVIF, ImageFormat::WEBP],
            sizes: sizes_attribute,
            dark_mode: false
          }
        )

        css_class = 'c_image'

        # Intentionally omit the alt text on promos, so screen reader users
        # don't have to listen to the alt text before hearing the title
        # of the item in the list.
        #
        # See https://github.com/wellcomecollection/wellcomecollection.org/issues/6007
        <<~HTML
          <picture>
            #{light_html}
            <img
              src="#{default_image}"
              class="#{css_class}"
              alt=""
              loading="lazy"
            >
          </picture>
        HTML
      end
    end

    def prepare_images(source_path, dst_prefix, im_format, widths)
      sources = Hash.new { [] }

      desired_formats = [im_format, ImageFormat::AVIF, ImageFormat::WEBP]

      widths.each do |this_width|
        desired_formats.each do |out_format|
          out_path = "#{dst_prefix}_#{this_width}w#{out_format[:extension]}"

          request = { 'in_path' => source_path, 'out_path' => out_path, 'target_width' => this_width }
          convert_image(request)

          sources[out_format] <<= "#{out_path.gsub('_site', '')} #{this_width}w"
        end
      end

      sources
    end
  end
end

Liquid::Template.register_tag('card_image', Jekyll::CardImageTag)
