package main

trait LockDao[LockDaoIdent, LockDaoContextId] {
  type Ident = LockDaoIdent
  type ContextId = LockDaoContextId

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
