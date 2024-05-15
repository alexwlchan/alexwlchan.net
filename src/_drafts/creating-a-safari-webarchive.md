---
layout: post
title: Creating a Safari webarchive from the command line
summary:
tags:
---

Prior art: https://github.com/newzealandpaul/webarchiver

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