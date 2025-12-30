# This plugin contains a bunch of logic for the way I do tagging.

Jekyll::Hooks.register :site, :post_read do |site|
  # This hook runs before the site is built, and adds the following fields
  # to the `site` object:
  #
  #   - `tag_tally` is a count of how many times each tag is used, e.g.
  #       {"paris" => 1, "programming" => 3, "photography" => 5}
  #
  #   - `visible_tags` is a list of tags which are used on visible posts --
  #     that is, posts which can be discovered from the global site index.
  #
  #     If a post is excluded from the global site index, I don't include
  #     it in tagging or allow it to show any tags.  This is to avoid
  #     weird interactions where you look at a post, click to see other
  #     posts with that tag, but that post isn't in the list.
  #
  # It also adds a field to each article/TIL:
  #
  #   - `visible_tags` is a list of tags, filtered to those which appear
  #     in the global site index.
  #
  # Note: posts which are hidden from index pages have no visible tags.
  #
  visible_posts = (site.posts.docs + site.collections['til'].docs)
                  .reject { |d| d.data.fetch('is_unlisted', false) }

  site.data['tag_tally'] =
    visible_posts
    .flat_map { |doc| doc.data['tags'] }
    .tally

  site.data['visible_tags'] = site.data['tag_tally'].keys

  visible_posts.each do |doc|
    doc.data['visible_tags'] = doc.data['tags'].filter do |tag_name|
      site.data['visible_tags'].include? tag_name
    end
  end

  # This hook adds a `popular_tags` field, which is used for the selection
  # of tags on the homepage.
  #
  # The rules are a bit fuzzy here; the rough thinking is:
  #
  #   - only tags with featured posts
  #   - prioritise tags with lots of posts or lots of featured posts
  #   - don't show namespaced tags, which are too granular for the homepage
  #
  featured_posts = site.posts.docs.filter { |d| d.data.fetch('is_featured', false) }
  featured_tag_tally = featured_posts.flat_map { |doc| doc.data['tags'] }.tally

  tag_scores = featured_tag_tally
               .filter { |tag_name, _| site.data['visible_tags'].include? tag_name }
               .reject { |tag_name, _| tag_name.include? ':' }
               .map do |tag_name, count|
                 total_uses = site.data['tag_tally'][tag_name]

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
      # By default, the list of documents is sorted in chronological order,
      # with the oldest posts at the front, but I want the opposite.
      visible_posts = (site.posts.docs + site.collections['til'].docs)
                      .reject { |d| d.data.fetch('is_unlisted', false) }
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

      posts_with_tag = visible_posts
                       .filter { |doc| doc.data['tags'].include? tag }

      featured_posts = posts_with_tag
                       .filter { |d| d.data.fetch('is_featured', false) }

      remaining_posts = posts_with_tag
                        .reject { |d| featured_posts.include? d }

      @data = {
        'layout' => 'tag',
        'namespace' => namespace,
        'tag_name' => tag_name,
        'title' => "Tagged with ‘#{tag}’",
        'featured_posts' => featured_posts,
        'remaining_posts' => remaining_posts
      }
    end
  end
end
