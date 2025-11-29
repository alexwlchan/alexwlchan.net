---
layout: til
title: Collapsing whitespace in a Liquid template
summary: Output an empty string with stripped whitespace, that is `{{- "" -}}`.
date: 2025-11-29 08:39:07 +0000
tags:
  - liquid
---
Here's an excerpt from one of my Liquid templates:

```html
<p class="title">
  {% raw %}{{- article.title -}}{% endraw %}
</p>

<p class="summary">
  {% raw %}{{- article.summary | strip -}}{% endraw %}
</p>
```

When this gets rendered, it inserts a space between the closing/opening `<p>` tags:
  
{% code lang="html" wrap="true" %}
<p class="title">This is the title of the article</p>·<p class="summary">This is the summary of the article</p>
{% endcode %}

I don't want the space in the final HTML -- it's unnecessary, and my current [HTML minifier][minifying-html] doesn't optimise it away.

I could remove the space by modifying the template to remove the newlines between the `</p>` and `<p class="summary">`, but that would make the template more difficult to read.
I recently thought of a better way to do it: insert an empty string between them, and use Liquid's [whitespace control][whitespace-control] to strip whitespace from both sides.
Here's the new template:

```html
<p class="title">
  {% raw %}{{- article.title -}}{% endraw %}
</p>

{% raw %}{{- "" -}}{% endraw %}

<p class="summary">
  {% raw %}{{- article.summary | strip -}}{% endraw %}
</p>
```

This renders the HTML without the unwanted space, and it keeps the template nice and readable.
Other templating languages have similar syntax for inserting values and stripping whitespace, so I'm sure I could use this technique there as well.

This is a micro-optimisation that affects the size of the final page by maybe 0.1% -- but it's already aggressively optimised, so tiny wins like this are all I can do to keep the page size down.

[minifying-html]: /2025/minifying-html/
[whitespace-control]: https://shopify.github.io/liquid/basics/whitespace/
