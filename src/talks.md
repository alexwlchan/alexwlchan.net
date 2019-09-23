---
layout: page
title: Talks and workshops
last_updated: 2019-09-23 21:29:55 +0200
---

This is a list of talks and workshops I've given, along with links to videos and slides where available.

If you'd like me to speak at your event, [contact me](/#contact) for details.

In general, I'm happy to speak at community organised, non-profit conferences that have a Code of Conduct, a diverse lineup of speakers, and cover my costs (travel, conference tickets and accommodation).
I'll also speak at a for-profit event if we can agree a reasonable fee.
The more your event is doing to be [inclusive and accessible](https://alexwlchan.net/ideas-for-inclusive-events/), the more likely I am to say yes.

If you enjoyed one of my talks, found it useful, or shared it with somebody else, [please let me know](/#contact) -- I love to know I've been helpful.



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
