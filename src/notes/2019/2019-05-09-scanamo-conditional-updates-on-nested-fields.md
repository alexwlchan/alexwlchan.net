---
layout: note
title: "Conditional updates on nested fields in DynamoDB"
date: 2019-05-09 12:12:24 +01:00
topics:
  - AWS
  - Scala
---

I always struggle with the ConditionalUpdate syntax for DynamoDB, so here's a snippet for the Java SDK that works (with a bit of Scanamo magic to turn case class instances into instances of `AttributeValue`):

```scala {"names":{"1":"com","2":"gu","3":"scanamo","4":"DynamoFormat","5":"com","6":"amazonaws","7":"services","8":"dynamodbv2","9":"model","10":"AttributeValue","11":"UpdateItemRequest","12":"scala","13":"collection","14":"JavaConverters","16":"Versioned","17":"T","18":"payload","20":"version","22":"value","25":"evidenceV","28":"evidenceT","31":"versionAv","37":"payloadAv","43":"updateItemRequest"}}
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

```scala {"names":{"1":"ops"}}
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
