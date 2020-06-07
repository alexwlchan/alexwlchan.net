module Jekyll
  class AllPostsByTag < Generator
    def generate(site)
      posts_by_tag = Hash.new([])

      site.posts.docs.reverse.each { |post|
        post.data["tags"].each { |tag|
          posts_by_tag[tag] = posts_by_tag[tag] + [post]
        }
      }

      site.data["posts_by_tag"] = posts_by_tag
    end
  end

  class PerYearArchives < Generator
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
        "layout" => "archive_per_year",
        "title" => "Posts from #{@year}",
        "posts" => @posts,
        "year" => @year,
        "url" => "/#{@year}/index.html",

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

    def destination(dest)
      File.join("/", dest, @year.to_s, "index.html")
    end
  end
end
