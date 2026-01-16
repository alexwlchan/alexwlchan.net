---
layout: post
date: 2023-10-20 23:08:51 +00:00
title: Making the fish shell more forgetful
summary: A few commands that help me keep unwanted entries out of my shell’s autocomplete.
tags:
  - shell scripting
  - fish shell
colors:
  index_light: "#c85b05"
  index_dark:  "#ff9306"
---

{% comment %}
  Cover image from https://pixabay.com/photos/veil-tail-fish-goldfish-swim-11453/
{% endcomment %}

For quite a few years, I've been using fish (<https://fishshell.com/>) as my shell.

One of the cool things it does is autosuggestions from my shell history.
As I'm typing, it suggests (in light grey) a command I've run before.
I can press the right arrow to accept the suggestion, or I can keep typing to ignore it.

{%
  picture
  filename="fish_autosuggestion.png"
  width="500"
  class="screenshot"
  alt="Screenshot of my terminal, showing three commands. The first is 'mate src/_drafts/forgetful-fish.md' and the second is 'make html'. For the third command, I've typed 'mate', and it’s suggested the filename 'src/_drafts/forgetful-fish.md' based on my first command."
%}

This feature is pretty smart and very useful, and it's probably saved me thousands of keystrokes.
But a few times recently it's gone wrong, and suggested me something I didn't want -- so I've been tweaking my fish config to make it easier for fish to "forget" certain commands.

## What I don't want suggested

There are a couple of categories of command that I don't want fish to remember or suggest:

1.  **Typos and mistakes.**
    If I ever mistype a command and run it, that mistake will be used for future autosuggestions.
    Getting a command wrong once is annoying; having my mistake be continually suggested is worse.
    
    A while back I mistyped `hdiutil attach` as `hdiutil atach`, and I kept getting the wrong version as an autosuggestion.
    (That annoyance is what led to the code in this post!)

2.  **Sensitive information.**
    Sometimes I end up with sensitive information in my shell commands -- either by accident, or because it's the fastest way to fix a problem.
    I know I'm not meant to do that, but nobody's perfect.
    
    My fish shell history lives unencrypted in a file on disk, where anything could find it (`~/.local/share/fish/fish_history`).
    I'd rather not have passwords, keys, and other credentials living there forever.

3.  **Potentially dangerous commands.**
    My example of this is doing a Git force push, which can delete data if I'm not careful.
    It's the right thing to do sometimes, but I never want to start typing a regular Git push and get a force push as an autosuggestion.
    
    I never want to do a force push accidentally, and I'm willing to give up the benefits of autosuggestion for a bit of extra safety.

To help me avoid autosuggestion in these three cases, I've added two functions to my shell config.

## Function #1: forget the last command

This function removes the last-typed command from my history, which prevents it from being suggested again.
I run this manually, whenever I mistype a command or some other one-off thing I don't want to remember.

```shell
function forget_last_command
    set last_typed_command (history --max 1)
    history delete --exact --case-sensitive "$last_typed_command"
    history save
end
```

You can test this with the following steps:

1.  Run a command like `echo "my password is hunter2"`
2.  Type `echo` into your shell, and see that the previous command is suggested
3.  Cancel that command, and instead, run `forget_last_command`
4.  Start typing `echo` again, and notice that the first command is no longer suggested
5.  Open a new session, start typing `echo`, and check that the first command isn't suggested

The heavy lifting is done by fish's [`history` command][history] -- first it looks up the last command I typed, then it removes that from the history, and finally it persists that change to disk.

(I'm not entirely sure the `history save` should be necessary, but with fish 3.6.1 -- the latest version -- it is required for this to work.
I think there's something [slightly funky][bug_10066] about `history delete --exact`, which made this maddening to debug until I started following my [`fish_history` file][file].)

[history]: https://fishshell.com/docs/current/cmds/history.html
[bug_10066]: https://github.com/fish-shell/fish-shell/issues/10066
[file]: https://fishshell.com/docs/current/cmds/history.html#customizing-the-name-of-the-history-file

## Function #2: never remember certain commands

Forgetting a command on a one-off basis is good for typos and accidental passwords, but what about commands I use on a semi-regular basis?
It'd be annoying if I had to type `forget_last_command` every time I ran `git push --force`.

This function looks at my last command, and if it's dangerous, it removes it from my history.
Crucially, this runs as part of my shell prompt, so it runs as soon as a command completes -- I don't need to remember to forget:

```shell
function forget_dangerous_history_commands
    set last_typed_command (history --max 1)

    if [ "$last_typed_command" = "git push origin (gcb) --force" ]
        history delete --exact --case-sensitive "$last_typed_command"
        history save
    end
end
```

You can test this with the following steps:

1.  Switch to a Git repository where it's safe to force push
2.  Run the command `git push origin (gcb) --force` (here `gcb` is an alias for `git rev-parse --abbrev-ref HEAD`, which prints the name of the currently checked-out branch)
3.  Start typing `git push` again, and notice that the force push isn't suggested

A force push is the only example of a dangerous command that I use regularly, but there could be others – anything involving `rm -rf`, for example.
If I ever find myself doing something dangerous that I never want suggested, it should be pretty easy to extend this function.
