# A generator for images used in "cards", which appear in two places:
#
#     - in social media previews
#     - in the site-wide index
#
# I put images whose path/name matches the slug of the original post in
# the `_cards` directory (e.g. `_cards/2021/kempisbot.jpg` is the card
# for the post `/2021/kempisbot/`).
#
# This generator will then create images in the appropriate size/format
# to use as cards.  This means:
#
#     - 400px and 800px wide variants, for 1x and 2x displays in the
#       site-wide index.  Also original and WebP variants for size.
#     - An 800px variant in the original format for use in social media
#       previews.
#
# All images _must_ have a 2:1 ratio.
#
# This process means I can put the highest resolution card images in the
# `src` directory, but the site doesn't pay a perf penalty.

require "fileutils"
require "rszr"
require "shellwords"

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

    # FileUtils.mkdir_p "_site/images/cards/#{year}"

    # For each matching source file in the card directory, create a 1x/2x
    # version of the card in the output directory.
    #
    # Cards are usually shown at ~350px wide.
    #
    # I'm using ImageMagick rather than the rszr gem because I can't seem
    # to get WebP images from rszr; if I try I get a slightly cryptic error:
    #
    #     Rszr::SaveError: Non-existant path component
    #
    # matching_images.each { |im_path|
    #   ext = File.extname(im_path)         # e.g. '.jpg'
    #   name = File.basename(im_path, ext)  # e.g. 'marquee-rocket'
    #
    #   for out_ext in [".webp", ext]
    #     out_path_1x = "_site/images/cards/#{year}/#{name}-1x#{out_ext}"
    #     out_path_2x = "_site/images/cards/#{year}/#{name}-2x#{out_ext}"
    #
    #     unless File.exist? out_path_1x
    #       `convert #{Shellwords.escape(im_path)} -background none -resize 400x200 #{Shellwords.escape(out_path_1x)}`
    #     end
    #
    #     unless File.exist? out_path_2x
    #       `convert #{Shellwords.escape(im_path)} -background none -resize 800x400 #{Shellwords.escape(out_path_2x)}`
    #     end
    #   end
    # }

    # Now work out which image is which the card for social media, which is
    # the card for the site-wide index (which may be different).
    if matching_images.length == 2
      index_card = matching_images.find { |p| p.include? ".index." }
      social_card = matching_images.find { |p| p.include? ".social." }
      
      puts social_card
      
    else
      index_card = social_card = matching_images[0]
    end

    # Now we attach enough data to the post that the downstream components
    # can render the necessary HTML.
    p.data["card"] = {
      "social" => {
        "name" => File.basename(social_card, File.extname(social_card)),
        "ext" => File.extname(social_card),
      },
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
