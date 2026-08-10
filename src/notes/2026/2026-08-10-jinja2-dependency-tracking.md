---
layout: note
date: 2026-08-10 03:07:37 +01:00
title: Track which templates are used by Jinja2
summary: Override the `get_template` method on the `Environment` and see which templates are summoned.
topic: Python
hidden_topics:
  - Jinja2
---
I write my own static site generator, and I do incremental rebuilds [when a source file changes][me-watch-files].
Currently I rebuild the entire website whenever a template changes, which is a lot of redundant work.

I thought it might be useful to track which templates are used by each page, and only rebuild a page if it uses the changed template.
I use [Jinja][jinja] for templating, and I wrote this script to work out where I should intercept template calls:

{% raw %}
```python {"names":{"1":"jinja2","2":"DictLoader","3":"Environment","4":"PrintingDictLoader","6":"get_source","7":"env","9":"template","17":"PrintingEnvironment","19":"get_template","20":"name","22":"args","23":"kwargs","31":"loader","33":"env"}}
from jinja2 import DictLoader, Environment


class PrintingDictLoader(DictLoader):
    def get_source(self, env: Environment, template: str):
        print(f"Loader.get_source({template!r})")
        return super().get_source(env, template)


class PrintingEnvironment(Environment):
    def get_template(self, name: str, *args, **kwargs):
        print(f"Environment.get_template({name!r})")
        return super().get_template(name, *args, **kwargs)


if __name__ == "__main__":
    loader = PrintingDictLoader(
        {
            "base.html": (
                "This is the base template"
                "{% block content %}{% endblock %}"
            ),
            "article.html": (
                '{% extends "base.html" %}'
                "{% block content %}"
                "This is article {{ title }}"
                "{% endblock %}"
            ),
        }
    )
    env = PrintingEnvironment(loader=loader)

    env.get_template("article.html").render(title="My first article")
    print("---")
    env.get_template("article.html").render(title="My second article")
```
{% endraw %}

Here's the output.
We can see the `get_template` method is called on both renders, but the loader method is only called once because the loaded template gets cached:

```console
$ python3 print_templates.py
Environment.get_template('article.html')
Loader.get_source('article.html')
Environment.get_template('base.html')
Loader.get_source('base.html')
---
Environment.get_template('article.html')
Environment.get_template('base.html')
```

I'm not pursuing this for now, because my template code is complicated enough already and I need to simplify it a bit before adding more complexity.
(Also, I spend less and less time editing templates, so I don't feel the effect as much.)

I'm writing this note in case I revisit this idea later.

[jinja]: https://jinja.palletsprojects.com/en/stable/
[me-watch-files]: /2026/watch-files-on-macos/#the-result
