---
layout: page
title: Talks and workshops
last_updated: 2019-10-22 21:38:31 +0100
---

Below is a list of talks and workshops I've given, along with links to videos and slides where available.

If you'd like me to speak at your event, [get in touch](/#contact) for details.

In general, I'm happy to speak at community organised, non-profit conferences that have a Code of Conduct, a diverse lineup of speakers, and cover my costs (travel, conference tickets and accommodation).
I'll also speak at a for-profit event if we can agree a reasonable fee.
The more your event is doing to be [inclusive and accessible](https://alexwlchan.net/ideas-for-inclusive-events/), the more likely I am to say yes.

I enjoy talking about the social implications of technology, and the intersections with ethics, accessibility, diversity and inclusion.
These talks are particular favourites, and I'd love an opportunity to present them to a new audience:

-   [*The Curb Cut Effect*.](/2019/01/monki-gras-the-curb-cut-effect/)
    If we design with accessibility and inclusion in mind from the start, we end up with a better design for everyone.

-   [*Assume Worst Intent*.](/2018/09/assume-worst-intent/)
    Safety can't be an afterthought -- we need to anticipate somebody using our tools for harassment or bullying, and design with that in mind.

-   *A Robot Stole My Job*.
    A fun story about the value (and perils!) of build automation.

I can also write new talks, and I have a couple of ideas I have yet to present anywhere.
Think your event would be a good fit?
[Let's chat](/#contact).

If you enjoyed one of my talks, found it useful, or shared it with somebody else, [please let me know](/#contact) -- I love to know I've been helpful.

<figure>
  <img src="/images/pyconuk-speaking.jpg" alt="A person in a green top standing at a podium, in front of a large screen with the words “duplicate bugs”.">
  <figcaption>
    Espousing the benefits of sans I/O programming at PyCon UK 2019.
    The coordination of my slides, jumper and eyeshadow is entirely deliberate.
    Image courtesy <a href="https://www.flickr.com/photos/184390836@N04/48726548731/">Mark Hawkins</a>.
  </figcaption>
</figure>

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
