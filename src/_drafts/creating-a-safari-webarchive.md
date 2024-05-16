---
layout: post
title: Creating a Safari webarchive from the command line
summary: We can use the `createWebArchiveData` method on `WKWebView` to write a Swift script that creates Safari webarchive files.
tags:
  - swift
  - digital-preservation
  - safari
colors:
  index_dark:  "#e9eaec"
  index_light: "#2076cc"
---

{% comment %}
  Card image based on https://pixabay.com/photos/compass-orientation-map-address-5261062/
{% endcomment %}

Recently I've been trying to create a local archive of my bookmarked web pages.
I already have tools to [take screenshots] and I love them as a way to take quick snapshots and skim the history of a site, but bitmap images aren't a great archival representation of a website.
What if I want to save the HTML, CSS, and JavaScript, and keep an interactive copy of the page?

There are lots of tools in this space; for my personal stuff I've come to like [Safari webarchives].
There are several reasons I find them appealing:

*   **Each saved web page is stored as a single file.**
    Each file includes the entire content of the page, and a single file per web page is pretty manageable.
    I can create backups, keep multiple copies, and so on.

*   **I can easily add pages to my archive that can't be crawled from the public web.**
    Lots of the modern web is locked behind paywalls, login screens, interstitial modals that are difficult for automated crawlers to get past.
    It's much easier for me to get through them as a human using Safari as my default browser.
    Once I have a page open, I can save it as a webarchive with the `File > Save As…` menu item.

*   **The archive can be stored locally and offline.**
    It will always remain available to me, as long as I keep up with backups and maintenance, and I can archive private web pages that I don't want to put in somebody else's archive.
    (For example, I wouldn't want to save private tweets in the publicly available Wayback Machine.)

*   **I can read the format without Safari.**
    Although Safari is only maintained by Apple, the Safari webarchive format can be read by non-Apple tools -- it's a [binary property list](/til/2024/whats-inside-safari-webarchive/) that stores the raw bytes of the original files.
    I'm comfortable that I'll be able to open these archives for a while, even if Safari unexpectedly goes away.

The one thing that's missing is a way to create webarchive files programatically.
Although I could open each page and save it in Safari individually, I have about 6000 bookmarks -- I'd like a way to automate this process.

I was able to write a short script in Swift that does this for me.

[take screenshots]: /2024/scheduled-screenshots/
[Safari webarchives]: https://en.wikipedia.org/wiki/Webarchive
[github]: https://github.com/newzealandpaul/webarchiver

## Prior art: newzealandpaul/webarchiver

I found an existing tool for creating Safari webarchives on the command line, [written by newzealandpaul][github].

I did some brief testing and it seems to work, but I had a few issues.
Some of my bookmarks failed to archive with an error like "invalid URL", even though the URL worked just fine in Safari and other browsers.
I went to read the code to work out what was happening, but it's written in Objective-C and uses deprecated classes like [`WebView`](https://developer.apple.com/documentation/webkit/webview) and [`WebArchive`](https://developer.apple.com/documentation/webkit/webarchive).

Given that it’s only about 350 lines of code, I wanted to see if I could rewrite it using Swift and the newest classes.
I thought that might be easier than trying to understand a language and classes that I'm not super familiar with.





## Playing with `WKWebView` and `createWebArchiveData`

It didn't take much googling to learn that `WebView` has been replaced by [`WKWebView`][WKWebView], and that class has a method [`createWebArchiveData`][createWebArchiveData] which "creates a web archive of the web view's current contents asynchronously".
Perfect!

I watched a [WWDC session] by Brady Eison, a WebKit engineer, where the `createWebArchiveData` API was introduced.
It gave me some useful context about the purpose of `WKWebView` -- it's for rendering web content inside Mac and iOS apps.
If you've ever used an in-app browser, there was probably an instance of `WKWebView` somewhere underneath.

There's some sample code for using this API, which I fashioned into an initial script:

```swift
import WebKit

let url = URL(string: "https://example.com/")
let savePath = URL(fileURLWithPath: "example.webarchive")

let webView = WKWebView()
let request = URLRequest(url: url!)

webView.load(request)

// https://developer.apple.com/videos/play/wwdc2020/10188/?time=1327
webView.createWebArchiveData(completionHandler: { result in
  do {
    let data = try result.get()
    try data.write(to: savePath)
  } catch {
    print("Unable to save webarchive file: \(error.localizedDescription)")
  }
})
```

I saved this code as `create_webarchive.swift`, and ran it on the command line:

```console
$ swift create_webarchive.swift
```

I was hoping that this would load `https://example.com/`, and save a webarchive of the page to `example.webarchive`.
The script completed successfully, but it only created an empty file.

I did a little debugging, and I realised that my `WKWebView` was never actually loading the web page.
I pointed it at a local web server, and even when I added a long sleep to the script, it never started fetching data from the server.
Hmm.

[WKWebView]: https://developer.apple.com/documentation/webkit/wkwebview
[createWebArchiveData]: https://developer.apple.com/documentation/webkit/wkwebview/3650491-createwebarchivedata
[WWDC session]: https://developer.apple.com/videos/play/wwdc2020/10188/





## We need a loop-de-loop

Using a `WKWebView` inside a Swift script isn't how it's normally used.
Most of the time, it appears as part of a web browser inside a Mac or iOS app.
In that context, you don't want fetching web pages to be a blocking operation -- you want the rest of the app to remain responsive and usable, and download the web page as a background operation.

This made me wonder if my problem was that my script doesn't have "background operations".
When I ask `WKWebView` to load my page, it's getting shoved in a queue of background tasks, but nothing is picking up work from that queue.
I don't fully understand what I did next, but I think I've got the gist of the problem.

I had another look at newzealandpaul's code, and I found [some lines](https://github.com/newzealandpaul/webarchiver/blob/4d04669a9cb3f8a7e5ab492e7c3a4175b5586ac5/KBWebArchiver.m#L214-L222) that look a bit like they're solving the same problem.
I think the `NSRunLoop` is doing work that's on that background queue, and it's waiting until the page has finished loading:

```objectivec
// Wait until the site has finished loading.
NSRunLoop *currentRunLoop = [NSRunLoop currentRunLoop];
NSTimeInterval resolution = _localResourceLoadingOnly ? 0.1 : 0.01;
BOOL isRunning = YES;

while (isRunning && _finishedLoading == NO) {
  NSDate *next = [NSDate dateWithTimeIntervalSinceNow:resolution];
  isRunning = [currentRunLoop runMode:NSDefaultRunLoopMode beforeDate:next];
}
```

I was able to adapt this idea for my Swift script, using `RunLoop.main.run()`.
I can track the progress of `WKWebView` with the `isLoading` attribute, so I kept running the main loop for short intervals until I could see this attribute is false.
One thing I realised is that `createWebArchiveData` is also an asynchronous operation that needs to run in the background, so I also need to wait for that to finish.

I added these two functions to `WKWebView`.
Here's my updated script:

```swift
import WebKit

let urlString = "https://www.example.com"
let savePath = URL(fileURLWithPath: "example.webarchive")

extension WKWebView {

  /// Load the given URL in the web view.
  ///
  /// This method will block until the URL has finished loading.
  func load(_ urlString: String) {
    if let url = URL(string: urlString) {
      let request = URLRequest(url: url)
      self.load(request)

      while (self.isLoading) {
        RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
      }
    } else {
      fputs("Unable to use \(urlString) as a URL\n", stderr)
      exit(1)
    }
  }

  /// Save a copy of the web view's contents as a webarchive file.
  ///
  /// This method will block until the webarchive has been saved,
  /// or the save has failed for some reason.
  func saveAsWebArchive(savePath: URL) {
    var isSaving = true

    self.createWebArchiveData(completionHandler: { result in
      do {
        let data = try result.get()
        try data.write(to: savePath)
        isSaving = false
      } catch {
        fputs("Unable to save webarchive file: \(error.localizedDescription)\n", stderr)
        exit(1)
      }
    })

    while (isSaving) {
      RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
    }
  }
}

let webView = WKWebView()

webView.load(urlString)
webView.saveAsWebArchive(savePath: savePath)
```

This works, but there's a fairly glaring hole -- it will archive whatever got loaded into the web view, even if the page wasn't loaded successfully.
Let's fix that next.





## The final script

```swift
#!/usr/bin/env swift
/// Save a web page as a Safari webarchive.
///
/// Usage: save_safari_webarchive [URL] [OUTPUT_PATH]
///
/// This will save the page to the desired file, but may fail for
/// several reasons:
///
///   - the web page can't be loaded
///   - the web page returns a non-200 status code
///   - there's already a file at that path (it won't overwrite an existing
///     webarchive)
///

import WebKit

/// Print an error message and terminate the process if there are
/// any errors while loading a page.
class ExitOnFailureDelegate: NSObject, WKNavigationDelegate {
  func webView(_: WKWebView, didFail: WKNavigation!, withError error: Error) {
    fputs("Failed to load web page: \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _: WKWebView,
    didFailProvisionalNavigation: WKNavigation!,
    withError error: Error
  ) {
    fputs("Failed to load web page: \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _: WKWebView,
    decidePolicyFor navigationResponse: WKNavigationResponse,
    decisionHandler: (WKNavigationResponsePolicy) -> Void
  ) {
    if let httpUrlResponse = (navigationResponse.response as? HTTPURLResponse) {
      if httpUrlResponse.statusCode != 200 {
        fputs("Loading web page failed with status code \(httpUrlResponse.statusCode)\n", stderr)
        exit(1)
      }
    }

    decisionHandler(.allow)
  }
}

let webView = WKWebView()

let delegate = ExitOnFailureDelegate()
webView.navigationDelegate = delegate

extension WKWebView {

  /// Load the given URL in the web view.
  ///
  /// This method will block until the URL has finished loading.
  func load(_ urlString: String) {
    if let url = URL(string: urlString) {
      let request = URLRequest(url: url)
      self.load(request)

      while (self.isLoading) {
        RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
      }
    } else {
      fputs("Unable to use \(urlString) as a URL\n", stderr)
      exit(1)
    }
  }

  /// Save a copy of the web view's contents as a webarchive file.
  ///
  /// This method will block until the webarchive has been saved,
  /// or the save has failed for some reason.
  func saveAsWebArchive(savePath: URL) {
    var isSaving = true

    self.createWebArchiveData(completionHandler: { result in
      do {
        let data = try result.get()
        try data.write(
          to: savePath,
          options: [Data.WritingOptions.withoutOverwriting]
        )
        isSaving = false
      } catch {
        fputs("Unable to save webarchive file: \(error.localizedDescription)\n", stderr)
        exit(1)
      }
    })

    while (isSaving) {
      RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
    }
  }
}

guard CommandLine.arguments.count == 3 else {
    print("Usage: \(CommandLine.arguments[0]) <URL> <OUTPUT_PATH>")
    exit(1)
}

let urlString = CommandLine.arguments[1]
let savePath = URL(fileURLWithPath: CommandLine.arguments[2])

webView.load(urlString)
webView.saveAsWebArchive(savePath: savePath)

print("Saved webarchive to \(savePath)")
```

## Checking the page loaded successfully with `WKNavigationDelegate`

If there's some error getting the page -- say, my Internet connection is down or the remote server doesn't respond -- the `WKWebView` will still complete loading and set `isLoading = false`.
My code will then proceed to archive the error page, which is unhelpful.
I'd rather the script threw an error, and prompted me to investigate.

While I was reading more about `WKWebView`, I came across the [`WKNavigationDelegate`][WKNavigationDelegate] protocol.
If you implement this protocol, you can track the progress of a page load, and get detailed events like "the page has started to load" and "the page failed to load with an error".

Among other things, this lets you track the progress of a page load, and it gives you more fine-grained events like "started loading" and "loading failed with an error".

There are [two methods][failures] you can implement to handle errors, which will be called if an error occurs during page load.
Because I'm working in a standalone script, I simply wrote two methods that print an error message and then terminate the entire process -- I don't need more sophisticated error handling than that.

I also wrote a method that checks the HTTP status code of the response, and terminates the script if it's not an HTTP 200 OK.

```swift
/// Print an error message and terminate the process if there are
/// any errors while loading a page.
class ExitOnFailureDelegate: NSObject, WKNavigationDelegate {
  func webView(_: WKWebView, didFail: WKNavigation!, withError error: Error) {
    fputs("Failed to load web page: \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _: WKWebView, didFailProvisionalNavigation: WKNavigation!,
    withError error: Error
  ) {
    fputs("Failed to load web page: \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _: WKWebView,
    decidePolicyFor navigationResponse: WKNavigationResponse,
    decisionHandler: (WKNavigationResponsePolicy) -> Void
  ) {
    if let httpUrlResponse = (navigationResponse.response as? HTTPURLResponse) {
      if httpUrlResponse.statusCode != 200 {
        fputs("Failed to load web page: got status code \(httpUrlResponse.statusCode)\n", stderr)
        exit(1)
      }
    }

    decisionHandler(.allow)
  }
}

let webView = WKWebView()

let delegate = ExitOnFailureDelegate()
webView.navigationDelegate = delegate
```

To check this error handling worked correctly, I tried loading a website while I was offline, a domain name that doesn't go anywhere, and a page that 404s on my own website.
All three failed as I want:

```console
$ swift save_webarchive.swift
Failed to load web page: The Internet connection appears to be offline.

$ swift save_webarchive.swift
Failed to load web page: A server with the specified hostname could not be found.

$ swift save_webarchive.swift
Failed to load web page: got status code 404
```

[failures]: https://developer.apple.com/documentation/webkit/wknavigationdelegate#2172386





## Adding some command-line arguments

Right now the URL string and save location are both hard-coded; I wanted to make them command-line arguments.
I can do this by inspecting `CommandLine.arguments`:

```swift
guard CommandLine.arguments.count == 3 else {
    print("Usage: \(CommandLine.arguments[0]) <URL> <OUTPUT_PATH>")
    exit(1)
}

let urlString = CommandLine.arguments[1]
let savePath = URL(fileURLWithPath: CommandLine.arguments[2])
```

For more complex command-line interfaces, Apple has an open-source [`ArgumentParser` library][ArgumentParser], but I'm not sure how I'd use that in a standalone script.

```console
$ swift s.swift
Usage: s.swift <URL> <OUTPUT_PATH>

$ swift save_webarchive.swift https://example.com example.webarchive
```

[ArgumentParser]: https://www.swift.org/blog/argument-parser/





## The final script

run over 6000 bookmarks, result?
cleaned up about 30 or so bookmarks with bad or duplicate URLs
(e.g. HTTP and HTTPS)

* improved error messages
* some web pages fail to load with timeout
* HTTP 204?

  3%|█▏                                    | 188/6153 [03:37<5:39:45,  3.42s/it]Failed to load https://authory.com/SwapnaKrishna/On-Star-Trek-Discovery-and-Michelle-Yeohs-accent-aa6d2eb01b3a24970abf406c39146df33: The request timed out.

 13%|███████████████████████                                                                                                                                                             | 786/6145 [08:08<58:46,  1.52it/s] 13%|███████████████████████▎                                                                                                                                                          | 804/6145 [08:27<1:37:27,  1.09s/it]Failed to load https://www.thisishowtocode.com/blog/atomically-moving-files-to-a-network-drive-with-python/ (2): The certificate for this server is invalid. You might be connecting to a server that is pretending to be “www.thisishowtocode.com” which could put your confidential information at risk.



  24%|███████████████████████████████████████████▌                                                                                                                                       | 1480/6085 [02:18<35:09,  2.18it/s]Failed to load https://filmcrithulk.blog/2017/12/15/the-force-belongs-to-us-the-last-jedis-beautiful-refocusing-of-star-wars/amp/?__twitter_impression=true (2): too many HTTP redirects

AMP pages

 29%|████████████████████████████████████████████████████                                                                                                                               | 1769/6085 [04:59<37:56,  1.90it/s]Failed to load https://jekyllthemes.dev/ (2): An SSL error has occurred and a secure connection to the server cannot be made.

 56%|███████████████████████████████████████████████████████████████████████████████████████████████████▊                                                                               | 3357/6022 [12:25<45:45,  1.03s/it]Failed to load http://www.gaystarnews.com/article/youtube-stars-long-distance-relationship/: got status code 530



  51%|██████████████████████████████████████████████████████████████████████████████████████████▋                                                                                        | 3036/5990 [01:10<05:20,  9.21it/s]Failed to load http://www.weeklystandard.com/article/2540: got status code 522



The script will live [in my scripts repo](https://github.com/alexwlchan/scripts/blob/main/web/save_safari_webarchive).


doesn't fully replictae webarchiver
e.g. tools for overwriting webarchive data
and fixes for particular sites