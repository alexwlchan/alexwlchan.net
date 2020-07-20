---
layout: post
date: 2020-07-20 09:06:38 +0000
title: Running concurrent Try functions in Scala
summary: If you have a function that returns Try[_], how do you call it more than once at the same time?
category: scala
---

Suppose you have a Scala function that returns `Try[_]`.
How do you call it more than once at the same time?

I had to solve this problem in a test suite at work.
We have a worker function that returns a Try, and the function contains some [locking logic] to ensure only one instance of it can run at a time.
I wanted to test it by calling multiple instances of the function, and checking that only one succeeded.

If you have a function that returns a Future, you can call it multiple times in a sequence and collect the results:


```scala
def greetF(name: String): Future[_] = Future {
  Thread.sleep(Random.nextInt(1000))
  println(s"Hello $name")
}

val futures: Seq[Future[_]] =
  Seq("alice", "bob", "carol", "dave", "erin").map { greetF }
```

When you run this code, you'll see the names printed in a different order each time.
Each instance of `greet` is running concurrently, so the `sleep`s are all counting down together.

What if we take this code, and replace `Future` with `Try`?

```scala
def greetT(name: String): Try[_] = Try {
  Thread.sleep(Random.nextInt(1000))
  println(s"Hello $name")
}

val tries: Seq[Try[_]] =
  Seq("alice", "bob", "carol", "dave", "erin").map { greetT }
```

Now the names get printed in alphabetical order.
The `Try`s run synchronously -- each one has to finish before the next one can start.
That's not what we want!

My first thought was to try wrapping my `Try` calls in [`Future.fromTry`]:

```scala
val futures: Seq[Future[_]] =
  Seq("alice", "bob", "carol", "dave", "erin")
    .map { name => Future.fromTry(greetT(name)) }
```

But this still prints the names in the same order -- because `Future.fromTry` wraps an already-completed Try, it waits for the result of the inner `Try` to complete.

The solution I found was to initiate a new `Future`, then flatmap over that to use the `Future.fromTry`:

```scala
val futures: Seq[Future[_]] =
  Seq("alice", "bob", "carol", "dave", "erin")
    .map { name =>
      Future.successful(()).flatMap { _ =>
        Future.fromTry(greetT(name))
      }
    }
```

Now I have five `Future`s running concurrently, each of which calls the `Try` function.
It's a bit ugly, but it does the trick.

[locking logic]: /2019/05/creating-a-locking-service-in-a-scala-type-class/
[`Future.fromTry`]: https://www.scala-lang.org/api/current/scala/concurrent/Future$.html#fromTry[T](result:scala.util.Try[T]):scala.concurrent.Future[T]
