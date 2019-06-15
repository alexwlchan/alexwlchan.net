# A base module for my Jekyll plugins, with a couple of handy tools and
# features that are used throughout.
#
# The design of this base module is heavily inspired by
# http://www.glitchwrks.com/2017/07/25/jekyll-plugins

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
