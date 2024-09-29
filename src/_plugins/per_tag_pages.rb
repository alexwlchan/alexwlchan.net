Jekyll::Hooks.register :site, :post_read do |site|
  visible_posts = (site.posts.docs + site.collections['til'].docs)
                  .reject { |d| d.data.fetch('index', {}).fetch('exclude', false) }

  site.data['tag_tally'] =
    visible_posts
    .flat_map { |doc| doc.data['tags'] }
    .tally

  site.data['visible_tags'] =
    site.data['tag_tally']
        .filter { |_tag, count| count >= 3 }
        .keys

  visible_posts.each do |doc|
    doc.data['visible_tags'] = doc.data['tags'].filter do |tag_name|
      site.data['visible_tags'].include? tag_name
    end
  end
end

module TagNavigation
  class Generator < Jekyll::Generator
    def generate(site)
      # By default, the list of documents is sorted in chronological order,
      # with the oldest posts at the front, but I want the opposite.
      visible_posts = (site.posts.docs + site.collections['til'].docs)
                      .reject { |d| d.data.fetch('index', {}).fetch('exclude', false) }
                      .sort_by { |d| d.data['date'] }
                      .reverse

      site.data['visible_tags'].each do |tag|
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
        'remaining_posts' => remaining_posts
      }
    end
  end
end
