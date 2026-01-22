#!/usr/bin/env ruby

def pprint_size(size)
  format('%6.1f KiB (%7s B)', size / 1024.0, size.to_s.gsub(/\B(?=(...)*\b)/, ','))
end

puts format('Homepage (/):            %s', pprint_size(File.size('_out/index.html')))
puts format('Articles (/articles/):   %s', pprint_size(File.size('_out/articles/index.html')))
puts format('TIL      (/til/):        %s', pprint_size(File.size('_out/til/index.html')))

sizes = []

Dir.glob('_out/**/*.html').each do |f|
  if f.include? '/files/'
    next
  end

  sizes.push(File.size(f))
end

puts format('Global average:          %s', pprint_size(sizes.sum / sizes.length))

puts ''

puts format('CSS (/static/style.css): %s', pprint_size(File.size('_site/static/style.css')))
