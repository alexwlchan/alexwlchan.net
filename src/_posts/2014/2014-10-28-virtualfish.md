---
date: 2014-10-28 20:06:00 +0000
layout: post
tags: fish-shell shell-scripting
title: '"Missing argument at index 2" in fish'
---

My default shell is [fish][fish]. I find it very pleasant and easy to use, and it was very friendly when I was first learning the shell. The downside is that it seems to have a relatively small user base, and so you can't always just do a Google search when you hit an error message.

Here's a rather odd one I came across this evening: running `cd` would throw up a "test: Missing argument" message, but any other command was fine:

```console
$ cd ~/bin
test: Missing argument at index 2

$ pwd
/Users/alexwlchan/bin
```

[Googling this error message][google] turns up just four results, and none of them were particularly useful in solving my problem. This is where I was hitting a problem, and how I fixed it.

<!-- summary -->

I started with the usual -- restarting the shell, rebooting, and switching from iTerm2 to Terminal -- to no avail. I didn't seriously expect either of those to work, but you have to try.

The next place to look was my `config.fish` (the configuration file for fish, similar to a `.bash_profile` or `.zshrc`). I quickly traced it to a script that I was loading:

```bash
# . ~/bin/virtualfish/virtual.fish
. ~/bin/virtualfish/auto_activation.fish
# . ~/bin/virtualfish/global_requirements.fish
```

These scripts are loading [Adam Brenecki's virtualfish][vf] to integrate virtualenv with my shell. Initially I was confused, because nothing had changed -- I hadn't updated fish, virtualfish or anything else.

But peeking inside `auto_activation.fish` turned up the instance of `test` that was throwing this error, and why it was upset:

<pre>
new_virtualenv_name (cat "$activation_root/$VIRTUALFISH_ACTIVATION_FILE")
[…]
if test $new_virtualenv_name != ""
</pre>

The `new_virtualenv_name` is reading a `.venv` file in the current tree. This file normally contains the name of a virtualenv, and when you enter that directory, virtualfish automatically activates it (and deactivates it when you leave). This is usually set up with the `vf connect` command, and it's incredibly convenient.

It was confused because, for reasons unknown, I had an empty `.venv` file in my home directory. When it tried to see which virtualenv it should be loaded, it got an empty string. The `test` was only getting two arguments, not three, and hence the error.

Deleting the empty `.venv` file makes the message go away.

This seems fairly obscure, and I don't know whether anybody else will hit this exact problem, but I hope it's useful to somebody -- even if that is just my future self.

[fish]: http://fishshell.com
[google]: https://www.google.co.uk/search?q=test%20missing%20argument%20at%20index%202#q=fish+test+missing+argument+at+index+2
[vf]: https://github.com/adambrenecki/virtualfish
