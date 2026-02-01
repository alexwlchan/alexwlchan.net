---
layout: topic
title: Terraform
date_updated: 2026-02-01 22:39:50 +00:00
topics: 
  - Computing
---
Terraform is an ["infrastructure-as-code" tool][wiki-iac] made by HashiCorp.
You write configuration files that define what infrastructure you want, and Terraform updates your deployed infrastructure to match.
Then those config files get checked in to your repo, alongside your source code.

I used Terraform to manage all the AWS resources at [Wellcome Collection][wellcome], and I use it occasionally in my current job at [Tailscale][tailscale].

[tailscale]: https://tailscale.com
[wellcome]: https://wellcomecollection.org
[wiki-iac]: https://en.wikipedia.org/wiki/Infrastructure_as_code



{% from "partials/topic_entries.html" import subtopics, topic_entries %}
{{ subtopics(page) }}

Here’s everything I’ve posted about Terraform:

{{ topic_entries(page) }}
