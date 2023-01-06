module Jekyll
  class AllPostsByMonth < Generator
    def posts_group_by_month(site)
      site.posts.docs.reverse_each.group_by { |post| [post.date.year, post.date.month] }
    end

    def generate(site)
      posts_group_by_month(site).each do |ym, posts|
        year, month = ym

        site.pages << PerMonth.new(site, year, month, posts)
      end
    end
  end

  class PerMonth < Page
    def initialize(site, year, month, posts)
      super

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
        "display_month" => Date.new(year, month).strftime("%B %Y"),
        "canonical_url" => "/all-posts/",
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
        site.pages << PerYear.new(site, year, posts)
      end
    end
  end

  class PerYear < Page
    def initialize(site, year, posts)
      super

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
        "year" => @year,
        "canonical_url" => "/all-posts/",
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
