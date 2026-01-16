---
layout: til
date: 2024-02-25 02:15:49 +00:00
title: Use the `-n`/`-i` flags to avoid overwriting files with `cp` and `mv`
tags:
  - shell scripting
---
The `mv` and `cp` builtins have a `-n` flag (no-clobber), and will prevent them from overwriting an existing file.
They also have a `-i` flag (interactive)

I saw these flags mentioned in a Discord; I wanted to do a few experiments to see how they work in practice (and whether they'd be useful for me).
I ran these tests with the macOS tools, but they may differ on other platforms.

## `cp`

This will prevent overwriting files, and gives you a distinct exit code if it's unable to copy the file.

Here's an example:

```shell
echo "red triangle" > shape.txt
echo "blue circle" > new_shape.txt

cp -n new_shape.txt shape.txt
echo "$?"       # --> 1
cat shape.txt   # --> red triangle

cp new_shape.txt shape.txt
echo "$?"       # --> 0
cat shape.txt   # --> blue circle
```

If you use `cp -i`, it has similar behaviour, returning different exit codes depending on whether or not the filw as overwritten:

```shell
echo "red triangle" > shape.txt
echo "blue circle" > new_shape.txt

cp -i new_shape.txt shape.txt  # --> n
echo "$?"                      # --> 1
cat shape.txt                  # --> red triangle

cp -i new_shape.txt shape.txt  # --> y
echo "$?"                      # --> 0
cat shape.txt                  # --> blue circle
```

## `mv`

This will prevent overwriting files, but it always has exit code 0, whether or not it moved the file.

Here's an example:

```shell
echo "red triangle" > shape.txt
echo "blue circle" > new_shape.txt

mv -n new_shape.txt shape.txt
echo "$?"      # --> 0
ls             # --> new_shape.txt shape.txt

mv new_shape.txt shape.txt
echo "$?"      # --> 0
ls             # --> shape.txt
```

And the same exit codes if you overwrite a file (or not) with `mv -i`:

```shell
echo "red triangle" > shape.txt
echo "blue circle" > new_shape.txt

mv -i new_shape.txt shape.txt  # --> n
echo "$?"                      # --> 0
ls                             # --> new_shape.txt shape.txt

mv -i new_shape.txt shape.txt  # --> y
echo "$?"                      # --> 0
ls                             # --> shape.txt
```
