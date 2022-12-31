# This provides a mechanism for posts to add "extra" CSS.
#
# If you create a file with the same year/slug as the post in the 'styles'
# directory, e.g.
#
#     src/styles/2021/2021-in-reading.scss
#
# then that CSS file will be run through the SCSS processor (so it can use
# mixins/filters/shared snippets), and inserted into the <head> of the page.

require_relative "css_fingerprint"

module Jekyll
  class PerPostCssTag < Liquid::Tag
    def render(context)
      site = context.registers[:site]
      src = site.config["source"]
      dst = site.config["destination"]

      if context.registers[:page].nil? || context.registers[:page]["date"].nil?
        return
      end

      year = context.registers[:page]["date"].year
      slug = context.registers[:page]["slug"]

      if year.nil?
        return
      end

      if File.exist? "#{src}/styles/#{year}/#{slug}.scss"
        <<-EOF
<link rel="stylesheet" href="/styles/#{year}/#{slug}.css?h=#{FINGERPRINT}">
EOF
      end
    end
  end
end

Liquid::Template.register_tag("per_post_css", Jekyll::PerPostCssTag)
