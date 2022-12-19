---
layout: page
title: Posts
summary: Some of my favourite posts on alexwlchan.net.
---

I've been writing my blog since 2012, which is now over 300 posts and 300,000 words.
If you're new to the site, this page has some of my favourite posts from the archive -- or if you're looking for something specific, you can [see a list of everything I've posted](/all-posts/).

You can subscribe to my posts [as an RSS feed](/atom.xml).

{% assign best_posts = site.posts | sort: "date" | reverse | where: "index.best_of", "true" %}

<!-- there are {{ best_posts | size }} posts on this page. -->

<ul class="post_cards">
{% for post in best_posts %}
  {% include post_card.html %}
{% endfor %}
</ul>

Want even more?
Here's a list of [everything I've ever posted](/all-posts/).
