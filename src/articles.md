---
layout: page
title: Articles
nav_section: articles
---
I write articles about a variety of non-fiction topics, from [books](/2023/2023-in-reading/) to [braille](/2019/ten-braille-facts/), from programming to photography, from [colour theory](/2019/finding-tint-colours-with-k-means/) to [Chinese dictionaries](/2019/reading-a-chinese-dictionary/).

This is a list of all the articles I've written, sorted by date.
If you want to hear about new ones, you can [subscribe to my RSS feed](/atom.xml) or [follow me on social media](/contact/).

---

{% include article_card_styles.html selected_articles=site.posts %}

<ul id="list_of_articles" class="plain_list article_cards">
{% for article in site.posts %}
  {% unless article.index.exclude %}
    {% include article_card.html %}
  {% endunless %}
{% endfor %}
</ul>
