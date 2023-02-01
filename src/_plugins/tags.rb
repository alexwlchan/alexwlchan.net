# This plugin makes a tally of all the posts on the site, which can
# then be used to make tag filters.

require 'json'

module Jekyll
  class TagTally < Generator
    def generate(site)
      # Create a tally of all tags used in visible posts on the site.
      #
      # This will be used to decide which tags have been used multiple times,
      # and which should be shown on posts/in the site wide index.
      tag_tally = Hash.new(0)

      site.posts.docs.each do |post|
        next if post.data.fetch('index', {}).fetch('exclude', false)

        post.data['tags'].each do |tag|
          tag_tally[tag] += 1
        end
      end

      # Tags are useful for finding other, similar posts.  If a tag is
      # only used on a single post, it's no good for that, so tags only
      # become visible when they're used at least twice.
      site.data['tag_tally'] = tag_tally
      site.data['visible_tag_tally'] = tag_tally.select { |_, count| count > 1 }

      visible_tags = site.data['visible_tag_tally'].keys.to_set

      site.posts.docs.each do |post|
        post.data['visible_tags'] = post.data['tags'].select { |t| visible_tags.include? t }
      end
    end
  end
end
