---
layout: topic
title: Builds and CI
---
This topic is about tools used to automate building software.
This includes local tools (like [Make][wiki-make]) and hosted services for continuous integration and deployment (like [Buildkite][buildkite] or [GitHub Actions][gh-actions]).

[buildkite]: https://buildkite.com/
[gh-actions]: https://github.com/features/actions
[wiki-make]: https://en.wikipedia.org/wiki/Make_(software)

## Notes about {{ page.title }}

{% with articles = site.notes | selectattr("topic", "eq", page.title) %}
{% include "partials/article_links.html" %}
{% endwith %}
