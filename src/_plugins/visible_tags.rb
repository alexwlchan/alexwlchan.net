# frozen_string_literal: true

# I use colons for namespacing my tags (e.g. `python` and `python:pillow`).
#
# Whenever I tag an article with a namespaced tag, I always tag it with the
# parent -- e.g. an article tagged `python:pillow` is always tagged with
# `python` also.  But because those tags are less useful on their own,
# I don't expose namespaced tags unless they're used at least three times.
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

  visible_tags = tag_tally.select { |tag_name, count| !tag_name.include?(':') or count > 2 }.keys.to_set

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
