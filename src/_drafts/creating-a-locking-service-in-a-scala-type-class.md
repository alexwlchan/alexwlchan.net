---
layout: post
title: Creating a locking service in a Scala type class
summary:
tags: scala
---

Last week, [Robert](https://github.com/kenoir) (one of my colleagues at Wellcome) and I wrote some code to implement [locking][locking].
I'm quite pleased with the code we wrote, and the way we used type classes to do all the tricky logic in memory.
In this post, I'm going to walk through the code we wrote.

[locking]: https://en.wikipedia.org/wiki/Lock_(computer_science)



## The problem

Robert and I are part of a team building a [storage service] for Wellcome's digital collections, which will eventually be the long-term, permanent storage for digital records.
That includes archives, images, photographs, and much more.

We're saving the files to an Amazon S3 bucket[^1], but Amazon doesn't have a way to lock around writes to S3.
If two processes try to write to the same location at the same time, there's no guarantee which will win!

<img src="/images/2019/locking.png" style="width: 327px;">

Our pipeline features lots of parallel processes -- lots of Docker containers running in parallel, and each container running multiple threads.
We want to lock around writes to S3, so that only a single process can write to S3 at a time.
We verify files after they've been written, and we don't overwrite a file if it exists already -- so locking gives an extra guarantee that a rogue process can't corrupt the archive.

Because S3 doesn't provide those locks for us, we have to manage them ourselves.

This is one example -- there are several other places where we need our own locking.
We wanted to build one locking implementation that we could use in lots of places.

[storage service]: https://github.com/wellcometrust/storage-service

[^1]: Eventually every file will be stored in multiple S3 buckets, all with versioning and [Object Locks](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html) enabled. We'll also be saving a copy in another geographic region and with another cloud provider, probably Azure.



## The idea

We already had a locking service that used DynamoDB as a backend.
DynamoDB supports locking in the form of conditional updates: "only store X if not Y".
You create a lock by writing a row with your lock ID, and the condition "only store this row if there isn't already a row with this lock ID".
If the condition is false, the write fails and you know you haven't acquired the lock.

This was fine, but being closely tied to DynamoDB can cause issues.

Testing it can be slow and fiddly (you need to set up a dummy DynamoDB table), it's closely tied to a specific service (we couldn't reuse this code with a SQL backend, for example), and the implementation was mixing bits of the DynamoDB API with locking logic.

callers

We wanted to have a go at creating a new locking service that didn't have a DynamoDB dependency.
We'd separate out the backend,

```scala
lockingService.withLocks(Set("1", "2", "3")) {
  // do some stuff
}
```

https://sans-io.readthedocs.io/how-to-sans-io.html#why-write-i-o-free-protocol-implementations

## Managing individual locks

First we need to be able to manage a lock around an individual resource.
We might write something like this (here, a dao is a [data access object][dao]):

```scala
trait LockDao[Ident] {
  def lock(id: Ident)
  def unlock(id: Ident)
}
```

This is a generic trait, which manages acquiring and releasing a single lock.
It has to decide if/when we can perform each of those operations.

We can create implementations with different backends that all inherit this trait, and which have different rules for managing locks.
A few ideas:

*   A DynamoDB-backed lock dao for use in production applications
*   An in-memory dao for use in tests
*   A dao that expires locks after a certain period if not explicitly unlocked

The type of the lock identifier is a type parameter, `Ident`.
An identifier might be a string, or a number, or a UUID, or something else -- we don't have to decide here.

[dao]: https://en.wikipedia.org/wiki/Data_access_object

Sometimes we need to acquire more than one lock at once, which needs multiple calls to `lock()` -- and then the caller has to remember which locks they've acquired to release them.
To make it simpler for the caller, we've added a second parameter -- a context ID -- to track which process owns a given lock.
A single call to `unlock()` releases all the locks owned by a process.

Here's what the new trait looks like:

```scala
trait LockDao[Ident, ContextId] {
  def lock(id: Ident, contextId: ContextId)
  def unlock(contextId: ContextId)
}
```

As before, the context ID could be any type, so we've made it a type parameter, `ContextId`.

Now let's think about what these methods should return.
We need to tell the caller whether the lock/unlock succeeded.

We probably want some context, especially if something goes wrong -- so more than a simple boolean.
We could use a `Try` or a `Future`, but that doesn't feel quite right -- we expect lock failures sometimes, and it'd be nice to type the errors.

Eventually we settled upon using an `Either`, with case classes for lock/unlock failures that include some context for the operation in question, and a Throwable that explains why the operation failed:

```scala
trait LockDao[Ident, ContextId] {
  type LockResult = Either[LockFailure[Ident], Lock[Ident, ContextId]]
  type UnlockResult = Either[UnlockFailure[ContextId], Unit]

  def lock(id: Ident, contextId: ContextId): LockResult
  def unlock(contextId: ContextId): UnlockResult
}

trait Lock[Ident, ContextId] {
  val id: Ident
  val contextId: ContextId
}

case class LockFailure[Ident](id: Ident, e: Throwable)

case class UnlockFailure[ContextId](contextId: ContextId, e: Throwable)
```

There's also a generic `Lock` trait, which holds an Ident and a ContextId.
Implementations can return just those two values, or extra data if it's appropriate.
(For example, we have an expiring lock that tells you when the lock is due to expire.)

Now we need to create implementations of this trait!



## Creating an in-memory LockDao for testing

Somebody who uses the LockDao can ask for an instance of that trait, and it doesn't matter whether it's backed by a real database or it's just in-memory.
So when we're testing code that uses the LockDao -- but not testing a LockDao implementation specifically -- we can use a simpler, in-memory implementation.
This makes our tests faster and easier to manage!

Let's create an in-memory implementation.
Here's a skeleton to start with:

```scala
class InMemoryLockDao[Ident, ContextId] extends LockDao[Ident, ContextId] {
  def lock(id: Ident, contextId: ContextId): LockResult = ???
  def unlock(contextId: ContextId): UnlockResult = ???
}
```

Because this is just for testing, we can store the locks as a map.
When somebody acquires a new lock, we store the context ID in the map.
Here's what that looks like:

```scala
case class PermanentLock[Ident, ContextId](
  id: Ident,
  contextId: ContextId
) extends Lock[Ident, ContextId]

class InMemoryLockDao[Ident, ContextId] extends LockDao[Ident, ContextId] {
  private var currentLocks: Map[Ident, ContextId] = Map.empty

  def lock(id: Ident, contextId: ContextId): LockResult =
    currentLocks.get(id) match {
      case Some(existingContextId) if contextId == existingContextId =>
        Right(
          PermanentLock(id = id, contextId = contextId)
        )
      case Some(existingContextId) =>
        Left(
          LockFailure(
            id,
            new Throwable(s"Failed to lock <$id> in context <$contextId>; already locked as <$existingContextId>")
          )
        )
      case None =>
        val newLock = PermanentLock(id = id, contextId = contextId)
        currentLocks = currentLocks ++ Map(id -> contextId)
        Right(newLock)
    }

  def unlock(contextId: ContextId): UnlockResult = ???
}
```

We have to remember to look for an existing lock, and compare it to the lock the caller is requesting.
It's fine to call `lock()` if you already have the lock, but you can't lock an ID if somebody else has already locked it.

Because this is only for testing, it doesn't need to be thread-safe or especially robust.
This code is quite simple, so we're more likely to get it right.
When a caller uses this in tests, they can trust the LockDao is behaving correctly and focus on how they use it, and not worry about bugs in the locking code.

Unlocking is much simpler: we just remove the entry from the map.

```scala
class InMemoryLockDao[Ident, ContextId] extends LockDao[Ident, ContextId] {
  def lock(id: Ident, contextId: ContextId): LockResult = ...

  def unlock(contextId: ContextId): UnlockResult = {
    currentLocks = currentLocks.filter { case (_, lockContextId) =>
      contextId != lockContextId
    }

    Right(Unit)
  }
}
```

This gives us a LockDao implementation that's pretty simple, and we can use whenever we need a LockDao in tests.
Here's what it looks like in practice:

```scala
import java.util.UUID

val dao = new InMemoryLockDao[String, UUID]()

val u1 = UUID.randomUUID
println(dao.lock(id = "1", contextId = u1))               // succeeds
println(dao.lock(id = "1", contextId = UUID.randomUUID))  // succeeds
println(dao.lock(id = "2", contextId = UUID.randomUUID))  // fails
println(dao.unlock(contextId = u1))
println(dao.lock(id = "1", contextId = UUID.randomUUID))  // succeeds
```

We also have a small number of tests that go with it, and check it behaves correctly:

*   It locks an ID/context pair
*   You can't lock the same ID under different contexts
*   You can lock different IDs under the same context
*   You can unlock all the IDs under the same context
*   When an ID is unlocked, it can be relocked in a new context

Because there's no I/O involved, those tests take a fraction of a second to run.




## Putting it all together

All the code this post was based on is in a public GitHub repository, [wellcometrust/scala-storage], which is a collection of our shared storage utilities (mainly for working with DynamoDB and S3).
These are the versions I worked from:

-   Managing individual locks

    *   [LockDao.scala @ 4000d97](https://github.com/wellcometrust/scala-storage/blob/4000d97bbacbed479e1b4302d1bae6d5cd0e5c33/storage/src/main/scala/uk/ac/wellcome/storage/LockDao.scala)

-   Creating an in-memory LockDao for testing

    *   [InMemoryLockDao.scala @ 263e29b](https://github.com/wellcometrust/scala-storage/blob/263e29bc5c72e44faedac713043a26110fd4b84a/storage/src/test/scala/uk/ac/wellcome/storage/fixtures/InMemoryLockDao.scala)
    *   [InMemoryLockDaoTest.scala @ 263e29b](https://github.com/wellcometrust/scala-storage/blob/263e29bc5c72e44faedac713043a26110fd4b84a/storage/src/test/scala/uk/ac/wellcome/storage/locking/InMemoryLockDaoTest.scala)

All the code linked above (and in this post) is available under the MIT licence.

[wellcometrust/scala-storage]: https://github.com/wellcometrust/scala-storage/

---



create a concrete implementation, see dynamolockdao

---

so now the locking service!

```
package uk.ac.wellcome.storage

import cats._
import cats.data._
import grizzled.slf4j.Logging

import scala.language.higherKinds

trait LockingService[Out, OutMonad[_], LockDaoImpl <: LockDao[_, _]]
    extends Logging {

  import cats.implicits._

  implicit val lockDao: LockDaoImpl

  type LockingServiceResult = Either[FailedLockingServiceOp, lockDao.ContextId]
  type Process = Either[FailedLockingServiceOp, Out]

  type OutMonadError = MonadError[OutMonad, Throwable]

  def withLocks(ids: Set[lockDao.Ident])(
    f: => OutMonad[Out]
  )(implicit m: OutMonadError): OutMonad[Process] = {
    val contextId: lockDao.ContextId = createContextId()

    val eitherT = for {
      contextId <- EitherT.fromEither[OutMonad](
        getLocks(ids = ids, contextId = contextId))

      out <- EitherT(safeF(contextId)(f))
    } yield out

    eitherT.value
  }

  protected def createContextId(): lockDao.ContextId

  def withLock(id: lockDao.Ident)(f: => OutMonad[Out])(
    implicit m: OutMonadError): OutMonad[Process] =
    withLocks(Set(id)) { f }

  private def safeF(contextId: lockDao.ContextId)(
    f: => OutMonad[Out]
  )(implicit monadError: OutMonadError): OutMonad[Process] = {
    val partialF = f.map(o => {
      debug(s"Processing $contextId (got $o)")
      unlock(contextId)
      Either.right[FailedLockingServiceOp, Out](o)
    })

    monadError.handleError(partialF) { e =>
      unlock(contextId)
      Either.left[FailedLockingServiceOp, Out](
        FailedProcess[lockDao.ContextId](contextId, e)
      )
    }
  }

  /** Lock the entire set of identifiers we were given.  If any of them fail,
    * unlock the entire context and report a failure.
    *
    */
  private def getLocks(ids: Set[lockDao.Ident],
                       contextId: lockDao.ContextId): LockingServiceResult = {
    val lockResults = ids.map { lockDao.lock(_, contextId) }
    val failedLocks = getFailedLocks(lockResults)

    if (failedLocks.isEmpty) {
      Right(contextId)
    } else {
      unlock(contextId)
      Left(FailedLock(contextId, failedLocks))
    }
  }

  private def getFailedLocks(
    lockResults: Set[lockDao.LockResult]): Set[LockFailure[lockDao.Ident]] =
    lockResults.foldLeft(Set.empty[LockFailure[lockDao.Ident]]) { (acc, o) =>
      o match {
        case Right(_)         => acc
        case Left(failedLock) => acc + failedLock
      }
    }

  private def unlock(contextId: lockDao.ContextId): Unit =
    lockDao
      .unlock(contextId)
      .leftMap { error =>
        warn(s"Unable to unlock context $contextId fully: $error")
      }
}

sealed trait FailedLockingServiceOp

case class FailedLock[ContextId, Ident](contextId: ContextId,
                                        lockFailures: Set[LockFailure[Ident]])
    extends FailedLockingServiceOp

case class FailedUnlock[ContextId, Ident](contextId: ContextId,
                                          ids: List[Ident],
                                          e: Throwable)
    extends FailedLockingServiceOp

case class FailedProcess[ContextId](contextId: ContextId, e: Throwable)
    extends FailedLockingServiceOp
```

can test extensively with in-memory, super fast!

```
  it("acquires a lock successfully, and returns the result") {
    val lockDao = new InMemoryLockDao()

    withLockingService(lockDao) { service =>
      assertLockSuccess(service.withLocks(lockIds) {
        lockDao.getCurrentLocks shouldBe lockIds
        f
      })
    }
  }

  it("allows locking a single identifier") {
    val lockDao = new InMemoryLockDao()

    withLockingService(lockDao) { service =>
      assertLockSuccess(service.withLock("a") {
        lockDao.getCurrentLocks shouldBe Set("a")
        f
      })
    }
  }

  it("fails if you try to re-lock the same identifiers twice") {
    val lockDao = new InMemoryLockDao()

    withLockingService(lockDao) { service =>
      assertLockSuccess(service.withLocks(lockIds) {
        assertFailedLock(service.withLocks(lockIds)(f), lockIds)

        // Check the original locks were preserved
        lockDao.getCurrentLocks shouldBe lockIds

        f
      })
    }
  }

  it("fails if you try to re-lock an already locked identifier") {
    val lockDao = new InMemoryLockDao()

    withLockingService(lockDao) { service =>
      assertLockSuccess(service.withLocks(lockIds) {
        assertFailedLock(
          service.withLocks(overlappingLockIds)(f),
          commonLockIds)

        // Check the original locks were preserved
        lockDao.getCurrentLocks shouldBe lockIds

        f
      })
    }
  }

  it("allows multiple, nested locks on different identifiers") {
    withLockingService { service =>
      assertLockSuccess(service.withLocks(lockIds) {
        assertLockSuccess(service.withLocks(differentLockIds)(f))

        f
      })
    }
  }

  it("unlocks a context set when done, and allows you to re-lock them") {
    withLockingService { service =>
      assertLockSuccess(service.withLocks(lockIds)(f))
      assertLockSuccess(service.withLocks(lockIds)(f))
    }
  }

  it("unlocks a context set when a result throws a Throwable") {
    withLockingService { service =>
      assertFailedProcess(
        service.withLocks(lockIds)(fError), expectedError)
      assertLockSuccess(
        service.withLocks(lockIds)(f))
    }
  }

  it("unlocks a context set when a partial lock is acquired") {
    withLockingService { service =>
      assertLockSuccess(service.withLocks(lockIds) {

        assertFailedLock(
          service.withLocks(overlappingLockIds)(f),
          commonLockIds
        )

        assertLockSuccess(
          service.withLocks(nonOverlappingLockIds)(f)
        )

        f
      })
    }
  }

  it("calls the callback if asked to lock an empty set") {
    withLockingService { service =>
      assertLockSuccess(
        service.withLocks(Set.empty)(f)
      )
    }
  }

  it("returns a success even if unlocking fails") {
    val brokenUnlockDao = new LockDao[String, UUID] {
      override def lock(id: String, contextId: UUID): LockResult =
        Right(PermanentLock(id = id, contextId = contextId))

      override def unlock(contextId: ContextId): UnlockResult =
        Left(UnlockFailure(contextId, new Throwable("BOOM!")))
    }

    withLockingService(brokenUnlockDao) { service =>
      assertLockSuccess(
        service.withLocks(lockIds)(f)
      )
    }
  }

  it("releases locks if the callback fails") {
    val lockDao = new InMemoryLockDao()

    withLockingService(lockDao) { service =>
      val result = service.withLocks(lockIds) {
        Try {
          throw new Throwable("BOOM!")
        }
      }

      result.get.left.value shouldBe a[FailedProcess[_]]
      lockDao.getCurrentLocks shouldBe Set.empty
    }
  }
```

beauty is that with lockign service:

```
class DynamoLockingService[Out, OutMonad[_]](
  implicit val lockDao: DynamoLockDao)
    extends LockingService[Out, OutMonad, LockDao[String, UUID]] {
  override protected def createContextId(): lockDao.ContextId =
    UUID.randomUUID()
}
```
