---
layout: til
date: 2024-02-24 06:55:47 +00:00
title: How to parse URLs in JXA
tags:
  - jxa
---
Whenever I want to do AppleScript-like automation which involves string manipulation, I reach for JXA instead.

If I want to parse URLs, I normally use the [URL() constructor](https://developer.mozilla.org/en-US/docs/Web/API/URL/URL):

```javascript
var urlString = "https://www.example.com/path/to/resource?param1=value1&param2=value2";

var url = new URL(urlString);
```

But if you try that in JXA, you get an error:

```
Error: ReferenceError: Can't find variable: URL
```

Instead, a way I've found to parse URLs in JXA is to use `NSURL`.
It's a slightly different interface to JavaScript's standard URL class, but better than writing a URL parser from scratch:

```javascript
var url = $.NSURL.URLWithString(urlString);

var scheme = ObjC.unwrap(url.scheme);
var host   = ObjC.unwrap(url.host);
var path   = ObjC.unwrap(url.path);
var query  = ObjC.unwrap(url.query);

console.log("Scheme:", scheme);
console.log("Host:",   host);
console.log("Path:",   path);
console.log("Query:",  query);
/* Scheme: https */
/* Host: www.example.com */
/* Path: /path/to/resource */
/* Query: param1=value1&param2=value2 */
```

Note that the returned attributes (`url.scheme`, `url.host`, etc.) are all instances of `NSString`, so they need to be unwrapped to get regular JavaScript strings.
