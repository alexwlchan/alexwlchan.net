# frozen_string_literal: true

# How this works:
#
#   - We write image requests to a file `.image_requests.json`
#   - Once we've got all the requests for this build, we call a Python script
#     that chews through all of them
#
# We use Jekyll hooks to reset this file before each build.

require 'json'
require 'open3'

def convert_image(request)
  if File.exist? request['out_path']
    return
  end

  File.open('.image_requests.json', 'a') do |f|
    f.write("#{JSON.generate(request)}\n")
  end
end

Jekyll::Hooks.register :site, :after_init do
  FileUtils.rm_f('.image_requests.json')
end

Jekyll::Hooks.register :site, :post_render do
  if File.exist?('.image_requests.json')
    _, status = Open3.capture2('python3', 'src/_plugins/pillow/convert_images.py')
    raise 'Unable to process image requests' unless status.success?
  end
end
