# A filter to check if one string ends with another string, e.g.
#
#     {% assign is_directory = page.url | endswith: "/" %}
#
# By user pilvikala on Stack Overflow; used under a CC BY-SA license.
# See https://stackoverflow.com/a/64120329

module Jekyll
  module StringFilter
    def endswith(text, query)
      return text.end_with? query
    end
  end
end

Liquid::Template.register_filter(Jekyll::StringFilter)
