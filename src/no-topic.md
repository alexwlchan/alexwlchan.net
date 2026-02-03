---
layout: page
title: No topics
---

<ol>
{% for p in site.pages + site.articles %}
  {% if not p.topics %}
  {% if p.md_path and p.template_name != "page.html" and p.template_name != "topic.html" %}
    <li><a href="txmt://open?url=file://{{ p.md_path.absolute() }}">{{ p.url }}</a> ({{ p.title | strip_html }})</li>
  {% endif %}
  {% endif %}
{% endfor %}
</ol>