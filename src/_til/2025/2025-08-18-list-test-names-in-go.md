---
layout: til
title: How to list the tests that will be run by a `go test` command
summary: "Use `go test -list={pattern}`."
date: 2025-08-18 11:06:00 +0100
tags:
  - golang
---
If you want to see what tests will run if you run `go test`, you can pass the `-list` flag with a pattern.
Here's an example:

```console
$ go test -list='TestGo*'
TestGoMod
TestGoVersion
ok  	tailscale.com	0.180s
```

If you want to see all the tests that will be run, use `.` as your pattern:

```console
$ go test -list=.
TestGoMod
TestLicenseHeaders
TestPackageDocs
TestDockerfileVersion
TestGoVersion
ok  	tailscale.com	0.201s
```

