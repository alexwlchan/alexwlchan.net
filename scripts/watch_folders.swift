// Watch for changes in the specified directories, and print
// directories with changes to stdout.

import Foundation




// TODO: Allow passing multiple paths to this script.
let pathsToWatch = CommandLine.arguments.count > 1 ? [CommandLine.arguments[1]] : ["."]

fputs("Watching for changes in \(pathsToWatch[0])\n", stderr)

let callback: FSEventStreamCallback = { (_, _, _, eventpathsToWatchs, _, _) in
  // TODO: Can I simplify this line?
  // https://developer.apple.com/documentation/swift/unsafebitcast(_:to:)
  let pathsToWatchs = Unmanaged<CFArray>.fromOpaque(eventpathsToWatchs).takeUnretainedValue() as! [String]

  for pathsToWatch in Set(pathsToWatchs) {
    let output = "\(pathsToWatch)\n"
    if let data = output.data(using: .utf8) {
      FileHandle.standardOutput.write(data)
    }
  }

  // Flush stdout to ensure it's printed immediately
  fflush(stdout)
}

let sinceWhen = FSEventStreamEventId(kFSEventStreamEventIdSinceNow)
let latency = 0.1
let flags = FSEventStreamCreateFlags(
  kFSEventStreamCreateFlagUseCFTypes | kFSEventStreamCreateFlagNoDefer
  // TODO: Use kFSEventStreamCreateFlagFileEvents instead
  // | kFSEventStreamCreateFlagFileEvents
)

// TODO: Improve error handling here
let eventStream = FSEventStreamCreate(
  kCFAllocatorDefault, callback, nil, pathsToWatch as CFArray, sinceWhen, latency, flags
)!

let queue = DispatchQueue(label: "net.alexwlchan.watcher")

FSEventStreamSetDispatchQueue(eventStream, queue)
FSEventStreamStart(eventStream)

dispatchMain()
