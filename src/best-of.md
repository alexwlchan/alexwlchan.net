---
layout: page
title: My favourite posts
---

{% assign posts = site.posts | where_exp: "post", "post.index != nil" | where: "index.best_of", true %}
{% include archive_list.html %}
