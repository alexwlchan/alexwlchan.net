module Jekyll
  class AllPostsByTag < Generator
    def generate(site)
      posts_by_tag = Hash.new([])

      site.posts.docs.reverse.each { |post|
        post.data["tags"].each { |tag|
          posts_by_tag[tag] = posts_by_tag[tag] + [post]
        }
      }

      # Tag cloud generator
      # See: https://gist.github.com/yeban/2290195
      # See: https://github.com/alexwlchan/notebook.alexwlchan.net/blob/live/src/_plugins/tag_cloud.rb
      tag_frequency = Hash[
        posts_by_tag.map { |tag_name, posts| [tag_name, posts.size] }
      ]

      tag_freq_min = tag_frequency.values.min
      tag_freq_max = tag_frequency.values.max

      tag_freq_range = tag_freq_max - tag_freq_min
      if tag_freq_range == 0
        tag_freq_range = 1
      end

      font_size_min = 12
      font_size_max = 24

      color_min = "#999999"
      color_max = "#d01c11"

      red   = {"min" => color_min[1..2].to_i(16), "max" => color_max[1..2].to_i(16)}
      green = {"min" => color_min[3..4].to_i(16), "max" => color_max[3..4].to_i(16)}
      blue  = {"min" => color_min[5..6].to_i(16), "max" => color_max[5..6].to_i(16)}

      # Remember to use .to_f to get precise answers; Ruby does int division
      # by default.
      size_diff  = font_size_max - font_size_min
      red_diff   = (red["max"] - red["min"])
      green_diff = (green["max"] - green["min"])
      blue_diff  = (blue["max"] - blue["min"])

      site.data["tag_cloud_data"] = Hash[tag_frequency.map {
        |tag_name, post_count|
          weight = (Math.log(post_count) - Math.log(tag_freq_min)) / (Math.log(tag_freq_max) - Math.log(tag_freq_min))
          red_c   = [(red["min"]   + weight * red_diff), 255].min
          green_c = [(green["min"] + weight * green_diff), 255].min
          blue_c  = [(blue["min"]  + weight * blue_diff), 255].min

          [tag_name,
            {
              "size"  => (font_size_min + weight * size_diff).to_i,
              "hex"   => "#%02x%02x%02x" % [red_c, green_c, blue_c],
            }
          ]
      }]

      site.data["posts_by_tag"] = posts_by_tag
    end
  end

  class AllPostsByMonth < Generator
    def posts_group_by_month(site)
      site.posts.docs.reverse_each.group_by { |post| [post.date.year, post.date.month] }
    end

    def generate(site)
      posts_group_by_month(site).each do |ym, posts|
        year, month = ym

        site.pages << PerMonth.new(
          site = site, year = year, month = month, posts = posts
        )
      end
    end
  end

  class PerMonth < Page
    def initialize(site, year, month, posts)
      @site = site
      @year = year
      @month = month
      @posts = posts

      # The Jekyll Page class expects these attributes to be set, and looks
      # up values in it later on.  If you don't set them, you'll get an error like:
      #
      #     NoMethodError: undefined method `fetch' for nil:NilClass
      #       /usr/local/bundle/gems/jekyll-4.0.0/lib/jekyll/page.rb:143:in `path'
      #
      self.ext = ".html"
      self.basename = "index"
      self.data = {
        "layout" => "all_posts_per_month",
        "title" => "Posts from #{Date.new(year, month).strftime("%B %Y")}",
        "posts" => @posts,
        "url" => File.join("/", "", year.to_s, month.to_s, "index.html"),
        "year" => @year,

        # This causes the archive list to render dates "4 May", not "May 2020".
        "post_list_date_format" => "day_month",
      }
    end

    def render(layouts, site_payload)
      payload = {
        "page" => self.data,
      }.merge(site_payload)

      do_layout(payload, layouts)
    end

    def destination(root)
      File.join("/", root, @year.to_s, "%02d" % @month, "index.html")
    end
  end

  class AllPostsByYear < Generator
    def posts_group_by_year(site)
      site.posts.docs.reverse_each.group_by { |post| post.date.year }
    end

    def generate(site)
      site.data["posts_by_year"] = posts_group_by_year(site)

      posts_group_by_year(site).each do |year, posts|
        site.pages << PerYear.new(
          site = site,
          year = year,
          posts = posts.group_by { |post| post.date.month }
        )
      end
    end
  end

  class PerYear < Page
    def initialize(site, year, posts)
      @site = site
      @year = year
      @posts = posts

      # The Jekyll Page class expects these attributes to be set, and looks
      # up values in it later on.  If you don't set them, you'll get an error like:
      #
      #     NoMethodError: undefined method `fetch' for nil:NilClass
      #       /usr/local/bundle/gems/jekyll-4.0.0/lib/jekyll/page.rb:143:in `path'
      #
      self.ext = ".html"
      self.basename = "index"
      self.data = {
        "layout" => "all_posts_per_year",
        "title" => "Posts from #{@year}",
        "posts" => @posts,

        # This causes the archive list to render dates "4 May", not "May 2020".
        "post_list_date_format" => "day_month",
      }
    end

    def render(layouts, site_payload)
      puts self.data
      payload = {
        "page" => self.data,
      }.merge(site_payload)

      do_layout(payload, layouts)
    end

    def destination(root)
      File.join("/", root, @year.to_s, "index.html")
    end
  end
end
