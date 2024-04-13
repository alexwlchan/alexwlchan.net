# frozen_string_literal: true

# Tags are useful for finding other, similar articles.  If a tag is
# only used on a single article, it's no good for that, so tags only
# become visible when they're used at least twice.
#
# This plugin adds a `visible_tags` field to every article, which is
# limited to tags with more than one use.

def create_visible_tags(collection_of_docs)
  tag_tally = Hash.new(0)

  collection_of_docs.each do |doc|
    next if doc.data.fetch('index', {}).fetch('exclude', false)

    doc.data['tags'].each do |tag|
      tag_tally[tag] += 1
    end
  end

  visible_tags = tag_tally.select { |_, count| count > 1 }.keys.to_set

  collection_of_docs.each do |doc|
    # I deliberately don't have visible tags from pages that are unlisted,
    # so you don't get a confusing navigation flow where:
    #
    # 1.  User lands on page
    # 2.  They click on the tags to find similar pages
    # 3.  The page they were just on isn't listed
    #
    doc.data['visible_tags'] = if doc.data.fetch('index', {}).fetch('exclude', false)
                                 []
                               else
                                 doc.data['tags'].select { |t| visible_tags.include? t }
                               end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  create_visible_tags(site.posts.docs)
  create_visible_tags(site.collections['til'].docs)
end
