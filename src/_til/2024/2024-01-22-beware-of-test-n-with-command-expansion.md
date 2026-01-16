---
layout: til
title: "Beware of using `test -n` with command expansion"
date: 2024-01-22 10:16:06 +00:00
tags:
  - fish shell
---
I'd written a fish script that used `test -n` (check for an empty string) and a command substitution, but I was seeing unexpected results:

```shell
if test -n (which keyring)
    echo "I know where keyring is!"
end
```

In particular, it would always execute the "true" body of the `if ` statement, even if `which keyring` returned an empty string.

This is because of the way fish's shell expansion work -- the `which keyring` gets reduced to nothing, and then it becomes `test -n` which is always true.
There's a long discussion of this in a GitHub ticket ["test -n not working as expected"][github].

You can see this more clearly in this example:

```shell
if test -n (printf "")
    echo "It's not empty!"
end
```

The fix is to assign the command substitution to a variable first, then check whether that's an empty string.
For example:

```shell
set location (which keyring)

if test -n "$location"
    echo "I know where keyring is"
end
```

or to do some other test on the output; in this case I decided to check the `$status` variable of the `which` command.

[github]: https://github.com/fish-shell/fish-shell/issues/2037
