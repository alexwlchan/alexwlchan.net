---
layout: note
title: Use `systemctl is-active` to determine if a service is running
date: 2026-02-05 16:25:19 +00:00
topic: Shell scripting
---
At work, we have some Linux VMs with services managed by `systemctl`.

If I want to check if a service is running, I can use `systemctl status`:

```console
$ systemctl status ssh
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2025-10-23 00:35:20 UTC; 3 months 14 days ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 451 (sshd)
      Tasks: 1 (limit: 37867)
     Memory: 4.6M
        CPU: 452ms
     CGroup: /system.slice/ssh.service
             └─451 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

If I want to automate the process of checking whether a service is running, I can use the [`is-active` subcommand][systemctl-is-active].
For example:

```console
$ systemctl is-active ssh
active
```

This returns exit code 0 if the service is `active`, and non-zero otherwise.
Adding `--quiet` will suppress the output.

This allows me to write shell scripts like:

```bash
if systemctl is-active --quiet ssh
then
    echo "SSH is running"
else
    echo "SSH is not running"
fi
```

I'm using this in some scripts to ensure they don't run while the service is running -- I can check for `is-active`, and block further execution until the service is stopped.

References:

*   [Stephen Kitt's answer on Unix Stack Exchange](https://unix.stackexchange.com/a/396638)
*   [systemctl manpage](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)

[systemctl-is-active]: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#is-active%20PATTERN%E2%80%A6
