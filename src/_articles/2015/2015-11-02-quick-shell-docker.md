---
layout: article
date: 2015-11-02 22:07:00 +00:00
summary: A Bash function for quickly getting shell access to Docker containers.
title: Quick shell access for Docker containers
topics:
  - Docker
  - Shell scripting
---

In the last few weeks, I've been spending a lot of time working with Docker containers.
When developing containers, I often need to get shell access to the container, so that I can inspect its contents.
This is a two-step process:

1. Look up the container ID with `docker ps`.
2. Shell into the container with `docker exec -it <container ID> sh`.

That's fine, but wouldn't it be nice if we could cut out the first step?
It's only short, but it gets tedious if you're doing it regularly &ndash; this is the sort of boring task that we can solve with scripting.

Most of the time, I'm shelling into my most recently started container.
So I wrote this short function, and put it in my bash_profile:

<pre class="lng-bash"><code>function <span class="n">docker-sh</span> <span class="p">{</span>
    if [[ $# -eq <span class="m">0</span> ]]<span class="p">;</span> then
        docker exec -it $(docker ps -l -q) sh
    else
        docker exec -it $1 sh
    fi
<span class="p">}</span></code></pre>

If I invoke it without any arguments, it will shell into my most recent container:

```console
$ docker-sh
```

But on the rare occasions I have another container in mind, I can specify it as an alternative, by supplying it as the first argument:

```console
$ docker-sh 8d8122c10f60
```