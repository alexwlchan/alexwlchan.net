# This plugin contains a bunch of logic for the way I do tagging.

def visible?(tag_name, count)
  if tag_name.include?(':') && (count >= 3)
    true
  end

  unless tag_name.include? ':'
    true
  end

  false
end

Jekyll::Hooks.register :site, :post_read do |site|
  # This hook runs before the site is built, and adds the following fields
  # to the `site` object:
  #
  #   - `tag_tally` is a count of how many times each tag is used, e.g.
  #       {"paris" => 1, "programming" => 3, "photography" => 5}
  #
  #   - `visible_tags` is a list of tags which are used multiple times.
  #     I don't show a tag if it's only used once -- to me, tags are only
  #     useful as a way to find related posts.  If there are no other
  #     posts on this topic, is it useful?
  #
  #     Note: I made this decision back when I didn't have a global tag
  #     index.  I should consider if this is still the case, and maybe
  #     do some tag cleaing.
  #
  # It also adds a field to each article/TIL:
  #
  #   - `visible_tags` is a list of tags, filtered to those which appear
  #     in the global site index.
  #
  # Note: posts which are hidden from index pages have no visible tags.
  #
  visible_posts = (site.posts.docs + site.collections['til'].docs)
                  .reject { |d| d.data.fetch('index', {}).fetch('exclude', false) }

  site.data['tag_tally'] =
    visible_posts
    .flat_map { |doc| doc.data['tags'] }
    .tally

  site.data['visible_tags'] =
    site.data['tag_tally']
        .filter { |tag_name, count| visible?(tag_name, count) }
        .keys

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
  #
  featured_posts = site.posts.docs.filter { |d| d.data.fetch('index', {}).fetch('feature', false) }
  featured_tag_tally = featured_posts.flat_map { |doc| doc.data['tags'] }.tally

  tag_scores = featured_tag_tally
               .filter { |tag_name, _| site.data['visible_tags'].include? tag_name }
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
