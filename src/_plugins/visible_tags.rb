# frozen_string_literal: true

# Tags are useful for finding other, similar articles.  If a tag is
# only used on a single article, it's no good for that, so tags only
# become visible when they're used at least twice.
#
# This plugin adds a `visible_tags` field to every article, which is
# limited to tags with more than one use.

Jekyll::Hooks.register :site, :post_read do |site|
  tag_tally = Hash.new(0)

  site.collections["articles"].docs.each do |article|
    next if article.data.fetch('index', {}).fetch('exclude', false)

    article.data['tags'].each do |tag|
      tag_tally[tag] += 1
    end
  end

  visible_tags = tag_tally.select { |_, count| count > 1 }.keys.to_set

  site.collections["articles"].docs.each do |article|
    article.data['visible_tags'] = article.data['tags'].select { |t| visible_tags.include? t }
  end
end
