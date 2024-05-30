require 'json'
require 'open3'

def create_ico_image(png16_path, png32_path, ico_path)
  stdout, status = Open3.capture2('python3', 'src/_plugins/pillow/create_ico_image.py', png16_path, png32_path,
                                  ico_path)
  raise "Unable to create ico at #{ico_path}" unless status.success?

  stdout
end
