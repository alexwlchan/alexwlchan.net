---
layout: page
title: Projects help
breadcrumb:
  - label: Projects
    href: /projects/
---
These are some personal notes on how I manage the Git repos I publish on `/projects/`.
These probably aren't useful for you directly, but maybe it'll be interesting to see how I use Git.

## Where do repos live?

The canonical copy of my repos is on `phaenna-mac-mini`, a Mac mini that lives on my desk.
Specifically, they live in `~/Media/repos`, where `~/Media` is a symlink to an external drive.

The repos published on this site live on `linode-vps`, a web server hosted by Linode.
Specifically, they live in `~/repos`.

## Cloning a repo

If I'm on Phaenna, run the following commands (this uses the fish shell):

```console
$ set repo_name chives
$ git clone ~/Media/repos/$repo_name $repo_name
Cloning into 'chives'...
done.
$ cd $repo_name
$ git remote set-url --add --push origin linode-vps:repos/$repo_name
$ git remote -v
origin	/Users/alexwlchan/Media/repos/chives (fetch)
origin	linode-vps:repos/chives (push)
```

This means pulls will come from `phaenna-mac-mini`, and pushes will be mirrored to `linode-vps`.

If I'm on a different Mac:

```console
$ set repo_name chives
$ git clone phaenna-mac-mini:Media/repos/$repo_name $repo_name
Cloning into 'chives'...
done.
$ cd $repo_name
$ git remote set-url --add --push origin linode-vps:repos/$repo_name
$ git remote -v
origin	phaenna-mac-mini:Media/repos/chives (fetch)
origin	linode-vps:repos/chives (push)
```

## Setting up a new/existing repo

1.  Create a bare repo on my Mac mini:

    ```console
    phaenna-mac-mini:~ $ cd ~/Media/repos
    phaenna-mac-mini:~/Media/repos $ git init --bare chives
    ```

2.  Create a bare repo on Linode:

    ```console {"wrap":true}
    linode-vps:~ $ cd ~/repos
    linode-vps:~/repos $ git init --bare --initial-branch=main chives
    ```

3.  Set the remotes in my working directory:

    ```console {"wrap":true}
    $ git remote set-url origin ~/Media/repos/chives/
    $ git remote set-url --add --push origin linode-vps:repos/chives
    ```

4.  Push the existing data:

    ```console {"wrap":true}
    $ git push origin main --tags
    ```
