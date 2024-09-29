# This hook runs at the end of a build, and generates a JSON file `sizes.json`
# in the root of the site which describes the size of each page, e.g.
#
#     {
#       "_site/index.html": 1234,
#       "_site/til/index.html": 5678
#     }
#
# This file is read by a GitHub Action which compares the sizes from
# a pull request build to the live site, so I can see how much (if any)
# the PR is changing the size of the site.

Jekyll::Hooks.register :site, :post_write do |site|
  dst = site.config['destination']

  sizes_json =
    Dir["#{dst}/**/*"]
      .filter { |f| File.file? f }
      .reject { |f| f.start_with? "#{dst}/images/" }
      .reject { |f| f.start_with? "#{dst}/favicons/" }
      .reject { |f| f.start_with? "#{dst}/files/" }
      .reject { |f| f.start_with? "#{dst}/static/" }
      .reject { |f| f.start_with? "#{dst}/theme/" }
      .reject { |f| f.start_with? "#{dst}/headers/" }
      .reject { |f| f.end_with? '/atom.xml' }
      .reject { |f| f.end_with? '.png' }
      .reject { |f| f == "#{dst}/robots.txt" }
      .reject { |f| f == "#{dst}/_redirects" }
      .to_h { |f| [f, File.size(f)] }
      .to_json

  File.write("#{dst}/sizes.json", sizes_json)
end
