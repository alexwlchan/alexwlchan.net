# frozen_string_literal: true

# This file contains some functions for working with the tint colours
# I apply to pages and posts. This logic is specific to my site.

require_relative 'colour'

module Alexwlchan
  module TintColourUtils

    # Verify the tint colours have sufficient contrast to be usable,
    # and throw an error if there's not enough contrast.
    def self.check_tint_colour_contrast(doc)
      warnings = []

      # If there are no colours, do nothing
      colours = doc.data["colors"]
      return if colours.nil?

      # For the CSS colours, compare the contrast when the tint colour
      # is the text colour.
      #
      # The goal is an ACPA of 60, for "content/fluent text" that isn't
      # a long block of body text.
      if colours["css_light"]
        contrast = calculate_apca_contrast(colours["css_light"], WhiteBg)
        if contrast < 60
          warnings << (
            "#{doc.path}: CSS light has insufficient contrast as link text "\
            "(#{colours["css_light"]}: #{contrast} < 60)"
          )
        end
      end

      if colours["css_dark"]
        contrast = calculate_apca_contrast(colours["css_dark"], BlackBg)
        if contrast.abs < 60
          warnings << (
            "#{doc.path}: CSS dark has insufficient contrast as link text "\
            "(#{colours["css_dark"]}: #{contrast.abs} < 60)"
          )
        end
      end

      puts warnings

      []
    end

    # Constants for my background colours
    WhiteBg = "#fcfcfc"
    BlackBg = "#0d0d0d"

    def self.calculate_apca_contrast(txt_hex, bg_hex)
      Alexwlchan::ColourUtils.calculate_apca_contrast(txt_hex, bg_hex)
    end
  end
end
