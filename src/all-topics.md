---
layout: page
title: All topics
---
This is a debugging page to help me see the hierarchy of topics.

{% macro topic(t) -%}
  <li>
    {% if t.url %}<a href="{{ t.url }}">{% endif %}{{ t.label | markdownify_oneline }}{% if t.url %}</a>{% endif %}
    {%- if t.children -%}
    <ul>
      {%- for c in t.children -%}
        {{- topic(c) -}}
      {%- endfor -%}
    </ul>
    {%- endif -%}
  </li>
{%- endmacro -%}

<ul>
{% for t in site.topics.values() | sort(attribute="label") %}
  {%- if t.parent == None -%}
    {{ topic(t) }}
  {%- endif -%}
{% endfor %}
</ul>
