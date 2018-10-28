# This is a plugin for embedding Flickr images.
#
# The ID needs to have a corresponding entry in the _flickr directory with image
# size data.
#
#     {% flickr 31732158558 %}
#
# You can also use flickr_captioned if you want a <figcaption> on the slide
# (e.g. to add image attribution):
#
#     {% flickr_captioned 2 %}
#       This slide uses an image from https://example.org/
#     {% flickr_captioned %}
#

require 'fileutils'
require 'json'

USER_ID = "165615218"

module Jekyll
  class FlickrTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @photo_id = text.strip
    end

    def render(context)
      get_image_tag(@photo_id)
    end
  end

  class FlickrCaptionedTag < Liquid::Block
    def initialize(tag_name, text, tokens)
      super
      @photo_id = text.strip
    end

    def render(context)
      site = context.registers[:site]
      converter = site.find_converter_instance(::Jekyll::Converters::Markdown)

      md_content = super.strip
      html_content = converter.convert(md_content)

<<-EOT
<figure>
  #{get_image_tag(@photo_id)}
  <figcaption>#{html_content}</figcaption>
</figure>
EOT
    end
  end
end

def get_image_tag(photo_id)
  flickr_data = get_flickr_data(photo_id)
  sizes = Hash[
    flickr_data.map { |size| [size["label"], size["source"]] }
  ]

<<-EOT
<a href="https://www.flickr.com/photos/#{USER_ID}@N03/#{photo_id}/">
<img
  src="#{sizes["Large"]}"
  srcset="#{sizes["Large"]} 1x, #{sizes["Large 2048"]} 2x, #{sizes["Original"]} 4x">
</a>
EOT
end

def get_flickr_data(photo_id)
  JSON.parse(File.read("src/_flickr/photo_#{photo_id}.json"))
end

Liquid::Template.register_tag('flickr', Jekyll::FlickrTag)
Liquid::Template.register_tag("flickr_captioned", Jekyll::FlickrCaptionedTag)
