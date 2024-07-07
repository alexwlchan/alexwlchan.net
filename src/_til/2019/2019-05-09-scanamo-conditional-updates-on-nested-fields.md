---
layout: til
title: "DynamoDB: Conditional updates on nested fields"
date: 2019-05-09 12:12:24 +0100
tags:
  - java
  - aws
  - amazon-dynamodb
  - scala
  - scala:scanamo
---

I always struggle with the ConditionalUpdate syntax for DynamoDB, so here's a snippet for the Java SDK that works (with a bit of Scanamo magic to turn case class instances into instances of `AttributeValue`):

```scala
import com.gu.scanamo.DynamoFormat
import com.amazonaws.services.dynamodbv2.model.{
  AttributeValue,
  UpdateItemRequest
}

import scala.collection.JavaConverters._

case class Versioned[T](payload: T, version: Version)

val value: Versioned[T]

val evidenceV: DynamoFormat[Version]
val evidenceT: DynamoFormat[T]

val versionAv: AttributeValue = evidenceV.write(value.version)
val payloadAv: AttributeValue = evidenceT.write(value.payload)

val updateItemRequest = new UpdateItemRequest()
  .withTableName(dynamoConfig.table)
  .addKeyEntry("id", new AttributeValue().withS(value.version.id))
  .withUpdateExpression(
    "SET payload = :payload, version = :version"
  )
  .withConditionExpression("attribute_not_exists(id) OR version < :currentVersion")
  .withExpressionAttributeValues(
    Map(
      ":currentVersion" -> new AttributeValue(value.version.version.toString),
      ":payload" -> payloadAv,
      ":version" -> versionAv
    ).asJava
  )
```

Here is the equivalent code in the Scanamo DSL:

```scala
val ops = table
  .given(
    not(attributeExists('id)) or
      (attributeExists('id) and 'version \ 'version < value.version.version)
  )
  .update(
    'id -> value.version.id,
    set('version -> value.version) and set('payload -> value.payload)
  )

Scanamo.exec(dynamoClient)(ops)
```

Note especially the use of `'version \ 'version` to access the nested field.

References:

-   <https://github.com/scanamo/scanamo/issues/136>
