---
layout: topic
title: Ruby
date_updated: 2026-02-01 22:36:45 +00:00
topics: 
  - Computing
---
Ruby is a programming language which is particularly popular for web development.
I don't have much experience in Ruby, but when I used [Jekyll][jekyll] to power this blog, I wrote a bit of Ruby for [some plugins][jekyll-plugins].
It felt similar to Python but with slightly different syntax to what I'm used to.

[jekyll]: https://jekyllrb.com/
[jekyll-plugins]: https://jekyllrb.com/docs/plugins/



{% from "partials/topic_entries.html" import subtopics, topic_entries %}
{{ subtopics(page) }}

Here’s everything I’ve posted about Ruby:

{{ topic_entries(page) }}
