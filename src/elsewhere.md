---
layout: page
title: Elsewhere
---

This is a list of articles I've written, talks I've given, and podcasts I've been a guest on.
I sometimes link to these in the main blog feed; this page is meant to be a convenient reference.

<style>
  table.archive {
    margin-top: 0;
  }

  h3, h2 {
    margin-bottom: 0.5em;
  }

  #talks_archive ul.dot_list {
    margin: 0;
  }

  #talks_archive tr:not(:last-child) .talk_description {
    padding-bottom: 0.75em;
  }
</style>

## Writing

{% assign writing_entries = site.data["elsewhere"]["writing"] | sort: "date" | reverse %}

{% comment %}
<table class="archive">
  {% for entry in writing_entries %}
    <tr class="archive__entry">
      <td class="archive__date">{{ entry.date | date: "%b %Y" }}</td>
      <td class="archive__bestof"></td>
      <td>
        <a href="{{ entry.url }}">{{ entry.title | smartify }}</a>{% if entry.publication %}<br/>{{ entry.publication }}{% endif %}
      </td>
    </tr>
  {% endfor %}
</table>
{% endcomment %}

### Last Week in AWS

<table class="archive">
  {% for entry in writing_entries %}
    {% if entry.publication == "Last Week in AWS" %}
      <tr class="archive__entry">
        <td class="archive__date">{{ entry.date | date: "%b %Y" }}</td>
        <td class="archive__bestof"></td>
        <td>
          <a href="{{ entry.url }}">{{ entry.title | smartify }}</a>
        </td>
      </tr>
    {% endif %}
  {% endfor %}
</table>

### The Wellcome Collection development blog

<table class="archive">
  {% for entry in writing_entries %}
    {% if entry.publication == "Wellcome Collection development blog" %}
      <tr class="archive__entry">
        <td class="archive__date">{{ entry.date | date: "%b %Y" }}</td>
        <td class="archive__bestof"></td>
        <td>
          <a href="{{ entry.url }}">{{ entry.title | smartify }}</a>
        </td>
      </tr>
    {% endif %}
  {% endfor %}
</table>


## Talks and workshops

{% assign talk_entries = site.data["elsewhere"]["talks"] | sort: "date" | reverse %}

<table class="archive" id="talks_archive">
  {% for talk in talk_entries %}
    <tr class="archive__entry">
      <td class="archive__date">{{ talk.date | date: "%b %Y" }}</td>
      <td class="archive__bestof"></td>
      <td class="talk_description">
        {{ talk.title }}{% if talk.event %} @ {{ talk.event }}{% endif %}
        {% if talk.links %}
        <ul class="dot_list">
          {% for talk_link in talk.links %}
          <li><a href="{{ talk_link[1] }}">{{ talk_link[0] }}</a></li>
          {% endfor %}
        </ul>
        {% endif %}
        <a href="{{ entry.url }}">{{ entry.title | smartify }}</a>{% if entry.publication %}<br/>{{ entry.publication }}{% endif %}
      </td>
    </tr>
  {% endfor %}
</table>



## Podcasts

{% assign podcast_entries = site.data["elsewhere"]["podcasts"] | sort: "date" | reverse %}

<table class="archive">
  {% for entry in podcast_entries %}
    <tr class="archive__entry">
      <td class="archive__date">{{ entry.date | date: "%b %Y" }}</td>
      <td class="archive__bestof"></td>
      <td>
        <a href="{{ entry.url }}">{{ entry.podcast}}: {{ entry.title | smartify }}</a>
      </td>
    </tr>
  {% endfor %}
</table>