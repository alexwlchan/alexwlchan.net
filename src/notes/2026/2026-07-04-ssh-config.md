---
layout: note
date: 2026-07-04 23:39:17 +01:00
title: Always-on SSH agent forwarding with my Git pushes
summary: If I want to use `ssh -A` every time I do a Git push, I need to add the remote host to my `~/.ssh/config`.
topic: Git
---
All the words and code for this website are in a Git repo.
The canonical copy of the repo is a bare repository on my Mac mini, which has a post-receive hook that builds a copy of the site and uploads the files to my web server.

If I'm working on my Mac mini, this works fine -- the SSH key for the web server is in my local keychain, so when I push the post-receive hook can upload to the web server.

If I'm working on my laptop, I need some extra config -- when I push to the Mac mini, the post-receive hook can't get the SSH key from the Mac mini's keychain, and publishing to the web server fails.

I've fixed this by adding an entry to `~/.ssh/config` on my laptop:

```
Host phaenna-mac-mini
    HostName phaenna-mac-mini
    User alexwlchan
    ForwardAgent yes
```

This tells my laptop that any time it opens an SSH connection to `phaenna-mac-mini`, it should use SSH agent forwarding.
(The equivalent of running `ssh -A` for a manual connection.)

This means my laptop's SSH keys get forwarded to the Mac mini, and they're available to the post-receive hook.
My laptop can SSH to my web server, so the forwarded keys allow the post-receive hook to publish correctly.

This config includes any SSH connection, including those created by Git.
I thought maybe I'd need config in every repo, but the global SSH config file seems to be enough.
