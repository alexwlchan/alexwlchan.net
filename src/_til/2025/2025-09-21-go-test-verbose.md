---
layout: til
title: Use the `-v` flag to get verbose output from Go tests
summary: This prints all `t.Log` and `t.Logf` calls, even if the test succeeds or times out.
date: 2025-09-21 22:23:42 +0100
tags:
  - golang
  - software testing
---
I had a Go test which was timing out, and I wanted to see the log messages being written by `t.Log` and `t.Logf` to find out where it was getting stuck.
Normally these messages are only written if the test fails, to help you with debugging.

Unfortunately, if you run `go test` with the `-timeout` flag and the test exceeds the timeout, Go panics and the test immediately ends.
None of the log messages get printed, the test just fails.

Running `go test` with the `-v` flag (verbose) means it prints log messages immediately, so they aren't lost if the test panics.

## Example

Here's an example of a test which prints a bunch of logs, and has a long hang halfway through:

{% code lang="go" names="0:chatty 1:TestChatty 2:t 7:i" %}
package chatty

import (
	"testing"
	"time"
)

func TestChatty(t *testing.T) {
	t.Log("starting the test")
	for i := range 5 {
		if i == 4 {
			time.Sleep(10 * time.Second)
		}
		t.Logf("running test case %d", i)
	}
	t.Log("finishing the test")
}
{% endcode %}

Here's the output of different `go test` commands, slightly elided for readability:

```console
$ go test chatty_test.go
ok  	command-line-arguments	10.142s

$ go test -v chatty_test.go
=== RUN   TestChatty
    chatty_test.go:9: starting the test
    chatty_test.go:14: running test case 0
    chatty_test.go:14: running test case 1
    chatty_test.go:14: running test case 2
    chatty_test.go:14: running test case 3
    chatty_test.go:14: running test case 4
    chatty_test.go:16: finishing the test
--- PASS: TestChatty (10.00s)
PASS
ok  	command-line-arguments	10.141s

$ go test -timeout 1s chatty_test.go
panic: test timed out after 1s
	running tests:
		TestChatty (1s)

goroutine 4 [running]:
testing.(*M).startAlarm.func1()
  […]

goroutine 1 [chan receive]:
testing.(*T).Run(0x14000002fc0, {0x100abf8d5?, 0x1400007ab38?}, 0x100b36560)
  […]

goroutine 3 [sleep]:
time.Sleep(0x2540be400)
  […]
FAIL	command-line-arguments	1.140s
FAIL

$ go test -v -timeout 1s chatty_test.go
=== RUN   TestChatty
    chatty_test.go:9: starting the test
    chatty_test.go:14: running test case 0
    chatty_test.go:14: running test case 1
    chatty_test.go:14: running test case 2
    chatty_test.go:14: running test case 3
panic: test timed out after 1s
	running tests:
		TestChatty (1s)

goroutine 35 [running]:
testing.(*M).startAlarm.func1()
  […]

goroutine 1 [chan receive]:
  […]

goroutine 34 [sleep]:
  […]
FAIL	command-line-arguments	1.141s
FAIL
```

When the test times out, adding the `-v` flag gives us more information about where the test got stuck.