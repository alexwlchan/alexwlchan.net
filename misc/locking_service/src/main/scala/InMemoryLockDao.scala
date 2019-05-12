package main

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

    def unlock(contextId: ContextId): UnlockResult = {
      currentLocks = currentLocks.filter { case (_, lockContextId) =>
        contextId != lockContextId
      }

      Right(Unit)
    }
}
