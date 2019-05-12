package main

import cats.MonadError
import cats.data.EitherT
import grizzled.slf4j.Logging

trait FailedLockingServiceOp

case class FailedProcess[ContextId](contextId: ContextId, e: Throwable)
  extends FailedLockingServiceOp

case class FailedLock[ContextId, Ident](
  contextId: ContextId,
  lockFailures: Set[LockFailure[Ident]]) extends FailedLockingServiceOp

trait LockingService[Out, OutMonad[_], LockDaoImpl <: LockDao[_, _]] extends Logging {

  import cats.implicits._

  type LockingServiceResult = Either[FailedLockingServiceOp, lockDao.ContextId]
  type OutMonadError = MonadError[OutMonad, Throwable]
  type Process = Either[FailedLockingServiceOp, Out]

  implicit val lockDao: LockDaoImpl

  def createContextId: lockDao.ContextId

  def withLocks(ids: Set[lockDao.Ident])(
    callback: => OutMonad[Out]
  )(implicit m: OutMonadError): OutMonad[Process] = {
    val contextId: lockDao.ContextId = createContextId

    val eitherT = for {
      contextId <- EitherT.fromEither[OutMonad](
        getLocks(ids = ids, contextId = contextId)
      )

      out <- EitherT(safeCallback(contextId)(callback))
    } yield out

    eitherT.value
  }

  private def safeCallback(contextId: lockDao.ContextId)(
    callback: => OutMonad[Out]
  )(implicit monadError: OutMonadError): OutMonad[Process] = {
    val partialResult: OutMonad[Process] = callback.map { out =>
      unlock(contextId)
      Either.right[FailedLockingServiceOp, Out](out)
    }

    monadError.handleError(partialResult) { err =>
      unlock(contextId)
      Either.left[FailedLockingServiceOp, Out](FailedProcess(contextId, err))
    }
  }

  private def getLocks(
    ids: Set[lockDao.Ident],
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
