---
layout: post
title: An AppleScript to toggle Voice Control
tags: applescript macos accessibility
---

On my Mac, I do a lot of writing using speech-to-text dictation.
I can speak much faster than I can type, so it gets my ideas on the page sooner, and then I tidy things up with a keyboard and mouse.
I don't have the sort of wrist problems that would force me to use dictation or minimise use of the keyboard (at least, not yet), but prevention is better than cure.

Until recently, I'd been using [Siri dictation](https://support.apple.com/en-gb/guide/mac-help/mh40584/mac), but you can only type a few sentences at a time.
It cuts off after a minute, and then you have to restart it, which really interrupts your flow.
Great for sending a short text, less helpful for writing a long blog post.

On [Mac Power Users #576](https://www.relay.fm/mpu/576), David and Stephen talked about [Voice Control](https://support.apple.com/en-us/HT210539).
This is a feature that was introduced in macOS Catalina, meant to give you full hands-free control of your Mac.
Among other things, it allows you to dictate continuously and add a custom vocabulary (for certain languages), so I really wanted to try it.
The latter is useful if your writing involves specialist terminology that isn't in the Siri dictation dictionary.

You can enable Voice Control in the Accessibility pane of System Preferences, but I don't want it enabled all the time.
Even when it's paused, I noticed other apps get sluggish -- so I want to be able to toggle it quickly, without opening System Preferences every time.

I found an AppleScript [on the Keyboard Maestro forum](https://forum.keyboardmaestro.com/t/how-to-enable-voice-control-in-catalina/20871) that toggles Voice Control, but I was a bit dissatisfied.
It quits System Preferences when it's done, which I find mildly annoying -- I'd rather it left the app in whatever state it was already in.

I've modified the script to leave System Preferences running (if it's open), and even return you to whatever pane you were using.
Here's my script:

```applescript
tell application "System Preferences"
  if it is running then
    set systemPreferencesIsAlreadyRunning to true
    set theCurrentPaneId to the id of the current pane
  else
    set systemPreferencesIsAlreadyRunning to false
  end if

  reveal anchor "Dictation" of pane id "com.apple.preference.universalaccess"

  delay 0.5

  tell application "System Events"
    tell process "System Preferences"
      click checkbox "Enable Voice Control" of group 1 of window "Accessibility"
    end tell
  end tell

  if systemPreferencesIsAlreadyRunning then
    reveal pane id theCurrentPaneId
  else
    quit
  end if
end tell
```

I have this wired up to [an Alfred shortcut](https://www.alfredapp.com), so I can toggle Voice Control by pressing ⌥+space, then typing "voicecontrol".
The icon is by <a href="https://www.deviantart.com/macoscrazy/art/Siri-MacOS-Sierra-Icon-647176896">macOScrazy on deviantART</a>, and you can <a href="/files/2021/Toggle Voice Control.alfredworkflow">download my workflow</a> if you'd find it useful.

<img src="/images/2021/voicecontrol_alfred.png" alt="An Alfred search box with the query “voicecontrol” and the selected command “Toggle Voice Control”">

I've only had this for a few days, but already I'm finding it useful.
I've dictated a number of pieces -- including this blog post -- and it's much nicer than being continually interrupted by Siri dictation.
Being able to toggle it without opening System Preferences is the icing on the cake.
