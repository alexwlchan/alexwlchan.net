---
layout: post
title: "Control Centre: one step forward, two steps back"
summary: I like aspects of Control Centre in iOS 11, but WiFi/Bluetooth and audio playback are both immensely frustrating.
tags: ios frustrations
---

<style>
  img.img__control_centre {
    max-width: 400px;
    padding-bottom: 5px;
  }
</style>

I'm not much of an iOS power user, and these days, most new features go straight over my head.
As such, there wasn't much in iOS 11 to interest me, and it took me a while to get round to upgrading.

One thing I *was* looking forward to was the new Control Centre.
The ability to customise controls could come in handy, and doing away with the two pages seemed like an easy win.
Plus, I think the new version just looks nicer.

Now I've been using it for several weeks, I'm more ambivalent.
Customisation has been really useful --- I've done away with the unused calculator shortcut, and brought in Low Power Mode, which I use all the time.
Most of the buttons look good and are easy to hit, and I'm having much more success with the chunky brightness and volume sliders.
But as it advances in one area, so it slips in another.

My first issue is one that's already been [widely reported][guardian].
Below is a screenshot of my Control Centre.
Pop quiz: are Wi-Fi and Bluetooth turned on or off?

<figure>
  <img class="img__control_centre" src="/images/2017/control_centre_base.png">
  <figcaption>
    There's a cluster of four circular icons in the top-left hand corner.
    First row: an airplane icon and a wireless tower icon.
    Second row: a WiFi icon and the Bluetooth logo.
    Only the wireless tower icon is highlighted, on a green background.
  </figcaption>
</figure>

On iOS 10, toggling those buttons would turn off WiFi or Bluetooth.
On iOS 11, they don't.

These buttons just control whether your device will accept new connections.
And even worse, those settings are only transient.
They re-enable if you restart your phone, or wait until 5am the following day.
Apple has a [support document][support] explaining the weird edge cases.
If you want to turn off WiFi or Bluetooth, you have to go to the Settings app --- just the sort of roundabout action Control Centre was meant to avoid.

I think this is a bad change.
Potential security implications aside, it's not how you expect those buttons to work.
The button presents a binary switch.
"On"/"Off" are clearly distinct, and fit the button nicely.
"On"/"On but with an asterisk" are a much more subtle distinction.
It could work if this was a three-way switch with "Off" as a third state --- but as it stands, it's really not obvious how this button works.

I routinely turn on power saving features to conserve battery life.
In iOS 10, I'd go to the Settings app to enable Low Power Mode, and turn off my WiFi and Bluetooth radios from Control Centre.
In iOS 11, it's the other way round.
One step forward, one step back.

[guardian]: https://www.theguardian.com/technology/2017/sep/21/ios-11-apple-toggling-wifi-bluetooth-control-centre-doesnt-turn-them-off
[support]: https://support.apple.com/en-us/HT208086
