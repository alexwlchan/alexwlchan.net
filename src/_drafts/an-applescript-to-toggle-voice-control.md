---
layout: post
title: An AppleScript to toggle Voice Control
tags: applescript macos accessibility
---

On [Mac Power Users #576](https://www.relay.fm/mpu/576), David and Stephen talked about [Voice Control](https://support.apple.com/en-us/HT210539) in macOS.
This is a feature that was introduced in macOS Catalina, and it allows you to control your Mac using your voice.
It's ideal for people who are unable to type, or who want to limit their use of the keyboard.

Macs have had Siri dictation for a couple of years (you might have seen a recent [viral video](https://twitter.com/anthonyjlang/status/1359644579344089089) about it), but you can only type for a few sentences at a time.
It cuts off after about a minute, which can really interrupt your flow.
Voice Control allows you to dictate continuously, so I was really keen on trying it.
I use dictation to do a lot of my initial writing, and then I tidy things up with keyboard and mouse.
I can dictate much faster than I can type, so it gets my ideas on to the page sooner.

You can enable Voice Control in the Accessibility pane of System Preferences, but I don't want it enabled all the time.
It uses a lot of memory and CPU, even when idling -- so I want to be able to toggle it quickly, without opening System Preferences every time.

I found an AppleScript [on the Keyboard Maestro forum](https://forum.keyboardmaestro.com/t/how-to-enable-voice-control-in-catalina/20871) that toggles Voice Control, but I was a bit dissatisfied.
It quit System Preferences when it's done, which I find mildly annoying -- I'd rather it left the app in whatever state it was already in.

I've modified the script to leave System Preferences running, and even return you to whatever pane you were using.
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

I have this wired up to [an Alfred shortcut](https://www.alfredapp.com), so I can toggle Voice Control by pressing ⌥+space, then typing "voicecontrol" (using an [icon by macOScrazy on deviantART](https://www.deviantart.com/macoscrazy/art/Siri-MacOS-Sierra-Icon-647176896)):

![An Alfred search box with the query "voicecontrol" and the selected command "Toggle Voice Control"](/images/2021/voicecontrol_alfred.png)

I've only had this for a few days, but already I'm finding it useful.
I've dictated a number of pieces -- including this blog post -- and it's much nicer than being continually interrupted by Siri dictation.
Being able to toggle it without opening System Preferences is just the icing on the cake.
