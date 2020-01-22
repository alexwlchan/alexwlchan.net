---
layout: post
date: 2020-01-22 08:23:50 +0000
title: "A deletion canary: testing your S3 bucket permissions"
summary: If you've tried to disable deletions in your S3 buckets, how do you know they're working?
category: Amazon Web Services
---

At Wellcome, we have a pair of S3 buckets (one primary, one replica) that hold the Collection's digital archives.
Once something is written to the archive, it should be stored permanently, so we want to ensure that people can't overwrite or delete objects in those buckets.

There are lots of mechanisms in S3 to enforce this sort of policy:

-  You could create an [S3 Bucket Policy] that blocks the s3:DeleteObject operation on the entire bucket
-  You could apply [IAM policies] that deny DeleteObject or PutObject permissions for your users
-  You could enable [S3 object lock] and legal holds

In practice, it would be safest to do [a combination of all three]: if one fails, the others will still protect you.
But how do you test that you've configured these protections correctly?

If we want to be completely sure, we should try to delete something, and see what happens.
But everything in the bucket is part of the archive, so this is quite risky – if we try to delete a file, and the permissions are wrong, we've just deleted an archive file.
That's exactly what we want to avoid!

So instead, in the root of both buckets, we have a file called `for_delete_permissions_testing.txt`.
It’s a [canary] that we can test with – it exists solely so we can try to delete it.

If we can't, great, everything is fine.

If we can, losing a copy of this file is less bad than deleting part of the archive.

<img src="/images/2020/s3_delete_canary_1x.png" srcset="/images/2020/s3_delete_canary_1x.png 1x, /images/2020/s3_delete_canary_2x.png 2x" alt="A file listing in the S3 console.  Four files are listed: three folders, and one text file highlighted in blue.">

What if somebody comes across this file in a decade's time, and wonders what it's for?
Then they can download it, and read the text inside the file, which explains what I just explained above.

This isn't the only way we can test our delete protections, but it's one of my favourites.
It's as close to a real deletion as possible, without risking any of the real data.

[S3 Bucket Policy]: https://docs.aws.amazon.com/AmazonS3/latest/user-guide/add-bucket-policy.html
[IAM policies]: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
[S3 object lock]: https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html
[canary]: https://en.wikipedia.org/wiki/Sentinel_species#Historical_examples
[a combination of all three]: https://en.wikipedia.org/wiki/Defence_in_depth
