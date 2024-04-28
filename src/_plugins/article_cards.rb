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

require_relative 'pillow/convert_image'
require_relative 'pillow/get_image_info'
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

    # Now we attach enough data to the post that the downstream components
    # can render the necessary HTML.
    post.data['card'] = {
      'attribution' => post.data['card_attribution'],
      'social' => File.basename(social_card),
      'index' => File.basename(index_card)
    }
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
          405, 405 * 2,  # 1-up column => ~405px wide
        ]

        sizes_attribute = "(max-width: 450px) 405px, (max-width: 1000px) 365px, 302px"

        year = article['date'].year

        source_path = "src/_images/cards/#{year}/#{card['index']}"
        dst_prefix = "_site/images/cards/#{year}/#{File.basename(card['index'], '.*')}"

        image = get_single_image_info(source_path)
        im_format = get_format(source_path, image)

        if image['width'] != image['height'] * 2
          raise "Card #{card['index']} doesn’t have a 2:1 aspect ratio"
        end

        sources = prepare_images(source_path, dst_prefix, im_format, widths)

        dark_source_path = File.join(
          File.dirname(source_path),
          "#{File.basename(source_path, File.extname(source_path))}.dark#{File.extname(source_path)}"
        )

        if File.exist? dark_source_path
          dark_image = get_single_image_info(dark_source_path)

          if dark_image['width'] != dark_image['height'] * 2
            raise "Card #{File.basename(dark_source_path)} doesn’t have a 2:1 aspect ratio"
          end

          dark_sources = prepare_images(dark_source_path, "#{dst_prefix}.dark", im_format, widths)
        else
          dark_sources = Hash.new
        end

        default_image = sources[im_format]
                        .map { |im| im.split[0] }
                        .find { |path| path.include? "_365" }

        dark_html = create_source_elements(
          dark_sources, im_format, {
            desired_formats:[im_format, ImageFormat::AVIF, ImageFormat::WEBP],
            sizes: sizes_attribute,
            dark_mode: true
          }
        )

        light_html = create_source_elements(
          sources, im_format, {
            desired_formats:[im_format, ImageFormat::AVIF, ImageFormat::WEBP],
            sizes: sizes_attribute,
            dark_mode: false
          }
        )

        # Make sure the CSS doesn't through a white background behind
        # this dark-aware image.
        if dark_sources.nil?
          css_class="c_image dark_aware"
        else
          css_class = "c_image"
        end

        # Intentionally omit the alt text on promos, so screen reader users
        # don't have to listen to the alt text before hearing the title
        # of the item in the list.
        #
        # See https://github.com/wellcomecollection/wellcomecollection.org/issues/6007
        <<~HTML
          <picture>
            #{dark_html}
            #{light_html}
            <img
              src="#{default_image}"
              class="#{css_class}"
              alt=""
              loading="lazy"
              style="aspect-ratio: 2 / 1;"
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
