# This plugin makes a tally of all the posts on the site, which can
# then be used to make tag filters.

require "json"

module Jekyll
  class TagTally < Generator
    def generate(site)

      # Create a tally of all tags used in visible posts on the site.
      #
      # This will be used to decide which tags have been used multiple times,
      # and which should be shown on posts/in the site wide index.
      tag_tally = Hash.new(0)

      site.posts.docs.each { |post|
        if post.data.fetch("index", {}).fetch("exclude", false)
          next
        end

        post.data["tags"].each { |tag|
          tag_tally[tag] += 1
        }
      }

      # Now we go through the posts a second time, and create a new
      # 'visible_tags' list of all the tags on this post that appear on
      # at least one other post.
      site.posts.docs.each { |post|
        post.data["visible_tags"] = post.data["tags"].select { |t| tag_tally[t] > 1 };
      }

      site.data["tag_tally"] = tag_tally
      site.data["visible_tag_tally"] = tag_tally.select { |t, count| count > 0 };

      File.open("tags.json", "w") { |f| f.write JSON.dump(tag_tally) }
    end
  end
end
