# module Jekyll
#   class YearsAndMonths < Generator
#     safe true
#
#     def generate(site)
#       years(site).each do |year|
#         year_string = year[0]
#         puts("Building #{year_string}")
#         posts = year[1].sort_by { |p| -p.date.to_f }
#         newpage = DateArchivePage.new(site, site.source,
#           "/#{year_string}",
#           "Posts from #{year_string}"
#         )
#         posts << newpage
#         puts(newpage)
#         puts("got to here?")
#       end
#     end
#
#     def years(site)
#       site.posts
#         .group_by {|post| post.date.year}
#         .values.map {|year| year
#           .group_by {|post| post.date.month}.values
#         }
#     end
#   end
#
#   class DateArchivePage < Page
#     def initialize(site, base, dir, title)
#       @site = site
#       @base = base
#       @dir = dir
#       @name = 'index.html'
#
#       self.process(@name)
#       self.read_yaml(File.join(base, '_layouts'), "date_archive.html")
#       self.data["title"] = title
#     end
#   end
# end
