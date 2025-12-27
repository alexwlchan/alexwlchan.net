require_relative 'utils/tint_colours.rb'

Jekyll::Hooks.register [:pages, :documents], :pre_render do |doc|
  Alexwlchan::TintColourUtils.check_tint_colour_contrast(doc)
end
