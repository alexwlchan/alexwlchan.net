---
layout: til
title: You can change the size of tabs on web pages with the `tab-size` property
date: 2025-07-08 19:50:29 +01:00
tags:
  - css
  - golang
---
I'm going to be writing more Go soon, and that means I'll want to write posts about Go.
I'll want to include snippets of Go code, and my Go code will probably be [indented with tabs][tabs].

That causes an issue with the default browser stylesheet, which uses 8 spaces for tabs -- I think that looks quite wide.
I prefer 4 space indents (which is also used by the [Go documentation](https://go.dev/doc/tutorial/getting-started)).

<pre><code>package main

import "fmt"

func main() {
&Tab;fmt.Println("hello world")
}</code></pre>

I could replace the tabs with spaces, but that means the Go code in my posts won't copy cleanly into a working Go program.
That feels icky.

I found a better fix: there's a [`tab-size` CSS property][tab-size] which lets me customise the width of tabs.
I can specify an exact width (e.g. `tab-size: 10px`) or as a number of spaces (e.g. `tab-size: 4`).

This reduces the indentation in my code blocks, and makes them more readable:

<pre style="tab-size: 4;"><code>package main

import "fmt"

func main() {
&Tab;fmt.Println("hello world")
}</code></pre>

(And a quick bit of spelunking reveals that's the same approach used by [the Go documentation](https://github.com/golang/pkgsite/blob/eac0bf970406fce3244072d54d7843a6697b91be/static/shared/typography/typography.css#L109).)

[tabs]: https://go.dev/doc/effective_go#:~:text=We%20use%20tabs%20for%20indentation
[tab-size]: https://developer.mozilla.org/en-US/docs/Web/CSS/tab-size