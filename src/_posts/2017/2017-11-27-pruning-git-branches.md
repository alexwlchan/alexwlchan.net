---
layout: post
date: 2017-11-27 22:41:36 +0000
title: Pruning old Git branches
tags: git
summary: "Two commands for managing Git branches: one for deleting branches which have already been merged, one for deleting branches which were deleted on a remote."
category: "Working with Git"
---

Here's a quick tip for Git users: if you want to delete every local branch that's already been merged into master, you can run this command:

```console
$ git branch --merged master | egrep -v "(^\*|master|dev)" | xargs git branch --delete
```

A quick breakdown:

*   `git branch --merged master` gives us a [list of branches][branch] "whose tips are reachable from the specified commit" --- any branch whose final commit has been merged into master.
    If your main branch has a different name, use that instead of _master_.

*   That gets piped to `egrep -v`, which excludes any lines which match the pattern.
    In this case, the pattern filters out branches whose name ends in _master_ or _dev_.
    You should adapt this for any long-lived branches in your repo.

*   Finally, any branches which remain are passed via `xargs` to `git branch --delete`, which deletes the branch.

I originally got the command from a [Stack Overflow answer][so], although I tweaked it when I read the documentation, to more closely match my use case.

If you want to see what branches this will delete without committing to it, run everything before the second pipe --- not the `xargs` bit at the end.

[so]: https://stackoverflow.com/a/6127884/1558022
[branch]: https://git-scm.com/docs/git-branch

---

The other command I often use is this one:

```console
$ git fetch origin --prune
```

If a branch has been deleted in the _origin_ remote, and you had a local branch which was tracking it, the local branch gets deleted as well.

For example: suppose you had a branch called _new-feature_.
You push the branch to GitHub, open a pull request, and later the branch gets merged and deleted through the GitHub web interface.
When you do your next `fetch` with `--prune`, it'll clean up the local branch _new-feature_.

---

Git branches are very cheap --- usually a single file that references a commit hash --- so deleting branches won't save disk space or improve performance.
I like to keep my repos neat and tidy, and not have a long branch list to scroll through, which is why I do this.
If a long branch list doesn't bother you, then you can ignore these commands.
