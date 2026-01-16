---
layout: til
date: 2024-02-22 18:40:37 +00:00
title: Using `errexit` and arithmetic expressions in bash
tags:
  - bash
  - shell scripting
---
I was having some issues with a Bash script that used `set -o errexit` and arithmetic expressions to increment a value:

```shell
set -o errexit

x=0

((x++))
((x++))
((x++))
```

When I tested this on my Mac, the script ran fine, but it failed when I tried to run it in GitHub Actions -- the first increment caused the entire script to fail.

My Mac only has Bash 3.2, whereas GitHub Actions has Bash 5 -- this was the root cause, and I learnt a couple of interesting things along the way.

## The return status of arithmetic expressions depends on the value

The first question is why `((x++))` returns a non-zero exit code.

Via a [Stack Overflow answer](https://stackoverflow.com/a/6877775/1558022), I found the relevant section of the bash manpage (emphasis mine):

> <dl>
> <dt><code>((expression))</code></dt>
> <dd>The expression is evaluated according to the rules described below under ARITHMETIC EVALUATION. <em>If the value of the expression is non-zero, the return status is 0; otherwise the return status is 1.</em> This is exactly equivalent to let "expression".</dd>
> </dl>

I expanded my minimal example to print the return code and the current value of `x`, and I used Docker to run it on several versions of Bash (Bash 3, Bash 4, and Bash 5):

```shell
#!/usr/bin/env bash

set -o errexit

bash --version

x=0

((x++)); echo "\$?=$?, x=$x"
((x++)); echo "\$?=$?, x=$x"
((x++)); echo "\$?=$?, x=$x"
```

The output was always the same:

```
$?=1, x=1
$?=0, x=2
$?=0, x=3
```

So why did it work on my Mac and not GitHub Actions?

## The behaviour of `errexit` changed in Bash 4.1

Via another Stack Overflow answer I've lost, it turns out that the definition of `-e`/`errexit` changed in Bash 4.1.

This is the Bash 4.0 manpage:

> <dl><dt><code>-e</code></dt>
> <dd>Exit immediately if a simple <em>command</em> (see SHELL GRAMMAR above) exits with a non-zero status.</dd></dl>

and this is the same section in Bash 4.1:

> <dl><dt><code>-e</code></dt>
> <dd>Exit immediately if a <em>pipeline</em> (which may consist of a single simple command), a <em>subshell</em> command enclosed in parentheses, or one of the commands executed as part of a command list enclosed by braces (see SHELL GRAMMAR above) exits with a non-zero status.</dd></dl>

I'm not entirely sure which of these is an arithmetic expression, but clearly stuff changed enough to change the behaviour of the overall script.

## How to fix it

If I'm incrementing a variable from `0` with `errexit`, now I just do:

```shell
(x++) || true
```
