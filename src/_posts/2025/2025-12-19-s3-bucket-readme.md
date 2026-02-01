---
layout: post
date: 2025-12-19 22:57:16 +00:00
title: Adding a README to S3 buckets with Terraform
summary: If you create an S3 bucket in Terraform, you can also create a README to help a future sysadmin understand what the bucket is for.
topics:
  - Terraform
colors:
  css_light: "#18860e"
  css_dark:  "#5ff042"
---
I was creating a new S3 bucket today, and I had an idea -- what if I add a README?

Browsing a list of S3 buckets is often an exercise in code archeology.
Although people try to pick meaningful names, it's easy for context to be forgotten and the purpose lost to time.
Looking inside the bucket may not be helpful either, if all you see is binary objects in an unknown format named using UUIDs.
A sentence or two of prose could really help a future reader.

We manage our infrastructure with Terraform and the Terraform AWS provider can [upload objects to S3][tf-s3-object], so I only need to add a single resource:

<pre><code><span class="k">resource</span> <span class="s2">"aws_s3_bucket"</span> <span class="s2">"example"</span> <span class="p">{</span>
  <span class="nx">bucket</span> <span class="o">=</span> <span class="s2">"alexwlchan-readme-example"</span>
<span class="p">}</span>

<span class="k">resource</span> <span class="s2">"aws_s3_object"</span> <span class="s2">"readme"</span> <span class="p">{</span>
  <span class="nx">bucket</span>  <span class="o">=</span> <span class="nx">aws_s3_bucket</span><span class="p">.</span><span class="nx">example</span><span class="p">.</span><span class="nx">id</span>
  <span class="nx">key</span>     <span class="o">=</span> <span class="s2">"README.txt"</span>
  <span class="nx">content</span> <span class="o">=</span> <span class="s2">&lt;&lt;EOF</span>
<span class="s2">This bucket stores log files for the Widget Wrangler Service.</span>

<span class="s2">These log files are anonymised and expire after 30 days.</span>

<span class="s2">Docs: http://internal-wiki.example.com/widget-logs</span>
<span class="s2">Contact: logging@example.com</span>
<span class="s2">EOF</span>
  <span class="nx">content_type</span> <span class="o">=</span> <span class="s2">"text/plain"</span>
<span class="p">}</span>
</code></pre>

Now when the bucket is created, it comes with its own explanation.
When you open the bucket in the S3 console, the README appears as a regular object in the list of files.

This is an example, but a real README needn't be much longer:

*   What is the bucket for?
*   Who do I talk to about what's in this bucket?
*   Where can I find out more?

This doesn't replace longer documentation elsewhere, but it can be a useful pointer in the right direction.
It's a quick and easy way to help the future sysadmin who's trying to understand an account full of half-forgotten S3 buckets, and my only regret is that I didn't think to use `aws_s3_object` this way sooner.

[tf-s3-object]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_object
