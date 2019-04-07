---
layout: post
date: 2018-08-25 08:20:24 +0000
title: Implementing parallel scan in DynamoDB with Scanamo
tags: aws scala
summary: Prototype code for running a parallel scan against a DynamoDB table, and using Scanamo to serialise rows as Scala case classes.
category: Working with AWS
best_of: true
---

At work, we use DynamoDB for storing large collections of records -- these get processed by the [catalogue pipeline][pipeline] that feeds our API, which ultimately powers search on the new Wellcome Collection website.

All of our models are defined as [Scala case classes][case_class], and we use [Scanamo][scanamo] to interact with DynamoDB.
Scanamo is a wrapper around the DynamoDB SDK which hides the work of serialising and deserialising case classes into the DynamoDB internal format.

When we change the pipeline, we want to reprocess all the existing records in DynamoDB (we call this "reindexing").
If you want to iterate over the records in DynamoDB, you have to do a [Scan operation][scan].
A Scan returns the records in sequence, so you can only run one worker at a time -- this is pretty slow.
We want to process the table in parallel, so we have a DIY mechanism for dividing the table into "shards", and then we process each shard separately.

{%
  image :filename => "dynamodb_lambda.png",
  :alt => "A two-way arrow between a blue rectangle (a DynamoDB table) and an orange circle (a Lambda). The arrows are labelled “DynamoDB stream” and “Add ‘reindex shard’”.",
  :style => "max-width: 600px;"
%}

DynamoDB tables can produce [an event stream][stream] of updates to the table.
We connect this stream to a Lambda function, which picks a "reindex shard" for a row, and writes that shard back to the table.
The shard ID is copied to a [global secondary index (GSI)][gsi], which allows us to efficiently work out which rows are in a particular reindex shard.

When we want to reindex the table, we run one worker per reindex shard -- every row is in exactly one reindex shard, and the GSI lets us look up the contents of each shard.
It runs significantly faster than processing the table in sequence.

It's also pretty brittle.
It relies on the DynamoDB stream and the Lambda working correctly (both of which can be flaky), it's extra infrastructure for us to maintain, and we're stuck with a fixed shard size.
If we decide to change the shard size later, we need to go back and reshard the entire table.

This has a whiff of [Not Invented Here syndrome][nih].
We can't be the only people who want to process a DynamoDB table in parallel!

Yesterday, I stumbled across an old blog post [announcing parallel scans][blog] in DynamoDB.
This is exactly what we need -- it's a supported API, doesn't require extra infrastructure from us, and it lets us pick a different shard size on each scan.
It's worth a look.

I couldn't find an implementation of parallel scan that also uses Scanamo and case classes, so I decided to write my own.
(I did Google it before diving in!)
It's a useful standalone component, so I thought I'd write up what I found.

Note: this is a prototype, not production code.
We'll probably put it in production at some point, but I don't know how long that'll be.

[pipeline]: https://stacks.wellcomecollection.org/whats-in-the-box-addfe6ae16d4
[case_class]: https://docs.scala-lang.org/tour/case-classes.html
[scanamo]: https://www.scanamo.org/
[scan]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html
[stream]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html
[gsi]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html
[nih]: https://en.wikipedia.org/wiki/Not_invented_here
[blog]: https://aws.amazon.com/blogs/aws/amazon-dynamodb-parallel-scans-and-other-good-news/

<!-- summary -->

## Creating an API client

Before we write any parallel scan code, we need an API client for working with the DynamoDB API:

```scala
import com.amazonaws.auth.{AWSStaticCredentialsProvider, BasicAWSCredentials}
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder

val AWS_ACCESS_ID         = "XXX"
val AWS_SECRET_ACCESS_KEY = "XXX"
val AWS_REGION            = "eu-west-1"

val dynamoDbClient = AmazonDynamoDBClientBuilder
  .standard
  .withCredentials(
    new AWSStaticCredentialsProvider(
      new BasicAWSCredentials(AWS_ACCESS_ID, AWS_SECRET_ACCESS_KEY)
    )
  )
  .withRegion(AWS_REGION)
  .build()
```

There are lots of ways to get credentials into the AWS SDK -- I'm using hard-coded keys here because they're the easiest for a standalone example.

{% comment %}
Then let's create a new, empty table:

```scala
import com.amazonaws.services.dynamodbv2.model.{
  AttributeDefinition,
  CreateTableRequest,
  KeySchemaElement,
  KeyType,
  ProvisionedThroughput
}

val TABLE_NAME = "ShapeSorter"

dynamoDbClient.createTable(
  new CreateTableRequest()
    .withTableName(TABLE_NAME)
    .withKeySchema(
      new KeySchemaElement()
        .withAttributeName("id")
        .withKeyType(KeyType.HASH)
    )
    .withAttributeDefinitions(
      new AttributeDefinition()
        .withAttributeName("id")
        .withAttributeType("S")
    )
    .withProvisionedThroughput(new ProvisionedThroughput()
      .withReadCapacityUnits(1L)
      .withWriteCapacityUnits(1L)
    )
)
```

Finally, let's create a case class to represent the rows in this table, and populate it with some data:

```scala
import com.gu.scanamo.Scanamo

import scala.util.Random

val COLOURS = List("red", "orange", "yellow", "green", "blue")

case class Shape(id: String, sides: Int, colour: String)

(1 to 5000).map { sides =>
  val shape = Shape(
    id = sides.toString,
    sides = sides,
    colour = COLOURS(Random.nextInt(COLOURS.length))
  )

  Scanamo.put(dynamoDbClient)(TABLE_NAME)(shape)
}
```
{% endcomment %}

## Step-by-step breakdown

There's a [Java example of a parallel scan][java_example] in the AWS docs, which performs the Scan, but it only prints the result.
I used it as a starting point, but then I had to dig deeper to work out how to pass the result around as a useful value.

A [parallel scan][parallel] divides the table into "segments".
You create a collection of workers, each of which makes its own Scan request with two parameters:

*   `TotalSegments` is the total number of segments.
    Every worker should use the same value.
*   `Segment` is the index of the segment being scanned by this particular worker -- note that this value is 0-indexed.
    Every worker passes a different value.

These parameters can be passed as an instance of [ScanSpec][scanspec], so let's construct that:

```scala
import com.amazonaws.services.dynamodbv2.document.spec.ScanSpec

val scanSpec = new ScanSpec()
  .withTotalSegments(totalSegments)   // totalSegments: Int
  .withSegment(segment)               // segment: Int
```

Then to perform the scan itself, we use the Document API and pass this ScanSpec as a parameter:

```scala
import com.amazonaws.services.dynamodbv2.document.{
  DynamoDB,
  ItemCollection,
  ScanOutcome
}

val documentApiClient = new DynamoDB(dynamoDbClient)
val table = documentApiClient.getTable(tableName)   // tableName: String

val itemCollection: ItemCollection[ScanOutcome] = table.scan(scanSpec)
```

I suspect this only returns the first page of results -- I've only played with this in toy tables with a handful of example rows, not our larger databases.
If I use this in production, I'll want some tests and checks around pagination.
(Or ensure that I choose sufficiently many segments that every segment fits inside a single page!)

Playing a bit in IntelliJ to see what methods I had available, I eventually stumbled across the following to turn the collection into a Scala list:

```scala
import com.amazonaws.services.dynamodbv2.document.Item
import scala.collection.JavaConverters._

val items: List[Item] = itemCollection.asScala.toList
```

This is an "Item" in the sense of a generic collection of key-value pairs, but it's not a proper Scala type, which is what I really want.
It's an internal DynamoDB representation of a row.

I went poking around in Scanamo to see how they serialise an Item as a case class.
I didn't quite find that, but looking [in ScanamoFree.scala][scanamofree], I stumbled across clues in two methods:

```scala
object ScanamoFree {
  ...

  def get[T](tableName: String)(key: UniqueKey[_])(
      implicit ft: DynamoFormat[T]): ScanamoOps[Option[Either[DynamoReadError, T]]] =
    for {
      res <- ScanamoOps.get(new GetItemRequest().withTableName(tableName).withKey(key.asAVMap.asJava))
    } yield Option(res.getItem).map(read[T])

  ...

  def read[T](m: java.util.Map[String, AttributeValue])(implicit f: DynamoFormat[T]): Either[DynamoReadError, T] =
    f.read(new AttributeValue().withM(m))
}
```

In the `get()` method, it looks like the body of the for comprehension is calling the DynamoDB Java SDK (GetItemRequest is a dead giveaway), and then it passes it to a `read()` method that unpacks it as a case class.
The `read()` method doesn't quite take an Item, but if I can get the String/AttributeValue map out of an Item, then I'm in business.

I stumbled across the method I need [in a Stack Overflow post][stack_overflow]:

```scala
import com.amazonaws.services.dynamodbv2.document.internal.InternalUtils
import com.amazonaws.services.dynamodbv2.model.AttributeValue
import com.gu.scanamo.ScanamoFree
import com.gu.scanamo.error.DynamoReadError

val caseClasses: List[Either[DynamoReadError, T]] = items.map { item =>
  val attributeValueMap: java.util.Map[String, AttributeValue]
    InternalUtils.toAttributeValues(item)
  ScanamoFree.read[T](attributeValueMap)
}
```

Scanamo will throw a DynamoReadError if it can't parse the row as a case class -- for example, if a field is missing or the wrong type.
You can extract the instance either using `.right.get`, or doing a pattern match on the result.

This is what I wanted when I started -- a list of instances of a case class, fetched using a parallel scan.

## Possible changes

In hindsight, I'm not sure this needs to use the Document API.
I copied it from the Java example, but there's also a ScanRequest (similar to GetItemRequest) that lets you set the table name, segment and total segments -- I didn't see that I was poking around in Scanamo.

Then there's the `get()` method on ScanamoFree that uses a GetItemRequest internally.
I wonder if you could write a similar method that uses a ScanRequest internally, and add it to Scanamo?
I confess the Scanamo internals always leave me a little confused, so I didn't dig into this further.

Finally, there's the pagination behaviour, which is a complete unknown.
I haven't tried running this on a really big table yet, and I'd want some tests around pagination before running it in prod.

[parallel]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan
[java_example]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ScanJavaDocumentAPI.html#DocumentAPIJavaParallelScanExample
[scanspec]: https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/dynamodbv2/document/spec/ScanSpec.html
[scanamofree]: https://github.com/scanamo/scanamo/blob/12554b8e24ef8839d5e9dd9a4f42ae130e29b42b/scanamo/src/main/scala/com/gu/scanamo/ScanamoFree.scala
[stack_overflow]: https://stackoverflow.com/a/27538483/1558022

## Final example

This combines all the snippets into a single, runnable example:

```scala
import com.amazonaws.auth.{AWSStaticCredentialsProvider, BasicAWSCredentials}
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder
import com.amazonaws.services.dynamodbv2.document.{
  DynamoDB,
  Item,
  ItemCollection,
  ScanOutcome
}
import com.amazonaws.services.dynamodbv2.document.internal.InternalUtils
import com.amazonaws.services.dynamodbv2.document.spec.ScanSpec
import com.amazonaws.services.dynamodbv2.model.AttributeValue
import com.gu.scanamo.{DynamoFormat, ScanamoFree}
import com.gu.scanamo.error.DynamoReadError

import scala.collection.JavaConverters._
import scala.concurrent.Future


val AWS_ACCESS_ID         = "XXX"
val AWS_SECRET_ACCESS_KEY = "XXX"
val AWS_REGION            = "eu-west-1"

val dynamoDbClient = AmazonDynamoDBClientBuilder
  .standard
  .withCredentials(
    new AWSStaticCredentialsProvider(
      new BasicAWSCredentials(AWS_ACCESS_ID, AWS_SECRET_ACCESS_KEY)
    )
  )
  .withRegion(AWS_REGION)
  .build()


def parallelScan[T](
  tableName: String, totalSegments: Int, segment: Int)(
  implicit ft: DynamoFormat[T]): Future[List[Either[DynamoReadError, T]]] = {
  val scanSpec = new ScanSpec()
    .withTotalSegments(totalSegments)
    .withSegment(segment)

  val documentApiClient = new DynamoDB(dynamoDbClient)
  val table = documentApiClient.getTable(tableName)

  Future {
    val itemCollection: ItemCollection[ScanOutcome] = table.scan(scanSpec)
    val items: List[Item] = itemCollection.asScala.toList

    items.map { item =>
      val attributeValueMap: java.util.Map[String, AttributeValue]
        InternalUtils.toAttributeValues(item)
      ScanamoFree.read[T](attributeValueMap)
    }
  }
}
```

I've wrapped the DynamoDB API calls in a Future for a non-blocking API, which feels more Scala-y.

Don't forget -- this is only some prototype code, not a final solution.
If I end up using this properly, I'll get it reviewed and tested first.
Even so, I hope it was instructive -- I expect to use bits of this again, even if not for this exact problem.
