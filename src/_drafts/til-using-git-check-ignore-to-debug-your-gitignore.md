---
layout: post
title: 'TIL: Using git check-ignore to debug your .gitignore'
tags: git
theme:
  minipost: true
---

Here's a useful thing I learnt today: you can use [git check-ignore](https://git-scm.com/docs/git-check-ignore) to debug your gitignore rules and find out why a particular file is (or isn't) being ignored.
It knows all the places where gitignore rules might be defined, and how Git decides between conflicting rules.

By calling `git check-ignore --verbose <PATH>`, you can see which rule applies to a given path, and where that rule is defined.

There are times I'd have found this very handy!

A few examples:

*   If a file is being ignored and you don't know why, it can show you which line of the .gitignore is causing it to be ignored.

    ```
    $ git check-ignore --verbose pictures.zip
    .gitignore:116:*.zip	pictures.zip
    ```

*   If a file isn't being ignored and you think it should be, it can show you which rule is negating your ignore rule:

    ```
    $ git check-ignore --verbose pictures/cats.zip
    pictures/.gitignore:17:!cats.zip	pictures/cats.zip
    ```

    Notice that it looks in .gitignore files that aren't in the root of the repo (the sort of thing I often forget about).

*   It can even look [in your `.git/info/exclude`](/2015/06/git-info-exclude/), a place for per-clone ignore rules that you don't want to keep in the repository:

    ```
    $ git check-ignore --verbose scripts/alex/downloader.py
    .git/info/exclude:7:scripts/alex/*.py	scripts/alex/downloader.py
    ```
