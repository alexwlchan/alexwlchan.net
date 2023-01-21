require 'color'

# Computes the WCAG contrast ratio, suing the procedure defined in
# https://www.w3.org/TR/WCAG20-TECHS/G17.html
def contrast(color1, color2)
  color1 = Color::RGB.by_hex(color1)
  color2 = Color::RGB.by_hex(color2)

  luminance1 = _relative_luminance(color1)
  luminance2 = _relative_luminance(color2)

  if luminance1 > luminance2
    (luminance1 + 0.05) / (luminance2 + 0.05)
  else
    (luminance2 + 0.05) / (luminance1 + 0.05)
  end
end

def _relative_luminance(color)
  r = _linearize(color.r)
  g = _linearize(color.g)
  b = _linearize(color.b)

  (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
end

def _linearize(component)
  if component <= 0.03928
    component / 12.92
  else
    ((component + 0.055) / 1.055)**2.4
  end
end
