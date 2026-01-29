---
date: 2019-09-05 23:16:04 +00:00
layout: post
summary: Code to turn an InputStream into an Iterator of entries from a tar.gz file
  or similar compressed archive in Java/Scala.
title: Iterating over the entries of a compressed archive (tar.gz) in Scala
tags:
  - scala
---

Six months ago, I wrote a post about [working with large S3 objects in Python][s3_python].
It's part of a project at work -- we get a compressed archive that's been uploaded to S3, and we need to unpack the individual files into another S3 bucket.

When we started, we were using zip archives; we've since switched to using tar.gz.
The latter is a streaming format -- we can unpack the files one-at-a-time, without downloading the entire file or jumping around, reading non-contiguous chunks of the file.
I'm quite pleased with the code we've written for doing this unpacking, so in this post I'm going to walk through it.

We start with an `InputStream` -- this could come from the S3 API, or a file on disk, or something else.
It contains the bytes of our compressed archive.
For example:

```scala {"names":{"1":"java","2":"io","3":"FileInputStream","4":"InputStream","5":"inputStream"}}
import java.io.{FileInputStream, InputStream}

val inputStream: InputStream = new FileInputStream("numbers.tar.gz")
```

The first step is to strip off the .gz compression.
We use the [Apache Commons libraries][commons] elsewhere in our codebase, so we used that to do the uncompression:

```scala {"names":{"1":"java","2":"io","3":"BufferedInputStream","4":"org","5":"apache","6":"commons","7":"compress","8":"compressors","9":"CompressorInputStream","10":"CompressorStreamFactory","11":"uncompressedInputStream"}}
import java.io.BufferedInputStream
import org.apache.commons.compress.compressors.{
  CompressorInputStream,
  CompressorStreamFactory
}

val uncompressedInputStream: CompressorInputStream =
  new CompressorStreamFactory().createCompressorInputStream(
    if (inputStream.markSupported())
      inputStream
    else
      new BufferedInputStream(inputStream)
  )
```

The stream needs to support `mark()`, or you get an IllegalArgumentException: *Mark is not supported* -- hence wrapping it in a BufferedInputStream.
The result is an InputStream whose bytes are equivalent to running `gunzip numbers.tar.gz` on the command line.

This is deliberately quite general -- although we're working with a gzip-compressed file, it strips off any compression layer.
For example, if you have a tar.xz file, it strips off the .xz compression instead.

Next we have to unpack the tar portion, using another Apache Commons helper:

```scala {"names":{"1":"org","2":"apache","3":"commons","4":"compress","5":"archivers","6":"ArchiveInputStream","7":"ArchiveStreamFactory","8":"archiveInputStream"}}
import org.apache.commons.compress.archivers.{
  ArchiveInputStream,
  ArchiveStreamFactory
}

val archiveInputStream: ArchiveInputStream =
  new ArchiveStreamFactory()
    .createArchiveInputStream(
      if (uncompressedInputStream.markSupported())
        uncompressedInputStream
      else
        new BufferedInputStream(uncompressedInputStream)
    )
```

ArchiveInputStream is a special type of InputStream that emits an EOF when it gets to the end of a file in the archive.
Once it's done, you call `getNextEntry` to reset the stream and start reading the next file.
When `getNextEntry` returns `null`, you're at the end of the archive.

One way to use this would be a `while` loop:

```scala
while (archiveInputStream.getNextEntry != null) {
  // do stuff with 'archiveInputStream'
}
```

but this isn't a very Scala-y solution.
I'd rather have something iterable, like a List() or Seq(), where I can use `.map()` and all my other functional programming constructs.

A better approach would be to use an Iterator -- it behaves similar to List() or Seq(), if we define `hasNext` and `next()` methods.
Here's an initial attempt, which prints the contents of each file:

```scala {"names":{"1":"org","2":"apache","3":"commons","4":"io","5":"IOUtils","6":"iterator","9":"hasNext","13":"next","18":"is"}}
import org.apache.commons.io.IOUtils

val iterator = new Iterator[InputStream] {
  override def hasNext: Boolean =
    archiveInputStream.getNextEntry != null

  override def next(): InputStream =
    archiveInputStream
}

iterator.foreach { is: InputStream =>
  println(new String(IOUtils.toByteArray(is)))
}
```

This is okay, but we're losing important information about the entries in the archive.
The `getNextEntry` method returns an ArchiveEntry, which includes the name and size of the original entry, and whether it's a file or a directory.
Let's modify our iterator to include that information:

```scala {"names":{"1":"org","2":"apache","3":"commons","4":"compress","5":"archivers","6":"ArchiveEntry","7":"iterator","11":"latestEntry","14":"hasNext","16":"latestEntry","20":"next","27":"archiveEntry","28":"is"}}
import org.apache.commons.compress.archivers.ArchiveEntry

val iterator = new Iterator[(ArchiveEntry, InputStream)] {
  var latestEntry: ArchiveEntry = _

  override def hasNext: Boolean = {
    latestEntry = archiveInputStream.getNextEntry
    latestEntry != null
  }

  override def next(): (ArchiveEntry, InputStream) =
    (latestEntry, archiveInputStream)
}

iterator.foreach { case (archiveEntry, is) =>
  println(s"The name is ${archiveEntry.getName}")
  println(new String(IOUtils.toByteArray(is)))
}
```

At this point, it might seem like we're done -- but there's a bug lurking here, which we discovered when we started uploading these streams to S3.
Although this iterator generates lots of `InputStream` instances, really these are all a view into the same underlying original stream -- it's all one sequence of bytes under the hood.

<figure>
{%
  inline_svg
  filename="streams.svg"
  alt="Four rectangles (file1.txt, file2.txt, file3.txt, file4.txt) in a horizontal line, each with an arrow pointing down to a single continuous rectangle (archiveInputStream)."
%}
</figure>

If you call `close()` on any of the individual streams, that gets passed down to the underlying stream.
When you go to read the next entry, you get an IOException: *input buffer is closed*.

We can't stop downstream code from calling `close()`, but we can stop a close breaking the entire process.
A CloseShieldInputStream prevents the underlying stream from being closed (even when you call `close()`) -- this is just the sort of thing it's designed for.
Here's a revised iterator:

```scala {"names":{"1":"org","2":"apache","3":"commons","4":"io","5":"input","6":"CloseShieldInputStream","7":"iterator","11":"latestEntry","14":"hasNext","16":"latestEntry","20":"next"}}
import org.apache.commons.io.input.CloseShieldInputStream

val iterator = new Iterator[(ArchiveEntry, InputStream)] {
  var latestEntry: ArchiveEntry = _

  override def hasNext: Boolean = {
    latestEntry = archiveInputStream.getNextEntry
    latestEntry != null
  }

  override def next(): (ArchiveEntry, InputStream) =
    (latestEntry, new CloseShieldInputStream(archiveInputStream))
}
```

Several of these steps can throw exceptions, so to finish off we can wrap them in some `Try` calls and chain them together in a `for` comprehension.
Here's a final version of the code:

```scala {"names":{"1":"java","2":"io","3":"BufferedInputStream","4":"InputStream","5":"org","6":"apache","7":"commons","8":"compress","9":"archivers","10":"ArchiveEntry","11":"ArchiveInputStream","12":"ArchiveStreamFactory","13":"org","14":"apache","15":"commons","16":"compress","17":"compressors","18":"CompressorInputStream","19":"CompressorStreamFactory","20":"org","21":"apache","22":"commons","23":"io","24":"input","25":"CloseShieldInputStream","26":"org","27":"scalatest","28":"FunSpec","29":"scala","30":"util","31":"Try","32":"Unpacker","33":"open","34":"inputStream","40":"uncompressedInputStream","43":"archiveInputStream","46":"iterator","50":"createUncompressedStream","51":"inputStream","60":"createArchiveStream","61":"uncompressedInputStream","70":"createIterator","71":"archiveInputStream","79":"latestEntry","82":"hasNext","84":"latestEntry","88":"next","94":"getMarkableStream"}}
import java.io.{BufferedInputStream, InputStream}

import org.apache.commons.compress.archivers.{
  ArchiveEntry,
  ArchiveInputStream,
  ArchiveStreamFactory
}
import org.apache.commons.compress.compressors.{
  CompressorInputStream,
  CompressorStreamFactory
}
import org.apache.commons.io.input.CloseShieldInputStream
import org.scalatest.FunSpec

import scala.util.Try

object Unpacker {

  /** Unpack a compressed archive from an input stream; for example, a stream of
      * bytes from a tar.gz or tar.xz archive.
      *
      * The result is an iterator of 2-tuples, one for each entry in the archive:
      *
      *   - An ArchiveEntry instance, with information like name, size and whether
      *     the entry is a file or directory
      *   - An InputStream of all the bytes in this particular entry
      *
      */
  def open(inputStream: InputStream): Try[Iterator[(ArchiveEntry, InputStream)]] =
    for {
      uncompressedInputStream <- createUncompressedStream(inputStream)
      archiveInputStream <- createArchiveStream(uncompressedInputStream)
      iterator = createIterator(archiveInputStream)
    } yield iterator

  private def createUncompressedStream(
    inputStream: InputStream): Try[CompressorInputStream] =
    Try {
      new CompressorStreamFactory().createCompressorInputStream(
        getMarkableStream(inputStream)
      )
    }

  private def createArchiveStream(
    uncompressedInputStream: CompressorInputStream): Try[ArchiveInputStream] =
    Try {
      new ArchiveStreamFactory()
        .createArchiveInputStream(
          getMarkableStream(uncompressedInputStream)
        )
    }

  private def createIterator(
    archiveInputStream: ArchiveInputStream): Iterator[(ArchiveEntry, InputStream)] =
    new Iterator[(ArchiveEntry, InputStream)] {
      var latestEntry: ArchiveEntry = _

      override def hasNext: Boolean = {
        latestEntry = archiveInputStream.getNextEntry
        latestEntry != null
      }

      override def next(): (ArchiveEntry, InputStream) =
        (latestEntry, new CloseShieldInputStream(archiveInputStream))
    }

  private def getMarkableStream(inputStream: InputStream): InputStream =
    if (inputStream.markSupported())
      inputStream
    else
      new BufferedInputStream(inputStream)
}
```

We've been using a variant of this code to unpack compressed archives for several weeks now, and it's unpacked thousands of files with no problems.

Our test suite only runs with tar.gz archives, because those are what we use in the pipeline.
If you want to use this for a different type of compressed archive, you might like to add some extra tests.
You might also consider splitting the Unpacker into two classes -- an Unarchiver and an Deompressor -- if you ever have to deal with standalone .tar archives or compressed .gz files.

Our pipeline is written in Scala, but the heavy lifting is done by Java libraries here -- I don't think it would be hard to rewrite this entirely in Java if that's what you need.

You can see the code this post is based on [in our public repo][ghurl], along with the [accompanying tests][tests].
It uses Either rather than Try to handle errors, which is a design pattern it inherits from the rest of our codebase -- for this standalone example, Try is simpler and easier to follow.

If you want to use this code in your project, all of Wellcome's code is available under [an MIT license][license] -- just the copyright notice and a link back to our repo.
If you found my walkthrough helpful, perhaps [say thanks on Twitter][thanks]?

[s3_python]: /2019/working-with-large-s3-objects/
[commons]: https://en.wikipedia.org/wiki/Apache_Commons
[ghurl]: https://github.com/wellcometrust/storage-service/blob/5582edcd3a3d1dd876aa311d1c8c03ba66347e7d/bag_unpacker/src/main/scala/uk/ac/wellcome/platform/archive/bagunpacker/storage/Unarchiver.scala
[tests]: https://github.com/wellcometrust/storage-service/blob/5582edcd3a3d1dd876aa311d1c8c03ba66347e7d/bag_unpacker/src/test/scala/uk/ac/wellcome/platform/archive/bagunpacker/storage/UnarchiverTest.scala
[license]: https://github.com/wellcometrust/platform/blob/ab7d6e6a31a4dd1ed6d900b222999dba23360b3f/LICENSE
[thanks]: https://twitter.com/intent/tweet?text=@alexwlchan%20
[kofi]: https://ko-fi.com/alexwlchan