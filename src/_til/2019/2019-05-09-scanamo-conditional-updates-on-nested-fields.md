---
layout: til
title: "DynamoDB: Conditional updates on nested fields"
date: 2019-05-09 12:12:24 +01:00
tags:
  - java
  - aws
  - aws:amazon dynamodb
  - scala
  - scala:scanamo
---

I always struggle with the ConditionalUpdate syntax for DynamoDB, so here's a snippet for the Java SDK that works (with a bit of Scanamo magic to turn case class instances into instances of `AttributeValue`):

{% code lang="scala" names="0:com.gu.scanamo.DynamoFormat 1:com.amazonaws.services.dynamodbv2.model. 2:AttributeValue 3:UpdateItemRequest 4:scala.collection.JavaConverters._ 5:Versioned 6:payload 7:version 8:value 9:evidenceV 10:evidenceT 11:versionAv 14:payloadAv 17:updateItemRequest" %}
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
{% endcode %}

Here is the equivalent code in the Scanamo DSL:

{% code lang="scala" names="0:ops 1:table 15:dynamoClient" %}
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
{% endcode %}

Note especially the use of `'version \ 'version` to access the nested field.

References:

-   <https://github.com/scanamo/scanamo/issues/136>
