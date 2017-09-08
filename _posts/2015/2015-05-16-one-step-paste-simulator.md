---
date: 2015-05-16 11:51:00 +0000
layout: post
slug: one-step-paste-simulator
summary: How to paste text directly from OS X into the iOS Simulator.
tags: os x
title: One-step paste in the iOS Simulator
---

On the [latest episode of *The Talk Show*][tts], John Gruber lamented the two-step paste process into the iOS Simulator (about fifteen minutes in). It goes like this:

1. In OS X, you copy some text, which gets saved to the OS X clipboard.
2. You switch to the iOS Simulator, and paste, which saves it to the iOS clipboard.
3. You long click in iOS within the Simulator, and paste *again* (this simulates the iOS paste action), which causes the text to be pasted in iOS.

Having to paste twice is mildly annoying, but it's easy to fix. I have a Keyboard Maestro macro that lets me paste directly into the copy of iOS running in the Simulator.

The macro itself is very simple:

![](/images/2015/simulator.png)

It's just a tweaked version of Gabe Weatherhead's [Paste as Typed Text macro][paste], which is useful for pasting passwords into fields where pasting is disabled. I have it inside a macro group, which is configured to only be enabled in the iOS Simulator.

For it to work, you need to have the hardware keyboard connected in the iOS Simulator (Hardware > Keyboard > Connect Hardware Keyboard). This is what allows you to type in the iOS Simulator with your regular keyboard, and lets Keyboard Maestro pass in keystrokes.

There are a few other notes:

* I have this mapped to ⌘V. This is the same as the default Paste shortcut in the Simulator. In my usage, the conflict hasn't caused any problems, but if it does, you can override the default Paste shortcut in the "Shortcuts" tab of the Keyboard Preference Pane.

* Occasionally I find apps in OS X that break the Paste as Typed Text. This macro has always worked for me in the iOS Simulator, but that's not to say it will always work everywhere.

* This will only work for text, not images or files.

* I've only tested this with the iOS Simulator that comes with Xcode 6. Apple has a habit of changing the Simulator between versions of Xcode, so it might not work if you use a different version. (Since the macro bypasses the Simulator, I'd expect it to keep working, but no guarantees.)

[tts]: http://daringfireball.net/thetalkshow/2015/05/15/ep-119
[paste]: http://www.macdrifter.com/2013/11/paste-as-typed-text.html