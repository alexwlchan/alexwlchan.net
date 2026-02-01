---
layout: post
date: 2023-05-30 19:41:48 +00:00
title: Starting Docker just before I need it
summary: I don’t keep Docker running all the time, but intercepting the `docker` command means it’s always running when I need it.
tags:
  - docker
  - shell scripting
colors:
  index_light: "#3a5781"
  index_dark:  "#cfe7f7"
  css_light:   "#3a5781"
  css_dark:    "#cfe7f7"
card_attribution: by Todd Cravens, https://unsplash.com/photos/QnBrjY-nFUs
---

Although I use Docker a lot, I don't leave it running all the time -- it can be quite a resource hog, and even if it's doing nothing it can make my laptop feel sluggish.
I'll often stop if it my computer feels slow, which is great right until the next time I need to use it:

```console
$ docker run -it alpine
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
```

After grumbling a few words of frustration, I start Docker, wait to see the whale icon appear in my menu bar, and then I re-run whatever it was I was trying to do in the first place.
It's not a big deal, but it is a slight interruption to my workflow.
It's a mild annoyance.

Recently, I wrote a small script to fix it.
The scripts intercepts any calls to the `docker` CLI, and checks to see if Docker is running.
If it is, the script forwards my command to the already-running Docker.
If it isn't, the script starts Docker and waits until it's ready before forwarding my command.

This is [the script], which I've named `docker` and put before the real Docker CLI in my PATH:

```bash
#!/usr/bin/env bash

set -o errexit
set -o nounset

is_docker_running() {
  if /usr/local/bin/docker info > /dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

if ! is_docker_running; then
  echo "Starting Docker..."
  open /Applications/Docker.app

  for i in $(seq 60)
  do
    if is_docker_running; then
      break
    fi
    sleep 1
  done
fi

/usr/local/bin/docker "$@"
```

It checks whether Docker is running with the `docker info` command, which returns a non-zero exit status if Docker isn't running.

If Docker isn't running, it prints `Starting Docker...` and then starts Docker.
The printing is just a clue to me that it might take a bit longer than normal -- usually a few extra seconds.
Then it runs in a loop waiting to see if Docker has finished starting, and exits when it's ready.

Once Docker is running, it passes all the arguments I passed to the script to the underlying CLI using `$@`, which is a [special Bash variable][dollar_at] containing all the positional arguments.

This is one of those scripts that seems super obvious in retrospect, and even if it doesn't save me much time, it's already saved plenty of frustration.
If I try to use Docker and it's not running, why can't the computer do the obvious thing and start Docker for me?!
With this script, it can.

[paper cut]: https://en.wikipedia.org/wiki/Paper_cut_bug
[dollar_at]: https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html#index-_0024_0040
[the script]: https://github.com/alexwlchan/scripts/blob/main/docker/docker
