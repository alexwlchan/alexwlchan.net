---
layout: post
title: Quick-and-dirty print debugging in Go
summary: I wrote a Go module to help with my print debugging, which logs expressions and values to a separate file.
tags:
  - golang
---
I've been writing a lot of Go in my new job, and trying to understand a new codebase.

When I'm reading unfamiliar code, I like to use [print debugging][print debugging] to follow what's happening.
I print what branches I'm in, the value of different variables, which functions are being called, and so on.
Some people like debuggers or similar tools, but when you're learning a new language they're another thing to learn -- whereas printing "hello world" is the first step in every language tutorial.

The built-in way to do print debugging in Go is `fmt.Printf` or `log.Printf`.
That's fine, but my debug messages get interspersed with the existing logs so they're harder to find, and it's easy for those debug statements to slip through code review.

Instead, I've taken inspiration from [Ping Yee's Python module "q"][pypi-q].
If you're unfamiliar with it, I recommend [his lightning talk][q-lightning], where he explains the frustration of trying to find a single variable in a sea of logs.
His module provides a function `q.q()`, which logs any expressions to a standalone file.
It's quick and easy to type, and the output is separate from all your other logging.

I created something similar for Go: a module which exports a single function `Q()`, and logs anything it receives to `/tmp/q.txt`.
Here's an example:

{% code lang="go" names="0:main 1:printShapeInfo 2:name 3:sides 8:main 14:err" %}
package main

import (
	"github.com/alexwlchan/q"
	"os"
)

func printShapeInfo(name string, sides int) {
	q.Q("a %s has %d sides", name, sides)
}

func main() {
	q.Q("hello world")

	q.Q(2 + 2)

	_, err := os.Stat("does_not_exist.txt")
	q.Q(err)

	printShapeInfo("triangle", 3)
}
{% endcode %}

The logged output in `/tmp/q.txt` includes the name of the function and the expression that was passed to `Q()`:

<pre><code><span style="color: var(--green);">main</span>: "hello world"

<span style="color: var(--green);">main</span>: <span style="color: var(--blue);">2 + 2</span> = 4

<span style="color: var(--green);">main</span>: <span style="color: var(--blue);">err</span> = stat does_not_exist.txt: no such file or directory

<span style="color: var(--green);">printShapeInfo</span>: a triangle has 3 sides</code></pre>

I usually open a terminal window running `tail -f /tmp/q.txt` to watch what gets logged by `q`.

The module is only 120 lines of Go, and [available on GitHub][github-q].
You can copy it into your project, or it's simple enough that you could write your own version.
It has two interesting ideas that might have broader use.

## Getting context with the `runtime` package

When you call `Q()`, it receives the final value -- for example, if you call `Q(2 + 2)`, it receives `4` -- but I wanted to log the original expression and function name.
This is a feature from Ping's Python package, and it's what makes q so pleasant to use.
This gives context for the log messages, and saves you typing that context yourself.

I get this information from Go's [`runtime` package][go-runtime], in particular the [`runtime.Caller`][go-runtime-caller] function, which gives you information about the currently-running function.

I call `runtime.Caller(1)` to step up the callstack by 1, to the actual line in my code where I typed `Q().`
It tells me the "program counter", the filename, and the line number.
I can resolve the program counter to a function name with [`runtime.FuncForPC`][go-runtime-funcforpc], and I can just open the file and look up that line to read the expression.
(This assumes the source code hasn't changed since compilation, which is always true when I'm doing local debugging.)

## Not affecting my coworkers with a local gitignore

To use this file, I copy `q.go` into my work repos and add it to my `.git/info/exclude`.
The latter is a local-only ignore file, unlike the `.gitignore` file which is checked into the repo.
This means I won't accidentally check in `q.go` or push it to GitHub.

It also means I can't forget to remove my debugging code, because if I do, the tests in CI will fail when they can't find `q.go`.

This avoids other approaches that would be more disruptive or annoying, like making it a project dependency or adding it to the shared `.gitignore` file.

[pypi-q]: https://github.com/zestyping/q
[q-lightning]: https://www.youtube.com/watch?v=OL3De8BAhME#t=25m15s
[print debugging]: https://en.wikipedia.org/wiki/Debugging#:~:text=Print%20debugging%20or%20tracing
[github-q]: https://github.com/alexwlchan/q.go/blob/main/q.go
[go-runtime]: https://pkg.go.dev/runtime
[go-runtime-caller]: https://pkg.go.dev/runtime#Caller
[go-runtime-funcforpc]: https://pkg.go.dev/runtime#FuncForPC
