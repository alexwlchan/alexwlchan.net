module TagNavigation
  class Generator < Jekyll::Generator
    def generate(site)

      # By default, the list of documents is sorted in chronological order,
      # with the oldest posts at the front, but I want the opposite.
      visible_posts = (site.posts.docs + site.collections['til'].docs)
        .reject { |d| d.data.fetch('index', {}).fetch('exclude', false) }
        .reverse

      # I deliberately don't have visible tags from posts that are unlisted,
      # so you don't get a confusing navigation flow where:
      #
      # 1.  User lands on post
      # 2.  They click on the tags to find similar posts
      # 3.  The post they were just on isn't listed
      #
      visible_tags = visible_posts
        .flat_map { |doc| doc.data['tags'] }
        .tally
        .filter { |tag, count| count >= 3 }
        .keys

      visible_tags.each do |tag|
        site.pages << TagPage.new(site, visible_posts, tag)
      end
    end
  end

  class TagPage < Jekyll::Page
    def initialize(site, visible_posts, tag)
      @site = site
      @base = site.source
      @dir  = "tags/#{tag}"

      @basename = 'index'
      @ext      = '.html'
      @name     = 'index.html'

      posts_with_tag = visible_posts
        .filter { |doc| doc.data['tags'].include? tag }

      featured_posts = posts_with_tag
        .filter { |d| d.data.fetch('index', {}).fetch('feature', false) }

      remaining_posts = posts_with_tag
        .reject { |d| featured_posts.include? d }

      @data = {
        'layout' => 'tag',
        'tag' => tag,
        'title' => "Tagged with ‘#{tag}’",
        'featured_posts' => featured_posts,
        'remaining_posts' => remaining_posts,
      }
    end
  end
end
