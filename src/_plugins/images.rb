def render_image(path:, alt_text:, title:)
  <<-EOT
<a href="#{path}"><img src="#{path}" alt="#{alt_text}" title="#{title}"></a>
EOT
end
