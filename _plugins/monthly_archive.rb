# Jekyll Module to create monthly archive pages
#
# Shigeya Suzuki, November 2013
# Copyright notice (MIT License) attached at the end of this file
#
# Amended by Alex Chan to support yearly and complete archives in the same
# format.  Modifications also MIT.
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

  module ArchiveUtil
    def self.archive_base(site, variant)
      key = "#{variant}_archive"
      site.config[key] && site.config[key]['path'] || ''
    end

    def self.archive_layout(site, variant)
      key = "#{variant}_archive"
      site.config[key] && site.config[key]['layout'] || key
    end
  end

  class MonthlyArchiveGenerator < Generator
    def generate(site)
      posts_group_by_year_and_month(site).each do |ym, posts|
        year, month = ym
        site.pages << ArchivePage.new(
          site = site,
          date = Date.new(year, month),
          variant = "monthly",
          posts = posts
        )
      end
    end

    def posts_group_by_year_and_month(site)
      site.posts.docs.each.group_by { |post| [post.date.year, post.date.month] }
    end
  end

  class YearlyArchiveGenerator < Generator
    def generate(site)
      posts_group_by_year(site).each do |y, posts|
        site.pages << ArchivePage.new(
          site = site,
          date = Date.new(y),
          variant = "yearly",
          posts = posts
        )
      end
    end

    def posts_group_by_year(site)
      site.posts.docs.each.group_by { |post| post.date.year }
    end
  end

  class ArchivePage < Page

    ATTRIBUTES_FOR_LIQUID = %w[
      year,
      month,
      date
    ]

    def initialize(site, date, variant, posts)
      @site = site
      @dir = ArchiveUtil.archive_base(site, variant)
      @year = date.year
      @month = date.month

      @date = date
      @layout = ArchiveUtil.archive_layout(site, variant)
      self.ext = '.html'
      self.basename = 'index'

      if variant == "yearly"
        @archive_dir_name = "%04d" % date.year
        title = "Posts from #{@date.strftime("%Y")}"
      elsif variant == "monthly"
        @archive_dir_name = "%04d/%02d" % [date.year, date.month]
        title = "Posts from #{@date.strftime("%B %Y")}"
      end

      self.data = {
          'layout' => @layout,
          'type' => 'archive',
          'title' => title,
          'posts' => posts,
          'year' => @year,
          'month' => @month,
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

  class MonthlyArchivePage < ArchivePage

    def initialize(site, dir, year, month, posts)

      @site = site
      @dir = dir
      @year = year
      @month = month
      @archive_dir_name = '%04d/%02d' % [year, month]
      @date = Date.new(@year, @month)
      @layout = ArchiveUtil.archive_layout(site, "monthly")
      self.ext = '.html'
      self.basename = 'index'

      self.data = {
          'layout' => @layout,
          'type' => 'archive',
          'title' => "Posts from #{@date.strftime("%B %Y")}",
          'posts' => posts,
          'year' => @year,
          'url' => File.join('/',
                     ArchiveUtil.archive_base(site, "monthly"),
                     @archive_dir_name, 'index.html')
      }
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
