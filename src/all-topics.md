---
layout: page
title: All topics
colors:
  css_light: "#115bda"
  css_dark:  "#40c3ff"
---
{% set top_level_topics = all_topics.values()
    | selectattr("parent", "none")
    | sort(attribute="name")
    | list %}

{%- macro topic_info(t) -%}
<li>
  <a href="{{ t.href }}">{{ t.name }}</a>
  {%- if t.children -%}
  <ul>
    {%- for c in t.children -%}
      {{- topic_info(c) -}}
    {%- endfor -%}
  </ul>
  {%- endif -%}
</li>
{%- endmacro -%}


<ul>
  {%- for t in top_level_topics -%}
    {{- topic_info(t) -}}
  {%- endfor -%}
</ul>
