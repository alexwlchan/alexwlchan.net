---
layout: til
title: How to create a footer that’s always at the bottom of the page
date: 2024-01-12 10:36:02 +00:00
tags:
  - css
---
I use a pretty standard structure for laying out basic web pages:

```html
<body>
  <header>This is my header</header>

  <main>This is the main content</main>

  <footer>This is the global footer</footer>
</body>
```

If I want to ensure the `<footer>` is always at the bottom of the screen, even if the `<main>` doesn't fill the height, the following CSS does the trick (based on a Stack Overflow answer [by vsync][vsync])

```css
body {
  min-height: 100vh;
  margin: 0;
}

/* The main fills all the space between header & footer */
body {
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
```

What's going on here:

*   The `min-height` on `body` ensures that the `<body>` element is always at least the full height of the window.
*   The `flex` allows the size of elements to change in size, and `flex: 1` only on the `<main>` element means it'll take up all the remaining space.
    In practice, that gets added at the bottom, pushing the `<footer>` down.

[vsync]: https://stackoverflow.com/q/643879/1558022
