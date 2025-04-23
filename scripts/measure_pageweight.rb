#!/usr/bin/env ruby

puts format('Homepage (/):           %2.1f KiB', File.size('_site/index.html') / 1024.0)
puts format('Articles (/articles/): %3.1f KiB', File.size('_site/articles/index.html') / 1024.0)

sizes = []

Dir.glob('_site/**/*.html').each do |f|
  if f.include? '/files/'
    next
  end

  sizes.push(File.size(f))
end

puts format('Global average:         %2.1f KiB', sizes.sum / sizes.length / 1024.0)
