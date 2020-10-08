---
layout: post
title: Replicating Wellcome Collection's digital archive to Azure Blob Storage
tags: wellcome digital-preservation azure
link: https://stacks.wellcomecollection.org/a-sprinkling-of-azure-6cef6e150fb2
---

I've written about some of the work we did at Wellcome Collection over the summer:

> Our cloud storage service is designed to ensure the [long-term preservation](https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e) of our digital collections.
> As an archive, we have an obligation to ourselves and to our depositors to keep our collections safe.
> We've spent millions of pounds digitising our physical objects, and some of our born-digital and audiovisual material is irreplaceable.
>
> One way we do this is by storing multiple copies of every file.
> If one copy were to be corrupted or deleted, we'd still have other copies that we could use to construct the complete archive.
>
> In the initial iteration of our storage service, we kept two copies of every file in a pair of Amazon S3 buckets.
> We've recently upgraded the storage service to keep a third copy of every file in Azure Blob Storage, and in a different geographic location.
> In this post, I'm going to explain why this change was important, and how we made it.
