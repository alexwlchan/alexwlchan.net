#!/usr/bin/env ruby
# frozen_string_literal: true

require 'html-proofer'

def run_html_linting
  HTMLProofer.check_directory(
    "_site", {
      check_html: true,
      check_img_http: true,
      check_opengraph: true,
      disable_external: true,
      report_invalid_tags: true
    }
  ).run
end

run_html_linting
