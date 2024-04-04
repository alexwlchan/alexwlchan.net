# frozen_string_literal: true

# Get some basic information about this image:
#
#     {
#       "path" => "src/_images/2024/flemingo.jpg",
#       "width" => 3028,
#       "height" => 3028,
#       "format" => "JPEG"
#     }
#
# Because it's the easiest way to get it working on macOS, I'm doing
# this by shelling out to a Python script in the same folder (yes, really,
# image libraries on Ruby were tricky to install).
#
# To avoid taking a big performance hit shelling out for every image, we
# cache the result based on the modified time of the image, so the data
# will be saved unless the source image changes.
#
def get_image_info(path)
  cache = Jekyll::Cache.new("ImageInfo")

  last_mtime = File.mtime(path)

  cache.getset("#{path} :: #{last_mtime}") do
    output = `.venv/bin/python3 src/_plugins/utils/get_image_info.py #{Shellwords.escape(path)}`
    JSON.parse(output)
  end
end
