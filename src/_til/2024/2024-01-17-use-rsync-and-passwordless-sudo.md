---
layout: til
title: How to move files when you need sudo on the remote server
date: 2024-01-17 10:54:23 +00:00
tags:
  - rsync
---
I wanted to upload some files to an EC2 instance.

I had an SSH key for the `ec2-user` on the instance, but I wanted to upload files to a directory that the `ec2-user` didn't have permissions to write to.
It could write to them using passwordless `sudo`, but not by default.

Steps:

1.  Try to upload the file with no authentication, it fails because of no SSH key:

    ```console
    $ rsync nginx.conf ec2-user@1.2.3.4:/etc/nginx/nginx.conf
    ec2-user@1.2.3.4: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
    rsync: connection unexpectedly closed (0 bytes received so far) [sender]
    ```

2.  Add the `--rsh` flag to specify an SSH key to use.
    Now it can connect to the remote server, but the remote server's filesystem permissions prevent the write:

    ```console
    $ rsync --rsh "ssh -i ~/.ssh/my_ssh_key" nginx.conf ec2-user@1.2.3.4:/etc/nginx/nginx.conf
    rsync: [receiver] mkstemp "/etc/nginx/.nginx.conf.NkcrAs" failed: Permission denied (13)
    ```

3.  Add the `--rsync-path` flag to specify what rsync command to run on the remote server.
    By prefixing this with `sudo`, we can now write into the directory:

    ```console
    $ rsync --rsync-path="sudo rsync" --rsh "ssh -i ~/.ssh/my_ssh_key" nginx.conf ec2-user@1.2.3.4:/etc/nginx/nginx.conf
    ```
