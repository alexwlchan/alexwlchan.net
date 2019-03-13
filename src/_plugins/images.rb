require_relative "alexwlchan_base"
require_relative "html_tag_builder"

include ::HtmlTagBuilder::Helper


def render_image(title:, **attrs)
  tag.a(href: attrs[:src]) do |inner|
    inner.tag("img", **attrs)
  end
end


module Jekyll
  class PostImageTag < Alexwlchan::Tag
    def bind_params(params)
      @params = params
      params[:filename] or raise SyntaxError, "Error in tag 'image', :filename parameter is required"
      params[:alt] or raise SyntaxError, "Error in tag 'image', :alt parameter is required"
    end

    def internal_render
      attrs = @params
      attrs[:title] = @params.fetch(:title, @alt_text)

      filename = attrs.delete(:filename)
      attrs[:src] = "/images/#{@context.registers[:page]["date"].year}/#{filename}"
      render_image(**attrs)
    end
  end
end


Liquid::Template.register_tag("image", Jekyll::PostImageTag)
