---
layout: page
title: Tags
---
{% assign visible_tags = site.data['visible_tags']|sort %}

<style>
  #tags {
    list-style-type: none;
    padding: 0;
    columns: 1;
    line-height: 1.7em;
  }

  #tags a:visited {
    color: var(--link-color);
  }

  @media screen and (min-width: 518px) {
    #tags {
      columns: 2;
    }
  }

  @media screen and (min-width: 747px) {
    #tags {
      columns: 3;
    }
  }
</style>

<ul id="tags">
  {% for tag_name in visible_tags %}
    <li>
      {% include tag_link.html %}
      ({{ site.data['tag_tally'][tag_name] }})
    </li>
  {% endfor %}
</ul>
