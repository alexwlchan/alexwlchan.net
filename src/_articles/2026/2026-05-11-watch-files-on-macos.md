---
layout: article
date: 2026-05-11 07:41:24 +01:00
title: Watching for file changes on macOS
summary: I've written a Swift script that uses the FSEvents API to get notified of file changes, then I'm using stdout as a bridge to forward those notifications to Python.
topics:
  - macOS
  - Swift
  - Blogging about blogging
colours:
  css_light: "#8b7434"
  css_dark:  "#dfcf96"
is_featured: true
---
{#
  Sharing image from Pixabay: https://pixabay.com/illustrations/domino-game-set-plate-strategy-9602003/
#}

When I'm working on this website, I want a local server with live reload.
I want to be able to open the site in my web browser, make changes to the source files, and have my browser automatically refresh the page when the site is updated.
I use this whenever I'm working on the site, and I find it helpful to see my writing in a different font/layout to my text editor; I spot lots of typos and mistakes that way.

When I was using Jekyll, I used the command `jekyll serve --livereload`.
Now I've written [my own static site generator][mosaic], I need to build my own version.
This was a fun challenge, because it touched a number of areas I've not worked in before -- macOS filesystem events, non-blocking I/O, and HTTP long polling.

In this post I'll explain how I detect changes to source files to trigger a rebuild; in my next post I'll explain how that automatically refreshes any open pages in my browser.
First we're going to build a Swift script that detects changes using the FSEvents API, then we'll get that information into a Python script.

{% table_of_contents %}



## Rejected approaches

**Using third-party libraries.**
Initially I was using the [python-livereload library][gh-python-livereload], but I wanted to replace it with my own implementation -- partly to remove a dependency, partly to understand how this functionality works.
There are other Python libraries that offer filesystem watching, including [fswatch][pypi-fswatch], [inotify][pypi-inotify], and [watchdog][pypi-watchdog], but I didn't want to use them for similar reasons.

I have an advantage over these library authors -- while they aim to support cross-platform filesystem watching, I only have to get it working on macOS.
Specifically, the exact versions of macOS that my Macs are running, and no others.
This means I can write a smaller, more focused bit of code.

**Polling the source files.**
This is easy to write, but I have enough source files that it's surprisingly slow -- about 90ms to scan 13,000 source files, and I'm worried about the effect on power consumption and the lifespan of my SSD if I polled in a hot loop.
For comparison, my final code only takes 2–4ms to detect a change and trigger a new build, and it's very judicious about CPU cycles and disk reads.



## The macOS FSEvents API

### Setting up the event stream

There are several ways to detect changes to files on macOS; I'm going to use the File System Events API (also called "FSEvents" for short).
This allows you to receive notifications about any changes to a directory tree, or files within it.
One of the main purposes of this API is to allow backup software to detect incremental changes without continuously rescanning an entire tree, but we can use it for other things.

Apple has a [File System Events Programming Guide][apple-fsevents-guide] which explains the FSEvents API in detail, and that it's exactly what I need: "The file system events API is designed for passively monitoring a large tree of files for changes".
It mentions a couple of alternatives -- kernel extensions for getting immediate notifications and pre-empting file changes, or kqueues for monitoring changes to a single file -- but they're not what I need, so I didn't explore them further.

The guide is a little outdated, but the broad strokes are still correct.
In [Using the File System Events API][apple-fsevents-guide-using], it explains the lifecycle of a file system events stream: create a stream, start listening, receive notifications, trigger a callback you provide, stop listening, release the stream.

Let's start with a script that prints a static message whenever it sees a change -- we don't care about what file it was yet, for now we just want to know when *any* file changed.

Here are the steps:

1.  Create a file systems event stream using [`FSEventStreamCreate`][cs-FSEventStreamCreate].
    This function takes a lot of arguments and you can't use named arguments, so I found it helpful to define each argument as a variable, then pass those variables into the function.
    I wrapped my `FSEventStreamCreate` call in another function:
    
    ```swift {"names":{"1":"Foundation","2":"createFSEventStream","3":"pathsToWatch","6":"callback","10":"context","13":"sinceWhen","16":"latency","17":"flags","19":"eventStream"}}
    import Foundation

    /// Create a new file system events stream that watches for changes
    /// in the given directories.
    func createFSEventStream(_ pathsToWatch: [String]) -> FSEventStreamRef {
      let callback: FSEventStreamCallback = { (_, _, _, _, _, _) in
        print("Detected file change!")
        
        // Flush stdout to ensure it's printed immediately
        fflush(stdout)
      }
      
      let context: UnsafeMutablePointer<FSEventStreamContext>? = nil
      let sinceWhen = FSEventStreamEventId(kFSEventStreamEventIdSinceNow)
      let latency = 0.01
      let flags = FSEventStreamCreateFlags()

      guard let eventStream = FSEventStreamCreate(
        kCFAllocatorDefault, callback, context, pathsToWatch as CFArray, sinceWhen, latency, flags
      ) else {
        fatalError("Failed to create FSEventStream: check your paths or permissions.")
      }
  
      return eventStream
    }
    ```
    
    The `callback` function is an instance of [`FSEventStreamCallback`][cs-FSEventStreamCallback], which will be called whenever a file changes.
    The arguments contain information about the file which just changed.
    For now we ignore all of that information, and just print a static message.
    
    The `context` argument allows us to attach some context to the stream.
    I'm not sure what it's for -- perhaps for applications that have multiple event streams, and need to distinguish between them in the callback?
    I don't think I need this, and the docs say I can pass NULL, so that's what I've done.
    
    The `sinceWhen` argument asks for events that happened after a given event ID.
    I imagine this is useful for long-running applications like backup software -- it means they can resume an event stream if the app is quit and relaunched, without rescanning the tree on every app launch.
    I just need events from when the script started running, so I can use the `kFSEventStreamEventIdSinceNow` constant.
    
    The `latency` argument is how long the OS will wait to coalesce rapid-fire events into a single event.
    A shorter latency means you get notifications faster, but you'll get more of them.
    I'll implement my own event coalescing later, so I set this quite low and accept the stream.
    
    The `flags` modify the behaviour of the event stream.
    We're using the defaults for now; we'll come back and add some more later.
    
    Finally, we create the event stream by using [`FSEventStreamCreate`][cs-FSEventStreamCreate].
    This returns an `Optional` value which can be `nil` if the stream wasn't created successfully; for example, if you try to watch a directory that doesn't exist or which you don't have permission to read.

1.  Choose the folders you want to watch.
    For this initial script, we'll use two folders that should be present on every Mac: the user's Desktop and Documents folder.
    
    ```swift {"names":{"1":"home","5":"pathsToWatch"}}
    let home = URL(fileURLWithPath: NSHomeDirectory())
    let pathsToWatch = [
      home.appendingPathComponent("Desktop").path,
      home.appendingPathComponent("Documents").path
    ]
    ```

1.  Schedule the event stream and start listening for changes.

    The FS Events Guide tells you to use [`FSEventStreamScheduleWithRunLoop`][cs-FSEventStreamScheduleWithRunLoop], but that function has been deprecated for several years.
    The recommended replacement is [`FSEventStreamSetDispatchQueue`][cs-FSEventStreamSetDispatchQueue]:
    
    ```swift {"names":{"1":"queue"}}
    let queue = DispatchQueue(label: "net.alexwlchan.watch_file_changes")
    FSEventStreamSetDispatchQueue(eventStream, queue)
    FSEventStreamStart(eventStream)

    print("Listening for changes in \(pathsToWatch.joined(separator: ", "))")

    dispatchMain()
    ```

1.  Clean up the event stream when we're done.
    In a simple script like mine that might not be necessary -- the system probably cleans up an event stream if it's not used for a while -- but it's good hygiene and ensures my Mac doesn't start tracking dozens of redundant event streams.
    
    First, here's a function to call the `FSEventStream` methods that stop, invalidate, and release references to the stream:
    
    ```swift {"names":{"1":"cleanupEventStream","2":"eventStream"}}
    /// Stop a file system events stream, invalidate it, and release our
    /// reference to it.
    func cleanupEventStream(_ eventStream: FSEventStreamRef) {
      FSEventStreamStop(eventStream)
      FSEventStreamInvalidate(eventStream)
      FSEventStreamRelease(eventStream)
    }
    ```
    
    Then, a function to create [dispatch source objects][dispatch-makeSignalSource] that watch for a termination signal (`SIGINT`, `SIGTERM`, `SIGHUP`) and runs our cleanup function.
    We have to disable the default handlers, or they can terminate the script before we run our cleanup code:
    
    ```swift {"names":{"1":"registerCleanup","2":"eventStream","5":"signals","9":"sources","11":"sig","13":"signalSource"}}
    /// Register cleanup handlers for SIGINT, SIGTERM and SIGHUP that
    /// clean up the event stream when the script exits.
    ///
    /// Returns an array of `DispatchSourceSignal`; the caller must hold
    /// a reference to these in a global variable, or they will be cancelled.
    func registerCleanup(_ eventStream: FSEventStreamRef) -> [DispatchSourceSignal] {
      let signals = [SIGINT, SIGTERM, SIGHUP]
      var sources: [DispatchSourceSignal] = []

      for sig in signals {
        let signalSource = DispatchSource.makeSignalSource(signal: sig, queue: .main)
        signalSource.setEventHandler {
          print("\nStopping listener...")
          cleanupEventStream(eventStream)
          exit(0)
        }
    
        signal(sig, SIG_IGN)
        signalSource.activate()
        sources.append(signalSource)
      }
  
      return sources
    }
    ```

    Finally, we call this function and hold a reference to the dispatch sources -- if not, Swift will deallocate them as unused, and then our cleanup code won't run.
    
    ```swift {"names":{"1":"cleanup"}}
    let cleanup = registerCleanup(eventStream)
    ```

Here's the complete script:

<details>
  <summary><code>watch_for_changes.swift</code></summary>
  
{% set md %}
```swift {"names":{"1":"Foundation","2":"createFSEventStream","3":"pathsToWatch","6":"callback","10":"context","13":"sinceWhen","16":"latency","17":"flags","19":"eventStream","30":"cleanupEventStream","31":"eventStream","39":"registerCleanup","40":"eventStream","43":"signals","47":"sources","49":"sig","72":"home","76":"pathsToWatch","83":"eventStream","86":"cleanup","89":"queue"}}
#!/usr/bin/env swift
/// Watch for changed files in a directory, and print a message when
/// something changes.
///
/// Example:
///
///     $ swift scripts/watch_for_changed_files.swift ~/Desktop/ ~/Documents/
///     Listening for changes in /Users/alexwlchan/Desktop/, /Users/alexwlchan/Documents/
///     Detected file change!
///     Detected file change!
///     Detected file change!
///

import Foundation

/// Create a new file system events stream that watches for changes
/// in the given directories.
func createFSEventStream(_ pathsToWatch: [String]) -> FSEventStreamRef {
  let callback: FSEventStreamCallback = { (_, _, _, _, _, _) in
    print("Detected file change!")
    
    // Flush stdout to ensure it's printed immediately
    fflush(stdout)
  }

  let context: UnsafeMutablePointer<FSEventStreamContext>? = nil
  let sinceWhen = FSEventStreamEventId(kFSEventStreamEventIdSinceNow)
  let latency = 0.01
  let flags = FSEventStreamCreateFlags()

  guard let eventStream = FSEventStreamCreate(
    kCFAllocatorDefault, callback, context, pathsToWatch as CFArray, sinceWhen, latency, flags
  ) else {
    fatalError("Failed to create FSEventStream: check your paths or permissions.")
  }

  return eventStream
}

/// Stop a file system events stream, invalidate it, and release our
/// reference to it.
func cleanupEventStream(_ eventStream: FSEventStreamRef) {
  FSEventStreamStop(eventStream)
  FSEventStreamInvalidate(eventStream)
  FSEventStreamRelease(eventStream)
}

/// Register cleanup handlers for SIGINT, SIGTERM and SIGHUP that
/// clean up the event stream when the script exits.
///
/// Returns an array of `DispatchSourceSignal`; the caller must hold
/// a reference to these in a global variable, or they will be cancelled.
func registerCleanup(_ eventStream: FSEventStreamRef) -> [DispatchSourceSignal] {
  let signals = [SIGINT, SIGTERM, SIGHUP]
  var sources: [DispatchSourceSignal] = []

  for sig in signals {
    let signalSource = DispatchSource.makeSignalSource(signal: sig, queue: .main)
    signalSource.setEventHandler {
      print("\nStopping listener...")
      cleanupEventStream(eventStream)
      exit(0)
    }

    signal(sig, SIG_IGN)
    signalSource.activate()
    sources.append(signalSource)
  }

  return sources
}

// Choose which folders to watch.
let home = URL(fileURLWithPath: NSHomeDirectory())
let pathsToWatch = [
  home.appendingPathComponent("Desktop").path,
  home.appendingPathComponent("Documents").path
]

// Create the event stream.
let eventStream = createFSEventStream(pathsToWatch)

// Register cleanup handlers that will run when the script exits.
let cleanup = registerCleanup(eventStream)

// Schedule the event stream and start listening for changes.
let queue = DispatchQueue(label: "net.alexwlchan.watch_file_changes")
FSEventStreamSetDispatchQueue(eventStream, queue)
FSEventStreamStart(eventStream)

print("Listening for changes in \(pathsToWatch.joined(separator: ", "))")

dispatchMain()
```
{% endset %}
{{ md|markdownify }}
</details>

When you run this script, you should see it print `Detected file change!` every time you change a file on your Desktop.
Stop the script with ^C.

```console
$ swift watch_for_changes.swift
Listening for changes in /Users/alexwlchan/Desktop, /Users/alexwlchan/Documents
Detected file change!
Detected file change!
Detected file change!
^C
Stopping listener...
```

This alone is enough to know I should kick off a site rebuild, but a full rebuild takes 10–15s.
If I know which file had changed, I can do an incremental rebuild that would be much faster.
Let's tackle that next.



### Knowing which files/folders had changes

If we want to know which file changed, and not merely that a file changed, we need to customise the `FSEventStreamCallback`.
This callback takes six parameters, and the fourth parameter `eventPaths` is an array of paths where changes occurred.

The type is a bit gnarly: by default it's a raw C array of raw C strings, or we can set the [`kFSEventStreamCreateFlagUseCFTypes` flag][cs-kFSEventStreamCreateFlagUseCFTypes] to get a `CFArrayRef` of `CFStringRef` objects.
(Here `CF` stands for Core Foundation, one of Apple's low-level frameworks.)
I started by setting theflag, and writing a function to converts the CFArrayRef into a vanilla Swift array:

```swift {"names":{"1":"flags","4":"convertFSEventPaths","5":"eventPaths","8":"cfArray"}}
let flags = FSEventStreamCreateFlags(kFSEventStreamCreateFlagUseCFTypes)

/// Convert a raw pointer from an FSEvent callback into a Swift String.
///
/// FSEventStream must be created with 'kFSEventStreamCreateFlagUseCFTypes'
func convertFSEventPaths(_ eventPaths: UnsafeRawPointer) -> [String] {
  let cfArray = Unmanaged<CFArray>.fromOpaque(eventPaths)
  return cfArray.takeUnretainedValue() as! [String]
}
```

I can imagine that if you're working in a very performance-sensitive application, you might skip this step and operate on the C types directly, but that's not necessary for me.

Then I modified the callback to parse the event paths, and print them one-by-one:

```swift {"names":{"1":"callback","3":"eventPaths","4":"p"}}
let callback: FSEventStreamCallback = { (_, _, _, eventPaths, _, _) in
  for p in convertFSEventPaths(eventPaths) {
    print("Detected change in \(p)")
  }
  
  // Flush stdout to ensure it's printed immediately
  fflush(stdout)
}
```

If we add these modifications to our script, it now prints the folder in which a change occurred -- for example, if I edit a file `/Users/alexwlchan/books/Reading List.txt`, it prints the parent folder `/Users/alexwlchan/Desktop/books`.

```console
$ swift watch_for_changed_folders.swift
Listening for changes in /Users/alexwlchan/Desktop, /Users/alexwlchan/Documents
Detected change in /Users/alexwlchan/Desktop/
Detected change in /Users/alexwlchan/Desktop/books/
Detected change in /Users/alexwlchan/Documents/My notes/
^C
Stopping listener...
```

One thing I noticed is that a single operation can sometimes emit multiple filesystem events -- for example, if I save a file in my text editor, that emits two events.
I'm guessing that's one event to write the contents of the file, one event to update the metadata, but I'm not sure.

Because I don't need fine-grained resolution of filesystem events, I use a `Set(…)` to de-duplicate events:

```swift {"names":{"1":"callback","3":"eventPaths","4":"p"}}
let callback: FSEventStreamCallback = { (_, _, _, eventPaths, _, _) in
  for p in Set(convertFSEventPaths(eventPaths)) {
    print("Detected change in \(p)")
  }
  
  // Flush stdout to ensure it's printed immediately
  fflush(stdout)
}
```

If we're interested in the individual files rather than the directories, we can use the [`kFSEventStreamCreateFlagFileEvents` flag][cs-kFSEventStreamCreateFlagFileEvents]:

```swift {"names":{"1":"flags"}}
let flags = FSEventStreamCreateFlags(
  kFSEventStreamCreateFlagFileEvents | kFSEventStreamCreateFlagUseCFTypes
)
```

This shows us every file which is changing, and often reveals clues about how our computers work under the hood -- for example, when I took a screenshot, we can see it got saved to a hidden file first (`.Screenshot`), before being moved into its final location.

```console
$ swift watch_for_changed_files.swift
Listening for changes in /Users/alexwlchan/Desktop, /Users/alexwlchan/Documents
Detected change in /Users/alexwlchan/Desktop/greeting.txt
Detected change in /Users/alexwlchan/Desktop/greeting.txt
Detected change in /Users/alexwlchan/Desktop/.Screenshot 2026-05-09 at 10.45.42.png
Detected change in /Users/alexwlchan/Desktop/Screenshot 2026-05-09 at 10.45.42.png
Detected change in /Users/alexwlchan/Desktop/.DS_Store
```

Here's the complete script:

<details>
<summary><code>watch_for_changed_files.swift</code></summary>
  
```swift {"names":{"1":"Foundation","2":"convertFSEventPaths","3":"eventPaths","6":"cfArray","14":"createFSEventStream","15":"pathsToWatch","18":"callback","21":"p","28":"context","31":"sinceWhen","34":"latency","35":"flags","39":"eventStream","50":"cleanupEventStream","51":"eventStream","59":"registerCleanup","60":"eventStream","63":"signals","67":"sources","69":"sig","92":"home","96":"pathsToWatch","103":"eventStream","106":"cleanup","109":"queue"}}
#!/usr/bin/env swift
/// Watch for changed files in a directory, and print the paths of
/// changed files.
///
/// Example:
///
///     $ swift scripts/watch_for_changed_files.swift ~/Desktop/ ~/Documents/
///     Listening for changes in /Users/alexwlchan/Desktop/, /Users/alexwlchan/Documents/
///     Detected change in /Users/alexwlchan/Desktop/greeting.txt
///     Detected change in /Users/alexwlchan/Desktop/booktracker/index.html
///     Detected change in /Users/alexwlchan/Documents/proposal.pdf
///

import Foundation

/// Convert a raw pointer from an FSEvent callback into a Swift String.
///
/// FSEventStream must be created with 'kFSEventStreamCreateFlagUseCFTypes'
func convertFSEventPaths(_ eventPaths: UnsafeRawPointer) -> [String] {
  let cfArray = Unmanaged<CFArray>.fromOpaque(eventPaths)
  return cfArray.takeUnretainedValue() as! [String]
}

/// Create a new file system events stream that watches for changes
/// in the given directories.
func createFSEventStream(_ pathsToWatch: [String]) -> FSEventStreamRef {
  let callback: FSEventStreamCallback = { (_, _, _, eventPaths, _, _) in
    for p in Set(convertFSEventPaths(eventPaths)) {
      print("Detected change in \(p)")
    }
    
    fflush(stdout)
  }

  let context: UnsafeMutablePointer<FSEventStreamContext>? = nil
  let sinceWhen = FSEventStreamEventId(kFSEventStreamEventIdSinceNow)
  let latency = 0.01
  let flags = FSEventStreamCreateFlags(
    kFSEventStreamCreateFlagFileEvents | kFSEventStreamCreateFlagUseCFTypes
  )

  guard let eventStream = FSEventStreamCreate(
    kCFAllocatorDefault, callback, context, pathsToWatch as CFArray, sinceWhen, latency, flags
  ) else {
    fatalError("Failed to create FSEventStream: check your paths or permissions.")
  }

  return eventStream
}

/// Stop a file system events stream, invalidate it, and release our
/// reference to it.
func cleanupEventStream(_ eventStream: FSEventStreamRef) {
  FSEventStreamStop(eventStream)
  FSEventStreamInvalidate(eventStream)
  FSEventStreamRelease(eventStream)
}

/// Register cleanup handlers for SIGINT, SIGTERM and SIGHUP that
/// clean up the event stream when the script exits.
///
/// Returns an array of `DispatchSourceSignal`; the caller must hold
/// a reference to these in a global variable, or they will be cancelled.
func registerCleanup(_ eventStream: FSEventStreamRef) -> [DispatchSourceSignal] {
  let signals = [SIGINT, SIGTERM, SIGHUP]
  var sources: [DispatchSourceSignal] = []

  for sig in signals {
    let signalSource = DispatchSource.makeSignalSource(signal: sig, queue: .main)
    signalSource.setEventHandler {
      print("\nStopping listener...")
      cleanupEventStream(eventStream)
      exit(0)
    }

    signal(sig, SIG_IGN)
    signalSource.activate()
    sources.append(signalSource)
  }

  return sources
}

// Choose which folders to watch.
let home = URL(fileURLWithPath: NSHomeDirectory())
let pathsToWatch = [
  home.appendingPathComponent("Desktop").path,
  home.appendingPathComponent("Documents").path
]

// Create the event stream.
let eventStream = createFSEventStream(pathsToWatch)

// Register cleanup handlers that will run when the script exits.
let cleanup = registerCleanup(eventStream)

// Schedule the event stream and start listening for changes.
let queue = DispatchQueue(label: "net.alexwlchan.watch_file_changes")
FSEventStreamSetDispatchQueue(eventStream, queue)
FSEventStreamStart(eventStream)

print("Listening for changes in \(pathsToWatch.joined(separator: ", "))")

dispatchMain()
```

</details>

This is great if I'm writing a Swift app -- but my static site generator is written in Python, so I'd really like to know about these changes in Python.
How can I pass this information to a Python script?


## Connecting Swift to Python

### Building a bridge with stdout and subprocess

I want my Python code to invoke the Swift script as a new process, specify what directories it wants to watch, and read lines from stdout to see which files changed.

This means I have to change the Swift script in three ways:

1.  Allow passing a list of directories to watch as command-line arguments;
2.  Write the `Listening for changes` and `Stopping listener` messages to stderr;
3.  Change the `Detected change` message to print just the path of the changed file.

What's nice is that there's nothing Python-specific about this mechanism; you could use this to expose a stream of changed files in any language.
(Although in practice I'll only use it in Python, which I use for the majority of my recreational coding.)

I briefly considered trying to create some Python-Swift bridge, similar to what I did with [`clonefile()` last year][clonefile], but I couldn't work out how to do it without bringing in more dependencies.
Plus, it would have been a Python-only solution.

Here's the updated Swift script:

<details>
<summary><code>watch_for_changed_files.swift [DIRS...]</code></summary>

```swift {"names":{"1":"Foundation","2":"convertFSEventPaths","3":"eventPaths","6":"cfArray","14":"createFSEventStream","15":"pathsToWatch","18":"callback","21":"p","28":"context","31":"sinceWhen","34":"latency","35":"flags","39":"eventStream","50":"cleanupEventStream","51":"eventStream","59":"registerCleanup","60":"eventStream","63":"signals","67":"sources","69":"sig","94":"pathsToWatch","103":"eventStream","106":"cleanup","109":"queue"}}
#!/usr/bin/env swift
/// Watch for changed files in a directory, and print the paths of
/// changed files to stdout.
///
/// Example:
///
///     $ swift scripts/watch_for_changed_files.swift ~/Desktop/ ~/Documents/
///     Listening for changes in /Users/alexwlchan/Desktop/, /Users/alexwlchan/Documents/
///     /Users/alexwlchan/Desktop/greeting.txt
///     /Users/alexwlchan/Desktop/booktracker/index.html
///     /Users/alexwlchan/Documents/proposal.pdf
///

import Foundation

/// Convert a raw pointer from an FSEvent callback into a Swift String.
///
/// FSEventStream must be created with 'kFSEventStreamCreateFlagUseCFTypes'
func convertFSEventPaths(_ eventPaths: UnsafeRawPointer) -> [String] {
  let cfArray = Unmanaged<CFArray>.fromOpaque(eventPaths)
  return cfArray.takeUnretainedValue() as! [String]
}

/// Create a new file system events stream that watches for changes
/// in the given directories.
func createFSEventStream(_ pathsToWatch: [String]) -> FSEventStreamRef {
  let callback: FSEventStreamCallback = { (_, _, _, eventPaths, _, _) in
    for p in Set(convertFSEventPaths(eventPaths)) {
      print(p)
    }
    
    fflush(stdout)
  }

  let context: UnsafeMutablePointer<FSEventStreamContext>? = nil
  let sinceWhen = FSEventStreamEventId(kFSEventStreamEventIdSinceNow)
  let latency = 0.01
  let flags = FSEventStreamCreateFlags(
    kFSEventStreamCreateFlagFileEvents | kFSEventStreamCreateFlagUseCFTypes
  )

  guard let eventStream = FSEventStreamCreate(
    kCFAllocatorDefault, callback, context, pathsToWatch as CFArray, sinceWhen, latency, flags
  ) else {
    fatalError("Failed to create FSEventStream: check your paths or permissions.")
  }

  return eventStream
}

/// Stop a file system events stream, invalidate it, and release our
/// reference to it.
func cleanupEventStream(_ eventStream: FSEventStreamRef) {
  FSEventStreamStop(eventStream)
  FSEventStreamInvalidate(eventStream)
  FSEventStreamRelease(eventStream)
}

/// Register cleanup handlers for SIGINT, SIGTERM and SIGHUP that
/// clean up the event stream when the script exits.
///
/// Returns an array of `DispatchSourceSignal`; the caller must hold
/// a reference to these in a global variable, or they will be cancelled.
func registerCleanup(_ eventStream: FSEventStreamRef) -> [DispatchSourceSignal] {
  let signals = [SIGINT, SIGTERM, SIGHUP]
  var sources: [DispatchSourceSignal] = []

  for sig in signals {
    let signalSource = DispatchSource.makeSignalSource(signal: sig, queue: .main)
    signalSource.setEventHandler {
      fputs("\nStopping listener...\n", stderr)
      cleanupEventStream(eventStream)
      exit(0)
    }

    signal(sig, SIG_IGN)
    signalSource.activate()
    sources.append(signalSource)
  }

  return sources
}

// Choose which folders to watch.
let pathsToWatch: [String]
if CommandLine.arguments.count > 1 {
  pathsToWatch = Array(CommandLine.arguments.dropFirst())
} else {
  pathsToWatch = ["."]
}

// Create the event stream.
let eventStream = createFSEventStream(pathsToWatch)

// Register cleanup handlers that will run when the script exits.
let cleanup = registerCleanup(eventStream)

// Schedule the event stream and start listening for changes.
let queue = DispatchQueue(label: "net.alexwlchan.watch_file_changes")
FSEventStreamSetDispatchQueue(eventStream, queue)
FSEventStreamStart(eventStream)

fputs("Listening for changes in \(pathsToWatch.joined(separator: ", "))\n", stderr)

dispatchMain()
```

</details>

And here's the first Python function I came up with:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"pathlib","5":"Path","6":"subprocess","7":"watch_for_changed_files","8":"dirs","13":"cmd","16":"d","18":"proc","27":"line","37":"p"}}
from collections.abc import Iterator
from pathlib import Path
import subprocess


def watch_for_changed_files(*dirs: str | Path) -> Iterator[Path]:
    """
    Watch one or more directory trees for changes, and yield the paths of
    files when they change.
    """
    cmd = ["swift", "watch_for_changed_files.swift"] + [str(d) for d in dirs]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)

    try:
        for line in proc.stdout:
            yield Path(line.strip())
    finally:
        proc.terminate()
        proc.wait()


for p in watch_for_changed_files("/Users/alexwlchan/Desktop"):
    print(p)
```

This function uses the [`subprocess module`][pydoc-subprocess] to start my Swift script in a new process, then it reads lines from `proc.stdout` and yields them to the caller.
The caller gets a stream of changed file paths, and doesn't need to worry about the underlying process.

The function will keep iterating over `proc.stdout` while `stdout` stays open, which lasts as long as the Swift process is running.
It's a long-running listener that only stops when I break out of the loop (whether with an explicit `break`, an exception, or stopping the whole Python script).

The `text=True` parameter means stdout will be opened in text mode rather than binary mode, and `bufsize=1` means the output will be line-buffered, so `proc.stdout` will be flushed every time the Swift script writes a newline.
(This pairs with `fflush(stdout)` in the Swift script to ensure there's no buffering delay when I get a filesystem event.)

The `try … finally` construction ensures the process is stopped and cleaned up correctly when I'm done.

In my live reload script, I can now do an incremental rebuild that only rebuilds parts of the site that have changed.
If I've changed the base template?
Rebuild the entire site.
If I've edited an article?
Only one page needs to change.
This is more efficient and makes rebuilds much faster.

### Debouncing with non-blocking I/O and selectors

One problem with this function is that it doesn't do [debouncing][mdn-debouncing].
If I change a lot of files at once -- say, a bulk find and replace -- this function will emit every file separately, kicking off a bunch of redundant rebuilds.
If I change ten files at once, I only need to do one rebuild, not ten.

What I'd like to do is coalesce all the changes that have happened since the last rebuild into a single event, then use them to inform the next rebuild.
You can do some of this coalescing in Swift by tweaking the `latency` parameter, but that doesn't work here because the latency is variable.
The length of a rebuild can vary from a hundred milliseconds to multiple seconds, depending on how much of the site is being rebuilt.

What I'd like to do is read everything that's available in `proc.stdout`, emit that to the caller, then wait for something else to be written.
By default, reading from `proc.stdout` is a blocking operation -- if we call `read()` and there's nothing available, it waits until there's something for us to read.
To debounce, we'll need to change this behaviour.

First, we change `proc.stdout` to be non-blocking:

```python {"names":{"1":"os"}}
import os

os.set_blocking(proc.stdout.fileno(), False)
```

Then, we need to know when anything has been written to stdout, so we can read all the available output and emit it to the caller.
We could poll `proc.stdout` repeatedly and look for non-empty output, but that would be very inefficient -- a better approach would be to use the [`selectors` module][pydoc-selectors] and get notified when something gets written.

We create a selector that waits until there's data waiting to be read from `proc.stdout`:

```python {"names":{"1":"selectors","2":"sel"}}
import selectors

sel = selectors.DefaultSelector()
sel.register(proc.stdout, selectors.EVENT_READ)
```

Then, we call the [`select()` method][pydoc-selectors-select], which blocks until an event is ready.
At that point, we read everything that's available `proc.stdout` and deliver it as a single changeset to the caller.
For some use cases you might want to capture and inspect the event, but here it's enough to know that an event was emitted, and start reading stdout:

```python {"names":{"3":"captured_paths","5":"line"}}
while True:
    sel.select()
    
    captured_paths = set()
  
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        captured_paths.add(Path(line.strip()))
  
    yield captured_paths
```

This changes the signature of the overall function, because now we're emitting changesets instead of single files.
Here's the updated function:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"os","5":"pathlib","6":"Path","7":"selectors","8":"subprocess","9":"watch_for_changed_files","10":"dirs","16":"cmd","21":"proc","35":"sel","46":"captured_paths","48":"line"}}
from collections.abc import Iterator
import os
from pathlib import Path
import selectors
import subprocess


def watch_for_changed_files(*dirs: str | Path) -> Iterator[set[Path]]:
    """
    Watch one or more directory trees for changes, and yield the paths of
    files when they change.
    """
    cmd = ["swift", "scripts/watch_for_changed_files.swift"] + [str(d) for d in dirs]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)
    
    os.set_blocking(proc.stdout.fileno(), False)
    
    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ)

    try:
        while True:
            sel.select()
    
            captured_paths = set()
    
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                captured_paths.add(Path(line.strip()))
    
            yield captured_paths
    finally:
        proc.terminate()
        proc.wait()
```

## The result

Here's a diagram which illustrates the code we've written: the FSEvents API emits an event to our Swift script, that prints the file paths to stdout, where they get read by a Python script that kicks off a site rebuild.
(Click for a larger version.)

<figure>
  {%
    inline_svg
    filename="macos-file-watcher.svg"
    alt="Sequence diagram showing the movement of messages between 'Filesystem events', 'Swift script', 'stdout (pipe)' and 'Python script'."
    link_to="original"
    class="dark_aware"
  %}
</figure>

In informal benchmarking, there's about 2–4 milliseconds between the on-disk modified time of a file and it being picked up by this function.
Given file changes only occur when I do something, this is plenty fast enough.
(I could click the "save" button as fast as I could, and the code would still have time for a long nap between consecutive clicks.)

Both the Swift and the Python code pause until something interesting happens, so this is very efficient -- no aggressive polling that could hurt my battery life or SSD longevity.

## Closing thoughts

Before I started this script, the only way I knew how to track file changes was by polling, which is undesirable for a number of reasons.
I wasn't sure if I could write an alternative, but now it's done, I'm proud of the result.

I learnt a lot about topics I only vaguely understood before, including the macOS FSEvents API, how blocking and non-blocking I/O works in Python, and using the `selectors` module.
Explaining it all for this article has cemented that learning, and I understand every line of this code.

I'm pleased I can do this without adding third-party dependencies, especially for something as low-level as filesystem access.
Even if I eventually replace this code with a library, I'll have a better mental model of how it works.

I'm surprised by how much this has improved my workflow.
I was waiting 5 to 10 seconds with Jekyll; now, my browser reloads almost instantly with new changes.
Everything feels a lot smoother, and it's renewed my interest in working on the site.

In [my next post][me-http-long-polling], I'll explain how I combine this watcher with HTTP long polling to trigger an automatic browser refresh the moment the rebuild finishes.

[apple-fsevents-guide]: https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/FSEvents_ProgGuide/UsingtheFSEventsFramework/UsingtheFSEventsFramework.html
[apple-fsevents-guide-using]: https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/FSEvents_ProgGuide/UsingtheFSEventsFramework/UsingtheFSEventsFramework.html#//apple_ref/doc/uid/TP40005289-CH4-SW4
[cs-FSEventStreamCreate]: https://developer.apple.com/documentation/coreservices/1443980-fseventstreamcreate
[cs-FSEventStreamCallback]: https://developer.apple.com/documentation/coreservices/fseventstreamcallback
[cs-FSEventStreamScheduleWithRunLoop]: https://developer.apple.com/documentation/coreservices/1447824-fseventstreamschedulewithrunloop
[cs-FSEventStreamSetDispatchQueue]: https://developer.apple.com/documentation/coreservices/1444164-fseventstreamsetdispatchqueue
[cs-kFSEventStreamCreateFlagUseCFTypes]: https://developer.apple.com/documentation/coreservices/kfseventstreamcreateflagusecftypes
[cs-kFSEventStreamCreateFlagFileEvents]: https://developer.apple.com/documentation/coreservices/1455376-fseventstreamcreateflags/kfseventstreamcreateflagfileevents
[dispatch-makeSignalSource]: https://developer.apple.com/documentation/dispatch/dispatchsource/makesignalsource(signal:queue:)
[gh-python-livereload]: https://github.com/lepture/python-livereload
[me-http-long-polling]: /2026/livereload-in-browser/
[mosaic]: /2026/mosaic/
[pypi-fswatch]: https://pypi.org/project/fswatch/
[pypi-inotify]: https://pypi.org/project/inotify/
[pypi-watchdog]: https://pypi.org/project/watchdog/
[pydoc-selectors]: https://docs.python.org/3/library/selectors.html#module-selectors
[pydoc-selectors-select]: https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.select
[pydoc-subprocess]: https://docs.python.org/3/library/subprocess.html#module-subprocess
[clonefile]: /2025/cloning-with-python/
[mdn-debouncing]: https://developer.mozilla.org/en-US/docs/Glossary/Debounce
