---
layout: til
title: "Manipulating URL query parameters in JavaScript"
date: 2019-04-20 21:24:30 +01:00
tags:
  - javascript
---

Last time I did this, I had to use some moderately fiddly code from Stack Overflow.
There are built-in tools for this now:

```javascript
function addQueryParameter(name, value) {
  var url = new URL(window.location.href);
  url.searchParams.append(name, value);
  return url.href
}

function setQueryParameter(name, value) {
  var url = new URL(window.location.href);
  url.searchParams.set(name, value);
  return url.href
}

function deleteQueryParameter(name) {
  var url = new URL(window.location.href);
  url.searchParams.delete(name);
  return url.href
}
```

All these methods return a string based on the current window location.

Read more:

*   MDN docs for URLSearchParams: <https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams>
