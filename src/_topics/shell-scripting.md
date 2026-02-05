---
layout: topic
title: Shell scripting
---

This topic is about bash, zsh, fish, and other shell languages.

## Notes about {{ page.title }}

{% with articles = site.notes|filter_for_topic(topic_name=page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
