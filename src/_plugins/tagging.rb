# This plugin contains a bunch of logic for the way I do tagging.

Jekyll::Hooks.register :site, :post_read do |site|
  posts = site.posts.docs + site.collections['til'].docs

  # Delete tags from unlisted posts. Unlisted posts don't appear in
  # the site index, and don't contribute to tags.
  posts.each do |p|
    if p.data['is_unlisted']
      p.data['tags'] = []
    end
  end
  
  # Find namespaced tags (tags with a {namespace}: prefix) that are
  # only used once, and delete them.
  namespaced_tags = posts.flat_map { |p| p.data['tags']}.filter{|t| t.include? ':' }.tally
  hidden_tags = namespaced_tags.filter { |t, count| count <= 2 }.keys
  
  posts.each do |p|
    p.data['tags'] = p.data['tags'].reject do |tag_name|
      hidden_tags.include? tag_name
    end
  end

  # Add a `tag_tally` field to site.data, which counts all the tags
  # which are used on visible posts.  
  site.data['tag_tally'] = {}
  
  Hash.new do |h, tag_name|
    h[tag_name] = {
      'tag_name': tag_name.split(':').last,
      'posts' => [],
      'description' => site.data['tag_descriptions'][tag_name]
    }
  end

  posts.each do |p|
    p.data['tags'].each do |tag_name|
      label = tag_name.split(':').last
      tag_info = site.data['tag_tally'].fetch(label, {
        'tag_name' => tag_name,
        'posts' => [],
        'description' => site.data['tag_descriptions'][tag_name]
      })
      tag_info['posts'].append(p)
      site.data['tag_tally'][label] = tag_info
    end
  end

  # Add a `popular_tags` field to site.data, which selects the tags used
  # on the homepage.
  #
  # The rules are a bit fuzzy here; the rough thinking is:
  #
  #   - only tags with featured posts
  #   - prioritise tags with lots of posts or lots of featured posts
  #   - don't show namespaced tags, which are too granular for the homepage
  #
  featured_tag_tally = posts.filter { |d| d.data['is_featured'] }.flat_map { |doc| doc.data['tags'] }.tally

  tag_scores = featured_tag_tally
               .reject { |tag_name, _| tag_name.include? ':' }
               .map do |tag_name, count|
                 total_uses = site.data['tag_tally'][tag_name].length

                 [tag_name, ((count * 5.0) + (total_uses - count))]
               end

  site.data['popular_tags'] = tag_scores
                              .sort_by { |_, score| score }
                              .reverse[...25]
                              .map { |tag_name, _| tag_name }
                              .sort
end

# This generator creates the per-tag pages for the visible tags.
#
# Each tag page shows the name of the tag, and a list of articles/TILs
# with that tag.  They're sorted so the featured articles appear first,
# then an interleaved list of articles and TILs.
module TagNavigation
  class Generator < Jekyll::Generator
    def generate(site)
      site.data['tag_tally'].each do |tag, tag_info|
        # By default, the list of documents is sorted in chronological order,
        # with the oldest posts at the front, but I want the opposite.
        tagged_posts = tag_info['posts'].sort_by { |d| d.data['date'] }
        .reverse

        site.pages << TagPage.new(site, tagged_posts, tag)
      end
    end
  end

  class TagPage < Jekyll::Page
    def initialize(site, tagged_posts, tag)
      @site = site
      @base = site.source

      if tag.include? ':'
        namespace, tag_name = tag.split(':')
        @dir = "tags/#{namespace}/#{tag_name.gsub(' ', '-')}"
      else
        namespace = ''
        tag_name = tag
        @dir = "tags/#{tag_name.gsub(' ', '-')}"
      end

      @basename = 'index'
      @ext      = '.html'
      @name     = 'index.html'

      @data = {
        'layout' => 'tag',
        'namespace' => namespace,
        'tag_name' => tag_name,
        'title' => "Tagged with ‘#{tag}’",
        'featured_posts' => tagged_posts.filter { |d| d.data['is_featured'] },
        'remaining_posts' => tagged_posts.reject { |d| d.data['is_featured'] }
      }
    end
  end
end
