---
layout: topic
title: Git
---

Git is a version control system, used for tracking changes to source code.

## Notes about {{ page.title }}

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
