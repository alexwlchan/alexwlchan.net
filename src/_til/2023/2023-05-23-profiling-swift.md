---
layout: til
date: 2023-05-23 21:05:27 +00:00
title: How to profile Swift code
tags:
  - swift
---
[Stack Overflow coughed up a snippet which I've adapted](https://stackoverflow.com/a/24755958/1558022):

```swift
let start = DispatchTime.now()
var elapsed = start

func printElapsed(_ label: String) -> Void {
  let now = DispatchTime.now()

  let totalInterval = Double(now.uptimeNanoseconds - start.uptimeNanoseconds) / 1_000_000_000
  let elapsedInterval = Double(now.uptimeNanoseconds - elapsed.uptimeNanoseconds) / 1_000_000_000

  elapsed = DispatchTime.now()

  print("Time to \(label):\n  \(elapsedInterval) seconds (\(totalInterval) total)")
}
```

e.g. in this profiling:

```console
$ time swift actions/run_action.swift 934BD809-D6D9-4147-AE7E-E1701C82AADD/L0/001 toggle-rejected
Time to waking up:
  1.3583e-05 seconds
Time to get photo:
  0.110328541 seconds
Time to enter switch:
  0.1103705 seconds
Time to toggle needs action:
  0.159904833 seconds
Time to all done:
  0.211530583 seconds

________________________________________________________
Executed in  523.46 millis    fish           external
   usr time  136.72 millis   60.00 micros  136.66 millis
   sys time   52.85 millis  683.00 micros   52.17 millis
```

it's pretty obvious the "time to get photo" step is the slow one

The Stack Overflow answer suggests using `ContinuousClock`; that was in a newer version of Swift than I had available when I wrote this snippet – for now I'm sticking with what I've got and which I know works.
