module Jekyll
  class AllPostsByYear < Generator
    def generate(site)
      site.data['posts_by_year'] =
        site.posts.docs.reverse_each.group_by { |post| post.date.year }
    end
  end
end
