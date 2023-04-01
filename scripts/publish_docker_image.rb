#!/usr/bin/env ruby

image_name = ENV.fetch('DOCKER_IMAGE_NAME', nil)
old_version = ENV['DOCKER_IMAGE_VERSION'].to_i
new_version = old_version + 1

existing_makefile = File.read('Makefile')

new_image_tag = "#{image_name}:#{new_version}"

system("docker buildx build --push \
  --platform linux/amd64,linux/arm64 \
  --tag #{new_image_tag} .")

new_makefile = existing_makefile.sub(
  "DOCKER_IMAGE_VERSION = #{old_version}",
  "DOCKER_IMAGE_VERSION = #{new_version}"
)

File.open('Makefile', 'w') do |f|
  f.puts new_makefile
end
