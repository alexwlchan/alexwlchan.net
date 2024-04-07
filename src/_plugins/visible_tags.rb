# frozen_string_literal: true

# Tags are useful for finding other, similar articles.  If a tag is
# only used on a single article, it's no good for that, so tags only
# become visible when they're used at least twice.
#
# This plugin adds a `visible_tags` field to every article, which is
# limited to tags with more than one use.

Jekyll::Hooks.register :site, :post_read do |site|
  tag_tally = Hash.new(0)

  site.posts.docs.each do |post|
    next if post.data.fetch('index', {}).fetch('exclude', false)

    post.data['tags'].each do |tag|
      tag_tally[tag] += 1
    end
  end

  visible_tags = tag_tally.select { |_, count| count > 1 }.keys.to_set

  site.posts.docs.each do |post|
    post.data['visible_tags'] = post.data['tags'].select { |t| visible_tags.include? t }
  end
end
