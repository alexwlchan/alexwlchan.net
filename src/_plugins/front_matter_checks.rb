module FrontMatterChecks
  class Generator < Jekyll::Generator
    def generate(site)
      entries = site.posts.docs + site.pages
      entries.each do |entry|
        assert_has_layout(entry)
        assert_summary_is_right_length(entry)
        assert_tags_dont_contain_slashes(entry)
        assert_tags_dont_have_trailing_commas(entry)
      end

      site.posts.docs.each do |post|
        assert_new_posts_have_summary(post)
      end
    end
  end
end


def assert_has_layout(entry)
  if entry.path =~ /^theme\/style(_[0-9a-fA-F]{6})?\.scss/
    return
  end

  if !entry.data.include? "layout"
    raise "No layout key in #{entry.path.inspect}"
  end
end


def assert_summary_is_right_length(entry)
  if !entry.data["is_micropost"]
    if entry.data.include? "summary"
      if entry.data["summary"] == nil
        raise "Empty summary in #{entry.path.inspect}"
      elsif entry.data["summary"].length > 200
        # https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/markup
        raise "Summary too long in #{entry.path.inspect} (#{entry.data["summary"].length} > 200):\n#{entry.data["summary"].inspect}"
      end
    end
  end
end


def assert_tags_dont_contain_slashes(entry)
  # This tends to screw with path handling somewhat
  if entry.data.include? "tags"
    if entry.data["tags"].any? { |t| t.include? "/" }
      raise "Tag contains slash in #{entry.path.inspect}: #{entry.data["tags"].inspect}"
    end
  end
end


def assert_tags_dont_have_trailing_commas(entry)
  if entry.data.include? "tags"
    if entry.data["tags"].any? { |t| t.end_with? "," }
      raise "Tag ends with trailing comma in #{entry.path.inspect}: #{entry.data["tags"].inspect}"
    end
  end
end


def assert_new_posts_have_summary(entry)
  if entry.data["date"].to_date >= Date.new(2017, 7, 19)
    if !entry.data.include? "summary"
      raise "Post doesn't contain a summary: #{entry.path.inspect}"
    end
  end
end
