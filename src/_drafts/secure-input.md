---
layout: post
title: Finding the app/process that's using Secure Input
summary: A Python script that shows me the name of processes that have Secure Input enabled.
tags: macos
---

macOS has a security feature called *"Secure Input"*.
If the OS detects that you're typing something sensitive, like a password, Secure Input prevents anything but the frontmost application from reading your keystrokes – even apps that you've explicitly allowed to do so (for example, text expansion utilities).
You can read more about Secure Input in [Apple's developer docs][tn2150].

Normally this is completely seamless, but sometimes it goes wrong.
If an app doesn't disable Secure Input, or macOS doesn't notice that you've switched to a different app, then other apps will continue to be unable to read your keystrokes.
This means that, for example, apps like TextExpander and Keyboard Maestro stop working.

I rely on Keyboard Maestro, so when this happens, I want to find the app or process that's keeping Secure Input enabled.
I've written a script that tries to find the offending processes, so I can stop or restart them as necessary.
Here's what it looks like:

```console
$ find_apps_using_secure_input
The following processes are using Secure Input:
  113 loginwindow
  302 Safari
14482 iTerm2
```

You can [download the script][script] if you'd find it useful.

It's based on some commands I found [in the Keyboard Maestro forums][forums].
My script does a bit more work to find the process ID and name, rather than having me look for it by hand.

The script relies on two commands:

*   `ioreg -a -l -w 0`

    This prints a load of information about the "I/O Kit Registry".
    I don't know what I/O Kit does, but I assume it's responsible for keyboard input (among other things).
    You can find a process using Secure Input by looking for the `kCGSSessionSecureInputPID` key.

    I've added the `-a` flag, which formats the data as XML.
    This is easier to parse programmatically -- command-line tools often have a flag or switch for machine-readable output, and it's worth looking for one before reaching for tools like grep or awk.

*   `ps -c -o command= -p <pid>`

    This prints the executable name associated with a given process ID (pid).

    The `-c` flag gets the executable name rather than the full terminal command, and `-o command=` prints just the command with no headers.
    The `-p` flag restricts it to a set of given process IDs.

Here's how you can test this script:

> 1.  Run `python -c 'import getpass; getpass.getpass()'` in a Terminal window.
>
>     This will open a secure password prompt, and Terminal will enable Secure Input.
>
> 2.  Switch to another window, and run `sleep 5; find_apps_using_secure_input`.
>
> 3.  Switch back to the first window, where the password prompt is still waiting.
>
> You should see "Terminal" in the list of processes that have Secure Input enabled (but only when the password prompt is the frontmost window).

This script doesn't stop the offending processes, and I don't want to.
The `loginwindow` process is a common culprit, but stopping that automatically would immediately log me out.

The script is a useful debugging tool it helps me identify the problem, and get back to whatever I was actually doing.
Packaging it in a command I can easily remember (or guess and use autocomplete) is the icing on the cake.

[tn2150]: https://developer.apple.com/library/archive/technotes/tn2150/_index.html
[script]: /files/2021/find_apps_using_secure_input
[forums]: https://forum.keyboardmaestro.com/t/disable-secure-input/2410/4
