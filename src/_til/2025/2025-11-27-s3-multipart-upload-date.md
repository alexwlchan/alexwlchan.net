---
layout: til
title: The LastModified date of an S3 multipart upload is when the upload started, not when it finished
date: 2025-11-27 21:59:35 +00:00
tags:
  - aws:amazon s3
---
When you upload a large file to Amazon S3 (more than 5GB), you need to use a [multipart upload][s3-multipart-upload].
This takes three steps:

1.  Create the multipart upload
2.  Upload the individual parts
3.  Complete the multipart upload

When that's done, what's the last modified date of the final object?

I thought it would be when the multipart object is *completed*, but the [Amazon S3 User Guide][s3-user-guide] explains that it's not:

> <dl><dt><code>Last-Modified-Date</code></dt><dd>The object creation date or the last modified date, whichever is the latest. For multipart uploads, the object creation date is the date of initiation of the multipart upload.</dd></dl>

I found this quite surprising!
I can imagine explanations for why this makes sense, but it wans't what I expected.

## How did I discover this?

I was watching a bucket for new uploads, and I saw objects appear that had ostensibly been uploaded hours prior -- which definitely hadn't been there a few minutes ago!

There was a process creating the files and uploading them to S3, and it took several hours to create each of those files.
The process was uploading the files progressively, rather than saving the file to a local disk and deferring the upload until the creation was complete.
This meant that the upload was initiated at the start of the process, but I couldn't see the object in the bucket until much later.

[s3-multipart-upload]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html
[s3-user-guide]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html
