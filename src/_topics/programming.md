---
layout: topic
title: Programming
---

I've been a professional software developer since 2014, and a hobbyist for several years before that.
This blog started as a way for me to share code snippets, and writing about my code has helped me grow as a programmer.

Sub-topics:

<ul>
  {%- for c in get_topic_by_name(page.title).children | sort(attribute="name") -%}
  <li>
    <a href="{{ c.href }}">{{ c.name }}</a>
  </li>
  {%- endfor -%}
</ul>

## Notes about {{ page.title }}

{% with articles = site.notes|filter_for_topic(topic_name=page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
