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

require "fileutils"
require "rszr"

Jekyll::Hooks.register :site, :post_read do |site|
  site.posts.docs.each { |p|
    year = p.date.year
    slug = p.data["slug"]

    matching_images = Dir["src/_images/cards/#{year}/#{slug}.*"]

    # If there are no cards, then both the social and index card should
    # use the default image.  Note that the social cards behave slightly
    # different in this case, so we defer the default to the template.
    if matching_images.empty?
      next
    end

    # Now work out which image is which the card for social media, which is
    # the card for the site-wide index (which may be different).
    if matching_images.length == 2
      index_card = matching_images.find { |p| p.include? ".index." }
      social_card = matching_images.find { |p| p.include? ".social." }
    else
      index_card = social_card = matching_images[0]
    end
    
    # Make sure we save a copy of the social card at the right size; this
    # won't be sent with srcset or similar.
    social_card_out = social_card.gsub('src/_images', '_site/images')
    
    # Create an image which is at least 800px wide, and at most 1000px wide.
    if !File.exist? social_card_out
      image = Rszr::Image.load(social_card)
      
      out_width = [[image.width, 800].max, 1000].min
      
      open(".missing_images.json", "a") { |f|
        f.puts JSON.generate({
          "out_path": social_card_out,
          "source_path": social_card,
          "width": out_width
        })
      }
    end

    # Now we attach enough data to the post that the downstream components
    # can render the necessary HTML.
    p.data["card"] = {
      "social" => File.basename(social_card),
      "index" => File.basename(index_card),
    }
  }
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
      post = context['post']
      
      if context['post']['card'].nil?
        <<-EOF
<img
  src="/images/default-card.png"
  alt=""
  loading="lazy"
  data-proofer-ignore
/>
EOF
      else
        input = <<-EOF
{%
  picture
  filename="#{post['card']['index']}"
  parent="/images/cards/#{post['date'].year}"
  visible_width="400px"
  alt=""
  loading="lazy"
  data-proofer-ignore
%}
EOF
      
        Liquid::Template.parse(input).render!(context)
      end
    end
  end
end

Liquid::Template.register_tag("card_image", Jekyll::CardImageTag)
