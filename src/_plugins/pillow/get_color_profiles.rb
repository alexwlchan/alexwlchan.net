require 'json'
require 'open3'

# Generates a map (path) -> (colour profile)
def get_color_profiles(dirname)
  stdout, status = Open3.capture2("python3", 'src/_plugins/pillow/get_color_profiles.py', dirname)
  raise "Unable to get color profiles for images in #{dirname}" unless status.success?

  JSON.parse(stdout)
end
