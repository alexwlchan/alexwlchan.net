import com.twitter.finagle.http.{Request, Response}
import com.twitter.finatra.http.{Controller, HttpServer}
import com.twitter.finatra.http.routing.HttpRouter


class CustomController() extends Controller {
  get("/healthcheck") { request: Request =>
    response.ok.json(Map("status" -> "ok"))
  }

  get("/:*") { request: Request =>
    response.notFound.json(Map(
      "status" -> 404,
      "description" -> s"Page not found for URL ${request.uri}"
    ))
  }
}


class Server extends HttpServer {
  override def configureHttp(router: HttpRouter) {
    router.add[CustomController]
  }
}


object ServerMain extends Server
