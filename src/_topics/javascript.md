---
layout: topic
title: JavaScript
---
JavaScript is a programming language which is widely used, especially on the web.
I mostly use it to add interactivity to web pages, although I have used frameworks like [React](https://react.dev) and [Next.js](https://nextjs.org) to build more complex interfaces in my day job.

## Articles about {{ page.title }}

{% with articles = site.articles | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}

## Notes about {{ page.title }}

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
