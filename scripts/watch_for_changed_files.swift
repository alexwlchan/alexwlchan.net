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