---
layout: post
date: 2020-06-20 08:36:39 +0000
title: Large things living in cold places
tags: digital-preservation wellcome aws amazon-s3
link: https://stacks.wellcomecollection.org/large-things-living-in-cold-places-66cbc3603e14
---

On Wednesday, I wrote about [some recent work we've been doing at Wellcome][stacks].
We keep our entire digital archive in Amazon S3, and we're using Glacier (a cold storage tier) to keep costs down as we bring in ever-larger files.
The article explains why we chose Glacier, how pricing for cloud storage works, and some of the practical pieces that make it work.

Writing this post was an interesting challenge, because I wanted it to make sense to two different audiences.
I wanted people who work in museums and archives to feel they understand the technical decisions, and to see cloud storage as more than a monolithic, opaque container.
I wanted people who work in technology to understand our archival context, and to see our real-world use case for cloud storage.
They meet in the middle, but they're starting from different places, and it took a lot of editing to get the right balance.

(The paragraph about the salt mine had lots of versions, because I'm less familiar with our physical collections.
I had to talk to multiple people before I understood it well enough to describe properly.)

If you've watched this blog carefully, you'll have seen bits of this work poking through already.
Last month I shared my [alternative diagram for illustrating S3 lifecycle transitions][transitions], which I created while I was doing research for this project.
I also shared [a script for measuring the size of your S3 buckets][buckets], which shows you how much data is in each storage class.

If you enjoy reading my blog, you might also enjoy the site whose name inspired the title of this post -- [Terrible things happening in cold places][coldplaces].

[stacks]: https://stacks.wellcomecollection.org/large-things-living-in-cold-places-66cbc3603e14
[transitions]: /2020/05/illustrating-lifecycle-transitions-in-amazon-s3/
[buckets]: /2020/03/finding-the-size-of-your-s3-buckets/
[coldplaces]: http://www.terriblethingshappeningincoldplaces.com/about
