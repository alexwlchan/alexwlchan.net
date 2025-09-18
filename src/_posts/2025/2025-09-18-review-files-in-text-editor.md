---
layout: post
date: 2025-09-18 21:14:29 +0000
title: Opening all the files that have been modified in a Git branch
summary: You can use Git to find where a branch diverged from `main`, what files have changed, then open those files in your editor.
tags:
  - git
---
Today a colleague asked for a way to open all the files that have changed in a particular Git branch.
They were reviewing a large pull request, and sometimes it's easier to review files in your local editor than in GitHub's code review interface.
You can see the whole file, run tests or local builds, and get more context than the GitHub diffs.

This is the snippet I suggested:

```shell
git diff --name-only "$BRANCH_NAME" $(git merge-base origin/main "$BRANCH_NAME") \
  | xargs open -a "Visual Studio Code"
```

It uses a couple of nifty Git features, so let's break it down.

## How this works

There are three parts to this command:

<ol>
  <li>
    <p>
      <strong>Work out where the dev branch diverges from main.</strong>
      We can use <a href="https://git-scm.com/docs/git-merge-base"><code>git-merge-base</code></a>:
    </p>

{% highlight console %}
$ git merge-base origin/main "$BRANCH_NAME"
9ac371754d220fd4f8340dc0398d5448332676c3
{% endhighlight %}

    <p>
      This command gives us the common ancestor of our main branch and our dev branch – this is the tip of main when the developer created their branch.
    </p>

    <p>
      In a small codebase, main might not have changed since the dev branch was created.
      But in a large codebase where lots of people are making changes, the main branch might have moved on since the dev branch was created.
    </p>

    <p>Here’s a quick picture:</p>

    {%
      inline_svg
      filename="git_history.svg"
      width="650px"
      alt="Simple illustration of Git history. There's a linear series of commits on the main branch, and then a development branch created later. The commit where the branch was created is highlighted in red."
    %}

    <p>
      This tells us which commits we’re reviewing – what are the changes in this branch?
    </p>
  </li>

  <li>
    <p>
      <strong>Get a list of files which have changed in the dev branch.</strong>
      We can use <a href="https://git-scm.com/docs/git-diff"><code>git-diff</code></a> to see the difference between two commits.
      If we add the <code>--name-only</code> flag, it only prints a list of filenames with changes, not the full diffs.
    </p>

{% highlight console %}
$ git diff --name-only "$BRANCH_NAME" $(git merge-base …)
assets/2025/exif_orientation.py
src/_drafts/create-thumbnail-is-exif-aware.md
src/_images/2025/exif_orientation.svg
{% endhighlight %}

    <p>
      Because we're diffing between the tip of our dev branch, and the point where our dev branch diverged from main, this prints a list of files that have changed in the dev branch.
    </p>

    <p>
      (I originally suggested using <code>git diff --name-only "$BRANCH_NAME" origin/main</code>, but that's wrong.
      That prints all the files that differ between the two branches, which includes changes merged to main after the dev branch was created.)
    </p>
  </li>

  <li>
    <p>
      <strong>Open the files in our text editor.</strong>
      I suggested piping to <code>xargs</code> and <code>open</code>, but there are many ways to do this:
    </p>

{% highlight console %}
$ git diff … | xargs open -a "Visual Studio Code"
{% endhighlight %}

    <p>
      The <a href="https://alexwlchan.net/man/man1/xargs.html"><code>xargs</code> command</a> is super useful for doing the same thing repeatedly – in this case, opening a bunch of files in VS Code.
      You feed it a space-delimited string, it splits the string into different pieces, and runs the same command on each of them, one-by-one.
      It’s equivalent to running:
    </p>

{% highlight shell %}
open -a "Visual Studio Code" "assets/2025/exif_orientation.py"
open -a "Visual Studio Code" "src/_drafts/create-thumbnail-is-exif-aware.md"
open -a "Visual Studio Code" "src/_images/2025/exif_orientation.svg"
{% endhighlight %}

    <p>
      The <a href="https://alexwlchan.net/man/man1/open.html"><code>open</code> command</a> opens files, and the <code>-a</code> flag tells it which application to use.
      We mostly use VS Code at work, but you could pass any text editor here.
    </p>

    <p>
      Reading the manpage for <code>open</code>, I'm reminded that you can open multiple files at once, so I could have done this without using <code>xargs</code>.
      I instinctively reached for <code>xargs</code> because I’m very familiar with it, and it’s a reliable way to take a command that takes a single input, and run it with many inputs.
    </p>
  </li>
</ol>
