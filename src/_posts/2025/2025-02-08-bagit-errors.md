---
layout: post
date: 2025-02-08 10:04:12 +0000
title: Unexpected errors in the BagIt area
summary: |
  Exploring the many ways a BagIt bag can be invalid, and how you might want to build a process for validating bags to ensure the quality of your digital archive.
tags:
  - bagit
  - digital preservation
index:
  feature: true
colors:
  index_light: "#8b623b"
  index_dark:  "#f0d0af"
---
Last week, James Truitt asked a question on Mastodon:

{% mastodon https://code4lib.social/@linguistory/113924700205617006 %}

The "bags" he's referring to are BagIt bags.
BagIt is [an open format][rfc] developed by the Library of Congress for packaging digital files.
Bags include manifests and checksums that describe their contents, and they're often used by libraries and archives to organise files before transfering them to permanent storage.

Although I don't use BagIt any more, I spent a lot of time working with it when I was a software developer at Wellcome Collection.
We used BagIt as the packaging format for files saved to our [cloud storage service][storage_service], and we built a microservice very similar to what James is describing.

The "bag verifier" would look for broken bags, and reject them before they were copied to long-term storage.
I wrote a lot of bag verifier test cases to confirm that it would spot invalid or broken bags, and that it would give a useful error message when it did.

All of the code for Wellcome's storage service is [shared on GitHub][github] under an MIT license, including the [bag verifier tests][tests].
They're wrapped in a Scala test framework that might not be the easiest thing to read, so I'm going to describe the test cases in a more human-friendly way.

Before diving into specific examples, it's worth remembering: context is king.

BagIt is described by [RFC 8493][rfc], and you could create invalid bags by doing a line-by-line reading and deliberately ignoring every "MUST" or "SHOULD" but I wouldn't recommend this aproach.
You'd get a long list of test cases, but you'd be overwhelmed by examples, and you might miss specific requirements for your system.

The BagIt RFC is written for the most general case, but if you're actually building a storage service, you'll have more concrete requirements and context.
It's helpful to look at that context, and how it affects the data you want to store.
Who's creating the bags?
How will they name files?
Where are you going to store bags?
How do bags fit into your wider systems?
And so on.

Understanding your context will allow you to skip verification steps that you don't need, and to add verification steps that are important to you.
I doubt any two systems implement the exact same set of checks, because every system has different context.

Here are examples of potential validation issues drawn from the BagIt specification and my real-world experience.
You won't need to check for everything on this list, and this list isn't exhaustive -- but it should help you think about bag validation in your own context.

[BagIt]: https://en.wikipedia.org/wiki/BagIt
[rfc]: https://tools.ietf.org/html/rfc8493
[storage_service]: /2020/archival-storage-service/
[github]: https://github.com/wellcomecollection/storage-service
[tests]: /2021/digital-verification/
[tests]: https://github.com/wellcomecollection/storage-service/tree/main/bag_verifier/src/test/scala/weco/storage_service/bag_verifier

<blockquote class="toc">
  <p>Table of contents:</p>
  <ul>
    <li><a href="#bagit">The Bag Declaration <code>bagit.txt</code></a></li>
    <li><a href="#payload_manifest">The Payload Files and Payload Manifest</a></li>
    <li><a href="#payload_filenames">Payload filenames</a></li>
    <li><a href="#tag_manifest">The Tag Manifest <code>tagmanifest-algorithm.txt</code></a></li>
    <li><a href="#bag_info">The Bag Metadata <code>bag-info.txt</code></a></li>
    <li><a href="#fetch">The Fetch File <code>fetch.txt</code></a></li>
    <li><a href="#conclusion">Conclusion</a></li>
  </ul>
</blockquote>

<style>
  .toc {
    background: var(--background-color);
    border-color: var(--primary-color);
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>

---

<h2 id="bagit">The Bag Declaration <code>bagit.txt</code></h2>

This file declares that this is a BagIt bag, and the version of BagIt you're using ([RFC 8493 §2.1.1](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.1)).
It looks the same in almost every bag, for example:

```
BagIt-Version: 1.0
Tag-File-Character-Encoding: UTF-8
```

This tightly prescribed format means it can only be invalid in a few ways:

*   **What if the bag doesn't have a bag declaration?**
    It's a required element of every BagIt bag; it has to be there.

*   **What if the bag declaration is the wrong format?**
    It should contain exactly two lines: a version number and a character encoding, in that order.

*   **What if the bag declaration has an unexpected version number?**
    If you see a BagIt version that you've not seen before, the bag might have a different structure than what you expect.

<h2 id="payload_manifest">The Payload Files and Payload Manifest</h2>

The payload files are the actual content you want to save and preserve.
They get saved in the payload directory `data/` ([RFC 8493 §2.1.2](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.2)), and there's a payload manifest `manifest-algorithm.txt` that lists them, along with their checksums ([RFC 8493 §2.1.3](https://datatracker.ietf.org/doc/html/rfc8493#section-2.1.3)).

Here's an example of a payload manifest with MD5 checksums:

```
37d0b74d5300cf839f706f70590194c3  data/waterfall.jpg
```

This tells us that the bag contains a single file `data/waterfall.jpg`, and it has the MD5 checksum `37d0…`.
These checksums can be used to verify that the files have transferred correctly, and haven't been corrupted in the process.

There are lots of ways a payload manifest could be invalid:

*   **What if the bag doesn't have a payload manifest?**
    Every BagIt bag must have at least one Payload Manifest file.

*   **What if the payload manifest is the wrong format?**
    These files have a prescribed format – one file per line, with a checksum and file path.

*   **What if the payload manifest refers to a file that isn't in the bag?**
    Either one of the files in the bag has been deleted, or the manifest has an erroneous entry.

*   **What if the bag has a file that isn't listed in the payload manifest?**
    The manifest should be a complete listing of all the payload files in the bag.
    If the bag has a file which isn't in the payload manifest, either that file isn't meant to be there, or the manifest is missing an entry.

    Checking for unlisted files is how I spotted unwanted `.DS_Store` and `Thumbs.db` files.

*   **What if the checksum in the payload manifest doesn't match the checksum of the file?**
    Either the file has been corrupted, or the checksum is incorrect.

*   **What if there are payload files outside the `data/` directory?**
    All the payload files should be stored in `data/`.
    Anything outside that is an error.

*   **What if there are duplicate entries in the payload manifest?**
    Every payload file must be listed exactly once in the manifest.

    This avoids ambiguity -- suppose a file is listed twice, with two different checksums.
    Is the bag valid if one of those checksums is correct?
    Requiring unique entries avoids this sort of issue.

*   **What if the payload directory is empty?**
    This is perfectly acceptable in the BagIt RFC, but it may not be what you want.
    If you know that you will always be sending bags that contain files, you should flag empty payload directories as an error.

*   **What if the payload manifest contains paths outside `data/`, or relative paths that try to escape the bag? (e.g. `../file.txt`)**
    Now we're into "malicious bag" territory -- a bag uploaded by somebody who's trying to compromise your ingest pipeline.
    Any such bags should be treated with suspicion and rejected.

    If you're concerned about malicious bags, you need a more thorough test suite to catch other shenanigans.
    We never went this far at Wellcome Collection, because we didn't ingest bags from arbitrary sources.
    The bags only came from internal systems, and our verification was mainly about spotting bugs in those systems, not defending against malicious actors.

A bag can contain multiple payload manifests -- for example, it might contain both MD5 and SHA1 checksums.
Every payload manifest must be valid for the overall bag to be valid.

<h2 id="payload_filenames">Payload filenames</h2>

There are lots of gotchas around filenames and paths.
It's a complicated problem, and I definitely don't understand all of it.

It's worth understanding the filename rules of any filesystem where you will be storing bags.
For example, Azure Blob Storage has a [number of rules][azure_rules] around how you can name files, and Amazon S3 has [different rules][s3_rules].
We stored files in both at Wellcome Collection, and so the storage service had to enforce the superset of these rules.

I've listed some edge cases of filenames you might want to consider, but it's not a complete list.
There are lots of ways that unexpected filenames could cause you issues, but whether you care depends on the source of your bags.
If you control the bags and you know you're not going to include any weird filenames, you can probably skip most of these.

We only checked for one of these conditions at Wellcome Collection, because we had a pre-ingest step that normalised filenames.
It converted filenames to ASCII, and saved a mapping between original and normalised filename in the bag.
However, the normalisation was only designed for one filesystem, and produced filenames with trailing dots that were still disallowed in Azure Blob.

*   **What if a filename is too long?**
    Some systems have a maximum path length, and an excessively deep directory structure or long filename could cause issues.

*   **What if a filename contains special characters?**
    Spaces, emoji, or special characters (`\`, `:`, `*`, etc.) can cause problems for some tools.
    You should also think about characters that need to be URL-encoded.

*   **What if a filename has trailing spaces or dots?**
    Some filesystems can't support filenames ending in a dot or a space.
    What happens if your bag contains such a file, and you try to save it to the filesystem?

    This caused us issues at Wellcome Collection.
    We initially stored bags just in Amazon S3, which is happy to take filenames with a trailing dot -- then we added backups to Azure Blob, which doesn't.
    One of the bags we'd stored in Amazon S3 had a trailing dot in the filename, and caused us headaches when we tried to copy it to Azure.

*   **What if a filename contains a mix of path separators?**
    The payload manifest uses a forward slash (`/`) as a path separator.
    If you have a filename with an alternative path separator, it might behave differently on different systems.

    For example, consider the payload file `a\b\c`.
    This would be a single file on macOS or Linux, but it would be nested inside two folders on Windows.

*   **What if the filenames are a mix of uppercase and lowercase characters?**
    Some fileystems are case-sensitive, others aren't.
    This can cause issues when you move bags between systems.

    For example, suppose a bag contains two different files `Macrodata.txt` and `macrodata.txt`.
    When you save that bag on a case-insensitive filesystem, only one file will be saved.

*   **What if the same filename appears twice with different Unicode normalisations?**
    This is similar to filenames which only differ in upper/lowercase.
    They might be treated as two files on one filesystem, but collapsed into one file on another.

    The classic example is the word "café": this can be encoded as `caf\xc3\xa9` (UTF-8 encoded é) or `cafe\xcc\x81` (e + combining acute accent).

*   **What if a filename contains a directory reference?**
    A directory reference is `/./` (current directory) or `/../` (parent directory).
    It's used on both Unix and Windows-like systems, and it's another case of two filenames that look different but can resolve to the same path.

    For example: `a/b`, `a/./b` and `a/subdir/../b` all resolve to the same path under these rules.

    This can cause particular issues if you're moving between local filesystems and cloud storage.
    Local filesystems treat filenames as hierarchical paths, where cloud storage like Amazon S3 often treats them [as opaque strings][s3_keys].
    This can cause issues if you try to copy files from cloud storage to a local system -- if you're not careful, you could lose files in the process.

[azure_rules]: https://learn.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-snapshots
[s3_rules]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
[s3_keys]: /2020/s3-keys-are-not-file-paths/

<h2 id="tag_manifest">The Tag Manifest <code>tagmanifest-algorithm.txt</code></h2>

Similar to the payload manifest, the tag manifest lists the tag files and their checksums.
A "tag file" is the BagIt term for any metadata file that isn't part of the payload ([RFC 8493 §2.2.1](https://datatracker.ietf.org/doc/html/rfc8493#section-2.2.1)).

Unlike the payload manifest, the tag manifest is optional.
A bag without a tag manifest can still be a valid bag.

If the tag manifest is present, then many of the ways that a payload manifest can invalidate a bag -- malformed contents, unreferenced files, or incorrect checksums -- can also apply to tag manifests.

There are some additional things to consider:

*   **What if a tag manifest lists payload files?**
    The tag manifest lists tag files; the payload manifest lists payload files in the `data/` directory.
    A tag manifest that lists files in the `data/` directory is incorrect.

*   **What if the bag has a file that isn't listed in either manifest?**
    Every file in a bag (except the tag manifests) should be listed in either a payload or a tag manifest.
    A file that appears in neither could mean an unexpected file, or a missing manifest entry.

Although the tag manifest is optional in the BagIt spec, at Wellcome Collection we made it a required file.
Every bag had to have at least one tag manifest file, or our storage service would refuse to ingest it.

<h2 id="bag_info">The Bag Metadata <code>bag-info.txt</code></h2>

This is an optional metadata file that describes the bag and its contents ([RFC 8493 §2.2.2](https://datatracker.ietf.org/doc/html/rfc8493#section-2.2.2)).
It's a list of metadata elements, as simple label-value pairs, one per line.

Here's an example of a bag metadata file:

```
Source-Organization: Lumon Industries
Organization-Address: 100 Main Street, Kier, PE, 07043
Contact-Name: Harmony Cobel
```

Unlike the manifest files, this is primarily intended for human readers.
You can put arbitrary metadata in here, so you can add fields specific to your organisation.

Although this file is more flexible, there are still ways it can be invalid:

*   **What if the bag metadata is the wrong format?**
    It should have one metadata entry per line, with a label-value pair that's separated by a colon.

*   **What if the `Payload-Oxum` is incorrect?**
    The `Payload-Oxum` contains some concise statistics about the payload files: their total size in bytes, and how many there are.
    For example:

    ```
    Payload-Oxum: 517114.42
    ```

    This tells us that the bag contains 42 payload files, and their total size is 517,114 bytes.

    If these stats don't match the rest of the bag, something is wrong.

*   **What if non-repeatable metadata element names are repeated?**
    The BagIt RFC defines a small number of reserved metadata element names which have a standard meaning.
    Although most metadata element names can be repeated, there are some which can't, because they can only have one value.

    In particular: `Bagging-Date`, `Bag-Size`, `Payload-Oxum` and `Bag-Group-Identifier`.

Although the bag metadata file is optional in a general BagIt bag, you may want to add your own rules based on how you use it.

For example, at Wellcome Collection, we required all bags to have an `External-Identifier` value, that matched a specific schema.
This allowed us to link bags to records in other databases, and our bag verifier would reject bags that didn't include it.

<h2 id="fetch">The Fetch File <code>fetch.txt</code></h2>

This is an optional element that allows you to reference files stored elsewhere ([RFC 8493 §2.2.3](https://datatracker.ietf.org/doc/html/rfc8493#section-2.2.3)).

It tells the person reading the bag that a file hasn't been included in this copy of the bag; they have to go and fetch it from somewhere else.
The file is still recorded in the payload manifest (with a checksum you can verify), but you don't have a complete bag until you've downloaded all the files.

Here’s an example of a `fetch.txt`:

```
https://topekastar.com/~daria/article.txt  1841  data/article.txt
```

This tells us that `data/article.txt` isn't included in this copy of the bag, but we we can download it from `https://topekastar.com/~daria/article.txt`.
(The number 1841 is the size of the file in bytes. It's optional.)

Using `fetch.txt` allows you to send a bag with “holes”, which saves disk space and network bandwidth, but at a cost -- we're now relying on the remote location to remain available.
From a preservation standpoint, this is scary!
If `topekastar.com` goes away, this bag will be broken.
I know some people don't use `fetch.txt` for precisely this reason.

If you do use `fetch.txt`, here are some things to consider:

*   **What if the fetch file is the wrong format?**
    There's a prescribed format -- one file per line, with a URL, optional file size, and file path.

*   **What if the fetch file lists a file which isn't in the payload manifest?**
    The `fetch.txt` should only tell us that a file is stored elsewhere, and shouldn't be introducing otherwise unreferenced files.

    If a file appears in `fetch.txt` but not the payload manifest, then we can't verify the remote file because we don't have a checksum for it.
    There's either an erroneous fetch file entry or a missing manifest entry.

*   **What if the fetch file points to a file at an unusable URL?**
    The URL is only useful if the person who receives the bag can use it to download the file.
    If they can't, the bag might technically be valid, but it's functionally broken.

    For example, you might reject URLs that don't start with `http://` or `https://`.

*   **What if the fetch file points to a file with the wrong length?**
    The `fetch.txt` can optionally specify the size of a file, so you know how much storage you need to download it.
    If you download the file, the actual size should match the stated size.

*   **What if the fetch files points to a file that's already included in the bag?**
    Now you have two ways to get this file: you can read it from the bag, or from the remote URL.
    If a file is listed in both `fetch.txt` and included in the bag, either that file isn't meant to be in the bag, or the fetch file has an erroneous entry.

We used fetch files at Wellcome Collection to [implement versioning][versioning], and we added extra rules about what remote URLs were allowed.
In particular, we didn't allow fetching a file from just anywhere -- you could fetch from our S3 buckets, but not the general Internet.
The bag verifier would reject a fetch file entry that pointed elsewhere.

[versioning]: https://stacks.wellcomecollection.org/how-we-store-multiple-versions-of-bagit-bags-e68499815184

---

<div id="conclusion"></div>

These examples illustrate just how many ways a BagIt bag can be invalid, from simple structural issues to complex edge cases.

Remember: the key is to understand your specific needs and requirements.
By considering your context -- who creates your bags, where they'll be stored, and how they fit into your wider systems -- you can build a validation process to catch the issues that matter to you, while avoiding unnecessary complexity.

I can give you my ideas, but only you can build your system.
