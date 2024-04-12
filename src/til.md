---
layout: page
title: Today I Learned (TIL)
nav_section: til
---
TIL stands for **today I learned**.
This is a collection of small, practical things I've learnt while writing software, which I thought were worth remembering and sharing with other people.

If you want to follow along, these posts have [their own RSS feed](/til/atom.xml).

<p>
  You can filter by tag:

  {% comment %}
    Get a list of all the tags in every TIL.
    Based on https://stackoverflow.com/a/41266780/1558022
  {% endcomment %}

  {% assign all_tags = '' | split: '' %}
  {% for til in site.til %}
    {% assign all_tags = all_tags | concat: til.visible_tags | uniq | sort %}
  {% endfor %}

  {% for tag in all_tags %}
    <a href="?tag={{ tag }}">{{ tag }}</a>
    {% unless forloop.last %} · {% endunless %}
  {% endfor %}
</p>

<script>
  function filterByTag(selectedTag) {
    document
      .querySelectorAll("#list_of_tils > li")
      .forEach(function(liElem) {
        const tags = liElem.getAttribute("data-tags").split(" ");

        if (tags.includes(selectedTag)) {
          liElem.style.display = "block";
        } else {
          liElem.style.display = "none";
        }
      });

    const filterStatus = document.querySelector("#filter_status");

    filterStatus.innerHTML = `Showing TILs tagged with <span class="selected_tag">${selectedTag}</span>. <a href="/til/" class="clear_filters">[x]</a>`;
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

<ul id="list_of_tils" class="plain_list">
{% for til in site.til reversed %}
  <li data-tags="{{ til.visible_tags | join }}">
    <h4><a href="{{ til.url }}">{{ til.title | markdownify_oneline }}</a></h4>

    <ul class="dot_list meta">
      <li>
        Posted
        <time datetime="{{ til.date | date: "%Y-%m-%d" }}">
          {{- til.date | date: site.date_format -}}
        </time>
      </li>

      {% if til.visible_tags.size > 0 %}
      <li>
        Tagged with
        {% assign tags = til.visible_tags | sort %}
        {% for t in tags %}
          <a href="?tag={{ t }}">{{ t }}</a>{% unless forloop.last %}, {% endunless %}
        {% endfor %}
      </li>
      {% endif %}
    </ul>

    {% if til.summary %}
      <p class="summary">{{ til.summary | markdownify_oneline }}</p>
    {% endif %}
  </li>
{% endfor %}
</ul>
