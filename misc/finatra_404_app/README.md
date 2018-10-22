# README

Build the Docker image:

```console
$ docker build --tag finatra_404_app .
```

Run the image:

```console
$ docker run --volume $(pwd):/code --publish 8888:8888 finatra_404_app sbt run
```

Hit the two endpoints:

```console
$ curl http://localhost:8888/healthcheck
{"status": "ok"}

$ curl http://localhost:8888/foo/bar
{"status":404,"description":"Page not found for URL /foo/bar"}
```
