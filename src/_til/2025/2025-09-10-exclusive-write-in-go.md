---
layout: til
title: Using Go to write to a file, but only if it doesn't exist yet
summary: Opening a file with `os.O_CREATE|os.O_EXCL` will ensure you only create the file if it doesn't already exist.
date: 2025-09-10 15:40:48 +01:00
tags:
  - golang
---
In Go, if you want to write to a file, but only if it doesn't exist (an "exclusive write"), you can call [`os.OpenFile`](https://pkg.go.dev/os#OpenFile) with a couple of flags:

{% code lang="go" names="0:f 1:err" %}
f, err := os.OpenFile(fname, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0666)
{% endcode %}

*   [`O_CREATE`](https://pkg.go.dev/os#O_CREATE) will create a new file if one doesn't exist already
*   [`O_EXCL`](https://pkg.go.dev/os#O_EXCL) means the file must not exist already
*   [`O_WRONLY`](https://pkg.go.dev/os#O_WRONLY) means you're opening the file as write-only; you can replace this with [`O_RDONLY`](https://pkg.go.dev/os#O_RDONLY) or [`O_RDWR`](https://pkg.go.dev/os#O_RDWR)

Here's an example program:

{% code lang="go" names="0:main 1:main 2:fname 3:f 4:err 28:err" %}
package main

import (
	"log"
	"os"
)

func main() {
	fname := "greeting.txt"

	f, err := os.OpenFile(fname, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0666)
	if err != nil {
		if os.IsExist(err) {
			log.Fatalf("File already exists: %s\n", fname)
		} else {
			log.Fatalf("Error creating file: %v\n", err)
		}
	}
	defer f.Close()

	_, err = f.WriteString("hello world\n")
	if err != nil {
		log.Fatalf("Error writing to file: %v\n", err)
	}

	log.Printf("Created file successfully: %s\n", fname)
}
{% endcode %}

Here's what happens when you run it:

```console
$ go run exclusive_write.go
Created file successfully: greeting.txt

$ go run exclusive_write.go
File already exists: greeting.txt
exit status 1
```