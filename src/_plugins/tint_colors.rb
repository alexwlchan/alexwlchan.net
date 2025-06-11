# Handle custom tint colours on pages.
#
# You can set a custom CSS colour in the front matter for a page,
# in which case the links/header for that page will all be tinted
# based on that colour.
#
# This plugin handles all the extra colour management.
#
# == Usage ==
#
# There are three parts to this plugin:
#
#   1.  A pre-render hook that checks there's sufficient contrast between
#       the chosen tint color and the background of the page.
#
#   2.  A pre-render hook that creates the "speckled" header images and
#       favicons for every tint color that I'm using.
#
#   3.  A tag you can use in the <head> of a page to get the custom CSS
#       variables (if any) for this page:
#
#           {% tint_color_css %}
#
#       The output of this tag may be empty, if this page doesn't use
#       any custom colours.
#

require_relative 'utils/contrast'
require_relative 'utils/tint_colors'

# Throws an error if the CSS colors on a given page don't have enough
# contrast with the white/black backgrounds.
def ensure_sufficient_contrast(css_colors)
  contrast_with_white = contrast(css_colors['light'], '#ffffff')

  if contrast_with_white < 4.5
    throw "light color: insufficient contrast between white and #{css_colors['light']}: #{contrast_with_white} < 4.5"
  end

  contrast_with_black = contrast(css_colors['dark'], '#000000')

  if contrast_with_black < 4.5
    throw "dark color: insufficient contrast between black and #{css_colors['dark']}: #{contrast_with_black} < 4.5"
  end
end

# This hook creates a header image and favicon for the default
# light/dark colours.
Jekyll::Hooks.register :site, :pre_render do
  default_light_color = read_default_light_color
  default_dark_color = read_default_dark_color

  create_header_image(default_light_color)
  create_header_image(default_dark_color)

  create_favicon(default_light_color)
  create_favicon(default_dark_color)

  hex_string = default_light_color.gsub('#', '')

  FileUtils.cp("_site/favicons/#{hex_string}.png", '_site/favicon.png')
  FileUtils.cp("_site/favicons/#{hex_string}.ico", '_site/favicon.ico')
end

# These hooks create the asset images for the custom CSS colors
# on each post, page, and TIL.
def create_asset_images(doc)
  css_colors = get_css_colors(doc.data)

  unless css_colors.nil?
    ensure_sufficient_contrast(css_colors)

    create_header_image(css_colors['light'])
    create_header_image(css_colors['dark'])

    create_favicon(css_colors['light'])
    create_favicon(css_colors['dark'])
  end
end

Jekyll::Hooks.register :pages, :pre_render do |page|
  create_asset_images(page)
end

Jekyll::Hooks.register :documents, :pre_render do |doc|
  create_asset_images(doc)
end
