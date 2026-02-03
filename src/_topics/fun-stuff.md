---
layout: topic
title: Fun stuff
---

This is silly stuff I've made and put on the Internet.

* [Checkbox text adventure](/fun-stuff/checkbox-text-adventure/)
* [How long is my data?](/fun-stuff/howlongismydata/)
* [Looped squares](/fun-stuff/looped-squares/)
* [Marquee rocket](/fun-stuff/marquee-rocket/)
* [Rainbow hearts](/fun-stuff/rainbow-hearts/)
* [Rainbow valknuts](/fun-stuff/rainbow-valknuts/)
* [UK stations map](/fun-stuff/uk-stations-map/)

## Notes about {{ page.title }}

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
