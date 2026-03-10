---
layout: note
date: 2024-04-07 08:01:50 +01:00
title: How to shuffle an array in a Jekyll template
summary: |
  If you want an array in random order, you can use the `sample` filter to get a random sample of the same size as the original array.
topic: Ruby
hidden_topics:
  - Jekyll
  - Liquid
---
As part of the site rebuild, I wanted a way to shuffle a list of selected articles at build time.
This order will get "baked in" to the rendered output, but it still introduces *an* element of randomness and I rebuild the site once a day anyway.

It turns out there's no way to do this in vanilla Liquid, but Jekyll has a [`sample` filter](https://jekyllrb.com/docs/liquid/filters/#sample) that can pick one or more random values from an array:

{% raw %}
<pre class="lng-liquid"><code><span class="p">{%</span> assign <span class="n">fruits</span> <span class="o">=</span> <span class="s2">"apple,banana,cherry,damson"</span> | split<span class="o">:</span> <span class="s2">","</span> <span class="p">%}</span>
<span class="p">{%</span> assign fruits <span class="o">=</span> fruits | sample<span class="o">:</span> fruits.size <span class="p">%}</span>

<span class="p">{%</span> for <span class="n">f</span> in fruits <span class="p">%}</span>
  <span class="p">{{</span> f <span class="p">}}</span>
<span class="p">{%</span> endfor <span class="p">%}</span></code></pre>
{% endraw %}

If you look at the [implementation](https://github.com/jekyll/jekyll/blob/dbbfc5d48c81cf424f29c7b0eebf10886bc99904/lib/jekyll/filters.rb#L355-L364), this is just a thin wrapper about [Array.sample](https://ruby-doc.org/core-3.0.1/Array.html#method-i-sample), and it has similar behaviour -- e.g. no duplicates, never returns more than the original array.
