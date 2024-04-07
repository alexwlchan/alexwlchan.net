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
                    'width' => 800
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
    # Intentionally omit the alt text on promos, so screen reader users
    # don't have to listen to the alt text before hearing the title
    # of the item in the list.
    #
    # See https://github.com/wellcomecollection/wellcomecollection.org/issues/6007
    #
    # The data-proofer-ignore attribute will exclude this from the linting
    # that checks images have alt text.
    # See https://github.com/gjtorikian/html-proofer#ignoring-content
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
        attribution_text = card['attribution'].nil? ? '' : "data-attribution=\"#{card['attribution']}\""

        input = <<~HTML
          {%
            picture
            filename="#{card['index']}"
            parent="/images/cards/#{article['date'].year}"
            width="400"
            max_width="800"
            alt=""
            loading="lazy"
            class="c_image"
            #{attribution_text}
            data-proofer-ignore
          %}
        HTML

        Liquid::Template.parse(input).render!(context)
      end
    end
  end
end

Liquid::Template.register_tag('card_image', Jekyll::CardImageTag)
