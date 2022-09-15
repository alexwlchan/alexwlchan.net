# This plugin makes a tally of all the posts on the site, which can
# then be used to make tag filters.
module Jekyll
  class TagTally < Generator
    def generate(site)
      tag_tally = Hash.new(0)

      site.posts.docs.each { |post|

        # Make sure that posts which are excluded from the site-wide index
        # don't count towards the tag totals; they don't have visible tags
        # and won't appear in the tag filters.
        if post.data.fetch("index", {}).fetch("exclude", false)
          next
        end

        post.data["tags"].each { |tag|
          tag_tally[tag] += 1
        }
      }

      site.data["tag_tally"] = tag_tally
    end
  end
end
