#!/usr/bin/env ruby
# frozen_string_literal: true

require 'html-proofer'

source = "src"
destination = "_site"

# Run HTML-Proofer to check the generated HTML is accurate, e.g. all the
# links point to real pages, no missing alt text.
#
# This uses the html-proofer gem.
# See https://github.com/gjtorikian/html-proofer
def run_html_proofer(html_dir)

  HTMLProofer.check_directory(
    html_dir, {
      check_html: true,
      check_img_http: true,
      check_opengraph: true,
      disable_external: true,
      report_invalid_tags: true
    }
  ).run
end

run_html_proofer(destination)
