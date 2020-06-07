module Jekyll
  class AllPostsByTag < Generator
    def generate(site)
      posts_by_tag = Hash.new([])

      site.posts.docs.reverse.each { |post|
        post.data["tags"].each { |tag|
          posts_by_tag[tag] = posts_by_tag[tag] + [post]
        }
      }

      site.data["posts_by_tag"] = posts_by_tag
    end
  end
end