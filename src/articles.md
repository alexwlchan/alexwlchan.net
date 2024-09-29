---
layout: page
title: Articles
nav_section: articles
---
I write articles about a variety of non-fiction topics, from [books](/2023/2023-in-reading/) to [braille](/2019/ten-braille-facts/), from programming to photography, from [colour theory](/2019/finding-tint-colours-with-k-means/) to [Chinese dictionaries](/2019/reading-a-chinese-dictionary/).

This is a list of all the articles I've written.
If you want to hear about new ones, you can [subscribe to my RSS feed](/atom.xml) or [follow me on social media](/contact/).

<style>
  .article_links + .article_cards {
    margin-top: 2em;
  }
</style>

---

{% comment %}
  The logic here is quite fiddly and took a lot of thought.  It may also be
  implementing a bad design.
  
  Here's the basic idea: I want to intersperse these two types:
  
  * featured articles (shown as cards)
  * regular articles (shown as links)
  
  I also want to maintain a vague semblance of chronological order, but it doesn't
  have to be strict.  In particular I would rather make it look nice than make the
  sorting completely accurate (because I make no guarantees that this is date sort).
  
  Showing a single card on its own looks a bit odd (maybe I should redesign the
  cards to be horizontal, but that's a bigger piece of work).
  
  Here's the rough idea:
  
  * go through the list of articles, and build a running list of featured/unfeatured
    articles that haven't been shown yet
  * whenever you have enough featured articles to show (i.e. 2), check how many
    unfeatured articles are waiting to be shown
    
    - if ≥3, show those first
    - if <3, keep them and wait for a later opportunity to display them
  * at the end, display anything not yet displayed
{% endcomment %}

{% assign featured_posts  = "" | split: ',' %}
{% assign remaining_posts = "" | split: ',' %}

{% assign add_data_metadata = true %}

{% for this_article in site.posts %}
  {% if this_article.index.exclude %}
    {% continue %}
  {% endif %}

  {% if this_article.index.feature %}
    {% assign featured_posts = featured_posts | push: this_article %}
  {% else %}
    {% assign remaining_posts = remaining_posts | push: this_article %}
  {% endif %}

  {% unless featured_posts.size == 2 %}
    {% continue %}
  {% endunless %}

  {%- include article_cards.html articles=featured_posts %}
  {% assign featured_posts = "" | split: ',' %}
  
  {% if remaining_posts.size >= 3 %}
  {%- include article_links.html articles=remaining_posts %}
  {% assign remaining_posts = "" | split: ',' %}
  {% endif %}
{% endfor %}

{% comment %}
  At the end, display anything not yet displayed
{% endcomment %}

{% include article_cards.html articles=featured_posts %}
{% include article_links.html articles=remaining_posts %}
