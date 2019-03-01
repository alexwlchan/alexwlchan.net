module Alexwlchan
  module Base
    def initialize(tag_name, params_string, tokens)
      super
      bind_params(eval("{#{params_string}}"))
    end

    def markdown_converter
      @context.registers[:site].find_converter_instance(::Jekyll::Converters::Markdown)
    end
  end

  class Block < Liquid::Block
    include Base

    def render(context)
      @context = context
      @text = super
      internal_render
    end
  end

  class Tag < Liquid::Tag
    include Base

    def render(context)
      @context = context
      internal_render
    end
  end
end
