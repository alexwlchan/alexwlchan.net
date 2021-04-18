---
layout: post
title: Using AppleScript to detect if a Safari window uses Private Browsing
summary:
tags: applescript macos
---

Last year, I wrote an AppleScript function that [opens a URL in a Private Browsing window in Safari](/2020/06/using-applescript-to-open-a-url-in-private-browsing-in-safari/).
I got an email from a reader asking if I knew how to open a URL in a Private Browsing *tab* – either adding it to an existing private window, or creating a new private window if not.

The difficult part is working out if a given window is using Private Browsing.
Although you can access Safari's windows and tabs using AppleScript, it doesn't tell you whether a window is private.
We need to work it out on our own.

This used to be possible by [using the `do JavaScript` action](https://stackoverflow.com/a/42546218/1558022) to run code within the webpage.
You couldn't use `localStorage.setItem` in private mode, so if it was unavailable you'd know you were in private browsing.
Unfortunately, browser vendors don't want web pages to be able to detect private browsing, and any JavaScript-based detection will usually get patched.
I'm not aware of a good way to detect private browsing using JavaScript in Safari&nbsp;14.

That said, we don't have to run in the web page.
We're running AppleScript on our Mac, so we have access to everything in the browser.
Windows, menus, web pages, the lot.

Is there some other clue that would tell us if we're in private browsing?

Poking around a bit, I discovered something interesting in the Window menu: the menu item to move a tab to a new window changes depending on whether you're in private browsing or not.

<table style="margin-left: auto; margin-right: auto;">
  <tr>
    <td style="width: 50%;">
      <img src="/images/2021/window_menu_public.png" style="width: 300px;" alt="A menu with an item 'Move Tab to New Window' highlighted in red.">
    </td>
    <td style="width: 50%;">
      <img src="/images/2021/window_menu_private.png" style="width: 317px;" alt="A menu with an item 'Move Tab to New Private Window' highlighted in red.">
    </td>
  </tr>
</table>

This gives us a way in – we can use System Events to inspect the items in the Window menu, and that will tell us if the frontmost window is private.
It works even if there's a single tab (or no tab) in the window – the menu item will be present, just inactive.

Here's what the code looks like:

```applescript
on isFrontmostSafariWindowPrivateBrowsing()
  -- If you don't activate Safari, the results are sometimes wrong.
  -- In particular, System Events doesn't have the most up-to-date
  -- information about the state of the menu.
  --
  -- I think this is the same problem as described in
  -- https://www.reddit.com/r/applescript/comments/an1cpj/information_in_system_events_not_updating/
  tell application "Safari" to activate

  tell application "System Events"
    set theWindowMenu to menu "Window" of ¬
      menu bar 1 of ¬
      application process "Safari"

    return (menu item "Move Tab to New Private Window" of theWindowMenu) exists
  end tell
end isFrontmostSafariWindowPrivateBrowsing
```

As I explained at the end of [my previous post](/2020/06/using-applescript-to-open-a-url-in-private-browsing-in-safari/), you'll need to give *Accessibility* permissions to whatever app uses this code.
Apps can't just inspect the menu items of other processes – that would open up all sorts of weird security holes.

This code has a couple of limitations:

*   It has to bring Safari to the front first.

    If you don't, System Events can get an outdated list of menu items, and then you get the wrong result.
    Say, you open a regular Safari window, switch to a private window, then to another app entirely.
    System Events might still get the menu items for the regular Safari window.

*   It can only work with the frontmost window.

    I'm not sure there's a way around this with Safari's current AppleScript dictionary.
    You can still interact with windows that aren't frontmost, and there are clues in the right-click menus, but I can't see how to get there with AppleScript.
    (In particular, right-clicking on a link will say "Open Link in New Tab" or "Open Link in New Private Tab".)

*   It might break in a future version of Safari.

    If Apple changes the name of this menu item in a future version, this code will stop working.

In an ideal world, Apple would add this property to a future version of the Safari AppleScript Scripting Dictionary.
In reality, they've given it very little attention in the last few years, and they're just as likely to remove it as improve it.
For now, this code works, and proves you can still make lots of useful things in AppleScript.
