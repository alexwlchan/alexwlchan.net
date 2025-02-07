---
layout: post
title: Examples of invalid BagIt bags
summary:
tags:
  - digital preservation
---
About a week ago, James Truitt asked a question on Mastodon:

{% mastodon https://code4lib.social/@linguistory/113924700205617006 %}

Here James is talking about [BagIt] bags.
BagIt is [an open format][rfc] developed by the Library of Congress for packaging files, which includes manifests and checksums that describe the files in a bag.
It's often used by libraries and archives to package files before ingesting them into some sort of permanent digital storage.

Although I don't use BagIt any more, I spent a lot of time working with it when I was a software developer at Wellcome Collection.
We used BagIt as the packaging format for the [cloud storage service][storage_service], and we built a microservice very similar to what James is describing.
The ["bag verifier"][verifier] service would look for broken bags, and reject them before they were copied to long-term storage.
I wrote a lot of [bag verifier test cases][tests] to confirm that it would spot broken bags, and give a useful error message when it did.

The BagIt format is described in [RFC 8493][rfc].
Let's go through the key parts of that RFC, line-by-line, and I'll talk about how ignoring them could lead to a broken bag.

Even if you don't use BagIt, this might be an interesting case study in how I write tests.
Being able to find breaking examples is a useful skill for lots of software development work.
Maybe you want to read the RFC and see how many broken bags you can think of.
Maybe you'll spot one I didn't!

[BagIt]: https://en.wikipedia.org/wiki/BagIt
[rfc]: https://tools.ietf.org/html/rfc8493
[storage_service]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[service]: https://github.com/wellcomecollection/storage-service
[verifier]: https://stacks.wellcomecollection.org/our-approach-to-digital-verification-79da59da4ab7
[tests]: https://github.com/wellcomecollection/storage-service/tree/main/bag_verifier/src/test/scala/weco/storage_service/bag_verifier


---

I thought it might be useful to create a more readable list of ways that a bag might be broken.
I don't have concrete examples of these, but it shouldn't be difficult to create them.

BagIt 

