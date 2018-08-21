module FrontMatterChecks
  class Generator < Jekyll::Generator
    def generate(site)
      site.posts.docs.each do |post|
        assert_has_layout(post)
      end

      site.pages.each do |page|
        assert_has_layout(page)
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
