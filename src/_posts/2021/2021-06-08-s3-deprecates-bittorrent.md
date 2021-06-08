---
layout: post
date: 2021-06-08 06:21:15 +0000
title: Amazon S3 has deprecated BitTorrent
summary:
tags: amazon-s3
---

Did you know S3 supported BitTorrent for downloads?
If not, too late, [it's going away soon](https://github.com/awsdocs/amazon-s3-userguide/commit/0d1759880ccb1818ab0f14129ba1321c519d2ac1#diff-72be9d82d9be9bda6a297a4fbd11aca66ecde97e4f90de6f86bdf95c5f6b72c0):

> As of April 29, 2021 Amazon S3 is discontinuing the S3 BitTorrent feature and it will no longer be available to enable.
> AWS will support customers currently using the S3 BitTorrent feature for 12 months.
> After April 29, 2022, BitTorrent clients will no longer connect to Amazon S3.

This news snuck out very quietly in an update to the S3 User Guide, but the entire page about S3 BitTorrent was [removed less than a week later](https://github.com/awsdocs/amazon-s3-userguide/commit/7a83e40b35637a9d42827b9b296b0112e688c15f#diff-72be9d82d9be9bda6a297a4fbd11aca66ecde97e4f90de6f86bdf95c5f6b72c0).

I assume AWS will actively reach out to customers who use S3 BitTorrent, but otherwise this news is almost impossible to find.
It's mentioned in a few forum threads, Reddit posts, and [tweets](https://twitter.com/alexwlchan/status/1402141021476167684), but that's it.
This short post is meant to create a more easily searchable link for a fairly rare example of an AWS feature deprecation.
