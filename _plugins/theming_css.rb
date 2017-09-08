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

    headerfile = "theme/specktre_#{color}.png"
    if ! File.file?(headerfile)
      puts("we need to build the header file!")
    end
  end
end
