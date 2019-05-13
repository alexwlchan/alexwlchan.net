package main

import cats.implicits._

import java.util.UUID
import scala.util.{Success, Try}

object Main extends App {
  val dao = new InMemoryLockDao[String, UUID]()

  val u1 = UUID.randomUUID
  println(dao.lock(id = "1", contextId = u1))               // succeeds
  println(dao.lock(id = "1", contextId = UUID.randomUUID))  // succeeds
  println(dao.lock(id = "2", contextId = UUID.randomUUID))  // fails
  println(dao.unlock(contextId = u1))
  println(dao.lock(id = "1", contextId = UUID.randomUUID))  // succeeds

  val lockingService = new LockingService[String, Try, LockDao[String, UUID]] {
    override implicit val lockDao: LockDao[String, UUID] =
      new InMemoryLockDao[String, UUID]()
    override def createContextId: UUID =
      UUID.randomUUID()
  }

  val result = lockingService.withLocks(Set("1", "2", "3")) {
    val innerResult1 = lockingService.withLocks(Set("3", "4", "5")) {
      Success("this is never evaluated")
    }
    println(innerResult1)

    val innerResult2 = lockingService.withLocks(Set("4", "5")) {
      Success("this will be evaluated")
    }
    println(innerResult2)

    Success("inside the top-level callback")
  }
  println(result)
}
