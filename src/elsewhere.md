---
layout: page
title: Elsewhere
---

This is a list of articles I've written, talks I've given, and podcasts I've been a guest on.
I sometimes link to these in the main blog feed; this page is meant to be a convenient reference.

<style>
.archive {
  margin-top: 1.2em;
  .archive__date {
    width: 68px;
    font-size: 0.85em;
    color: var(--accent-grey);
    text-align: right;
    vertical-align: top;
  }
}
</style>

<style>
  table.archive {
    margin-top: 0;
  }

  h3 {
    margin-bottom: 0.5em;
  }

  #talks_archive ul.dot_list {
    margin: 0;
  }

  #talks_archive tr:not(:last-child) .talk_description {
    padding-bottom: 0.75em;
  }

  .talk_description p:last-child {
    margin-bottom: 0;
  }
</style>

## Writing

{% set writing_entries = site.data["elsewhere"]["writing"] | sort(attribute="date", reverse=True) %}

### Last Week in AWS

<table class="archive">
  {%- for entry in writing_entries -%}
    {%- if entry.publication == "Last Week in AWS" -%}
      <tr>
        <td class="archive__date">{{ entry.date.strftime("%b %Y") }}</td>
        <td>
          <a href="{{ entry.url }}">{{ entry.title }}</a>
        </td>
      </tr>
    {%- endif -%}
  {%- endfor -%}
</table>

### Stacks development blog for Wellcome Collection

<table class="archive">
  {%- for entry in writing_entries -%}
    {%- if entry.publication == "Wellcome Collection development blog" -%}
      <tr>
        <td class="archive__date">{{ entry.date.strftime("%b %Y") }}</td>
        <td>
          <a href="{{ entry.url }}">{{ entry.title }}</a>
        </td>
      </tr>
    {%- endif -%}
  {%- endfor -%}
</table>

### Other writing

<table class="archive">
  {%- for entry in writing_entries -%}
    {%- if entry.publication == "Last Week in AWS" -%}
      {%- continue -%}
    {%- endif -%}

    {%- if entry.publication == "Wellcome Collection development blog" -%}
      {%- continue -%}
    {%- endif %}

    <tr>
      <td class="archive__date">{{ entry.date.strftime("%b %Y") }}</td>
      <td>
        <a href="{{ entry.url }}">{{ entry.title }}</a> – {{ entry.publication }}
      </td>
    </tr>
  {%- endfor -%}
</table>


## Talks and workshops

{% set talk_entries = site.data["elsewhere"]["talks"] | sort(attribute="date", reverse=True) %}

<table class="archive" id="talks_archive">
  {%- for talk in talk_entries -%}
    <tr>
      <td class="archive__date">{{ talk.date.strftime("%b %Y") }}</td>
      <td class="talk_description">
        {{ talk.title }}{% if talk.event %} @ {{ talk.event }}{% endif %}
        {%- if "links" in talk -%}
        <ul class="dot_list">
          {%- for label, link in talk.links.items() -%}
          <li><a href="{{ link }}">{{ label }}</a></li>
          {%- endfor -%}
        </ul>
        {%- endif -%}
        {%- if "description" in talk -%}
        {{ talk.description | markdownify }}
        {%- endif -%}
      </td>
    </tr>
  {%- endfor -%}
</table>



## Podcasts

{% set podcast_entries = site.data["elsewhere"]["podcasts"] | sort(attribute="date", reverse=True) %}

<table class="archive">
  {% for entry in podcast_entries %}
    <tr>
      <td class="archive__date">{{ entry.date.strftime("%b %Y") }}</td>
      <td>
        <a href="{{ entry.url }}">{{ entry.podcast}}: {{ entry.title }}</a>
      </td>
    </tr>
  {% endfor %}
</table>