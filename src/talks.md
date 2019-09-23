---
layout: page
title: Talks and workshops
last_updated: 2018-09-23 22:34:26 +0100
---

{% for talk_year in site.data["talks"] %}
  {% assign year = talk_year[0] %}
  {% assign talks = talk_year[1] %}
  <h2>{{ year }}</h2>

  <ul class="talks">
  {% for t in talks %}
    <li>
      <div class="talk__date">{{ t.date }}</div>
      <div class="talk__description">
        <span class="talk__title">
          {% if t.is_new %}<span class="talk__new">{% endif %}
          <em>{{ t.title | smartify }}</em>, {{ t.event | smartify }}
          {% if t.is_new %}</span>{% endif %}
          {% if t.variant %}({{ t.variant }}){% endif %}
        </span>
        {% if t.links %}
        <ul class="dot_list">
          {% for talk_link in t.links %}
          <li><a href="{{ talk_link[1] }}">{{ talk_link[0] }}</a></li>
          {% endfor %}
        </ul>
        {% endif %}

        {% if t.description %}
        <p>{{ t.description | smartify | render_markdown }}</p>
        {% endif %}
      </div>
    </li>
  {% endfor %}
  </ul>
{% endfor %}

<hr/>
