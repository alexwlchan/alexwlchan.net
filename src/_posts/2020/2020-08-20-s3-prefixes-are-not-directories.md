---
layout: post
date: 2020-08-20 06:50:04 +0000
title: S3 prefixes are not directories
summary: Although an S3 prefix looks a lot like a directory path, they aren't the same. Whether or not you include a trailing slash can change the behaviour.
tags:
  - aws:amazon s3
  - aws
  - path-problems
---

I didn't expect to be writing another post about S3 keys so soon, but life comes at you fast.
Less than twenty-four hours after posting [S3 keys are not file paths](/2020/s3-keys-are-not-file-paths/), I hit a *different bug* caused by poor handling of S3 keys.
(Yes, really.)

The storage service I work on has to store [different versions of a "bag"](https://stacks.wellcomecollection.org/how-we-store-multiple-versions-of-bagit-bags-e68499815184), and we want those versions to be human-readable.
We number those versions `v1`, `v2`, `v3`, and we include that version as part of the S3 key for each object in the archive.

If we want to list the files in a directory on a filesystem (say, all the files in v1), we can use something like [the `ls` command](https://en.wikipedia.org/wiki/Ls):

```console
$ ls bags/b1234/v1/
```

If `v1` is a directory, this returns the same results whether or not you include the trailing slash.
I've seen various arguments about whether you should include the trailing slash in a directory path, but as far as I know it doesn't change the behaviour when it comes to listing files.

If we want to list the objects under a prefix in S3 (again, all the files in v1), we can use `aws s3 ls`, which is a wrapper around the [ListObjectsV2 API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html):

```
$ aws s3 ls s3://bukkit/bags/b1234/v1/
s3://bukkit/bags/b1234/v1/bagit.txt
s3://bukkit/bags/b1234/v1/bag-info.txt
```

Here, the trailing slash is more significant -- when S3 asks *"does a key match a prefix"*, it's doing a simple string comparison.
If we omit the slash, it will find other objects that we might not be expecting -- what happens if, say, we've got more than nine versions?

```
$ aws s3 ls s3://bukkit/bags/b1234/v1
s3://bukkit/bags/b1234/v1/bagit.txt
s3://bukkit/bags/b1234/v1/bag-info.txt
s3://bukkit/bags/b1234/v10/bagit.txt        # Err, is this what we want?
s3://bukkit/bags/b1234/v10/bag-info.txt
s3://bukkit/bags/b1234/v11/bagit.txt
...
```

The API is behaving as specified -- `v1` is indeed a prefix of `v10` -- but if you're thinking of prefixes as directory paths, this result might surprise you.
It certainly surprised me!

**If you're listing the objects in an S3 prefix, consider carefully whether you want a trailing slash.**
If you want to list it "as a directory", you probably do.
