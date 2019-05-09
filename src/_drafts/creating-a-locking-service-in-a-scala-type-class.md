---
layout: post
title: Creating a locking service in a Scala type class
summary:
tags: scala
---

```
trait LockDao[LockDaoIdent, LockDaoContextId] {
  type Ident = LockDaoIdent
  type ContextId = LockDaoContextId

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

sealed trait FailedLockDaoOp

case class LockFailure[Ident](id: Ident, e: Throwable) extends FailedLockDaoOp

case class UnlockFailure[ContextId](contextId: ContextId, e: Throwable)
    extends FailedLockDaoOp
```

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
