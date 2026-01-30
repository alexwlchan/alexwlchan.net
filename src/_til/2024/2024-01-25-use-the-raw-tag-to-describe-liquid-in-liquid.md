---
layout: til
date: 2024-01-25 21:55:11 +00:00
title: Use the `{% raw %}` tag to describe Liquid in Liquid
summary: |
  If you're trying to write about using Liquid tags in a Liquid-based site, wrapping your tags in the `{% raw %}` tag will prevent them being rendered.
tags:
  - liquid
  - jekyll
---
This is a problem I had when trying to write my TIL about [the `{% raw %}{% capture %}{% endraw %}` tag](/til/2024/use-the-capture-tag-for-complex-strings/).
I'd written an example in my Markdown source code:

{% raw %}
<pre><code>You can use the [capture tag] to create a new variable:<br>
&grave;&grave;&grave;liquid
{% capture variable %}
  value
{% endcapture %}
&grave;&grave;&grave;</code></pre>

{% endraw %}

but the rendered `<pre>` block was empty -- Liquid ran before the Markdown processor, so it had captured the variable and left empty space.

I found [an answer by Marcel Jackwerth](https://stackoverflow.com/a/7585479/1558022) on Stack Overflow that suggests using the `{% raw %}{% raw %}{% endraw %}` tag, which in this case became:

<pre><code>You can use the [capture tag] to create a new variable:

&grave;&grave;&grave;liquid
{&percnt; raw &percnt;}{% raw %}{% capture variable %}
  value
{% endcapture %}{% endraw %}{&percnt; endraw &percnt;}
&grave;&grave;&grave;</code></pre>

(Trying to write a TIL about the `{% raw %}{% raw %}{% endraw %}` is even more of a mess of `raw` tags and percent-encoding to get the right output from Liquid.)