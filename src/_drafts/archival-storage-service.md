---
layout: post
title: Building Wellcome Collection’s new archival storage service
summary:
category: Wellcome Collection
link: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e

index:
  best_of: true
---

Yesterday, I posted an article about the new cloud storage service I've been helping to build at Wellcome.
It was a fun project to work on, with much longer-term implications than most software projects.
Archives don’t aim to last for months and years, they aim for decades and *centuries*.
These files will have to last a long time, so we were designing a service meant to outlive all of us!

The files themselves will likely outlive any particular software stack, so we had to organise them in a way that will remain useful long after all our code is gone.
That means UUIDs and opaque databases are out, plain text and human-readable paths are in.

The post is meant for everyone, not just people who work in software or digital preservation.
It explains why digital preservation is important, why we need special storage, and what it takes to build this sort of service (beyond just "write code").
If you enjoy the posts on my blog, I hope you'll enjoy this article too.

Building the new storage service took nearly two years to finish, and it was a big piece of work.
I'm super pleased by how it turned out -- a reliable, robust platform for storing millions of files in the digital archive -- and I'm glad I get to share stories about how it was made.
