module Jekyll
  class PostSeparatorTag < Liquid::Tag
    def render(context)
      "<div class=\"post__separator\" aria-hidden=\"true\">&#9671;</div>"
    end
  end
end

Liquid::Template.register_tag('post_separator', Jekyll::PostSeparatorTag)
