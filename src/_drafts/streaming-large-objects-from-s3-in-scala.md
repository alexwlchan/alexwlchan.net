---
layout: post
title: Reading large objects from S3 as a Java InputStream
summary:
category: Code from Wellcome
---

In [yesterday's post](/2019/09/unpacking-compressed-archives-in-scala/), I talked about how to take a Java `InputStream` for a tar.gz file, and get an iterator of `(ArchiveEntry, InputStream)`.
Next we need to get an InputStream for our tar.gz file -- which in our case, is stored in S3.
Some of our archives are very big (the biggest is half a terabyte), so we need to get a little inventive.

In this post, I'm going to walk through some code we've written to reliably stream large objects from S3.
This overlaps with some code I write in February about [doing something similar in Python][s3_python], but you don't need to read that post before this one.

[s3_python]: /2019/02/working-with-large-s3-objects/

As a starting point, we can use the GetObject API in the S3 SDK:

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
The bigger the file, the longer you have to maintain that connection, and the greater the chance that it times out or drops unexpectedly.
If the stream drops, you can get a slightly cryptic error from the S3 SDK:

> com.amazonaws.SdkClientException: Data read has a different length than the expected: dataLength=162480427095; expectedLength=528801304583; includeSkipped=true; in.getClass()=class com.amazonaws.services.s3.AmazonS3Client$2; markedSupported=false; marked=0; resetSinceLastMarked=false; markCount=0; resetCount=0

In this case, the SDK was expecting to read 528&nbsp;GB from the stream.
Because the connection dropped midway through, it got an EOF and only read 162.5&nbsp;GB -- hence this error.
It took us a while to work out why it was happening!

I haven't tried it myself, but I think the [TransferManager][transfer_manager] in the AWS SDK helps with this -- you can download large files, and it manages the threads and connections to keep the download going.
If you have the disk space to download your files, that might be worth a look.
Unfortunately TransferManager doesn't support [downloading to streams][issue_893] (yet), so we found a way to do it manually.

[transfer_manager]: https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/s3/transfer/TransferManager.html
[issue_893]: https://github.com/aws/aws-sdk-java/issues/893

I had the idea to try breaking up the object into chunks, downloading each chunk individually, then stitching them back together into a single stream.
We'd only be holding open a connection for as long as it takes to download a chunk, so it's much less likely to timeout or drop.
Let's break it down in a couple of pieces:

## How big is an object in S3?

To know how many chunks we'll need (and when we're run out of object to stream), we need to know how big the object is.
One way to do this is to use the `getObjectMetadata` method (aka the HeadObject API):

```scala
def getSize(bucketName: String, key: String): Try[Long] = Try {
  s3Client
    .getObjectMetadata(bucketName, key)
    .getContentLength
}
```

Compared to the GetObject API, I find the error messages from this API a little terse.
For example, if you try to look up a non-existent object, the HeadObject API just returns *NotFound*.
The GetObject API gives a bit more detail: *The specified bucket does not exist*.

Here's another version of this function, which uses GetObject -- the result is the same, but we get slightly better error messages:

```scala
def getSize(bucketName: String, key: String): Try[Long] = Try {
  val s3Object = s3Client.getObject(bucketName, key)

  // Remember to close the InputStream, or eventually we'll run out
  // of HTTP connections
  s3Object.getObjectContent.close()

  s3Object.getObjectMetadata.getContentLength
}
```

Unfortunately the cost of the better error reporting is a spurious warning:

> WARNING: Not all bytes were read from the S3ObjectInputStream, aborting HTTP connection. This is likely an error and may result in sub-optimal behavior. Request only the bytes you need via a ranged GET or drain the input stream after use.

When we close the stream,
