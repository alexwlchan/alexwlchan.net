# Given the front matter from a page, get the CSS colors (if any).
def get_css_colors(page)
  colors = page.fetch('colors', {})

  primary_color_light = colors['css_light']
  primary_color_dark = colors['css_dark']

  if primary_color_light.nil? && primary_color_dark.nil?
    return
  end

  { 'light' => primary_color_light, 'dark' => primary_color_dark }
end
