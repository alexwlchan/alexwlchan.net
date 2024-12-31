#!/usr/bin/env ruby

sizes = []

Dir.glob('_site/**/*.html').each do |f|
  if f.include? '/files/'
    next
  end

  sizes.push(File.size(f))
end

puts format('The average page size %.3f KiB', (sizes.sum / sizes.length / 1024.0))
