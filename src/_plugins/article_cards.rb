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

require_relative 'utils/markdownify_oneline'
require_relative 'utils/pictures'

Jekyll::Hooks.register :site, :post_read do |site|
  (site.posts.docs + site.collections['til'].docs).each do |post|
    year = post.date.year
    slug = post.data['slug']

    matching_images = Dir["src/_images/cards/#{year}/#{slug}.*"]

    next unless matching_images.length == 1

    card_path = matching_images[0]

    # Make sure we save a copy of the social card at the right size; this
    # won't be sent with srcset or similar.
    convert_image({
                    'in_path' => card_path,
                    'out_path' => card_path.gsub('src/_images', '_site/images'),
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

      'name' => File.basename(card_path),
      'path' => card_path,

      'color_lt' => color_lt,
      'color_dk' => color_dk,
      'title' => title,
      'summary' => summary
    }
  end

  posts_with_index_cards = site.posts.docs
                               .reject { |p| p.data['card'].nil? }
                               .filter { |post| post.data.fetch('index', {}).fetch('feature', false) }

  # Set the "is_new" attribute on any posts which were published
  # in the last few weeks.
  posts_with_index_cards.each do |post|
    post.data['is_new'] = Time.now - post.data['date'] < 21 * 24 * 60 * 60
  end

  # Now work out unique abbrevations for the names of each card.
  #
  # Because these filenames will be used a lot on the global index page,
  # we don't want them to be longer than necessary.
  #
  # We construct minimal prefixes that uniquely identify each card name,
  # e.g. "digital-decluttering.jpg" might become "di", which is much shorter!

  # A list of card names e.g. "2025/cool-to-care.jpg", "2024/in-reading.png"
  index_names = posts_with_index_cards.map do |p|
    year = p.data['card']['year']
    name = p.data['card']['name']
    "#{year}/#{name}"
  end

  # A map from full card name to unique prefix,
  # e.g. "2025/cool-to-care.jpg" => "2025/c"
  index_prefixes = Abbrev.abbrev(index_names)
                         .group_by { |_, v| v }
                         .transform_values { |v| v.flatten.min_by(&:length) }

  # Add the prefix to each card object, without the year.
  posts_with_index_cards.each do |p|
    year = p.data['card']['year']
    name = p.data['card']['name']
    key = "#{year}/#{name}"

    p.data['card']['index_prefix'] = File.basename(
      index_prefixes[key].gsub("#{year}/", ''), '.*'
    )
  end

  # Go ahead and verify that all of the cards have a 2:1 aspect ratio.
  #
  # The "article card" component assumes that all these images have a 2:1
  # ratio, and I use the same -- different social media networks want
  # a slightly different ratio, but it's good enough.
  posts_with_index_cards.each do |post|
    card = post.data['card']

    index_im = get_single_image_info(card['path'])
    if index_im['width'] != index_im['height'] * 2
      raise "Card #{card['path']} doesn’t have a 2:1 aspect ratio"
    end

    # Create/queue resized versions of the index image.
    #
    # Save the metadata in the format to be passed into the <picture> template.
    card = post.data['card']

    # Where will this card be written?
    # e.g. _site/c/25/cool-to-care
    year = post.data['date'].year
    dst_prefix = "_site/c/#{year - 2000}/#{card['index_prefix']}"

    # What format do we want to create this card in?
    #
    # All three formats are fine.
    image = get_single_image_info(card['path'])
    desired_formats = [image['format'], ImageFormat::AVIF, ImageFormat::WEBP]

    # What widths do I want to create cards at?
    desired_widths = [
      365, 365 * 2,  # 2-up column => ~365px wide
      302, 302 * 2,  # 3-up column => ~302px wide
      405, 405 * 2 # 1-up column => ~405px wide
    ]
    target_width = nil

    # Create the various image sizes
    sources = create_image_sizes(
      card['path'],
      dst_prefix,
      desired_formats,
      desired_widths,
      target_width
    )

    # Choose the default/fallback image -- we use the 1x version of
    # the light image.  If you're running a browser which doesn't
    # know about the <picture> tag, you're unlikely to be on a
    # device with a hi-res screen or dark mode.
    default_image = sources[image['format']['mime_type']].split[0]

    sources = sources.map do |media_type, srcset|
      {
        'srcset' => srcset,
        'type' => media_type
      }
    end

    card['card_image'] = image

    card['card_image_template_params'] = {
      'sources' => sources,
      'default_image' => default_image
    }
  end
end
