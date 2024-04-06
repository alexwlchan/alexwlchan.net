---
layout: page
title: Articles
nav_section: articles
---
If you want to follow along, these articles have [an RSS feed](/tom.xml).

<p>
  You can filter by tag:

  {% comment %}
    Get a list of all the tags in every article.
    Based on https://stackoverflow.com/a/41266780/1558022
  {% endcomment %}

  {% assign all_tags = '' | split: '' %}
  {% for article in site.articles %}
    {% assign all_tags = all_tags | concat: article.tags | uniq | sort %}
  {% endfor %}

  {% for tag in all_tags %}
    <a href="/articles/?tag={{ tag }}">{{ tag }}</a>
    {% unless forloop.last %} · {% endunless %}
  {% endfor %}
</p>

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

    filterStatus.innerHTML = `Showing articles tagged with <span class="selected_tag">${selectedTag}</span>. <a href="/til/" class="clear_filters">[x]</a>`;
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

---

<p id="filter_status">These are the current filters.</p>

<ul id="list_of_articles" class="plain_list">
{% for article in site.articles reversed %}
  {% unless article.index.exclude %}
    {% include article_card.html %}
  {% endunless %}
{% endfor %}
</ul>
