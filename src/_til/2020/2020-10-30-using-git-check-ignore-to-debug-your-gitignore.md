---
layout: til
date: 2020-10-30 18:25:23 +00:00
title: 'Use `git check-ignore` to debug your `.gitignore`'
summary: |
  Running `git check-ignore --verbose <PATH>` will tell you which rule applies to a given path, and where that rule is defined.
tags:
  - git
---

Here's a useful thing I learnt today: you can use [`git check-ignore`](https://git-scm.com/docs/git-check-ignore) to debug your gitignore rules and find out why a particular file is (or isn't) being ignored.
It knows all the places where gitignore rules might be defined, and how Git decides between conflicting rules.

A few examples:

*   If a file is being ignored and you don't know why, it can show you which line of the .gitignore is causing it to be ignored.

    ```console
    $ git check-ignore --verbose pictures.zip
    .gitignore:116:*.zip	pictures.zip
    ```

*   If a file isn't being ignored and you think it should be, it can show you which rule is negating your ignore rule:

    ```console
    $ git check-ignore --verbose pictures/cats.zip
    pictures/.gitignore:17:!cats.zip	pictures/cats.zip
    ```

    Notice that it looks in .gitignore files that aren't in the root of the repo (the sort of thing I often forget about).

*   It can even look [in your `.git/info/exclude`](/2015/git-info-exclude/), a place for per-clone ignore rules that you don't want to keep in the repository:

    ```console
    $ git check-ignore --verbose scripts/alex/downloader.py
    .git/info/exclude:7:scripts/alex/*.py	scripts/alex/downloader.py
    ```
