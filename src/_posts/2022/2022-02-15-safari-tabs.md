---
layout: post
date: 2022-02-15 20:54:35 +00:00
title: Closing lots of Safari tabs with JXA
summary: To help me keep my tab count down, I wrote a JXA script to close tabs that can easily be recreated.
tags:
  - jxa
  - macos:safari
  - macos
---

I have a lot of browser tabs.
I open way more tabs than I close, so by the end of the week my computer often has hundreds of tabs open.
(I currently have 182 tabs.)

Occasionally I keep a tab open because I want to look at it later, but most of these are tabs I just haven't closed yet -- and which I could recreate easily if needed.
For example, when I want to see our planning board, it's faster to open a new tab than find the existing tab.
I look at the board several times a day, so I open several different tabs – and they all sink into the background mass of windows on my computer.

This might seem ridiculous, but it works for me.
I have a bunch of [Alfred shortcuts](https://www.alfredapp.com) set up to open different bookmarks, which means I can get to important URLs quickly -- and my computer is powerful enough that I don't feel the drag of all the tabs.
It's just as snappy with 300 tabs as with 3.

But all these repetitive tabs make it harder to find the few tabs I do want to look at later -- so I wrote a script that cleans them up.
I run this at the end of each day, and a bunch of tabs get closed.

I'm using JavaScript for Automation (JXA) for this script -- I've been trying to learn more JavaScript for my day job, and JXA seems like a step up from AppleScript.
I still get all the automation hooks in macOS, but I don't have to suffer AppleScript's control flow or string handling.

[osascript]: https://ss64.com/osx/osascript.html


## Getting a list of browser tabs

I use Safari as my browser, so that's what I'm using in this script.
Chrome and Firefox have similar hooks for AppleScript/JXA, but I leave those as an exercise for the reader.

In JXA, you can look up Safari's windows as the `.windows` property on the application, which returns an array.
For example, this tells me I have 23 windows open:

```javascript
const safari = Application("Safari");

console.log(safari.windows.length);
/* 23 */
```

Each of those windows has a `.tabs` property, which returns another array.
For example, this tells me I have 7 tabs open in my 3rd window:

```javascript
console.log(safari.windows[2].tabs.length);
/* 7 */
```

And I can look up the URL of individual tabs, for example the 5th tab of the 3rd window:

```javascript
console.log(safari.windows[2].tabs[4].url());
/* https://en.wikipedia.org/wiki/Route_53 */
```

Windows are ordered front-to-back, and tabs are ordered left-to-right.
The first entry of `safari.windows` is my front window, the second entry is the window behind it, the third entry the window behind that, and so on.
The entries of `window.tabs` are in left-to-right order.

We can put these calls together in a for loop to get the URL of every tab in every window:

```javascript
function* tabGenerator() {
  window_count = safari.windows.length;

  for (window_index = window_count - 1; window_index >= 0; window_index--) {
    this_window = safari.windows[window_index];

    tab_count = this_window.tabs.length;

    for (tab_index = tab_count - 1; tab_index >= 0; tab_index--) {
      tab = this_window.tabs[tab_index];
      yield [window_index, tab_index, tab.url()];
    }
  }
}
```

This `function` followed by an asterisk is a JavaScript [generator function], which is something I learnt about while writing this script.
I'm already very familiar with generators in Python (if you're not, I recommend [Ned Batchelder's PyCon talk][nedbat]), and I stumbled upon generator functions by searching for "python generator in javascript".

It returns the tabs in reverse: from right-to-left, bottom-to-top.
This is to make the rest of the script simpler.
When you close a tab or a window, the `.tabs` and `.windows` arrays get renumbered.
For example, when I close window 3, what was previously window 4 becomes the new window 3, and window 5 becomes window 4, and window 6 becomes window 5, and so on.

If I went through the tabs in forward orderm it'd be fiddly to make sure I visited every one.
After closing window 3, I'd have to go back and check the tabs in the new window 3 to see if any of them needed closing.
If I go through the tabs in reverse, the only tabs and windows that get renumbered are ones I've already checked, so I don't need to check them again.

[generator function]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*
[nedbat]: https://nedbatchelder.com/text/iter.html



## Deciding whether to close a tab

This is the "business logic" of the script -- deciding whether a tab can be safely closed.
For me, a simple list of URL prefixes is plenty -- if any of them match, it's a tab I know I can recreate later.

```javascript
function isSafeToClose(url) {

  // Sometimes we get a `null` as the URL of a tab; I'm not sure why,
  // so leave this tab open.
  if (url === null) { return false; }

  return (
    url.startsWith("https://zoom.us/") ||
    url.startsWith("https://trustnet.wellcome.org/") ||
    url.startsWith("https://search.wellcomelibrary.org") ||
    url.startsWith("https://logging.wellcomecollection.org") ||
    url.startsWith("https://console.aws.amazon.com/") ||
    url.startsWith("https://us-east-1.signin.aws.amazon.com/") ||
    url.startsWith("https://eu-west-1.console.aws.amazon.com/") ||
    url.startsWith("https://github.com/wellcomecollection/") ||
    url.startsWith("https://github.com/search?type=Code&q=org:wellcomecollection") ||
    url.startsWith("https://buildkite.com/orgs/wellcomecollection/") ||
    url.startsWith("http://localhost:3000/") ||
    url.startsWith("https://api.wellcomecollection.org/") ||
    url.startsWith("https://www-stage.wellcomecollection.org/")
  );
}
```

I did consider putting the URL prefixes in an array, and using `.some()` to look for matches:

```javascript
prefixes = [ /*...*/ ];

return prefixes.some(url.startsWith);
```

but that returns a mysterious TypeError, and I don't care enough to dig into it.
The OR statement is a bit repetitive, but it's fine.

If you want to use a version of this script, replace this function with logic to decide what tabs you can safely close.



## Putting these two functions together

This is the final part of my script:

```javascript
for (const [window_index, tab_index, url] of tabGenerator()) {
  if (isSafeToClose(url)) {
    console.log(url);
    safari.windows[window_index].tabs[tab_index].close();
  }
}
```

It iterates over the URLs returned by `tabGenerator()`, and then calls `isSafeToClose()` on each URL.
If it's going to be closed, it prints the URL (so I can see if it closed the wrong tab, and get it back), then calls the `.close()` method to actually close the tab.

I have everything saved in a file called `close_work_tabs`, and at the top I have this line:

```
#!/usr/bin/env osascript -l JavaScript
```

This shebang means that when I run `close_work_tabs` from the command line, it gets picked up by [`osascript`](https://ss64.com/osx/osascript.html) and interpreted as a JavaScript file (rather than AppleScript, the default).

If you'd find it helpful, you can download this script as a single file:

{% download filename="close_work_tabs.js" %}

This was my first time using JXA for Mac automation, but it won't be my last.
I often help family, friends, and coworkers debug things on their Macs, and a good scripting language is super helpful.
Where possible, I prefer to solve their problems with the builtin tools, rather than installing lots of extra stuff on their computers.

I used to rely on the builtin Python, but now Apple is (finally) [removing it][python], I'll have to switch to something else, and JXA seems like the best choice.
Although I'll continue to have a Python installation on my own computers, I'll start reaching for JXA in future automations – as a way to practice for when I'm working on somebody else's Mac.

[python]: https://developer.apple.com/documentation/macos-release-notes/macos-12_3-release-notes#Python
