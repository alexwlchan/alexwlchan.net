# Use Python to get some basic info about an image, including the
# dimensions and format.

require 'json'
require 'open3'

def get_single_image_info(path)
  cache = Jekyll::Cache.new('ImageInfo')

  # How this works:
  #
  #   - When we have an empty cache, we get the info for every image
  #     we can find in `_src/images` and warm the cache.
  #
  #   - If the image isn't in the cache (e.g. it was just added) or the
  #     cache entry is invalid (the image has changed), we get the info
  #     for just that image.
  #
  # We want to minimise the calls to Python, because each one involves
  # a minor performance penalty we'd rather avoid.
  #
  # Jekyll will clear the cache every time `_config.yml` changes, or you
  # change your options (e.g. adding the `--profile` flag), so we warm
  # the cache to speed up that initial build.

  unless cache.key?('-1')
    stdout, status = Open3.capture2('python3', 'src/_plugins/pillow/get_all_image_info.py')

    if status.success?
      JSON.parse(stdout).each do |im_path, info|
        cache["#{im_path}--#{info['mtime']}"] = info
      end

      cache['-1'] = -1
    end
  end

  mtime = File.mtime(path).to_i

  cache.getset("#{path}--#{mtime}") do
    stdout, status = Open3.capture2('python3', 'src/_plugins/pillow/get_image_info.py', path)
    raise "Unable to get info for image #{path}" unless status.success?

    JSON.parse(stdout)
  end
end
