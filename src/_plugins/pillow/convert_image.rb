require 'json'
require 'open3'

def convert_image(request)
  unless File.exist? request['out_path']
    _, status = Open3.capture2("#{ENV["VIRTUAL_ENV"]}/bin/python3", 'src/_plugins/pillow/convert_image.py', JSON.generate(request))
    raise "Unable to resize image #{request}" unless status.success?
  end
end
