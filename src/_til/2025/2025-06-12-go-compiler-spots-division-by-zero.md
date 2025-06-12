---
layout: til
title: Go's compiler is smart enough to spot division by zero errors
date: 2025-06-12 17:18:46 +0100
tags:
  - golang
---
I've been doing a couple of Go experiments, and I wanted to test if Go has lazy evaluation of `if` conditions.

I wrote the following simple program -- the first condition is true, so I'm looking for Go to print the message on line 7 rather than try to evaluate the invalid condition:

{% annotatedhighlight lang="go" %}
package main

import "fmt"

func main() {
	if 2%2 == 0 || 1/0 == 0 {
		fmt.Println("one of these conditions is true")
	}
}
{% endannotatedhighlight %}

But surprisingly, Go won't let me compile this program:

```console
$ go run division.go
# command-line-arguments
./division.go:6:19: invalid operation: division by zero
```

This also works if your divisor is a `const` -- presumably the compiler inlines it at some point, and notices the same mistake.
This code fails for a similar reason:

```go
const divisor = 0

if 2%2 == 0 || 1/divisor == 0 {
	fmt.Println("one of these conditions is true")
}
```

But it's fine if your divisor is a regular variable.
This makes sense -- the compiler can't know if the value might change at runtime and make this a legal operation.
This code compiles and runs successfully, which also proves that Go is doing lazy evaluation of `if` conditions:

```go
divisor := 0

if 2%2 == 0 || 1/divisor == 0 {
	fmt.Println("one of these conditions is true")
}
```
