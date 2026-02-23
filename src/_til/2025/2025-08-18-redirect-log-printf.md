---
layout: til
title: How to redirect the output of `log.Printf` in Go
date: 2025-08-18 12:29:00 +01:00
tags:
  - golang
---
Suppose I have some Go code that uses `log.Printf`:

```go
package main

import (
	"log"
)

func main() {
	log.Printf("Hello world!")
}
```

If I run this with its default arguments, it prints a log message to stdout:

```console
$ go run hello.go 
2025/08/18 12:29:59 Hello world!
```

What if I want to change its behaviour?