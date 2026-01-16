---
layout: til
title: Sort a list of DOM elements by sorting and calling `appendChild()`
date: 2024-01-11 21:52:57 +00:00
tags:
  - javascript
---
From [an answer by ahuigo][ahuigo] on Stack Overflow, here's a snippet to sort DOM elements:

```javascript
const list = document.querySelector('ul');

[...list.children]
  .sort((a, b) => a.innerText > b.innerText ? 1 : -1)
  .forEach(node => list.appendChild(node));
```

Most of this is syntax I'm already familiar with; the interesting bit is how [appendChild()][appendChild] is behaving here:

> If the given child is a reference to an existing node in the document, `appendChild()` moves it from its current position to the new position.

By calling this on every node in the list, in sorted order, the nodes get moved into sorted order.

## What does 1/-1 returned from the sort comparison mean?

Here's [a table from the MDN docs][sort_comparison] that explains what the custom sort comparison should return, which I always forget:

<blockquote>
  <table>
    <thead>
      <tr>
        <th><code>compareFn(a, b)</code> return value</th>
        <th>sort order</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>&gt; 0</td>
        <td>sort <code>a</code> after <code>b</code>, i.e. <code>[b, a]</code></td>
      </tr>
      <tr>
        <td>&lt; 0</td>
        <td>sort <code>a</code> before <code>b</code>, i.e. <code>[a, b]</code></td>
      </tr>
      <tr>
        <td>=== 0</td>
        <td>keep original order of <code>a</code> and <code>b</code></td>
      </tr>
    </tbody>
  </table>
</blockquote>

[ahuigo]: https://stackoverflow.com/q/282670/1558022
[sort_comparison]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
[appendChild]: https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild
