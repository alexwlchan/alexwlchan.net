require 'json'
require 'open3'

def create_base64_avatar(path, size)
  cache = Jekyll::Cache.new('Base64Avatars')
  mtime = File.mtime(path).to_i

  cache.getset("#{path}--#{mtime}--#{size}") do
    stdout, status = Open3.capture2('python3', 'src/_plugins/pillow/create_base64_avatar.py', path, size.to_s)
    raise "Unable to create base64 info for #{path}" unless status.success?

    stdout
  end
end
