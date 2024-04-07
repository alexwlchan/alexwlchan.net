require 'json'
require 'open3'

def create_base64_tweet_avatar(path, size)
  stdout, status = Open3.capture2("#{ENV["VIRTUAL_ENV"]}/bin/python3", 'src/_plugins/pillow/create.py', path, size)
  raise "Unable to get info for images #{image_paths}" unless status.success?
  stdout
end
