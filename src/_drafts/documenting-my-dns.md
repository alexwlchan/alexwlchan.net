---
layout: post
title: Documenting my DNS records
summary: |
  Saving my DNS records as TOML gives me a plaintext file where I can track changes, add comments, and feel more confident about managing my DNS.
tags:
  - dns
  - blogging-about-blogging
  - ruby
colors:
  index_light: "#c53f70"
  index_dark:  "#bbc660"
---
{% comment %}
    Card photo from https://www.pexels.com/photo/close-up-shot-of-a-hummingbird-4838540/
{% endcomment %}

# https://stackoverflow.com/questions/1162230/how-can-i-get-dns-records-for-a-domain-in-python

# https://stackoverflow.com/questions/2913226/getting-a-dns-txt-record-in-ruby



* I configure all my DNS in a web dashboard
    Always a bit wary of making changes
    What are all these records for?
    Can I revert easily?
    Want better way to manage

* Considered using an infra-as-code tool
    Appealing in theory
    Two issues:
        1. Can't do in my current provider would have to migrate away from existing, working setup
        2. Adds a lot of complexity, and I don't change things that often -- odds of it still working? Low

* Why is infra-as-code appealing?
    Track changes
    Put comments in code
    Easy rollbacks
    Can I get that without IaC? Yes

* Can dump existing DNS records with Python (kinda)
    Found Stack Overflow answer (link)
    Need to known all subdomains and record types, but I do -- can see in my web console
    So wrote script that dumps all DNS records
    Formats as TOML (example)

* Then I can add comments!
    Can reformat TOML with comments, example

* Check the commented TOML file into Git
    Then create GitHub Actions scheduled action to compare saved DNS records to current
    Can spot drift, and have a point of reference if I ever need to roll back
