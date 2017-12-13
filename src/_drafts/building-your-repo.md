---
layout: post
title: Your repo should be easy to build, and how
tags: make docker, software-development
---

Whenever I look at a new repository, I have a simple smell test: *how long does it take me to clone, build and get the code running?*

Here, I'm usually counting the steps I have to do; the clock time is less important (although fast builds are still nice!).
Ideally, there's a simple command (say, *make build*) which takes me from a fresh checkout to a clean build --- and without me having to fiddle with dependencies first.

Once I have a working build, I can start fiddling with code and find my way around.
That first build is key.

Making it easy to do a fresh build has a number of benefits.

The obvious one is speed --- I run one command, then I can walk away while the computer fetches dependencies/compiles code/sets up the local environment.
It might take a while to finish, but I don't have to be supervising the build.
I can spend that time doing something more useful.

It's also simpler.
Remembering "make build" is easy.
Remembering six calls to different shell scripts, the different arguments, and how it all fits together, is much harder.
If the build is simple, there's less to get wrong, and it's more likely I'll get it right first time.

Automation also means reliability.

and first impressions count!

In the last year, I've spent a lot of time simplifying my build systems, both in my work and my personal repos.
It's not perfect, but I'm very pleased with the results.

---

> First and foremost, clone and build it. If you cannot clone, build and get it running within an hour, it's generally crap and not worth your time[0].
Once you get it building and running, you can now start making simple changes in order to find your way around.
[0] Developers should pride themselves on how (relatively)simple this process is for their project(s).

---

https://twitter.com/alexwlchan/status/938694360681590791

I really felt this on Monday.
There was an unusual amount of snow and ice at the weekend, and I found myself working from home.
I normally commute to London by train, but this weather wreaks havoc on the railways.
If I even reached the office, I'd be late and cold.

Because I wasn’t expecting to work from home when I left on Friday, I’d left my work laptop in the office.
And even worse, I’ve just reinstalled my home computer, so I didn’t have any of my existing setup.

Not to worry: all our projects [are on GitHub][github], open-source and under an MIT license (so working on a personal computer doesn't cause legal issues) --- I could easily get the code.
We run all our dev processes in Docker containers, so I didn't need to install any dependencies.
Then we have make to manage Docker itself: building the relevant containers, keeping them up-to-date, and running my test commands.

So after I'd cloned the repo, I could run my tests with one command:

```console
$ make api-test
```

followed by fifteen minutes of dependencies compiling in the background, which I could spend catching up on email.

Other projects I’ve worked on took much longer to get set up.
At a past job, the instructions for your first build ran to two sides of A4 (!).
Tweaking compiler flags, laying out submodules, getting my network settings ~just so – I’d been working for a fortnight before I saw “build: ok”.

If I had to go through that again, I'd have wasted the whole day.
Instead, I was back up-and-running in less than half an hour.

In the rest of this post, I’ll explain how it all works.

[github]: https://github.com/wellcometrust/platform

---

Let's start by dissecting that command.

Our API is a Scala application, with tests and builds managed by a build tool [called sbt][sbt].
If you have the right versions of sbt and Scala installed, that make command is equivalent to running:

```console
$ sbt "project api" "dockerComposeUp;test;dockerComposeStop"
```

(Did I mention you need to install docker-compose as well?
We run a couple of mock AWS services in Docker containers, configured with docker-compose.)

The first thing we can do is write a make task that wraps this command:

```make
api-test:
    sbt "project api" "dockerComposeUp;test;dockerComposeStop"
```

This masks the individual complexities of this command on a day-to-day basis.
Rather than remember this moderately detailed sbt command, I just have to remember the task name: *api-test*.
Tests for our other applications have a similar naming scheme: *transformer-test*, *loris-test*, *id_minter-test*, and so on --- so I don't have to worry exactly how to run sbt, or even if they use sbt at all!

But I still need to install Scala, sbt and docker-compose on my local machine.
The next step is to push the dependencies into a Docker container.
We have [a Dockerfile][dockerfiles] that wraps these dependencies:

```dockerfile
# sbt_wrapper.Dockerfile

FROM pvansia/scala-sbt:0.13.13

RUN apk update && apk add docker py-pip
RUN pip install docker-compose

VOLUME /repo
WORKDIR /repo

ENTRYPOINT ["sbt"]
```

and we can write a make task that builds this image:

```make
build-sbt-docker-image:
    docker build --tag sbt_wrapper --file sbt_wrapper.Dockerfile .

api-test:
    docker run \
        --volume $$(pwd):/repo \
        --volume /var/run/docker.sock:/var/run/docker.sock \
        --net host \
        sbt_wrapper "project api" "dockerComposeUp;test;dockerComposeStop"
```

The extra flags on the `docker run` command share the repo into the container, share the Docker socket (so processes inside the container can issue Docker commands), and expose the host network into the container (so our mock containers are accessible).

We're improving: Docker means minimal dependencies are required on the host, and make gives us human-friendly ways to invoke the tasks.
But we have to remember to build the Docker image before we run the tests, or it won't work.
Could we have the computer do it automatically?

Yes!
An important feature of make is dependency tracking: you can tell make that one file depends on another.
We can tell it that *api-test* depends on *build-sbt-docker-image* with the following syntax:

```make
api-test: build-sbt-docker-image
    ...
```

And now, if you run *make api-test*, it will start by running *make build-sbt-docker-image* first --- so a single command builds the Docker image and runs the test.
Hooray!

So we're done... right?

There's one more step.
The dependency tracking in make is really built around files.
A target is the name of the file that it creates, and then inspecting the modified date on the files can tell make when it needs to rebuild.
Because it never sees a file called *build-sbt-docker-image*, it assumes it needs to rebuild the Docker image each time.
This doesn't take long, but it's mildly annoying and clutters up the console.

So we have make drop a marker for us, which tells it when it last rebuilt the container.
Like so:

```make
.docker/sbt_wrapper: sbt_wrapper.Dockerfile
    docker build --tag sbt_wrapper --file sbt_wrapper.Dockerfile .
    mkdir -p .docker
    touch .docker/sbt_wrapper

api-test: .docker/sbt_wrapper
    ...
```

So when make has built the container, it puts an empty file in the `.docker` repo.
As long as the Dockerfile is older than that file, it won't rebuild the container --- and subsequent runs of *api-test* will skip straight to the tests.
The whole `.docker` directory is gitignored, so this just tracks the images we've built locally.

We've been running with this system for a number of months, and it's worked remarkably well.
We get one-step rebuilds, human-friendly names for our build processes, and a really mature and powerful dependency management system.

Sometimes, the old ways are still the best.

[sbt]: https://en.wikipedia.org/wiki/Sbt_(software)
[dockerfiles]: https://github.com/wellcometrust/dockerfiles/blob/master/sbt_wrapper/Dockerfile
