---
layout: post
title: Finding the app/process that's using Secure Input
summary: A Python script that shows me the name of processes that have Secure Input enabled.
tags: macos
---

macOS has a security feature called [*"Secure Input"*][sec_input].
If the OS detects that you're typing something sensitive, like a password, Secure Input will prevent anything but the frontmost application from reading your keystrokes – even apps that you've explicitly allowed to do so (for example, text expansion utilities).

Normally this is completely seamless, but sometimes it goes wrong.
If an app doesn't disable Secure Input, or macOS doesn't notice that you've switched to a different window, then other apps will continue to be unable to read your keystrokes.
This means that, for example, apps like TextExpander and Keyboard Maestro stop working.

I rely on that sort of tool, so when Secure Input breaks, I want to find the app or process that's keeping it enabled, and I want to find it quickly.
I've written a script that finds the offending processes, so I can decide how to handle them.
Here's how it works:

```console
$ find_processes_using_secure_input
The following processes are using Secure Input:
  113 loginwindow
  302 Safari
14482 iTerm2
```

You can [download the script][script] if you'd find it useful.

It's based on some commands [from the Keyboard Maestro forum][forums].
My script does a bit of work to find the process info automatically, rather than me looking through command output by hand.

The script relies on two shell commands:

*   `ioreg -a -l -w 0`

    This prints a load of information about the "I/O Kit Registry".
    I don't know what I/O Kit does, but I assume it's responsible for keyboard input (among other things).
    You can find a process using Secure Input by looking for the `kCGSSessionSecureInputPID` key.

    I've added the `-a` flag, which outputs the data as XML.
    This is easier to parse programmatically -- command-line tools often have a flag or switch for machine-readable output, and it's worth looking for one before reaching for regular expressions or the like.

    By traversing this XML, my script can find all the processes that have the special SecureInputPID key.

*   `ps -c -o pid=,command= -p <pid1>,<pid2>,...`

    This prints the executable name associated with the given process IDs (pids).

    The `-c` flag gets the executable name rather than the full terminal command.
    The `-o pid=,command=` prints just the pid and command (normally `ps` prints a table with headings, but I omit those).
    The `-p` flag restricts it to the given list of process IDs.

    By calling this with the PIDs I got from the `ioreg` output, I can see the names of the offending processes.

Here's how you can test the script:

> 1.  In a Terminal window, run
>
>     ```
>     python -c 'import getpass; getpass.getpass()'
>     ```
>
>     This will open a secure password prompt, and Terminal will enable Secure Input.
>
> 2.  Switch to another Terminal window, and run
>
>     ```
>     sleep 5; find_processes_using_secure_input
>     ```
>
> 3.  Switch back to the first window, where the password prompt is still waiting.
>
> You should see "Terminal" in the list of processes that have Secure Input enabled (but only when the password prompt is the frontmost window).

My script doesn't stop the offending processes, and I don't want it to.
I'll decide how to deal with them -- but only once I know which process is the problem.
In particular, the `loginwindow` process is a common culprit, and stopping that automatically would immediately log me out.

The script is a useful debugging tool that helps me identify the problem, un-break Keyboard Maestro, and get back to whatever I was actually doing.
Packaging it in a command I can easily remember (or guess and use autocomplete) is the icing on the cake.

[sec_input]: https://security.stackexchange.com/a/47786/9814
[script]: /files/2021/find_processes_using_secure_input
[forums]: https://forum.keyboardmaestro.com/t/disable-secure-input/2410/4
