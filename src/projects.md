---
layout: page
title: Projects
---

<ul>
{% for p in git_repos %}
<li><a href="/projects/{{ p.name }}/">{{ p.name }}</a> – {{ p.description }}</li>
{% endfor %}
</ul>