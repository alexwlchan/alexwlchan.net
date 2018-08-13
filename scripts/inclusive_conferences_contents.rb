#!/usr/bin/env ruby
# Generates the table of contents for my inclusive-conferences post.
# Run from the root of the repository.

def slugify(title)
  title.downcase.strip.gsub(/[^a-z]/, '-').gsub(/\-{2,}/, '-')
end


File.open("src/_drafts/inclusive-conferences-contents.md", "w") do |outfile|
  File.open("src/_drafts/inclusive-conferences.md") do |infile|
    infile.each_line do |line|
      if line.start_with?("## ")
        title = line[3..line.size].strip
        puts "*   [**#{title}**](##{slugify(title)})"
        outfile.write("<h2 id=\"#{slugify(title)}\">#{title} <a class=\"anchor\" href=\"##{slugify(title)}\"></a></h2>\n")

      elsif line.start_with?("### ")
        title = line[3..line.size].strip
        puts "    *   [#{title}](#{slugify(title)})"
        outfile.write("<h3 id=\"#{slugify(title)}\">#{title} <a class=\"anchor\" href=\"##{slugify(title)}\"></a></h3>\n")

      else
        outfile.write(line)
      end
    end
  end
end


File.rename(
  "src/_drafts/inclusive-conferences-contents.md",
  "src/_drafts/inclusive-conferences.md"
)
