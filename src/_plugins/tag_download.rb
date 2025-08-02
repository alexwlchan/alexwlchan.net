require_relative 'utils/attrs'

def get_icon(filename)
  case File.extname(filename)
  when '.js'
    'javascript'
  when '.py'
    'python'
  when '.rb'
    'ruby'
  when '.zip'
    'zip'
  else
    raise "Unrecognised file extension: #{File.extname(filename)}"
  end
end

module Jekyll
  class DownloadLinkTag < Liquid::Tag
    def initialize(tag_name, params_string, tokens)
      super

      @attrs = parse_attrs(params_string)

      @filename = get_required_attribute(
        @attrs, { tag: 'download', attribute: 'filename' }
      )
    end

    def render(context)
      icon_name = get_icon(@filename)

      year = context.registers[:page]['date'].year

      icon = Liquid::Template.parse(
        <<~HTML
          {%
            picture
            filename="download_#{icon_name}.png"
            parent="/images/icons"
            width="64"
            alt=""
            data-proofer-ignore
          %}
        HTML
      ).render!(context).gsub("\n", '')

      <<~HTML
        <style type="x-text/scss">
          @use "components/download";
        </style>
        <a href="/files/#{year}/#{@filename}" class="download">#{icon} #{@filename} </a>
      HTML
    end
  end
end

Liquid::Template.register_tag('download', Jekyll::DownloadLinkTag)
