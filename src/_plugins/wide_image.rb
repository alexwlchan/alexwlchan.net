module Jekyll
  class WideImageTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @image_id = text.strip
    end

    def render(context)
      site = context.registers[:site]
      if File.exists? "#{site.config["source"]}/_images/#{@image_id}_4x.jpg"
        <<-EOT
<a href="/images/#{@image_id}_4x.jpg">
  <img src="/images/#{@image_id}_1x.jpg" srcset="/images/#{@image_id}_1x.jpg 1x, /images/#{@image_id}_2x.jpg 2x, /images/#{@image_id}_3x.jpg 3x, /images/#{@image_id}_4x.jpg 4x">
</a>
EOT
      elsif File.exists? "#{site.config["source"]}/_images/#{@image_id}_3x.jpg"
        <<-EOT
<a href="/images/#{@image_id}_3x.jpg">
  <img src="/images/#{@image_id}_1x.jpg" srcset="/images/#{@image_id}_1x.jpg 1x, /images/#{@image_id}_2x.jpg 2x, /images/#{@image_id}_3x.jpg 3x">
</a>
EOT
      else
        <<-EOT
<a href="/images/#{@image_id}_2x.jpg">
  <img src="/images/#{@image_id}_1x.jpg" srcset="/images/#{@image_id}_1x.jpg 1x, /images/#{@image_id}_2x.jpg 2x">
</a>
EOT
      end
    end
  end
end


Liquid::Template.register_tag('wide_image', Jekyll::WideImageTag)
