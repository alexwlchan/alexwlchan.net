require 'json'
require 'open3'

def convert_image(request)
  convert_multiple_images([request])
end

def convert_multiple_images(requests)
  json_requests = requests.reject { |req| File.exist? req['out_path'] }
                          .map { |req| JSON.generate(req) }

  if json_requests.empty?
    return
  end

  _, status = Open3.capture2('python3', 'src/_plugins/pillow/convert_image.py', *json_requests)
  raise "Unable to process requests #{json_requests}" unless status.success?
end
