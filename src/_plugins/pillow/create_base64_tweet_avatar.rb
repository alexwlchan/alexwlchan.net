require 'json'
require 'open3'

def create_base64_tweet_avatar(path, size)
  stdout, status = Open3.capture2('python3', 'src/_plugins/pillow/create_base64_tweet_avatar.py', path, size.to_s)
  raise "Unable to create base64 info for #{path}" unless status.success?

  stdout
end
