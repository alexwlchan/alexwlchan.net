# This plugin allows me to inline a file as highlighted code.
#
# It means I can have a file that can be downloaded, and include the complete
# code in the body of the post, and the two will stay in sync.
# (For example, a Python script.)
#
# Takes two parameters: the language code, and the path to the file.
#
# e.g. {% inline_code python _files/2020/redrive_sqs_queue.py %}
#

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
