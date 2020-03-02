---
layout: post
date: 2020-03-02 07:48:10 +0000
title: Finding the size and cost of each of your S3 buckets
summary: A Python script that tells you how many objects and how many bytes there are in each of your S3 buckets.
category: Amazon Web Services
link: https://github.com/alexwlchan/s3_summary_spreadsheet_script
---

Whenever I look at [our AWS bill], one of the biggest costs is always S3 storage.
That's not a surprise -- our account holds, among other things, two copies of Wellcome Collection's [entire digital archive], which is nearly 120TB and growing every day.
If we ever got a bill and there *wasn't* a big number next to S3, that's a reason to to panic.

[our AWS bill]: /2019/11/aws-costs-graph/
[entire digital archive]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e

We spend about $25,000 on S3 storage every year.
That's not nothing, but it's also not exorbitant in the context of a large organisation.
It'd be nice to find some easy wins, but developer time costs money too -- it's worth an hour to save a few thousand dollars a year, but a complete audit to squeeze out a few extra dollars is out of the question.

If we wanted to reduce this cost, we'd need to know where it’s coming from: which buckets have the biggest files?
That would give us an idea of where to start deleting things first – given what we use all our buckets for, are any of them surprisingly large or populous?

I wrote a script to get an overview of our buckets.
It creates a spreadsheet that tells me:

*   How many buckets do I have?
*   How many objects are in each bucket?
*   How many bytes are in each bucket?

Among other things, the first time I ran it I discovered:

*   Some leftover files from old experiments that could be deleted
*   A bucket with versioning enabled, where we'd "deleted" all the objects, but we were still paying to keep the files anyway
*   A bucket where objects were being saved in the wrong storage class

It uses CloudWatch Metrics to get an idea of the total number of bytes in each bucket.
Those figures are only updated every couple of days, but they're accurate enough to get an idea of which buckets are worth further investigation.

It took about half an hour to write the initial version, and a few hours more to tidy it up.
I've posted the script [on GitHub](https://github.com/alexwlchan/s3_summary_spreadsheet_script) so other people can use it to find quick wins in their own AWS accounts.
If you have a big S3 bill too, you might want to try it and see if you have any unexpectedly large buckets.
