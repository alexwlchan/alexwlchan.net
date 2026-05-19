---
layout: page
title: Projects
---

<ul>
{% for p in site.repos %}
<li><a href="/projects/{{ p.name }}/">{{ p.name }}</a> – {{ p.description }}</li>
{% endfor %}
</ul>