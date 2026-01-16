---
layout: til
title: How to get a macOS file/folder icon in Swift
summary:
  Use `NSWorkspace.shared.icon` to get the icon as an `NSImage`, then you can save it to disk or do something else with it.
date: 2025-02-22 00:10:03 +00:00
tags:
  - swift
---
I was working on a project where I needed the icons of a list of folders on macOS.
I wanted to see if I could automate this process.

The key method I need is [`NSWorkspace.shared.icon(forFile:)`](https://developer.apple.com/documentation/appkit/nsworkspace/icon(forfile:)), which returns the icon for a file/folder as an `NSImage`.
You can then use this in a variety of ways; I wrote a short script that saves this as a PNG image:

```swift
#!/usr/bin/env swift
// Get the macOS Finder icon for a file/folder.
//
// This script saves the icon as a PNG image, and prints the path to
// the PNG file.
//
// Example:
//
//    $ swift scripts/get_folder_icon.swift ~/Desktop
//    /tmp/Desktop.png
//

import Cocoa
import Foundation

let arguments = CommandLine.arguments

if arguments.count != 2 {
  fputs("Usage: \(arguments[0]) FOLDER_PATH\n", stderr)
  exit(1)
}

// Get the icon as an NSImage
let folderURL = URL(fileURLWithPath: arguments[1])
let icon = NSWorkspace.shared.icon(forFile: folderURL.path)

// Convert the NSImage to a Data blob containing PNG data
let bitmap = NSBitmapImageRep(data: icon.tiffRepresentation!)!
let pngData = bitmap.representation(using: .png, properties: [:])!

// Get a temporary path to write to
let outputFileURL = URL(fileURLWithPath: NSTemporaryDirectory())
  .appendingPathComponent(folderURL.lastPathComponent)
  .appendingPathExtension("png")

// Write the PNG data to the file
try? pngData.write(to: outputFileURL)
print(outputFileURL.path)
```

This script is fairly scrappy, and in particular doesn't have any error handling.
It would need tidying up before you use it for a "real" project, but it was fine for some quick automations.
