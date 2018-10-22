import com.twitter.finagle.http.{Request, Response}
import com.twitter.finatra.http.{Controller, HttpServer}
import com.twitter.finatra.http.routing.HttpRouter


class CustomController() extends Controller {
  get("/greeting") { request: Request =>
    response.ok.json(Map("hello" -> "world"))
  }

  get("/:*") { request: Request =>
    response.notFound.json(Map(
      "error" -> s"page not found: ${request.uri}"
    ))
  }
}


class Server extends HttpServer {
  override def configureHttp(router: HttpRouter) {
    router.add[CustomController]
  }
}


object ServerMain extends Server
