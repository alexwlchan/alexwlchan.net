require 'json'
require 'open3'

def get_image_info(image_paths)
  stdout, status = Open3.capture2("#{ENV["VIRTUAL_ENV"]}/bin/python3", 'src/_plugins/pillow/get_image_info.py', JSON.generate(image_paths))
  raise "Unable to get info for images #{image_paths}" unless status.success?
  JSON.parse(stdout)
end

def get_single_image_info(path)
  info = get_image_info([path])
  info[path]
end
