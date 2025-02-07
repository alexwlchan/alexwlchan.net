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
BagIt is [an open format][std] developed by the Library of Congress for packaging files, which includes manifests and checksums that describe the files in a bag.
It's often used by libraries and archives to package files before ingesting them into some sort of permanent digital storage.

Although I don't use BagIt any more, 

[BagIt]: https://en.wikipedia.org/wiki/BagIt
[std]: https://tools.ietf.org/html/rfc8493

---

When I was building the [Wellcome Collection storage service][service], we had a ["bag verifier"][verifier] service that would look for broken bags and reject them before they were copied to permanent storage.
We had alerting so we'd know if the bag verifier rejected a bag, and we could go and investigate.

We wrote a large test suite for the bag verifier, which included a lot of invalid bags.
We'd test that the bag verifier rejected all of them, and that it gave meaningful and useful error messages.

All the storage service code is [published on GitHub][service] under an MIT license, including the [bag verifier tests][tests] -- but the broken bag tests are split across several files, and wrapped in a bespoke Scala test framework that might be tricky to read.
(It may also be missing some test cases; I bet I could think of more ways to break a bag now than I could several years ago.)

I thought it might be useful to create a more readable list of ways that a bag might be broken.
I don't have concrete examples of these, but it shouldn't be difficult to create them.

BagIt 

[service]: https://github.com/wellcomecollection/storage-service
[verifier]: https://stacks.wellcomecollection.org/our-approach-to-digital-verification-79da59da4ab7
[tests]: https://github.com/wellcomecollection/storage-service/tree/main/bag_verifier/src/test/scala/weco/storage_service/bag_verifier
