---
layout: til
date: 2024-05-16 14:49:57 +01:00
title: Writing a file in Swift, but only if it doesn't already exist
summary: |
  Adding `.withoutOverwriting` to your `write()` call will prevent you from overwriting a file that already exists.
tags:
  - swift
---
In Python I'm fairly used to the idea of using file mode `x` to do an "exclusive" file open.
This allows you to write to a file, but only if it doesn't already exist.
In this example, if `greeting.txt` already exists, the `open()` call will throw a `FileExistsError`.

```python
with open("greeting.txt", "x") as f:
    f.write("Hello world")
```

How can I do the same in Swift?

Let's start with a simple Swift script that writes the current date to a file:

```swift
import Foundation

let now = Date()
let data: Data = "\(now)\n".data(using: .utf8)!

let savePath = URL(fileURLWithPath: "now.txt")

do {
  try data.write(to: savePath)
} catch {
  print("Unable to write data: \(error.localizedDescription)")
}
```

And if I run it twice, the second run will overwrite the file created by the first run:

```console
$ swift write_date.swift ; cat now.txt
2024-05-16 14:05:04 +0000

$ swift write_date.swift ; cat now.txt
2024-05-16 14:05:18 +0000
```

What if I want to ensure a file never gets overwritten?

It turns out you can pass a list of options to the `write()` call, which is a list of `Data.WritingOptions` values.
This is an alias for [`NSData.WritingOptions`](https://developer.apple.com/documentation/foundation/nsdata/writingoptions).
One of the options is `withoutOverwriting`, which will fail if the file you're trying to write to already exists:

```swift
do {
  try data.write(to: savePath, options: [.withoutOverwriting])
} catch {
  print("Unable to write data: \(error.localizedDescription)")
}
```

If I run the new script twice, the second run will fail with an error that I can catch and react to:

```console
$ swift write_date2.swift; cat now.txt
2024-05-16 14:07:38 +0000

$ swift write_date2.swift
Unable to write data: The file “now.txt” couldn’t be saved in the folder
“tmp.QYW2iXbbmt” because a file with the same name already exists.
```

There are a couple of other interesting values in `NSData.WritingOptions`.
The one I'm mostly likely to use is `atomic` (for atomic write).
There are also a couple of options related to encryption and file access that I don't really understand -- I think I'm missing some context for the security approach here.
