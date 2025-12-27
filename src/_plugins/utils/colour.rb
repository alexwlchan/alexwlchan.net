# frozen_string_literal: true

# This file contains some functions for working with colours; these
# calculations are for general colour math and not specific to my site.

require 'color'

module Alexwlchan
  module ColourUtils
    # Calculate the ACPA contrast between two colours.
    #
    # This returns a value between 107 and -108; higher numbers mean
    # more contrast.
    #
    # This implementation is based on "APCA-W3 Basic Math (sRGB)" from
    # https://github.com/Myndex/apca-w3/, retrieved 27 December 2025
    def self.calculate_apca_contrast(txt_hex, bg_hex)
      # 1. Convert hex to RGB
      txt_rgb = Color::RGB.by_hex(txt_hex)
      bg_rgb = Color::RGB.by_hex(bg_hex)

      # 2. Estimate screen luminance
      yc_txt = self._estimate_screen_luminance(txt_rgb)
      yc_bg = self._estimate_screen_luminance(bg_rgb)

      # 3. Soft clamp black levels
      y_txt = self._soft_clamp_black_levels(yc_txt)
      y_bg = self._soft_clamp_black_levels(yc_bg)

      # 4. Find perceptual difference
      #
      #              Normal polarity: dark text/light bg, Y_bg > Y_txt
      #     S_norm = Y_bg ^ 0.56 - Y_txt ^ 0.57
      #
      #              Reverse polarity: light text/dark bg, Y_bg < Y_txt
      #     S_rev  = Y_bg ^ 0.65 - Y_txt ^ 0.62
      #
      if y_bg > y_txt
        s_norm = y_bg ** 0.56 - y_txt ** 0.57
      else
        s_rev = y_bg ** 0.65 - y_txt ** 0.62
      end

      # 5. Clamp noise then scale
      #
      #         | 0.0                   |Y_bg-Y_txt| < P_in
      #     C = | S_norm * R_scale      Y_txt < Y_bg
      #         | S_rev * R_scale       Y_txt > Y_bg
      #
      c = if (y_bg - y_txt).abs < P_in
            0
          elsif y_txt < y_bg
            s_norm * R_scale
          else
            s_rev * R_scale
          end

      # 6. Clamp minimum contrast then offset
      #
      #             | 0.0             |C| < P_out
      #     S_apc = | C - W_offset    C > 0
      #             | C + W_offset    C < 0
      #
      s_apc = if c.abs < P_out
                0
              elsif c > 0
                c - W_offset
              else
                c + W_offset
              end

      # 7. Result: lightness contrast
      #
      #     L_c = S_apc × 100
      #
      l_c = s_apc * 100
      l_c
    end

    # Constants for the ACPA contrast calculation
    B_exp = 1.414
    B_thresh = 0.022
    R_scale = 1.14
    W_offset = 0.027
    P_in = 0.0005
    P_out = 0.1

    # Estimate screen luminance
    #
    #             | (R' ÷ 255.0)^2.4 × 0.2126729
    #     Y_c = Σ | (G' ÷ 255.0)^2.4 × 0.7151522
    #             | (B' ÷ 255.0)^2.4 × 0.0721750
    #
    #     R', G', B' ∈ sRGB
    #
    def self._estimate_screen_luminance(rgb)
      # The color gem returns RGB values in (0,1) so we can skip dividing
      # by 255.0.
      (rgb.r**2.4 * 0.2126729) + (rgb.g**2.4 * 0.7151522) + (rgb.b**2.4 * 0.0721750)
    end

    # Soft clamp black levels
    #
    #     f_clamp(Y_c) = | Y_c                            Y_c >= B_thresh
    #                    | Y_c + (B_thrsh - Y_c)^B_exp    Y_c < B_thresh
    #
    def self._soft_clamp_black_levels(y_c)
      if y_c >= B_thresh
        y_c
      else
        y_c + (B_thresh - y_c) ** B_exp
      end
    end
  end
end
