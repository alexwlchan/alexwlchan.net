---
layout: post
date: 2020-06-17T19:01:38.764Z
title: Large things living in cold places
tags:
  - digital preservation
  - wellcome collection
  - aws
  - aws:amazon s3
summary: Using cold storage tiers to reduce the cost of storing Wellcome's digital collections in the cloud.
canonical_url: https://stacks.wellcomecollection.org/large-things-living-in-cold-places-66cbc3603e14
colors:
  css_light: "#704f35"
  css_dark:  "#aea6a2"
is_featured: true
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/large-things-living-in-cold-places-66cbc3603e14) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<figure>
  {%
    picture
    filename="v797vg8b.jpg"
    width="750"
    alt=""
  %}
  <figcaption>A group of developers set off on an expedition to find the objects stored in Glacier. Colour lithograph by J. Arnout, 1843, <a href="https://wellcomecollection.org/works/v797vg8b">Wellcome Collection</a>. CC BY.</figcaption>
</figure>

<p>In <a href="/2020/archival-storage-service/">our digital archive</a>, we store everything in cloud storage. One advantage of cloud storage is that capacity becomes a non-issue — our cloud provider has to worry about buying disks or installing hardware, not us. We upload new files and our bill goes up, but we’ll never run out of disk space.</p><p>This is especially useful for one of our current projects, which is the digitisation of our A/V material. We’re trying to digitise all our magnetic media before it becomes unplayable — either because the media itself degrades, or because there are no more working players.</p><p>We make two copies of every piece of A/V:</p><ul><li>An <em>access copy</em>: a file that we use to create derivatives suitable for viewing on our website.</li><li>A <em>preservation copy</em>: a file for long-term storage. This is a lossless format with a higher bitrate and resolution than the access copy. We can use it to create new copies if our preferred video formats change, or in cases where we need the highest quality possible.</li></ul><p>The preservation copies are <em>big</em> — the biggest so far is 166GB from a single video, and there may be bigger ones to come. We estimate the project is going to triple the amount of data we have in the archive.</p><p>Because cloud storage is effectively unlimited, that rough estimate is fine — we don’t need to pre-buy the exact amount of storage we need. But tripling the amount of data means tripling our monthly storage bill. Oof. <strong>Can we do something about that?</strong></p>

---

<p>How much you pay for cloud storage depends on three things:</p><ul><li><em>How much stuff do you have? </em>Storing more stuff costs more money.</li><li><em>How much redundancy do you want? </em>It’s cheap to keep one copy of your files, but you’re a single failure away from data loss. If you want better protection, you can store additional copies in different locations, but those extra copies cost more money.</li><li><em>How quickly do you need to get stuff out? </em>If you need to be able to retrieve things immediately, it’s quite expensive. If you’re willing to wait, your files can be pushed into cheaper storage that’s slower to access.</li></ul><p>You choose how much redundancy and access you want by selecting a <em>storage class</em>. Each class has a fixed price per GB stored, and that price is smaller for classes with less redundancy or slower access. That gives predictable, linear pricing within a storage class: store twice as much stuff, pay twice as much.</p>

---

<p>We can’t store less stuff or compromise on redundancy — but we don’t need to get these large preservation copies out very often. They’re not served directly to website users, so we can accept a small delay in retrieving them. <strong>We can store our preservation copies in a cold storage class with slower access, and save some money.</strong></p><p>This isn’t a new idea — we do the same thing for physical material. Some of our books and archives are kept on-site in London, and the rest are kept in <a href="http://www.deepstore.com/">an underground salt mine</a>. There’s a delay to retrieve something from the mine — among other things, it’s a nearly 200 mile drive — but space in Cheshire is cheaper than central London. Different material is stored in different ways.</p><p>The primary copy of all our data is in Amazon S3. At the time of writing, S3 has <a href="https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html">seven storage classes</a>, with two of them cold: <em>Glacier</em> and <em>Deep Archive. </em>They’re both significantly cheaper than the standard class, and typically take several hours to retrieve a file. One difference is that Glacier has <a href="https://aws.amazon.com/about-aws/whats-new/2016/11/access-your-amazon-glacier-data-in-minutes-with-new-retrieval-options/"><em>expedited retrievals</em></a> — if you need something quickly, you can retrieve it in minutes, not hours.</p><p>We will need expedited retrieval on occasion, so we picked Glacier over Deep Archive. We’ve already used Glacier to store high-resolution masters from our photography workflow — and yes, we do restore files sometimes! — so on balance, the extra cost over Deep Archive is worth it.</p><p>(We use Deep Archive elsewhere — for a second, backup copy of all our data.)</p><p><strong>We store the primary copy of our large preservation files in Glacier to reduce our storage costs.</strong></p>

---

<p>One of our priorities for our digital archive is human-readability: it should be possible for a person to understand how the files are organised, even if they don’t have any of our software or databases. The preservation and access copies are the same conceptual object, so we want to group them together within the archive — ideally in the same folder/prefix.</p><p>Within S3, the storage class is managed at the per-object level — you can have objects with different storage classes within the same bucket or prefix. This means we can keep the preservation and access copies together.</p><p>This is what a digitised A/V item looks like in our storage buckets:</p>

```
b12345678/
 ├── METS.xml          (metadata file)
 ├── b12345678.mp4     (access copy, warm storage - Standard IA)
 └── b12345678.mxf     (preservation copy, cold storage – Glacier)
```

<p>So how do we tell S3 which objects should go in which storage class?</p><p>We’ve created an app that watches files being written to the storage service. When it sees a new preservation file, it adds a tag to the corresponding object in S3. (<a href="https://docs.aws.amazon.com/AmazonS3/latest/dev/object-tagging.html">Tags</a> are key-value pairs that you can attach to individual objects.)</p><p>Then we have <a href="https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-lifecycle.html">an S3 lifecycle policy</a> that automatically moves objects with certain tags to Glacier. (We don’t write objects straight to Glacier — immediately after we write an object, we read it back out to verify it against an externally-provided checksum. If we wrote straight to Glacier, we’d be unable to perform this verification step.)</p><p>All the pieces of this system are now up and running, and it’s going to be a substantial cost saving as we start to bring in our digitised A/V material:</p>

<figure>
  {%
    picture
    filename="1*yiQSoTDnUUndwKM806VzNA.png"
    width="664"
    alt=""
  %}
  <figcaption>We spent about a month adding Glacier support to the storage service, so the 100TB of A/V material we’re about to ingest will pay for this work within a year or so.</figcaption>
</figure>

<p>We can do this because we have a clear understanding of how our files are used and retrieved, and a few simple rules give us a noticeable saving. <strong>If you have a big storage bill and you want to make it smaller, understanding how your files are used is often a good place to start. </strong>Whatever cloud storage provider you’re using, you can often save money by selecting a storage class that’s appropriate to your use case.</p><p><em>Thanks to Harkiran Dhindsa, Jonathan Tweed, Sarah Bird, and Tom Scott for their help writing this article.</em></p>
