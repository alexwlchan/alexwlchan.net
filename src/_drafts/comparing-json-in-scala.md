---
layout: post
title: Comparing JSON strings in Scala test
summary: There are lots of ways to format JSON. How do you know if two JSON strings have the same data, just differently roamtted?
category: Scala
---

For my day job, I write APIs that return JSON responses.
The APIs are written in Scala, and we use [Circe] for serialising JSON.

When we test these APIs, we want to assert that they return the correct responses, but JSON makes this tricky.
Consider the following two JSON strings:

```
{"name":"triangle","sides":3,"type":"Shape"}
```

```
{
  "name": "triangle",
  "sides": 3,
  "type": "Shape"
}
```

These two strings contain the same data, but the formatting is different.
A simple string comparison would fail.
If this was the actual and the expected JSON, we'd treating this as a passing test.
This presents a problem:

**How do we know if two JSON strings are the same, modulo formatting?**

We've written a trait that gives us some assertion helpers for comparing JSON in tests:

```scala
import io.circe.Json
import io.circe.parser._

trait JsonAssertions {
  def assertJsonStringsAreEqual(json1: String, json2: String): Unit = {
    val tree1 = parseOrElse(json1)
    val tree2 = parseOrElse(json2)
    assert(tree1 == tree2)
  }

  def assertJsonStringsDiffer(json1: String, json2: String): Unit = {
    val tree1 = parseOrElse(json1)
    val tree2 = parseOrElse(json2)
    assert(tree1 != tree2)
  }

  private def parseOrElse(jsonString: String) match {
    case Right(json) => json
    case Left(failure) =>
      println(s"Error parsing $jsonString")
      throw failure
  }
}
```

We mix this trait into our test classes, and then we can call the two assertion methods to compare JSON strings.
**These methods only compare the structure of JSON, not the exact formatting.**

The helper [parses the JSON strings](https://circe.github.io/circe/parsing.html) into a generic Circe class `io.circe.Json`.
That class has equality methods, so we can compare the parsed JSON, rather than the literal strings.

I've used Scala's vanilla assertion method in the example above, so that this can be used with any testing framework.
In practice, we use [ScalaTest] and some of its assertion helpers, but these JSON assertions aren't ScalaTest-specific.
You can find that version [in our scala-json repo](https://github.com/wellcomecollection/scala-json/blob/master/src/test/scala/uk/ac/wellcome/json/utils/JsonAssertions.scala).

These assertions allow us to write our tests with literal JSON strings as the expected output:

```scala
case class Shape(name: String, sides: Int)
val triangle = Shape(name = "triangle", sides = 3)

val expectedJson: String =
  s"""
  {
    "name": "${triangle.name}",
    "sides": ${triangle.sides},
    "type": "Shape"
  }
  """

assertJsonStringsAreEqual(expectedJson, actualJson)
```

This means our tests aren't coupled to the inner workings of the API -- we know the JSON output always looks the same, even if the internals change.
(At one point we completely swapped out the JSON serialisation library, and tests like this helped ensure there wasn't any user-facing change.)

We've used these assertions in hundreds of tests, and they make it easy to compare JSON.
If this is something you have to do in Scala, feel free to copy and paste this code into your own project.

[Circe]: https://circe.github.io/
[ScalaTest]: http://www.scalatest.org/
