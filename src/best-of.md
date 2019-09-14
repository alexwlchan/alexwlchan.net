---
layout: page
title: My favourite posts
---

I've written a lot of posts -- this page has some of my favourites.
If you'd rather read the complete list, I have [another page](/all-posts/) with those too.

{% assign posts = site.posts | where_exp: "post", "post.index != nil" | where: "index.best_of", true %}
{% include archive_list.html %}
