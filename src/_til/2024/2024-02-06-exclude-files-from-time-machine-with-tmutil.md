---
layout: til
date: 2024-02-06 20:17:11 +00:00
title: Exclude files from Time Machine with `tmutil addexclusion`
tags:
  - macos
---
If you want to programatically exclude files from Time Machine backups, you can use the [`tmutil` command-line tool](https://ss64.com/mac/tmutil.html).

The manpage says there are "two kinds of user-configurable exclusions in Time Machine"; I have notes on each of them separately.

## Location-independent exclusions

> The first, which is the default behavior for the `addexclusion` verb, is a location-independent ("sticky") exclusion that follows a file or directory. When the file or directory is moved, the exclusion goes with the item to the new location. Additionally, when the item is copied, the copy retains the exclusion.

This works by adding an extended attribute to the file, which looks like this:

```console
$ tmutil addexclusion example.txt
$ xattr -l example.txt
com.apple.metadata:com_apple_backup_excludeItem: bplist00_com.apple.backupd
```

You don't need to be root to run this, but the files won't appear in the Time Machine preferences.

## Fixed-path exclusions

> The second kind of exclusion is what is known as a fixed-path exclusion. In this scenario, you tell Time Machine that you want a specific path to be excluded, agnostic of the item at that path. If there is no file or directory at the specified path, the exclusion has no effect; if the item previously at the path has been moved or renamed, the item is not excluded, because it does not currently reside at the excluded path. As a consequence of these semantics, moving a file or directory to the path will cause the item to be excluded--fixed-path exclusions are not automatically cleaned up when items are moved or deleted and will take effect again once an item exists at an excluded path.

You need to add the `-p` flag, use `sudo` privileges, and pass an absolute path:

```console
$ sudo tmutil addexclusion -p $(pwd)/example.txt
```

This will cause the file to appear in the Time Machine preferences.

Additionally, you can inspect the relevant value with this command:

```console
$ defaults read /Library/Preferences/com.apple.TimeMachine SkipPaths
```

## How I use it

I ran the following command to exclude a bunch of directories in my checked-out repos that (1) have a lot of small files and (2) aren't worth backing up:

```shell
find ~/repos \
  -name '.venv' \
  -o -name '.tox' \
  -o -name 'node_modules' \
  -o -name 'target' \
  -o -name '.terraform' | xargs sudo tmutil addexclusion -p
```

Additionally, I've added a line to my script for creating virtual environments