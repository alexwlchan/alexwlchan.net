# A vendored copy of https://github.com/webit-de/html_tag_builder/, because
# it doesn't seem to be available as a gem.

require 'set'
require 'erb'
require 'json'

module HtmlTagBuilder
  module Helper
    def tag(name = nil, opts = nil, open = false, *args, **options)
      if name.nil?
        tag_builder
      else
        tag_builder.tag_string(name, options.merge(open_only: open).merge(opts || {}))
      end
    end

    def content_tag(name, content = nil, opts = nil, *args, **options, &block)
      options = options.merge(opts) if opts.is_a?(Hash)
      if content.is_a?(Hash)
        content = options.merge(content)
        options = nil
      end
      tag_builder.tag_string(name, content, options, &block)
    end

    # Returns a CDATA section with the given +content+. CDATA sections
    # are used to escape blocks of text containing characters which would
    # otherwise be recognized as markup. CDATA sections begin with the string
    # <tt><![CDATA[</tt> and end with (and may not contain) the string <tt>]]></tt>.
    #
    #   cdata_section("<hello world>")
    #   # => <![CDATA[<hello world>]]>
    #
    #   cdata_section(File.read("hello_world.txt"))
    #   # => <![CDATA[<hello from a text file]]>
    #
    #   cdata_section("hello]]>world")
    #   # => <![CDATA[hello]]]]><![CDATA[>world]]>
    def cdata_section(content)
      splitted = content.to_s.gsub(/\]\]\>/, "]]]]><![CDATA[>")
      "<![CDATA[#{splitted}]]>"
    end

    private

    def tag_builder
      Builder.new
    end
  end

  class Builder

      BOOLEAN_ATTRIBUTES = %w(allowfullscreen async autofocus autoplay checked
                              compact controls declare default defaultchecked
                              defaultmuted defaultselected defer disabled
                              enabled formnovalidate hidden indeterminate inert
                              ismap itemscope loop multiple muted nohref
                              noresize noshade novalidate nowrap open
                              pauseonexit readonly required reversed scoped
                              seamless selected sortable truespeed typemustmatch
                              visible).to_set

      BOOLEAN_ATTRIBUTES.merge(BOOLEAN_ATTRIBUTES.map(&:to_sym))

      TAG_PREFIXES = ["aria", "data", :aria, :data].to_set

      PRE_CONTENT_STRINGS             = Hash.new { "" }
      PRE_CONTENT_STRINGS[:textarea]  = "\n"
      PRE_CONTENT_STRINGS["textarea"] = "\n"


    VOID_ELEMENTS = %i(area base br col embed hr img input keygen link meta param source track wbr).to_set

    class Buffer
      include HtmlTagBuilder::Helper

      def initialize
        @output = ''.dup
      end

      def text(str)
        @output << str
      end
      alias << text

      def to_s
        @output
      end

      private

      def tag_builder
        @tag_builder ||= Builder.new(self)
      end
    end

    def initialize(buffer = nil)
      @buffer = buffer
    end

    def tag_string(name, content = nil, opts = nil, *args, escape_attributes: true, open_only: false, **options, &block)
      options.merge!(opts) if opts.is_a?(Hash)
      if content.is_a?(Hash)
        options.merge!(content)
        content = nil
      end
      if block_given?
        content =
          if block.arity == 1
            b = Buffer.new
            block.call(b)
            b.to_s
          else
            block.call
          end
      end

      tag_options = tag_options(options, escape_attributes) unless options.empty?

      name = dasherize(name.to_s)
      open_tag = "<#{name}#{tag_options}>"
      full_tag_string =
        if open_only || (VOID_ELEMENTS.include?(name.to_sym) && content.nil?)
          open_tag
        else
          "#{open_tag}#{PRE_CONTENT_STRINGS[name]}#{content}</#{name}>"
        end
      @buffer ? @buffer.text(full_tag_string) : full_tag_string
    end

    alias content_tag_string tag_string

    def tag_options(options, escape = true)
      return if options&.empty?
      output = "".dup
      sep    = " "
      options.each_pair do |key, value|
        if TAG_PREFIXES.include?(key) && value.is_a?(Hash)
          value.each_pair do |k, v|
            next if v.nil?
            output << sep
            output << prefix_tag_option(key, k, v, escape)
          end
        elsif BOOLEAN_ATTRIBUTES.include?(key)
          if value
            output << sep
            output << boolean_tag_option(key)
          end
        elsif !value.nil?
          output << sep
          output << tag_option(key, value, escape)
        end
      end
      output unless output.empty?
    end

    def boolean_tag_option(key)
      %(#{key}="#{key}")
    end

    def tag_option(key, value, escape)
      if value.is_a?(Array)
        value = (escape ? value.map { |v| ::ERB::Util.html_escape(v) } : value).join(" ".freeze)
      else
        value = escape ? ::ERB::Util.html_escape(value) : value.to_s
      end
      %(#{key}="#{value.gsub('"'.freeze, '&quot;'.freeze)}")
    end

    private

    def dasherize(str)
      str.tr("_".freeze, "-".freeze)
    end

    def prefix_tag_option(prefix, key, value, escape)
      key = "#{prefix}-#{dasherize(key.to_s)}"
      unless value.is_a?(String) || value.is_a?(Symbol) || value.is_a?(BigDecimal)
        value = value.to_json
      end
      tag_option(key, value, escape)
    end

    def respond_to_missing?(*args)
      true
    end

    def method_missing(called, *args, &block)
      tag_string(called, *args, &block)
    end

  end
end