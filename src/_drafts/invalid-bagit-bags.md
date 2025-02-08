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

The “bag verifier”service would look for broken bags, and reject them before they were copied to long-term storage.
I wrote a lot of bag verifier test cases to confirm that it would spot broken bags, and give a useful error message when it did.

One way to come up with a list of invalid bags is to do a line-by-line reading of [RFC 8493][rfc], a specification which describes the BagIt format.
That would get you an exhaustive list of test cases, but I'm not sure it would be useful -- you'd be overwhelmed by examples.
It might become easier for mistakes to slip through, because the test suite would be too large to be comprehensible.

All of the code for Wellcome's storage service is [shared on GitHub][github] under an MIT license, including the [bag verifier tests][tests].
They're wrapped in a Scala test framework that might not be the easiest thing to read, so I'm going to describe the invalid bags we tested in a more human-friendly way.

[BagIt]: https://en.wikipedia.org/wiki/BagIt
[rfc]: https://tools.ietf.org/html/rfc8493
[storage_service]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[github]: https://github.com/wellcomecollection/storage-service
[tests]: https://stacks.wellcomecollection.org/our-approach-to-digital-verification-79da59da4ab7
[tests]: https://github.com/wellcomecollection/storage-service/tree/main/bag_verifier/src/test/scala/weco/storage_service/bag_verifier

## The Bag Declaration `bagit.txt`

This file declares that this is a BagIt bag, and says what version of BagIt you're using.
It's described in [RFC 8493 §2.1.1](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.1).

*   **What if the bag doesn't have a `bagit.txt` file?**
    This is a required element of every BagIt bag.
    If there isn't one, the bag is invalid.

*   **What if the `bagit.txt` is the wrong format?**
    This file has a tightly prescribed format -- exactly two lines, a version number and a character encoding.
    If it doesn't match this format exactly, the bag is invalid.

## The Payload Files and Payload Manifest

The payload files are the actual content files you want to save and preserve.
These are saved in the payload directory `data/` ([RFC 8493 §2.1.2](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.2)), and there's a payload manifest `manifest-algorithm.txt` that lists them, along with their checksums ([RFC 8493 §2.1.3](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.3)).

*   **What if the bag doesn't have a payload manifest file?**
    Every BagIt bag must have at least one Payload Manifest file.
    If it doesn't, then it's invalid.

*   **What if the payload manifest file is the wrong format?**
    These files have a prescribed format – one file per line, with a checksum and file path.
    If one of these files doesn't match this format, the bag is invalid.

*   **What if the payload manifest refers to a file that isn't in the bag?**
    Either one of the files in the bag has been deleted, or the manifest is incorrect.

*   **What if the bag has a file that isn't listed in the payload manifest?**
    The manifest is meant to be a complete listing of all the payload files in the bag.
    If the bag has a file which isn't in the payload manifest, either that file isn't meant to be there, or the manifest is incorrect.

*   **What if the checksum in the payload manifest doesn't match the checksum of the file?**
    Either one of the files in the bag has been corrupted, or the checksum is incorrect.

*   **What if there are payload files outside the `data/` directory?**
    The BagIt spec says that all the payload files should be stored in `data/`.

*   **What if there are duplicate entries in the payload manifest?**
    The BagIt spec says that every payload file must be listed exactly once.

    This avoids ambiguity -- suppose a payload manifest listed a file twice, with two different checksums.
    Is the bag valid if one of those checksums is correct?
    Requiring unique entries avoids this sort of issue.

*   **What if the payload manifest contains paths outside `data/`, or relative paths that try to escape the bag? (e.g. `../file.txt`)**
    This is approaching "malicious bag" territory -- a bag uploaded by somebody who's trying to compromise your ingest pipeline.
    Any such bags should be treated with suspicion and rejected.
    
    If you're concerned about malicious bags, you probably need a more thorough test suite to catch other shenanigans.
    We never did this at Wellcome Collection, because we didn't take bags from arbitrary sources.
    The bags only came from internal systems, and our verification was more about spotting bugs in those systems than defending against malicious actors.

A bag can contain multiple payload manifests -- for example, it might contain both MD5 and SHA1 checksums.
Every payload manifest must be valid for the overall bag to be valid.

## The Tag Manifest `tagmanifest-algorithm.txt`

Similar to the payload manifest, the tag manifest lists the tag files and their checksums -- that is, the metadata files that aren't part of the payload ([RFC 8493 §2.2.1](https://datatracker.ietf.org/doc/html/rfc8493#section-2.2.1)).

Unlike the payload manifest, the tag manifest is optional.
A bag without a tag manifest can still be a valid bag.

If the tag manifest is present, then many of the ways that a payload manifest can invalidate a bag -- like malformed contents, unreferenced files, or incorrect checksums -- can also apply to tag manifests.

There are some additional things to consider:

*   **What if a tag manifest lists payload files?**
    The tag manifest should only list non-payload files; payload files are listed in the payload manifest.
    If the tag manifest lists a file in the `data/` directory, then something is wrong.

*   **What if the bag has a file that isn't listed in a manifest?**
    Every file in a bag (except the tag manifests) should be listed in either a payload or a tag manifest.
    A file that appears in neither could mean an unexpected file, or a missing manifest entry.

Although the tag manifest is optional in the BagIt spec, at Wellcome Collection we made them a required file.
Every bag had to have at least one tag manifest file, or our storage service would refuse to ingest it.

## The Bag Metadata `bag-info.txt`

This is an optional file that describes the bag and its contents.
It has a simple label-value pair format, with one pair per line.

*   **What if `bag-info.txt` is the wrong format?**
    This file has a prescribed format – one metadate entry per line, with a label-value pair that's separated by a colon.
    If `bag-info.txt` doesn't match this format, the bag is invalid.

*   **What if the `Payload-Oxum` is incorrect?**
    This contains some concise statistics about the files in the bag: the number of files, and their total size in bytes.
    If these stats don't match the rest of the bag, something is wrong.

Although the bag metadata is optional in a general BagIt bag, you may want to require the presence of certain fields within a specific system.
For example, you might want to require that all bags have an `External-Identifier` value, so you can link bags to records in other databases.

## The Fetch File `fetch.txt`

This is an optional file that allows you to reference files stored elsewhere.

It tells the person reading the bag that a file hasn't been included in this copy of the bag; they have to go and fetch it from elsewhere.
The file is still recorded in the payload manifest (so it has a checksum you can verify), but you don't have a complete bag until you've downloaded all the files ([RFC 8493 §2.2.3](https://datatracker.ietf.org/doc/html/rfc8493#section-2.2.3)).

Here’s an example of a fetch.txt:

```
https://example.org/~alex/article.txt  1729  data/article.txt
```

This tells us that `data/article.txt` isn't included in this copy of the bag -- we can download it from `https://example.org/~alex/report.pdf`.
(The number 1729 is the size of the file. It's an optional field.)

Using `fetch.txt` allows you to send a bag with “holes”, which saves disk space and network bandwidth, but at a cost -- we're now relying on the remote location to remain available.
From a preservation standpoint, this is scary!
If `example.org` goes away, this bag will be broken.
I know some people don't use `fetch.txt` for precisely this reason.

If you do use `fetch.txt`, here are some things to consider:

*   **What if `fetch.txt` is the wrong format?**
    There's a prescribed format -- one final per line, with a URL, file size, and file path.
    If it doesn't match this format, the bag is invalid.

*   **What if `fetch.txt` lists a file which isn't in the payload manifest?**
    The `fetch.txt` is only about telling us that a file is stored elsewhere, not telling us about otherwise unreferenced files.

    If a file is mentioned in `fetch.txt` but not the payload manifest, we have no checksum we can use to verify the remote file.
    It means either an erroneous `fetch.txt` entry or a missing manifest entry.

*   **What if the `fetch.txt` points to a file at an unusable URL?**
    The URL is only useful if the person who receives the bag can use it to download the file.
    If they can't, the bag might technically be valid, but it's functionally broken.

*   **What if the `fetch.txt` points to a file with the wrong length?**
    The `fetch.txt` can optionally specify the size of a file, so you know how much storage you need to download it.
    If you download the file, and the actual size doesn't match the stated size, this inconsistency is worth investigating.

## Other considerations

What if the bag contains deeply nested directories?
Some filesystems have path length limits—could an excessively deep structure break certain tools?
What if the filenames contain special characters?
Spaces, Unicode, emoji, or reserved characters (\, :, *, etc.) could cause problems on some operating systems.


What if the bag contains an empty data/ directory?
Should an empty payload directory be considered valid or an error?

