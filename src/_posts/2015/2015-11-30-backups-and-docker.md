---
date: 2015-11-30 22:39:00 +0000
layout: post
summary: The Docker folder on your computer can quickly fill up space. Don't forget
  to exclude it from backups.
tags: docker
title: Backups and Docker
---

I've spent a lot of time recently playing with [Docker](http://www.docker.com/).

I've been building lots of images and containers, and that starts to take up disk space.
Lots of disk space.
That's not much of a problem on a local system &ndash; space is cheap &ndash; but it becomes a problem with incremental backup programs like [Time Machine](https://en.wikipedia.org/wiki/Time_Machine_(OS_X)).
Suddenly I noticed backups were taking an order of magnitude longer, and backing up gigabytes at a time.
Oops.

Incremental backups of my Docker images aren't very useful, but they force out older snapshots of important data, and slow down my backups.
Wouldn't it be nice to cut that out?

<!-- summary -->

There are two folders than can swell with Docker images:

* On Linux, look at **/var/lib/docker** &ndash; this is where Docker keeps its internal state.

* On OS X or Windows, look at **~/.docker** &ndash; this includes any VMs you have for running Docker Machine. The VM images are stored as large binary blobs, so any changes require a completely new backup.

I'd recommend excluding both of those from your backups &ndash; and perhaps search indexes as well.
The exact contents of those folders probably isn't useful to most users; it's just a collection of binary files that Docker stitches together into something more meaningful.

If you do need to backup a particular image or container, Docker already has commands for saving images and containers to a file, which can be moved around and backed up as usual.
But these files are portable across computers, and take up far less space in backups.

*   The [`docker save`](http://docs.docker.com/engine/reference/commandline/save/) command can export an image to a tarfile.
    You can load the image on a new system with the `docker load` command:

    <!-- ```console
    $ docker save busybox > busybox.tar
    $ docker load < busybox.tar
    ``` -->

    <div class="codehilite"><pre><span></span><span class="gp">$</span> docker save busybox &gt; busybox.tar
    <span class="gp">$</span> docker load &lt; busybox.tar
    </pre></div>

*   The [`docker export`](http://docs.docker.com/engine/reference/commandline/export/) command saves the filesystem of a running container to a tarfile.
    You can restore it with `docker import`, which creates an empty container filesystem and then loads the contents of the export.

    <!-- ```console
    $ docker export awlc/red_mcclean > mycontainer.tar
    $ cat mycontainer.tar | docker import - awlc/red_mcclean:new
    ``` -->

    <div class="codehilite"><pre><span></span><span class="gp">$</span> docker <span class="nb">export</span> awlc/red_mcclean &gt; mycontainer.tar
    <span class="gp">$</span> cat mycontainer.tar <span class="p">|</span> docker import - awlc/red_mcclean:new
    </pre></div>

In practice, I rarely use these commands.
I usually have the Dockerfiles and/or Docker Hub to restore any images, and containers are supposed to be ephemeral.
If I have lots of stuff in a container that I want to keep, I've probably done something wrong.
