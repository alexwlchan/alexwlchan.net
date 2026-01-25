---
layout: til
date: 2024-06-06 17:41:39 +01:00
title: How to highlight Python console sessions in Jekyll
summary: |
  Adding a couple of options to the `console` lexer (`console?lang=python&prompt=>>>`) gets you syntax highlighting for a Python console session.
tags:
  - jekyll
  - ruby:rouge
  - python
---
I was writing another article for this site, and I created a code block with backticks and the language identifier `pycon`, for a Python console session:

{% comment %}
  There's a zero-width space after "pycon" to stop my plugin from blatting it.
{% endcomment %}

<pre><code>&grave;&grave;&grave;pycon​
>>> print("Hello world!")
Hello world!
&grave;&grave;&grave;
</code></pre>

Apparently this doesn't work with Rouge, the syntax highlighter used by Jekyll and this site -- I got an unformatted `<pre>` block.
(A fact which has taken me far too long to notice!)

That language identifier works with several other Markdown syntax highlighting libraries, but apparently not Rouge.

## Rouge already knows how to do this!

I had a Google, and I found a [six-year old issue](https://github.com/rouge-ruby/rouge/issues/919) on the Rouge repo asking for syntax highlighting for Python console sessions.
And it has it!
It's just a bit non-obvious.

Rouge has a `console` lexer which I've used quite a few times, and that lexer can take options including `lang` and `prompt`.
By passing these options to the language identifier, I was able to get Python console session with syntax highlighting:

<pre><code>&grave;&grave;&grave;console?lang=python&prompt=>>>,...
>>> print("Hello world!")
Hello world!
&grave;&grave;&grave;
</code></pre>

(It occurs to me that if Rouge ever adds support [for the Fish shell](https://github.com/rouge-ruby/rouge/issues/1108), I might want to add `lang=fish` to my other uses of <code>```console</code>.)

## Enabling the `pycon` language identifier

That solution works, but it's a bit ugly and I won't remember to do it.

So I wrote [a Jekyll hook](https://jekyllrb.com/docs/plugins/hooks/) that modifies my Markdown source to replace `pycon` with `console?lang=…` whenever my site gets built:

{% code lang="ruby" names="3:p" %}
# _plugins/pycon_rouge_highlighter.rb
Jekyll::Hooks.register(%i[pages posts], :pre_render) do |p|
  p.content = p.content.gsub("\n```pycon\n", "\n```console?lang=python&prompt=>>>,...\n")
end
{% endcode %}

This is quite a brittle fix, but for my small site it should be fine.

As a sidebar: if you want `\n` to be the newline character in Ruby, you need to wrap it in double quotes.
`'a\nb'` is a string with a backslash in the middle.
`"a\nb"` is a string with a newline in the middle.
I got this wrong when I first wrote this code, and I was quite confused because I'm used to quote marks being interchangeable in Python.
