# This filter returns a list of posts to show in the "Recent posts" list
# on the homepage.

module Jekyll
  module HomepagePostsFilter
    def homepage_posts(posts)
      result = []
      posts.each do |post|
        if post.data.fetch("theme", {}).fetch("minipost", false) == true
          next
        end

        if result.length >= 5
          break
        end

        result.push(post)
      end
      result
    end
  end
end

Liquid::Template.register_filter(Jekyll::HomepagePostsFilter)
