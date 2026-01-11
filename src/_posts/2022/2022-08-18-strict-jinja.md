---
layout: post
date: 2022-08-18 07:22:44 +0000
title: I always want StrictUndefined in Jinja
summary: When I'm writing templates with Jinja, strict behaviour is what I want, even if it's not the default.
tags:
  - python
  - python:jinja
colors:
  index_light: "#470906"
  index_dark:  "#FF4242"
---

I was doing some work with the templating library [Jinja] recently, and I was confused by some misbehaving code.
This is a simplified version of my project:

{% code lang="python" names="0:jinja2 1:t" %}
import jinja2

t = jinja2.Template("""
{% raw %}{% for copy in book_availablity %}
  {{ copy }}
{% endfor %}{% endraw %}
""")

print(t.render(book_availability=["copy 1", "copy 2", "copy 3"]))
{% endcode %}

I was expecting to see `copy 1`, `copy 2` and `copy 3` in the output -- but instead, the output was empty.
In the real code, there were several steps to build the `book_availability` value I was passing to the template, and I spent quite a bit of time checking I wasn't passing an empty list before spotting the actual issue.

Can you see it?

The variable I'm passing to the template is `book_availability`.
The variable the template is using is `book_availablity`.
In the latter, I've misspelt "availability", and Jinja lets the undefined value pass silently.
Rather than alert me to the error, it dropped in an empty collection.

Once I'd seen it, it was easy to fix, but I was frustrated I'd had to spot this myself.
Aren't computers meant to do this for me?

After a bit of reading, I found the Jinja documentation for [undefined values], which explains that if I pass `undefined=StrictUndefined`, it will warn me about any undefined template variables:

{% code lang="python" names="0:jinja2 1:t" %}
import jinja2

t = jinja2.Template("""
{% raw %}{% for copy in book_availablity %}
  {{ copy }}
{% endfor %}{% endraw %}
""", undefined=jinja2.StrictUndefined)

print(t.render(book_availability=["copy 1", "copy 2", "copy 3"]))
{% endcode %}

And indeed, if I run the updated code, it highlights my typo:

```
Traceback (most recent call last):
  File "/example.py", line 9, in <module>
    print(t.render(book_availability=['copy 1', 'copy 2', 'copy 3']))
  File "/root/.local/lib/python3.10/site-packages/Jinja/environment.py", line 1301, in render
    self.environment.handle_exception()
  File "/root/.local/lib/python3.10/site-packages/Jinja/environment.py", line 936, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "<template>", line 2, in top-level template code
Jinja.exceptions.UndefinedError: 'book_availablity' is undefined
```

I'm sure I've learnt this lesson before, and apparently I forgot.
Erroring on undefined variables is pretty much always what I want, so maybe this blog post will remind me to include `StrictUndefined` in my next project from the start.

[Jinja]: https://palletsprojects.com/p/jinja/
[undefined values]: https://jinja.palletsprojects.com/en/3.0.x/api/#undefined-types
