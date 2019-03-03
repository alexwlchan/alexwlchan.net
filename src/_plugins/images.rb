def render_image(src:, alt_text:, title:)
  <<-EOT
<a href="#{src}"><img src="#{src}" alt="#{alt_text}" title="#{title}"></a>
EOT
end


module Jekyll
  class PostImageTag < Alexwlchan::Tag
    def bind_params(params)
      @filename = params[:filename] or raise SyntaxError, "Error in tag 'image', :filename parameter is required"
      @alt_text = params[:alt] or raise SyntaxError, "Error in tag 'image', :alt_text parameter is required"
      @title = params.fetch(:title, @alt_text)
    end

    def internal_render
      src = "/images/#{@context.registers[:page]["date"].year}/#{@filename}"
      render_image(src: src, alt_text: @alt_text, title: @title)
    end
  end
end


Liquid::Template.register_tag("image", Jekyll::PostImageTag)
