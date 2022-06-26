# Validating the front matter in Markdown files

All the source files for the blog are written in Markdown, and at the top they have some structured data, in the form of [Front Matter]:

```
---
layout: post
title: Checking lots of URLs with curl
---
```

I want to make sure I'm using these fields consistently, so I have a JSON Schema definition for my front matter: [front-matter.json](../front-matter.json).

Then I validate every Markdown file's front matter against this schema as part of my [linting plugin](../src/_plugins/linter.rb).

[Front Matter]: https://jekyllrb.com/docs/front-matter/



## Alternative approaches

-   I considered using the [jekyll-data_validation plugin][plugin], but you have to run the validation as part of a separate `jekyll validate` command; I wanted it as part of my existing `jekyll lint` command.

[plugin]: https://github.com/cityoffortworth/jekyll-data_validation
