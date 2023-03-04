module Jekyll
  class AllPostsByYear < Generator
    def generate(site)
      site.data['posts_by_year'] =
        site.posts.docs.reverse_each.group_by { |post| post.date.year }

      site.data['posts_by_year'].each do |year, posts|
        site.pages << PerYear.new(site, year, posts)
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
      self.ext = '.html'
      self.basename = 'index'
      self.data = {
        'layout' => 'all_posts_per_year',
        'title' => "Posts from #{@year}",
        'posts' => @posts,
        'year' => @year,
        'canonical_url' => '/all-posts/'
      }
    end

    def destination(root)
      File.join('/', root, @year.to_s, 'index.html')
    end
  end
end
