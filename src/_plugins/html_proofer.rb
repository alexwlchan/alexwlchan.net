require "html-proofer"

Jekyll::Hooks.register :site, :post_write do |site|
  HTMLProofer.check_directory(
    site.config["destination"], opts = {
      :check_html => false,
      :check_img_http => true,
      :disable_external => true,
      :report_invalid_tags => true,
    }).run
end
