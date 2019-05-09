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

This is a generic trait for acquiring and releasing a single lock.
We can create implementations with different backends that all inherit this trait -- for example, a DynamoDB dao for use in production, and an in-memory dao for use in tests.

The type of the lock identifier is a type parameter, `Ident`.
An identifier might be a string, or a number, or a UUID, or something else -- we don't have to decide here.

[dao]: https://en.wikipedia.org/wiki/Data_access_object

```scala
trait LockDao[Ident, ContextId] {
  type LockResult = Either[LockFailure[Ident], Lock[Ident, ContextId]]
  type UnlockResult = Either[UnlockFailure[ContextId], Unit]

  /** Lock a single ID.
    *
    * The context ID is used to identify the process that wants the lock.
    * Locking an ID twice with the same context ID should be allowed;
    * locking with a different context ID should be an error.
    *
    */
  def lock(id: Ident, contextId: ContextId): LockResult

  /** Release the lock on every ID that was part of this context. */
  def unlock(contextId: ContextId): UnlockResult
}

trait Lock[Ident, ContextId] {
  val id: Ident
  val contextId: ContextId
}

case class LockFailure[Ident](id: Ident, e: Throwable)

case class UnlockFailure[ContextId](contextId: ContextId, e: Throwable)
```

---



```
class InMemoryLockDao extends LockDao[String, UUID] with Logging {
  private var locks: Map[String, PermanentLock] = Map.empty

  var history: List[PermanentLock] = List.empty

  override def lock(id: String, contextId: UUID): LockResult = {
    info(s"Locking ID <$id> in context <$contextId>")

    locks.get(id) match {
      case Some(r @ PermanentLock(_, existingContextId)) if contextId == existingContextId => Right(r)
      case Some(PermanentLock(_, existingContextId)) if contextId != existingContextId => Left(
        LockFailure[String](
          id,
          new Throwable(s"Failed to lock <$id> in context <$contextId>; already locked as <$existingContextId>")
        )
      )
      case _ =>
        val rowLock = PermanentLock(
          id = id,
          contextId = contextId
        )
        locks = locks ++ Map(id -> rowLock)
        history = history :+ rowLock
        Right(rowLock)
    }
  }

  override def unlock(contextId: UUID): UnlockResult = {
    info(s"Unlocking for context <$contextId>")
    locks = locks.filter { case (id, PermanentLock(_, lockContextId)) =>
      debug(s"Inspecting $id")
      contextId != lockContextId
    }

    Right(())
  }

  def getCurrentLocks: Set[String] =
    locks.keys.toSet
}

case class PermanentLock(id: String, contextId: UUID) extends Lock[String, UUID]
```

* can lock an ID/context pair
* can't lock an ID under a different context
* can lock multiple IDs under a single context
* can unlock all the IDs in a context
* can relock an unlocked ID in a new context
* original locks in a different context are preserved

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
