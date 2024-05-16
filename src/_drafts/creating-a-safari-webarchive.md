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

(This is a personal archive, and nothing to do with my day job.)

There are lots of tools in this space; for my purposes I've come to like [Safari webarchives].
There are several reasons I find them appealing:

*   **Each saved web page is stored as a single file.**
    Each file includes the entire content of the page, and a single file per web page is a manageable amount of stuff.
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
    I'm comfortable that I'll be able to open these archives for a while.

The one thing that's missing is a way to create webarchive files programatically.
Although I could open each page and save it in Safari individually, I have about 6000 bookmarks -- I'd like a way to automate this process.

I was able to write a short script in Swift that does this for me.

[take screenshots]: /2024/scheduled-screenshots/
[Safari webarchives]: https://en.wikipedia.org/wiki/Webarchive
[github]: https://github.com/newzealandpaul/webarchiver

## Prior art: newzealandpaul/webarchiver

I found a tool for creating Safari webarchives on the command line, [written by newzealandpaul][github].

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
#!/usr/bin/env swift

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
    print("Encountered error: \(error)")
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





## Observing the (lack of) page loads with `WKNavigationDelegate`

While I was reading more about `WKWebView`, I came across the [`WKNavigationDelegate`][WKNavigationDelegate] protocol.

This allows you to control which sites can be loaded -- for example, the ACME app might allow you to visit pages on `https://acme.com/` with the in-app browser, but send you to the system browser for other sites.
This protocol can also track the progress of a "navigation request" -- that is, to know what a page starts and finishes loading.
The latter is more useful to this project.

I wrote another script which creates a `WKNavigationDelegate` that just logs when a request starts and finishes (either with a success or failure).

```swift
#!/usr/bin/env swift

import WebKit

let url = URL(string: "https://www.example.com/")

let webView = WKWebView()
let request = URLRequest(url: url!)

class LoggingDelegate: NSObject, WKNavigationDelegate {
  func webView(_: WKWebView, didStartProvisionalNavigation: WKNavigation!) {
    print("Started loading web page...")
  }

  func webView(_: WKWebView, didFinish: WKNavigation!) {
    print("Web page loaded successfully!")
  }

  func webView(_: WKWebView, didFailProvisionalNavigation: WKNavigation!, withError error: Error) {
    print("Web page failed to load! \(error.localizedDescription)")
  }
}

let navigationDelegate = LoggingDelegate()
webView.navigationDelegate = navigationDelegate

print("Starting script!")
webView.load(request)
print("Finishing script!")
```

This gave me further clues that my `WKWebView` was never actually loading anything from the web page -- I never saw any of the log messages from my navigation delegate:

```console
$ swift load_with_logging_delegate.swift
Starting script!
Finishing script!
```

Hmm.





## Time for a loop-de-loop

Using a `WKWebView` inside a Swift script isn't how it's normally used.
Most of the time, it appears as part of a web browser inside a Mac or iOS app.
In that context, you don't want fetching web pages to be a blocking operation -- you want the rest of the app to remain responsive and usable, and download the web page as a background operation.

This made me wonder if my problem was that my script doesn't have "background operations".
When I ask `WKWebView` to load my page, it's getting shoved in a queue of background tasks, but nothing is picking up that queue.
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

I was able to take this idea, and adapt it to my script.
My first attempt was just calling `RunLoop.main.run()` after I tell `WKWebView` to load a page:

```swift
print("Starting script!")
webView.load(request)
RunLoop.main.run()
print("Finishing script!")
```

I could see my navigation delegate log the completed request, but the script never stopped running -- the `RunLoop` is just going to run forever, because I never told it to stop.

The navigation delegate knows when my page has finished loading, so I added a boolean variable `isLoadingComplete`.
Then I can use that to control the `RunLoop` -- like the code in webarchiver, I run the loop for 0.1 seconds at a time, and keep running until the web page is fully loaded:

```swift
import WebKit

let url = URL(string: "https://www.example.com/")

let webView = WKWebView()
let request = URLRequest(url: url!)

class LoggingDelegate: NSObject, WKNavigationDelegate {
  var isLoadingComplete = false

  func webView(_: WKWebView, didStartProvisionalNavigation: WKNavigation!) {
    print("Started loading web page...")
  }

  func webView(_: WKWebView, didFinish: WKNavigation!) {
    print("Web page loaded successfully!")
    isLoadingComplete = true
  }

  func webView(_: WKWebView, didFailProvisionalNavigation: WKNavigation!, withError error: Error) {
    print("Web page failed to load! \(error.localizedDescription)")
    isLoadingComplete = true
  }
}

let navigationDelegate = LoggingDelegate()
webView.navigationDelegate = navigationDelegate

print("Starting script!")
webView.load(request)

while !navigationDelegate.isLoadingComplete {
  RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
}

print("Finishing script!")
```

And now I see the script start, load the web page correctly, then finish:

```console
$ swift run_with_loop.swift
Starting script!
Started loading web page...
Web page loaded successfully!
Finishing script!
```

[WKNavigationDelegate]: https://developer.apple.com/documentation/webkit/wknavigationdelegate





## Putting it together

---




---

Prior art: 

WKWebView: https://developer.apple.com/documentation/webkit/wkwebview
WKNavigationDelegate: https://developer.apple.com/documentation/webkit/wknavigationdelegate

```swift
import Foundation
import WebKit

// Function to load web page
func loadWebPage(fromURL url: URL) {
  let webView = WKWebView()
  let navigationDelegate = WebViewNavigationDelegate()
  webView.navigationDelegate = navigationDelegate

  print("Loading web page from URL: \(url)")
  webView.load(URLRequest(url: url))

  while !navigationDelegate.isLoadingComplete {
    RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))  // Run loop for 0.1 seconds
  }
}

// Custom navigation delegate to handle web view events
class WebViewNavigationDelegate: NSObject, WKNavigationDelegate {
  var isLoadingComplete = false

  func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
    print("Web page loaded successfully!")
    isLoadingComplete = true

    let savePath = FileManager.default.temporaryDirectory.appendingPathComponent(
      "example_web_archive.webarchive")

    print(savePath)

    // https://developer.apple.com/videos/play/wwdc2020/10188/?time=1327
    webView.createWebArchiveData(completionHandler: { (result: Result<Data, Error>) in
      // createWebArchiveDataWithCompletionHandler
      do {
        let data = try result.get()
        try data.write(to: savePath)
      } catch {
        print("Encountered error: \(error)")
      }
    })
  }

  func webView(
    _ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!,
    withError error: Error
  ) {
    print("Failed to load web page: \(error.localizedDescription)")
    isLoadingComplete = true
  }
}

// Example usage
let url = URL(string: "https://alexwlchan.net/")!

loadWebPage(fromURL: url)

```

doesn't fully replictae webarchiver
e.g. tools for overwriting webarchive data
and fixes for particular sites