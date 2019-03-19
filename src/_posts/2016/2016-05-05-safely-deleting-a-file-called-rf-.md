---
layout: post
date: 2016-05-05 21:03:00 +0000
desc: "If for some reason you create a file called `-rf *`, it\u2019s possible to\
  \ delete it safely. But really, don\u2019t create it in the first place."
tags: linux shell-scripting
title: "Safely deleting a file called \u2018-rf *\u2019"
category: Programming and code
---

Odd thing that happened at work today: we accidentally created a file called `-rf *` on one of our dev boxes.
Linux allows almost any character in a filename, with the exception of the null byte and a slash, which lets you create unhelpfully-named files like this.
(Although you can't create `-rf /`.)

You have to be a bit careful deleting a file like that, because running `rm -rf *` usually deletes everything in the current directory.
You could try quoting it – `rm "-rf *"`, perhaps – but you have to be careful to get the quotes right.

On systems with a GUI, you can just use the graphical file manager, which doesn't care about shell flags.
But most of our boxes are accessed via SSH, and only present a command line.

Another possible fix is to rename the file to something which doesn't look like a shell command, and delete the renamed file.
But trying to do `mv "-rf *"` has the same quoting issues as before.

In the end, I went with an inelegant but practical solution:

```console
$ python -c 'import shutil; shutil.move("-rf *", "deleteme")'
```

Python doesn't know anything about these Unix flags, so it renames the file without complaint.

I feel like I should probably know how to quote the filename correctly to delete this without going to Python, but sometimes safety and pragmatism trump elegance.
This works, and it got us out of a mildly tricky spot.

Hopefully this is not something many people need to fix, but now it's all sorted, I can't help but find the whole thing mildly amusing.
