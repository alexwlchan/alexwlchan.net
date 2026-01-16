---
layout: post
date: 2022-11-17 22:38:39 +00:00
title: Changing the macOS accent colour without System Preferences
summary: Updating the accent colour everywhere, with immediate effect, using a script written in Swift.
tags:
  - macos
  - swift
  - colour
---

In System Preferences, you can change the accent colour of your Mac:

{%
  picture
  filename="appearance_prefs.png"
  alt="The macOS General preferences, with a preview of Light/Dark/Auto mode and a selection of coloured buttons to choose the accent colour. The currently selected colour is red, which can be seen in the outline of a selected search field in the upper-right corner, the arrows on two select menus, and a checkbox."
  width="520"
%}

This affects colours throughout your Mac's user interface, including buttons, menus, and tickboxes.
When you pick a new colour, it updates everywhere, immediately.

I want to write some automations that update the accent colour, which I thought would be pretty easy -- but I couldn't find a pre-built solution.
The top results on Google fell into one of two camps, neither of which I found satisfactory:

1.  An AppleScript which opens the System Preferences window, then uses UI scripting to click the button like a person would.
2.  A shell command which updates the preference, using numeric values for the colours:

    ```
    $ defaults write -globalDomain AppleAccentColor -int 0
    ```

    but this doesn't take effect until you restart an app.

But by searching a little deeper, I found enough to write a script which sets the accent colour *and* updates it in every app.
I can now run a command like:

```
$ set_accent_colour red
```

and the UI of my Mac switches to red.
If you want, you can go [straight to the script][the_script], or you can read on and I'll explain how I found the important pieces.

---

My first clue came from googling the name of the preference, which led me to [a Stack Overflow post by Henrik Helmers][so]:

> The accent color can be read from `AppleAccentColor`. Changes can be observed by listening for the `AppleColorPreferencesChangedNotification` notification.

Presumably when you pick a new colour in System Preferences, it sends this notification, and other apps are listening out for it.

That notification name is very specific, so I went looking for other code that uses it on GitHub.
I found a [pull request by Garth Mortensen][garth_pr] that sends this notification using Swift.

This was enough to cobble together a basic Swift script that I thought would work:

```swift
#!/usr/bin/env swift

import Foundation

UserDefaults.standard.setPersistentDomain(
  ["AppleAccentColor": Optional(0) as Any],
  forName: UserDefaults.globalDomain
)

let notifyEvent = Notification.Name("AppleColorPreferencesChangedNotification")
DistributedNotificationCenter.default().post(name: notifyEvent, object: nil)
```

But on my Mac, running macOS Monterey, this didn't work correctly -- the preference would change, but apps wouldn't update their accent colour until I relaunched them.

I continued googling for the name of the notification, and I found a helpful comment from Robert Sesek [in the Chromium source code][chromium]:

> CoreUI expects two distributed notifications to be posted as a result of
> the Aqua color variant being changed: AppleAquaColorVariantChanged and
> AppleColorPreferencesChangedNotification.

I modified my code to send both these notifications, and now it seems to work correctly.

I've wrapped it [in a script][the_script] that allows me to set named colours, rather than remembering the numeric codes, and saved it to my path.
I've only tested it on my iMac running Monterey, and it sounds like maybe this system changes between different macOS releases, so it may not work on your Mac -- but if it doesn't, I hope this gives you some clues for how to get it working.

[so]: https://stackoverflow.com/a/51695756/1558022
[garth_pr]: https://github.com/kentcdodds/dotfiles/pull/3
[chromium]: https://chromium.googlesource.com/chromium/src.git/+/62.0.3202.58/content/renderer/theme_helper_mac.mm#31

[the_script]: https://github.com/alexwlchan/pathscripts/blob/main/macos/set_accent_colour
