---
layout: post
title: Storing multiple, human-readable versions of BagIt bags
summary:
category: Digital preservation
link: https://stacks.wellcomecollection.org/how-we-store-multiple-versions-of-bagit-bags-e68499815184
---

I've written some more about [Wellcome Collection's new storage service][service] -- this time, one of the implementation details.

Our unit of storage is a "bag", stored in the [BagIt packaging format][bagit].
A bag is a collection of related files: for example, all the digitised images from a single book.
We want to be able to update and modify bags after they're originally stored, and further, to keep a history of every distinct version of a bag.
The BagIt specification doesn't support versioning of bags, so we had to come up with our own design.

My [latest post][latest] on our development blog explains how we do the versioning, in a way that ensures human-readability and understandability.
Even if you're not using BagIt, versioning is an evergreen question in data management, and you might find some ideas that apply to your use case.

[service]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[bagit]: https://en.wikipedia.org/wiki/BagIt
[latest]: https://stacks.wellcomecollection.org/how-we-store-multiple-versions-of-bagit-bags-e68499815184
