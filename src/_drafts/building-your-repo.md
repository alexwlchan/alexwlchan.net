---
layout: post
title: Your repo should be easy to build, and how
tags: make docker, software-development
---

Whenever I look at a new repository, I have a simple smell test: *how long does it take me to clone, build and get the code running?*

Here, I'm usually counting the steps I have to do, the commands I have to run.
The clock time is less important (although fast builds are still nice!).
Ideally, there's a single command which takes me from a fresh checkout to a clean build --- and without me having to fiddle with dependencies first.

Once I have a working build, I can start fiddling with code and find my own way around.
Getting that first build is key.

Making it easy to do a fresh build has a number of benefits.

The obvious one is speed --- I run one command, then I can walk away while the computer does all the slow bits.
Downloading dependencies, compiling code, setting up the local environment, that sort of thing.
It might take a while to finish, but I don't need to supervise it while that happens.
I can spend that time doing something more useful.

It's also simpler.
Remembering "make build" is easy.
Remembering six calls to different shell scripts, the different arguments, and how it all fits together, is much harder.
If the build is simple, there's less to get wrong, and it's more likely I'll get it right first time.
Automating the build process makes it more reliably.

And finally, first impressions count!
Being able to start working quickly is a pleasant experience.
If writing and testing my first patch is easy, I'm more likely to do it a second time.
And a third.
And so on.
Particularly in open source repos where patches come from people giving up their time for free, it's good to spend as little of it as possible.

In the last year, I've spent a lot of time simplifying my build systems, both in my work and my personal repos.
Most of my current repos now have a single-step build process.
It's not perfect, but I'm very pleased with the results.

In this post, I'll explain my typical setup, and how I use Make and Docker to get fast and simple builds.

<!-- summary -->

{% tweet https://twitter.com/alexwlchan/status/938694360681590791 %}

I really felt the benefits on Monday.
Normally I commute to London on the train, but there was snow and ice at the weekend, and cold weather wreaks havoc on the railways.
I decided to work from home, rather than sit on a train that would probably be delayed or cancelled.

Because I wasn’t expecting to work from home when I left on Friday, I'd left my work laptop in the office.
And even worse, I recently had to reinstall my home computer, so I didn’t have any of my existing setup.

Not to worry: all our projects [are on GitHub][github], open-source and under an MIT license (so working on a personal computer doesn't cause legal issues) --- I could easily get the code.
We run all our dev processes in [Docker containers][docker], so I didn't need to install any dependencies.
Then we use [Make][make] to manage Docker itself: building the relevant containers, keeping them up-to-date, and running the test commands.

So after I'd cloned the repo, I could run my tests with just one command:

```console
$ make api-test
```

followed by fifteen minutes of dependencies compiling in the background, which I could spend catching up on email.
When I came back, the code had compiled, the tests run, and I was ready to start work.

Other projects I’ve worked on took much longer to get set up.
At a past job, the instructions for your first build ran to two sides of A4 (!).
Tweaking compiler flags, laying out submodules, getting my network settings ~just so – I’d been working for a fortnight before I saw “build: ok”.

If I had to go through something like that, I'd have wasted the whole day.
Instead, I was back up-and-running in less than half an hour.

[github]: https://github.com/wellcometrust/platform
[docker]: https://en.wikipedia.org/wiki/Docker_(software)
[make]: https://en.wikipedia.org/wiki/Make_(software)

## How to set up Make and Docker for one-step builds

Let's start without Make or Docker.
Our API Our API is a Scala application, with tests and builds managed by a build tool called [sbt][sbt].
If you have the right versions of sbt and Scala installed, you run our tests with the command:

```console
$ sbt "project api" ";dockerComposeUp;test;dockerComposeStop"
```

Did I mention you need to install docker-compose as well?
We use some mock AWS services in our tests, which are Docker containers orchestrated by docker-compose.

### My first Makefile

The first thing we can do is write a Makefile, and a Make rule that wraps this command:

```make
# Makefile

api-test:
    sbt "project api" ";dockerComposeUp;test;dockerComposeStop"
```

Now we can run `make api-test`, and that has the same effect as running the sbt command, but we've hidden the details behind a human-friendly name.

You don't have to remember the sbt command, just *api-test*.
Tests for our other applications have a similar naming scheme: *transformer-test*, *loris-test*, *ingestor-test*, and so on --- you don't have to worry exactly how to run sbt, or even if those tests use sbt at all!
And if the test command ever changes, you only have to edit the Makefile once, and everybody picks up the change.

If you already know how Make works, you can skip to the next section.
If you're unfamiliar with Make, there's a quick primer below.

```make
target: [dependency dependency ...]
    [command 1]
    ...
    [command n]
```

A Makefile is a series of *rules*.
Each rule starts with a *dependency line*, with a *target* before the colon, and a list of *dependencies* after the colon.
In the example above, the target is `api-test`, and there are no dependencies (we'll come back to those later).
Usually the target is the name of the file you want to create, but a rule doesn't have to create a file --- there's no output from running tests, for example.

Each dependency line is followed by a series of tab-indented *commands* which need to be run to build this target (and the indents have to be tabs, not spaces).
In the first example, the rule has a single command: the sbt call that runs the API tests.

Here's what happens when you run `make <target>`:

*   Make looks to see if the target already exists.

    *   If the target already exists, it looks at the modified dates: is the target newer than all of the dependencies?
        If so, it's already up-to-date, and there's nothing to do.
        If not, the target is out-of-date, and needs to rebuilt.

    *   If it doesn't exist, it needs to be built from scratch.

*   If the target needs to be built, it runs the commands in sequence.
    If any of the commands fail (have a non-zero exit code), the build has failed and make will error out.

We'll see some more complicated examples in the rest of the post.
Check you understand what they're doing.

### Pushing it inside Docker

If I want to run these tests, I need to install Scala, sbt, and docker-compose on my local machine.
I'd better hope they're available in my package manager, and I can install them easily, and they don't break something else I've installed... yuck.

This is precisely the sort of problem that can be solved with Docker.
Rather than installing dependencies on our main machine, we can install them in a Docker image, and run them our tests there.
It runs in a pristine, reproducible environment, and the installation process can be entirely automated.

We can write a Dockerfile for installing our dependencies:

```dockerfile
# sbt_wrapper.Dockerfile

FROM pvansia/scala-sbt:0.13.13

RUN apk update && apk add docker py-pip
RUN pip install docker-compose

WORKDIR /repo

ENTRYPOINT ["sbt"]
```

This file defines a new Docker image:

*   It starts from an existing image that has sbt and Scala involved
*   Then it runs apk and pip (package managers for Alpine Linux and Python, respectively) to install our extra dependencies
*   It sets a working directory
*   It prepares to run `sbt` when we run this container
    Any arguments we put on the end of `docker run` will be passed to sbt

The [Dockerfile reference][dockerfile] explains the syntax in much more detail.

We can build this image with `docker build`, which we'll wrap inside a Make rule:

```make
build-sbt-docker-image:
    docker build --tag sbt_wrapper --file sbt_wrapper.Dockerfile .
```

And then we can modify our first Make rule to use the Docker image:

```make
api-test:
    docker run \
        --volume $$(pwd):/repo \
        --volume /var/run/docker.sock:/var/run/docker.sock \
        --net host \
        sbt_wrapper "project api" ";dockerComposeUp;test;dockerComposeStop"
```

The extra flags on `docker run`:

*   Share our current directory into the container, so it has all our code
*   Share the Docker socket with the container, so processes inside the container can run Docker commands on the host (your machine)
*   Share the host network with the container, so it can see the new Docker containers it starts
*   Finally, the name of the image, and the two arguments are passed through to `sbt`.

So now we have to build the image, then run the tests:

```console
$ make build-sbt-docker-image
$ make api-test
```

We're improving: Docker means minimal dependencies are required on the host, the installation is automated, and we still hve human-friendly ways to run our tasks.
But we have to remember to build the Docker image first, or it won't work.
Can we automate that as well?

[dockerfile]: https://docs.docker.com/engine/reference/builder/

### Make dependency management, take 1

Remember that Make allows us to declare dependencies for a rule.
If we add dependencies after the colon, Make will try to build those first before it builds the main target.

So we can tell Make that *api-test* depends on *build-sbt-docker-image* like so:

```make
api-test: build-sbt-docker-image
    ...
```

And we're back to running:

```console
$ make api-test
```

When you run that command, Make will build a Docker image, install its dependencies, then run your tests inside the image.
Hooray!

So we're done… right?

### Make dependency management, part 2

If you try this out, you'll find that Make rebuilds your Docker image every time you run your tests.
Because Make never sees a file called *build-sbt-docker-image*, it assumes it has to rebuild it, and re-runs the rule.
Docker caching means the rebuild is fairly fast on subsequent runs, but it still clutters up your console with logs.
Could we do better?

We need Make to know when we've built the Docker image, so let's modify the Make rule to drop a marker after it's build the image.
The next time Make runs, it'll see the marker, know the image has already been built, and skip rebuilding it.

This is the pattern I typically use:

```make
.docker/sbt_wrapper: sbt_wrapper.Dockerfile
    docker build --tag sbt_wrapper --file sbt_wrapper.Dockerfile .
    mkdir -p .docker
    touch .docker/sbt_wrapper

api-test: .docker/sbt_wrapper
    ...
```

(Notice that I've also added a dependency on the Dockerfile, so if the Dockerfile does change, we'll get a one-off rebuild.)

The whole `.docker` directory is gitignored, and it serves as a collection of markers for Docker images.

This pattern makes a small difference to build times, but a big difference to console noise.

## Putting this into practice

I've been using this system for about half a year, and it's worked remarkably well.
I have one-step rebuilds, human-friendly names for my build process, and a really mature and powerful dependency management system.
You can see some examples in the [platform repo's Makefiles][platform], or the Makefile [for this blog][blog].

If you're looking for a way to simplify or improve your build processes, I'd really encourage giving these technique a look.

[platform]: https://github.com/wellcometrust/platform/blob/master/Makefile
[blog]: https://github.com/alexwlchan/alexwlchan.net/blob/master/Makefile
