---
layout: note
title: "Manipulating URL query parameters in JavaScript"
date: 2019-04-20 21:24:30 +01:00
topic: JavaScript
---

Last time I did this, I had to use some moderately fiddly code from Stack Overflow.
There are built-in tools for this now:

```javascript {"names":{"1":"addQueryParameter","2":"name","3":"value","4":"url","16":"setQueryParameter","17":"name","18":"value","19":"url","31":"deleteQueryParameter","32":"name","33":"url"}}
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
