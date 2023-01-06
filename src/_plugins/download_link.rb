module Jekyll
  class DownloadLinkTag < Liquid::Tag
    def initialize(_tag_name, text, _tokens)
      super
      @path = text.strip
    end

    def render(_)
      if @path.end_with?('.py')
        lang = 'python'
      elsif @path.end_with?('.zip')
        lang = 'zip'
      elsif @path.end_with?('.js')
        lang = 'javascript'
      end

      name = @path.split('/').last

      html = <<-EOF
      <a href="#{@path}" class="download">
        <img
          src="/theme/file_#{lang}_1x.png"
          srcset="/theme/file_#{lang}_1x.png 1x, /theme/file_#{lang}_2x.png 2x"
          alt=""
        >
        #{name}
      </a>
      EOF

      html.strip
    end
  end
end

Liquid::Template.register_tag('download', Jekyll::DownloadLinkTag)
