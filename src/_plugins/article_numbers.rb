# This hook adds an "order" value to the data associated with each post.
#
# This identifies where each post appears in the list of visible posts,
# which is used for ordering on the /articles page.

Jekyll::Hooks.register :site, :post_read do |site|
  site.posts.docs
      .reject { |d| d.data.fetch('is_unlisted', false) }
      .sort_by { |post| post.data['date'] }
      .each_with_index { |post, order| post.data['order'] = order }
end
