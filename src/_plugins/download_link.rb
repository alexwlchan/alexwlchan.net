module Jekyll
  class DownloadLinkTag < Liquid::Tag
    def initialize(_tag_name, text, _tokens)
      super
      @path = text.strip
    end

    def render(context)
      site = context.registers[:site]
      src = site.config["source"]

      if @path.end_with?(".py")
        lang = "python"
      end

      name = @path.split("/").last

      html = <<-EOF
      <a href="#{@path}" class="download"><img src="/theme/file_#{lang}_2x.png" srcset="/theme/file_#{lang}_1x.png 1x, /theme/file_#{lang}_2x.png 2x" alt="">#{name}</a>
      EOF

      html.strip
    end
  end
end

Liquid::Template.register_tag("download", Jekyll::DownloadLinkTag)
