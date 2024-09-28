---
layout: page
title: Today I Learned (TIL)
nav_section: til
---
TIL stands for **today I learned**.
This is a collection of small, practical things I've learnt while writing software, which I thought were worth remembering and sharing with other people.

If you want to follow along, these posts have [their own RSS feed](/til/atom.xml).

---

<ul id="list_of_tils" class="plain_list">
{% for til in site.til reversed %}
  <li data-tags="{{ til.visible_tags | join }}">
    <h4><a href="{{ til.url }}">{{ til.title | markdownify_oneline }}</a></h4>

    <ul class="dot_list meta">
      {% if til.visible_tags.size > 0 %}
      <li>
        Tagged with
        {% assign tags = til.visible_tags | sort %}
        {% for t in tags %}
          <a href="/tags/{{ t }}/">{{ t }}</a>{% unless forloop.last %}, {% endunless %}
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
