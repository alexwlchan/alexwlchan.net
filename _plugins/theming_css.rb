Jekyll::Hooks.register :posts, :post_render do |post|
  if post["theme"] && post["theme"]["color"]
    color = post["theme"]["color"]
    mainfile = "theme/style_#{color}.scss"
    if ! File.file?(mainfile)
      File.open(mainfile, 'w') { |file| file.write(<<-EOT
---
---

$primary-color: ##{color};

@import "_main.scss";
EOT
) }
      puts(mainfile)
    end
  end
end
