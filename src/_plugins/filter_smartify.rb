# Creates a cached version of the built-in `smartify` filter.
#
# The `smartify` filter converts "quotes" into “smart quotes”.  I use
# it in a lot of places, and often it will be called with the same
# input multiple times (e.g. the title of a post will be rendered in
# the post itself, and in the RSS feed, and in the site-wide index).
# Caching the output has a noticeable performance gain.
#
# See https://jekyllrb.com/docs/liquid/filters/#smartify

module Jekyll
  module Filters
    def cache
      @@cache ||= Jekyll::Cache.new("Smartify")
    end

    # See https://github.com/jekyll/jekyll/blob/4.3-stable/lib/jekyll/filters.rb#L22-L31
    def smartify(input)
      cache.getset(input) do
        @context.registers[:site]
                .find_converter_instance(Jekyll::Converters::SmartyPants)
                .convert(input.to_s)
      end
    end
  end
end
