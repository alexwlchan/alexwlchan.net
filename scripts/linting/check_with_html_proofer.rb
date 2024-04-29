require 'html-proofer'

def check_with_html_proofer(html_dir)
  HTMLProofer.check_directory(
    html_dir, {
      checks: %w[
        Images
        Links
        Scripts
        Favicon
        OpenGraph
      ],
      check_external_hash: false,
      check_html: true,
      check_opengraph: true,
      disable_external: true,

      ignore_files: [
        '_site/400/index.html',
        %r{_site/files/.*},
        # This is because of an overly slow regex in HTML-Proofer.
        # See https://github.com/gjtorikian/html-proofer/issues/816
        '_site/2013/google-maps/index.html'
      ],
      report_invalid_tags: true,
      #
      # As of April 2024, I have 334 links which don't use HTTPS.
      # It might be nice to fix them all and/or whitelist them, but
      # they're all external links -- I don't care that much.
      #
      # For now, skip HTTPS checking.
      enforce_https: false
    }
  ).run
end

if __FILE__ == $PROGRAM_NAME
  check_with_html_proofer('_site')
end
