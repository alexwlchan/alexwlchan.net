---
layout: til
title: There are limits on the styles you can apply with `:visited`
date: 2024-12-25 20:04:39 +00:00
tags:
  - css
summary: |
  Because the `:visited` selector will tell you whether somebody has been to a URL, browsers limit what styles you can apply to such links -- to prevent somebody nefarious stealing your browsing history.
---
I was tweaking the `a:visited` style on this site, and I was confused about why this wasn't working:

```
a:visited {
  text-decoration-style: dashed;
}
```

I thought it might be a browser bug, or maybe some bad interaction between other `text-decoration` rules, but it turns out to be an intentional choice by browser makers.

A [Stack Overflow answer](https://stackoverflow.com/a/35037025/1558022) pointed to a page on MDN [Privacy and the :visited selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Privacy_and_the_:visited_selector#limits_to_visited_link_styles), which explains:

> Before about 2010, the CSS :visited selector allowed websites to uncover a user's browsing history and figure out what sites the user had visited. […] To mitigate this problem, browsers have limited the amount of information that can be obtained from visited links.

and there are only a few styles you can apply to `:visited` links:

> You can style visited links, but there are limits to which styles you can use. Only the following styles can be applied to visited links:
>
> * `color`
> * `background-color`
> * `border-color` (and its sub-properties)
> * `column-rule-color`
> * `outline-color`
> * `text-decoration-color`
> * `text-emphasis-color`
> * The color parts of the `fill` and `stroke` attributes

This is annoying for my purposes, but it makes sense, and I'm glad to know it's not my own incompetence that was preventing this CSS from working!

I briefly considered trying to find ways around this, like doing something with variables or trying to trick the browser somehow, but I decided against it.
It'd be a fragile hack, and any loophole I found should be reported and fixed rather than used for my own enjoyment.
