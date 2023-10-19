---
layout: post
title: Making the fish shell more forgetful
summary: A few commands that help me keep unwanted entries out of my shell’s autocomplete.
tags:
  - shell-scripting
  - fish-shell
colors:
  index_light: "#c85b05"
  index_dark:  "#ff9306"
---

{% comment %}
  Cover image from https://pixabay.com/photos/veil-tail-fish-goldfish-swim-11453/
{% endcomment %}

fish shell is great
one feature is autocomplete

mostly useful!

but occasionally I mistype a command or put sensitive info in history, and then fish will try to suggest it to me

a while back i mistyped `hdiutil attach` as `hdiutil atach`.
not a big deal until fish started suggesting it, and I'd tab to autocomplete before I'd finished reading what it was suggesting
oops!

---

## forget the last command

added function to my shell config:

```shell
# Removes the last-typed command from my fish history.
#
# This means that if I mistype a command and it starts appearing in
# my suggested commands, I can type it one more time then purge it from
# my history, to prevent it being suggested again.
function forget_last_command
    history delete --exact --case-sensitive (history --max 1)
    history merge
end
```

the `delete` command purges it from the shell
the `merge` command updates current session

to test:

1.  run a command like `echo "my password is hunter2"`
2.  type `echo` into shell, see it offers to autocomplete
3.  cancel that command, instead, run `forget_last_command`
4.  type `echo` again, notice it no longer offers to autocomplete

---

## never remmeber certain commands

there are other commands that aren't sensitive or mistyped, but I never want offered as autocomplete
e.g. a force push in git – potentially dangerous!
case where I'm willing to give up benefits of autocomplete for safety

```shell
# Allow me to prevent certain dangerous commands from ever
# appearing in autocomplete.
function forget_dangerous_history_commands
    set LAST_COMMAND (history --max 1)

    if [ "$LAST_COMMAND" = "git push origin (gcb) --force" ]
        history delete --exact --case-sensitive "$LAST_COMMAND"
        history merge
    end
end
```