# frozen_string_literal: true

# Create a "fingerprint" of the CSS files.
#
# We want to be able to cache the CSS file for a long time, but we need
# to bust that cache if/when the CSS changes.  So we create a "fingerprint"
# of the CSS that will change whenever the CSS file changes.
#
# We then include this as a query parameter, which will invalidate
# browser caches when necessary.
#
# == Usage ==
#
# There are two parts to this plugin:
#
#   1.  A pre-render hook that generates the fingerprint and stores it
#       in the Jekyll cache.
#
#   2.  A tag you can use to retrieve the fingerprint and retrieve it
#       in the page:
#
#           {% css_fingerprint %}
#

require 'digest/md5'

# Before rendering the site, update the cached fingerprint of the CSS.
Jekyll::Hooks.register :site, :pre_render do |site|
  source = site.config['source']

  # Read the file that becomes /static/style.css
  sass_source = File.read "#{source}/static/style.scss"

  # Remove the front matter
  sass_source = sass_source.split('---')[-1]

  # Convert to CSS
  css = site.find_converter_instance(Jekyll::Converters::Scss)
            .convert(sass_source)

  # Create a fingerprint of it
  fingerprint = Digest::MD5.hexdigest(css)

  # Store that fingerprint in the Jekyll cache, so we can access it later.
  Jekyll::Cache.new('CssFingerprint')['style.scss'] = fingerprint
end

module Jekyll
  class CssFingerprintTag < Liquid::Tag
    def render(_context)
      # We only grab the first few characters of the hash; we don't
      # need all of it.
      Jekyll::Cache.new('CssFingerprint')['style.scss'][..6]
    end
  end
end

Liquid::Template.register_tag('css_fingerprint', Jekyll::CssFingerprintTag)
