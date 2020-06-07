# Jekyll Module to create monthly archive pages
#
# Shigeya Suzuki, November 2013
# Copyright notice (MIT License) attached at the end of this file
#
# Amended by Alex Chan to support yearly and complete archives in the same
# format.  Modifications also MIT.
#
# Modified further in 2019 to group posts by category.
#

#
# This code is based on the following works:
#   https://gist.github.com/ilkka/707909
#   https://gist.github.com/ilkka/707020
#   https://gist.github.com/nlindley/6409459
#

#
# Archive will be written as #{archive_path}/#{year}/#{month}/index.html
# archive_path can be configured in 'path' key in 'monthly_archive' of
# site configuration file. 'path' is default null.
#

module Jekyll

  class MonthlyArchiveGenerator < Generator
    def generate(site)
      posts_group_by_year_and_month(site).each do |ym, posts|
        year, month = ym
        site.pages << ArchivePage.new(
          site = site,
          posts = posts,
          post_list_date_format = "day_month",
          archive_dir_name = "%04d/%02d" % [year, month],
          title = "Posts from #{Date.new(year, month).strftime("%B %Y")}",
          layout = "archive_month",
          date = Date.new(year, month)
        )
      end
    end

    def posts_group_by_year_and_month(site)
      site.posts.docs.reverse_each.group_by { |post| [post.date.year, post.date.month] }
    end
  end

  # class YearlyArchiveGenerator < Generator
  #   def generate(site)
  #     posts_group_by_year(site).each do |y, posts|
  #       site.pages << ArchivePage.new(
  #         site = site,
  #         posts = posts,
  #         post_list_date_format = "day_month",
  #         archive_dir_name = "%04d" % y,
  #         title = "Posts from #{Date.new(y).strftime("%Y")}",
  #         layout = "archive_year",
  #         date = Date.new(y)
  #       )
  #     end
  #   end
  #
  #   def posts_group_by_year(site)
  #     site.posts.docs.reverse_each.group_by { |post| post.date.year }
  #   end
  # end

  class ArchivePage < Page

    ATTRIBUTES_FOR_LIQUID = %w[
      year,
      month,
      date
    ]

    def initialize(site, posts, post_list_date_format, archive_dir_name, title, layout, date = Date.today)
      @site = site
      @dir = ""

      @archive_dir_name = archive_dir_name
      @date = date
      @year = date.year
      @month = date.month

      self.ext = '.html'
      self.basename = 'index'

      raw_grouped_posts = posts
        .group_by { |post| post.data.fetch("category", "Uncategorised") }

      grouped_posts = []
      raw_grouped_posts
        .sort
        .map { |category, posts|
          if category != "Uncategorised"
            grouped_posts << [category, posts]
          end
        }

      if !raw_grouped_posts["Uncategorised"].nil?
        grouped_posts << ["Uncategorised", raw_grouped_posts["Uncategorised"]]
      end

      self.data = {
        'layout' => layout,
        'type' => 'archive',
        'title' => title,
        'posts' => posts,
        "grouped_posts" => grouped_posts,
        'year' => @year,
        'month' => @month,
        'post_list_date_format' => post_list_date_format,
        'url' => File.join('/', @dir, @archive_dir_name, 'index.html')
      }
    end

    def render(layouts, site_payload)
      payload = {
        'page' => self.to_liquid,
        'paginator' => pager.to_liquid
      }.merge(site_payload)
      do_layout(payload, layouts)
    end

    def to_liquid(attr = nil)
      self.data.merge({
        'date' => @date,
        'month' => @month,
        'year' => @year
      })
    end

    def destination(dest)
      File.join('/', dest, @dir, @archive_dir_name, 'index.html')
    end
  end
end

# The MIT License (MIT)
#
# Copyright (c) 2013 Shigeya Suzuki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
