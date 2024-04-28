# frozen_string_literal: true

# I use colons for namespacing my tags (e.g. `python` and `python:pillow`).
#
# Whenever I tag a post with a namespaced tag, I always tag it with the
# parent -- e.g. a post tagged `python:pillow` is always tagged with
# `python` also.  But because those tags are less useful on their own,
# I don't expose namespaced tags unless they're used at least three times.
#
# This plugin adds a `visible_tags` field to every post, which is
# limited to tags with more than one use.

# Returns true if a tag is visible, false otherwise
def visible?(tag_tally, tag_name)
  is_namespaced = tag_name.include?(':')

  if is_namespaced
    tag_tally[tag_name] >= 3
  else
    true
  end
end

def create_visible_tags(collection_of_docs)
  # I deliberately don't have visible tags from posts that are unlisted,
  # so you don't get a confusing navigation flow where:
  #
  # 1.  User lands on post
  # 2.  They click on the tags to find similar posts
  # 3.  The post they were just on isn't listed
  #
  visible_docs = collection_of_docs.reject do |doc|
    doc.data.fetch('index', {}).fetch('exclude', false)
  end

  tag_tally = visible_docs.flat_map { |doc| doc.data['tags'] }.tally

  visible_docs.each do |doc|
    doc.data['visible_tags'] = doc.data['tags'].filter do |tag_name|
      visible?(tag_tally, tag_name)
    end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  create_visible_tags(site.posts.docs)
  create_visible_tags(site.collections['til'].docs)
end
