---
layout: page
title: Articles
nav_section: articles
---
I write articles about a variety of non-fiction topics, from [books](/2023/2023-in-reading/) to [braille](/2019/ten-braille-facts/), from programming to photography, from [colour theory](/2019/finding-tint-colours-with-k-means/) to [Chinese dictionaries](/2019/reading-a-chinese-dictionary/).

This is a list of all the articles I've written, sorted by date.
If you want to hear about new ones, you can [subscribe to my RSS feed](/atom.xml) or [follow me on social media](/contact/).

<details>
  <summary>Filter by tag</summary>
  <p>
    {% comment %}
      Get a list of all the tags in every article.
      Based on https://stackoverflow.com/a/41266780/1558022
    {% endcomment %}

    {% assign all_tags = '' | split: '' %}
    {% for article in site.posts %}
      {% unless article.index.exclude %}
        {% assign all_tags = all_tags | concat: article.visible_tags | uniq | sort %}
      {% endunless %}
    {% endfor %}

    {% for tag in all_tags %}
      <a href="?tag={{ tag }}">{{ tag }}</a>
      {% unless forloop.last %} · {% endunless %}
    {% endfor %}
  </p>
  
  <hr/>
</details>

<script>
  function filterByTag(selectedTag) {
    document
      .querySelectorAll("#list_of_articles > li")
      .forEach(function(liElem) {
        const tags = liElem.getAttribute("data-tags").split(" ");

        if (tags.includes(selectedTag)) {
          liElem.style.display = "block";
        } else {
          liElem.style.display = "none";
        }
      });

    const filterStatus = document.querySelector("#filter_status");

    filterStatus.innerHTML = `Showing articles tagged with <span class="selected_tag">${selectedTag}</span>. <a href="/articles/" class="clear_filters">[x]</a>`;
    filterStatus.style.display = "block";
  }

  window.addEventListener("DOMContentLoaded", function() {
    const selectedTag = new URLSearchParams(window.location.search).get("tag");

    if (selectedTag !== null) {
      filterByTag(selectedTag);
    }

    document.querySelector("#tag_cloud").style.display = "block";
  });
</script>

<noscript>
  <p>
    (Enable JavaScript to allow filtering by tag.)
  </p>
</noscript>

<p id="filter_status">These are the current filters.</p>

{% include article_card_styles.html selected_articles=site.posts %}

<ul id="list_of_articles" class="plain_list article_cards">
{% for article in site.posts %}
  {% unless article.index.exclude %}
    {% include article_card.html %}
  {% endunless %}
{% endfor %}
</ul>
