---
layout: til
title: "`console.log()` holds a reference to an object, not a copy of it"
summary: When you view an array/object with `console.log()`, you see the contents at the time you expand it, not as it existed when you called `console.log()`.
date: 2025-04-18 10:34:25 +01:00
tags:
  - javascript
---
I was having a weird issue with some JavaScript.
I was loading a JSON object and logging it to the console in my browser dev tools, but it didn't match the object that was defined in my code.
What was going on?!

I started commenting out the rest of my code, and I discovered that code that appears after the `console.log()` was affecting what got printed in my browser.
Huh!

Here's a snippet that illustrates the issue:

```html
<script>
  window.addEventListener("DOMContentLoaded", function() {
    var kitchen = {
      fruitBowl: ['apple', 'banana', 'cherry'],
    };

    console.log(kitchen);  /* I expected a/b/c here but get a/c */

    kitchen.fruitBowl.splice(1, 1);
    console.log(kitchen);  /* Here I expect a/c */
  });
</script>
```

And here's what gets logged if I expand the objects in my browser console:

{%
  picture
  filename="console_log_wtf.png"
  class="screenshot"
  alt="Screenshot of an object being printed twice in my browser console; in both cases it has two entries, apple and cherry."
  width="345"
%}

As best I can tell, what's happening is that `console.log()` is getting a *reference* to the object, but it isn't being expanded until later.
I'm seeing the value at the point it was expanded, not when I originally called `console.log()`, so any subsequent modifications to the value will be reflected in what I see in my browser console.

There are two things I can do to avoid this biting me again:

1.  **Create a copy of an object before I `console.log()` it.**
    This could mean cloning it with `{...object}` or `[...array]`, or turning it into a string with `JSON.stringify(…)`.
    This means it won't be affected by subsequent changes to the value.

    (You need to do a "deep" clone here, because JavaScript will try to be efficient and reuse values where possible.
    A "shallow" clone may still be affected by other changes to the value.)

2.  **Treat JavaScript values as immutable.**
    This is a good habit I've got into from writing Scala, and it's what I do most of the time, which is why I didn't realise sooner what was going on.
    It's fairly unusual for me to modify a JavaScript object after it's defined, so it didn't occur to me that might be an issue.
