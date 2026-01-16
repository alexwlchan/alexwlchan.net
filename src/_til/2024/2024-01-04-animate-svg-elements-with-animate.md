---
layout: til
date: 2024-01-04 21:53:05 +00:00
title: "Animate an attribute of an element with &lt;animate&gt;"
tags:
  - svg
---

You can animate an attribute of an SVG element using the [`<animate>` element][mdn].
Here's one example from MDN:

```xml
<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>
```

<svg viewBox="0 0 10 10" width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="10" height="10">
    <animate
      attributeName="rx"
      values="0;5;0"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>

You can include multiple `<animate>` elements to animate multiple attributes simultaneously.
Here's an example I didn't end up using that animates both the `width` and `x` attributes to make a rectangle that expands from its vertical centre:

```xml
<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
  <rect width="0" height="10">
    <animate
      attributeName="width"
      values="0;10;0"
      dur="10s"
      repeatCount="indefinite" />
    <animate
      attributeName="x"
      values="5;0;5"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>
```

<svg viewBox="0 0 10 10" width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="0" height="10">
    <animate
      attributeName="width"
      values="0;10;0"
      dur="10s"
      repeatCount="indefinite" />
    <animate
      attributeName="x"
      values="5;0;5"
      dur="10s"
      repeatCount="indefinite" />
  </rect>
</svg>

[mdn]: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate