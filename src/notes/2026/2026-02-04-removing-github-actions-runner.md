---
layout: note
title: Removing a self-hosted runner from GitHub Actions
date: 2026-02-04 10:00:27 +00:00
topic: Builds and CI
---
My old book tracker was `books.alexwlchan.net`, which was built and published by a self-hosted GitHub Actions runner on my web server.
I wanted to remove the old runner when I deleted that site, so I went to **Settings** > **Actions** > **Runners** in the repository settings, which gave me a one-line command to run on my web server:

{%
  picture
  filename="gh-actions-remove-runner.png"
  width="600"
  class="screenshot"
  alt="A 'Remove runner' modal in the GitHub Actions settings. There's a command to remove the runner by running a 'config.sh' script on the runner."
%}

I tried running that command on my web server in `~/github-actions-runner/books.alexwlchan.net`, but it returned an error:

```console
$ ./config.sh remove --token AACJRJHJBR4LKTQMA62MCALJQMLI2

# Runner removal

Removing service
Failed: Removing service
Uninstall service first
```

Running the command with `sudo` didn't work either.
If you try, the script returns an error "Must not run with sudo".

A [issue on the actions/runner repo][gh-issue-1022] gave me the missing piece: I had to use the `svc.sh` script (which was already saved on my runner) to remove the service, then re-run the `config.sh` script.

```console
$ sudo ./svc.sh uninstall

/etc/systemd/system/actions.runner.alexwlchan-books.alexwlchan.net.harmonia.service
○ actions.runner.alexwlchan-books.alexwlchan.net.harmonia.service - GitHub Actions Runner (alexwlchan-books.alexwlchan.net.harmonia)
     Loaded: loaded (/etc/systemd/system/actions.runner.alexwlchan-books.alexwlchan.net.harmonia.service; enabled; preset: enabled)
     Active: inactive (dead) since Wed 2026-02-04 08:52:15 UTC; 22ms ago
   Duration: 5month 2w 22h 6min 23.096s
    Process: 662311 ExecStart=/home/alexwlchan/github-actions-runner/books.alexwlchan.net/runsvc.sh (code=exited, status=0/SUCCESS)
   Main PID: 662311 (code=exited, status=0/SUCCESS)
        CPU: 1h 46min 8.524s

Feb 04 08:52:14 harmonia.linode systemd[1]: Stopping actions.runner.alexwlch…...
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Shutting down runner listener
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Sending SIGINT to runner …top
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Sending SIGKILL to runner…ner
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Exiting...
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Runner listener exited wi…e 0
Feb 04 08:52:14 harmonia.linode runsvc.sh[662313]: Runner listener exit with…ed.
Feb 04 08:52:15 harmonia.linode systemd[1]: actions.runner.alexwlchan-books.…ly.
Feb 04 08:52:15 harmonia.linode systemd[1]: Stopped actions.runner.alexwlcha…a).
Feb 04 08:52:15 harmonia.linode systemd[1]: actions.runner.alexwlchan-books.…me.
Hint: Some lines were ellipsized, use -l to show in full.
Removed "/etc/systemd/system/multi-user.target.wants/actions.runner.alexwlchan-books.alexwlchan.net.harmonia.service".

$ ./config.sh remove --token AACJRJHJBR4LKTQMA62MCALJQMLI2

# Runner removal


√ Runner removed successfully
√ Removed .credentials
√ Removed .runner
```

[gh-issue-1022]: https://github.com/actions/runner/issues/1022#issuecomment-855813457
