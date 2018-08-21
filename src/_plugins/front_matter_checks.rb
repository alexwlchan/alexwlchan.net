module FrontMatterChecks
  class Generator < Jekyll::Generator
    def generate(site)
      entries = site.posts.docs + site.pages
      entries.each do |entry|
        assert_has_layout(entry)
        assert_summary_is_right_length(entry)
        assert_tags_dont_have_trailing_commas(entry)
      end
    end
  end
end


def assert_has_layout(entry)
  if entry.path =~ /^theme\/style(_[0-9a-f]{6})?\.scss/
    return
  end

  if !entry.data.include? "layout"
    raise "No layout key in #{entry.path.inspect}"
  end
end


def assert_summary_is_right_length(entry)
  if entry.data.include? "summary"
    # https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/markup
    if entry.data["summary"].length > 200
      raise "Summary too long in #{entry.path.inspect} (#{entry.data["summary"].length} > 200):\n#{entry.data["summary"].inspect}"
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
