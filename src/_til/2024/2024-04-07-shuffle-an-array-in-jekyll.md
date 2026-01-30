---
layout: til
date: 2024-04-07 08:01:50 +01:00
title: How to shuffle an array in a Jekyll template
summary: |
  If you want an array in random order, you can use the `sample` filter to get a random sample of the same size as the original array.
tags:
  - jekyll
  - liquid
---
As part of the site rebuild, I wanted a way to shuffle a list of selected articles at build time.
This order will get "baked in" to the rendered output, but it still introduces *an* element of randomness and I rebuild the site once a day anyway.

It turns out there's no way to do this in vanilla Liquid, but Jekyll has a [`sample` filter](https://jekyllrb.com/docs/liquid/filters/#sample) that can pick one or more random values from an array:

```liquid
{% raw %}{% assign fruits = "apple,banana,cherry,damson" | split: "," %}
{% assign fruits = fruits | sample: fruits.size %}

{% for f in fruits %}
  {{ f }}
{% endfor %}{% endraw %}
```

If you look at the [implementation](https://github.com/jekyll/jekyll/blob/dbbfc5d48c81cf424f29c7b0eebf10886bc99904/lib/jekyll/filters.rb#L355-L364), this is just a thin wrapper about [Array.sample](https://ruby-doc.org/core-3.0.1/Array.html#method-i-sample), and it has similar behaviour -- e.g. no duplicates, never returns more than the original array.
