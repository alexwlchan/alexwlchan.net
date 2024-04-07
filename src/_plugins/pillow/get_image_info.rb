require 'json'
require 'open3'

def get_image_info(image_paths)
  stdout, status = Open3.capture2("python3", 'src/_plugins/pillow/get_image_info.py', JSON.generate(image_paths))
  raise "Unable to get info for images #{image_paths}" unless status.success?

  JSON.parse(stdout)
end

def get_single_image_info(path)
  cache = Jekyll::Cache.new('ImageInfo')
  mtime = File.mtime(path)

  cache.getset("#{path}--#{mtime}") do
    info = get_image_info([path])
    info[path]
  end
end
