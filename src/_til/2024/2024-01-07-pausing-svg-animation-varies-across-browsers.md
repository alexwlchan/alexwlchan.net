---
layout: til
title: "Pausing the animation of &lt;svg&gt; elements can affect child &lt;svg&gt; elements differently in different browsers"
date: 2024-01-07 20:49:46 +00:00
tags:
  - svg
---
Consider the following SVG, which contains two animated rectangles:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" width="100" id="outer">
  <rect width="0" height="10" fill="black">
    <animate attributeName="width" values="0;10;0" dur="20s"/>
  </rect>

  <svg id="inner">
    <rect width="0" height="5" fill="red">
      <animate attributeName="width" values="0;10;0" dur="7s"/>
    </rect>
  </svg>
</svg>
```

Suppose you pause animations in the outer SVG with JavaScript, e.g.:

```javascript
document.querySelector("svg#outer").pauseAnimations();
```

What happens next depends on the browser.

*   In Firefox, both rectangles stop animating.
*   In Safari, only the black ("outer") rectangle stops animating.
    The red rectangle continues animating, because it's wrapped in a separate `<svg>` tag.
