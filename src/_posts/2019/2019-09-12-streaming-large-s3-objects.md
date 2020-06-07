---
category: Amazon Web Services
date: 2019-09-12 19:53:53 +0000
layout: post
summary: Walking through some Java/Scala code that lets you read very large objects
  from S3 as a single InputStream.
title: Streaming large objects from S3 with ranged GET requests
tags: aws amazon-s3 scala
---

In [my last post](/2019/09/unpacking-compressed-archives-in-scala/), I talked about how to take a Java `InputStream` for a tar.gz file, and get an iterator of `(ArchiveEntry, InputStream)`.
If we want to use that code, we need to get an InputStream for our tar.gz file -- which in our case, is stored in S3.
Some of our archives are very big (the biggest is half a terabyte), and getting a reliable InputStream for an S3 object turns out to be non-trivial.

In this post, I'm going to walk through some code we've written to reliably stream large objects from S3.
This is similar to something I wrote in February about [reading large objects in Python][s3_python], but you don't need to read that post before this one.

[s3_python]: /2019/02/working-with-large-s3-objects/

To get an InputStream for an object, we can use the GetObject API in the S3 SDK:

```scala
import java.io.InputStream
import com.amazonaws.services.s3.AmazonS3

val s3Client: AmazonS3

val is: InputStream =
  s3Client
    .getObject("bukkit", "myarchive.tar.gz")
    .getObjectContent
```

As you read bytes from this stream, it holds open the same HTTP connection to S3.
The bigger the object, the longer you have to maintain that connection, and the greater the chance that it times out or drops unexpectedly.
If the stream drops, you can get a slightly cryptic error from the S3 SDK:

> com.amazonaws.SdkClientException: Data read has a different length than the expected: dataLength=162480427095; expectedLength=528801304583; includeSkipped=true; in.getClass()=class com.amazonaws.services.s3.AmazonS3Client$2; markedSupported=false; marked=0; resetSinceLastMarked=false; markCount=0; resetCount=0

In this case, the SDK was expecting to read 528&nbsp;GB from the stream.
Because the connection dropped midway through, it got an EOF and only read 162.5&nbsp;GB -- hence this error.
It took us a while to work out why it was happening!

I haven't tried it myself, but I think the [TransferManager][transfer_manager] in the AWS SDK helps with this -- you can download large objects to a file, and it manages the threads and connections to keep the download going.
If you have the disk space to download your objects, that might be worth a look.
Unfortunately TransferManager doesn't support [downloading to streams][issue_893] (yet), and we don't have much local disk space, so we had to find a way to do it manually.

[transfer_manager]: https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/s3/transfer/TransferManager.html
[issue_893]: https://github.com/aws/aws-sdk-java/issues/893

When you want to upload a large file to S3, you can do a *multipart upload*.
You break the file into smaller pieces, upload each piece individually, then they get stitched back together into a single object.
What if you run that process in reverse?

**Break the object into smaller pieces, download each piece individually, then stitch them back together into a single stream.**
We'd only be holding open a connection for as long as it takes to download a chunk, so it's much less likely to timeout or drop.
Let's walk through the code:

## How big is a single object?

To know how many chunks we'll need (and when we're finished reading the object), we need to know how big the object is.
One way to do this is to use the `getObjectMetadata` method (aka the HeadObject API):

```scala
def getSize(bucketName: String, key: String): Long =
  s3Client
    .getObjectMetadata(bucketName, key)
    .getContentLength
```

## How do we get a single chunk of an object?

Let's suppose we want to read the first 1000 bytes of an object -- we can use a ranged GET request to get just that part of the file:

```scala
import com.amazonaws.services.s3.model.GetObjectRequest

val getRequest = new GetObjectRequest(bucketName, key)
  .withRange(0, 999)

val is: InputStream =
  s3Client
    .getObject(getRequest)
    .getObjectContent
```

Note that the Range header is an inclusive boundary -- in this example, it reads everything up to and including the 999th byte.

If the object only has 500 bytes, that's all we'll get -- it quietly truncates the range to the bytes available.

## How do we stitch the pieces back together?

Now we know how big the object is, and how to read an individual piece.
Reading any one piece gives us an `InputStream`, so we have a series of InputStreams -- but ideally we'd present a single InputStream back to the caller.
How can we do that?

Java has a `SequenceInputStream` type that's just what we need -- we give it an Enumeration of InputStream instances, and it reads bytes from each one in turn.
It we create the streams as they're needed by the Enumeration, this will join them together for us.

<img src="/images/2019/sequence_stream.svg" alt="A series of rectangles for InputStreams, one from 0–999, then 1000–1999, then 2000–2999, all pointing up into a single recetangle labelled SequenceInputStream.">

We can create the Enumeration like so:

```scala
import java.util
import com.amazonaws.services.s3.model.S3ObjectInputStream

val pieceSize: Long

val enumeration = new util.Enumeration[S3ObjectInputStream] {
  var currentPosition = 0L
  val totalSize: Long

  override def hasMoreElements: Boolean =
    currentPosition < totalSize

  override def nextElement(): InputStream = {
    // The Range request is inclusive of the `start` and `end` parameters,
    // so to read `pieceSize` bytes we need to go to `pieceSize - 1`.
    val getRequest =
      new GetObjectRequest(bucketName, key)
        .withRange(currentPosition, currentPosition + pieceSize - 1)

    currentPosition += pieceSize

    s3Client.getObject(getRequest).getObjectContent
  }
}
```

On each step of the enumeration, we read the next chunk from S3, and track how far we've read with `currentPosition`.
On the last step, we might ask for more bytes than are available (if the remaining bytes are less than the buffer size), but that seems to work okay.
The S3 SDK returns all the remaining bytes, but no more.

And then we put that enumeration into a SequenceInputStream:

```scala
import java.io.SequenceInputStream

val combinedStream: InputStream = new SequenceInputStream(enumeration)
```

When the Enumeration reaches the end of one of the individual streams, it closes that stream and calls `nextElement()` to create the next one.

This can be more expensive than doing a single GetObject call -- Amazon charge for each use of the GetObject API, and while the individual cost is small, the cost of multiple calls could add up if you're making lots of them.
You can play with the chunk size to get a mixture of reliability and cost.
Smaller chunks are more reliable (because each connection is open for a shorter time), but cost more in the aggregate.

In our testing, we found that this alone still wasn't wholly reliable.
The SequenceInputStream won't close the stream for a single piece until it's read all the bytes for that piece, and started reading the next one -- and it holds the underlying connection open.
If it takes a long time to process a single piece, that connection can still drop.
We could turn down the buffer size to make it more reliable, but that gets expensive.

What we're trying instead is reading the entire contents of a single piece into memory as soon as we do the GetObject call, then closing the connection.
We're trading memory for increased reliability.
Here's what that buffering looks like:

```scala
import java.io.ByteArrayInputStream

val underlying: util.Enumeration[InputStream]

val bufferedEnumeration = new util.Enumeration[ByteArrayInputStream] {
  override def hasMoreElements: Boolean = underlying.hasMoreElements

  override def nextElement(): ByteArrayInputStream = {
    val nextStream = underlying.nextElement()
    val byteArray = IOUtils.toByteArray(nextStream)
    nextStream.close()
    new ByteArrayInputStream(byteArray)
  }
}
```

We can drop this enumeration into another SequenceInputStream, and get a single InputStream again – but this time the S3ObjectInputStream is read and closed almost immediately.

## Putting it all together

If we take all those pieces, we can combine them into a single Scala class like so:

```scala
import java.io.{ByteArrayInputStream, InputStream, SequenceInputStream}
import java.util

import com.amazonaws.services.s3.model.{GetObjectRequest, S3ObjectInputStream}
import com.amazonaws.services.s3.AmazonS3
import org.apache.commons.io.IOUtils

import scala.util.Try

/** Read objects from S3, buffering up to `bufferSize` bytes of an object
  * in-memory at a time, minimising the time needed to hold open
  * an HTTP connection to S3.
  *
  * This is useful for reading very large objects to an InputStream,
  * especially where a single GetObject call would time out before
  * reading the entire object.
  *
  */
class S3StreamReader(s3Client: AmazonS3, bufferSize: Long) {
  def get(bucketName: String, key: String): Try[InputStream] = Try {
    val totalSize = getSize(bucketName, key)

    val s3Enumeration = getEnumeration(bucketName, key, totalSize)
    val bufferedEnumeration = getBufferedEnumeration(s3Enumeration)

    new SequenceInputStream(bufferedEnumeration)
  }

  private def getSize(bucketName: String, key: String): Long =
    s3Client
      .getObjectMetadata(bucketName, key)
      .getContentLength

  private def getEnumeration(
    bucketName: String,
    key: String,
    totalSize: Long): util.Enumeration[S3ObjectInputStream] =
    new util.Enumeration[S3ObjectInputStream] {
      var currentPosition = 0L

      override def hasMoreElements: Boolean =
        currentPosition < totalSize

      override def nextElement(): InputStream = {
        // The Range request is inclusive of the `start` and `end` parameters,
        // so to read `bufferSize` bytes we need to go to `bufferSize - 1`.
        val getRequest =
          new GetObjectRequest(bucketName, key)
            .withRange(currentPosition, currentPosition + bufferSize - 1)

        currentPosition += bufferSize

        s3Client.getObject(getRequest).getObjectContent
      }
    }

  private def getBufferedEnumeration[IS <: InputStream](
    underlying: util.Enumeration[IS]): util.Enumeration[ByteArrayInputStream] =
    new util.Enumeration[ByteArrayInputStream] {
      override def hasMoreElements: Boolean = underlying.hasMoreElements

      override def nextElement(): ByteArrayInputStream = {
        val nextStream = underlying.nextElement()
        val byteArray = IOUtils.toByteArray(nextStream)
        nextStream.close()
        new ByteArrayInputStream(byteArray)
      }
    }
}
```

That's a standalone snippet you can drop into your project if it's useful (remembering to include the platform [MIT licence][MIT]).

We've been running this code in our pipeline for several weeks, and in that time it's read tens of thousands of objects, ranging from a few kilobytes to half a terabyte.
Our apps have a 128MB buffer, with up to ten threads at once and 2GB of memory.
It's fixed a persistent source of flakiness when ranging from S3, and the cost of the extra GetObject calls has been negligible.

This could behave unexpectedly if an object changes under your feet -- the data from one piece would be inconsistent with another piece.
Our objects should never change once they're written, so that's not a problem for us.

All of the heavy lifting is done by Java classes, so if your project uses Java rather than Scala, you should be able to port this for your needs.
And the general idea -- using a ranged GET request to fetch an object a piece at a time, then stitching them together -- is language agnostic, so you can use this technique even if you're not using a JVM language.

[MIT]: https://github.com/wellcometrust/platform/blob/ab7d6e6a31a4dd1ed6d900b222999dba23360b3f/LICENSE
