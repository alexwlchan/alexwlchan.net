---
layout: page
title: Notes
---

<style>
  @use "components/under_construction";
</style>

<blockquote class="under_construction">
  <p>
    <strong>This page is under construction!</strong>
  </p>
</blockquote>

Congratulations on finding a secret page!
There's not much here yet, is there?
But there will be soon!

{% with articles = site.notes %}
{% include "partials/article_links.html" %}
{% endwith %}
