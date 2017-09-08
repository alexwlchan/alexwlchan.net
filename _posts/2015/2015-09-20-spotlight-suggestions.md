---
date: 2015-09-20 09:32:00 +0000
layout: post
slug: spotlight-suggestions
summary: In iOS 9, you can turn off the News in Spotlight by toggling Spotlight Suggestions.
  But what else does this disable?
tags: ios
title: "What does \u201CSpotlight Suggestions\u201D turn off?"
---

One of the "features" of iOS 9 is news articles appearing in Spotlight searches.
If you swipe to the search screen, and haven't typed anything into the search field, it gets pre-populated with headlines.
Lots of people (including me) think this is just a distraction, and have been looking for ways to turn it off.

In Settings, you can toggle what sort of results show up in Spotlight.
For headlines, it turns out to be the relatively innocent-sounding switch "Spotlight Suggestions".
Turning off this Spotlight result will get rid of the news items; detailed instructions are on [CGP Grey's blog](http://www.cgpgrey.com/blog/how-to-turn-off-news-in-spotlight-in-ios-9).

On the [latest episode of *Cortex*](https://overcast.fm/+EtBkms44w/35:00), CGP was discussing this toggle with Myke Hurley.
As part of their conversation, they were puzzling over the name of the label:

> I don't know why on earth this label is [Spotlight Suggestions], because as far as I can tell, if you turn it off, the only thing it removes is the news. Everything else it will still show you: it'll still show you results from your documents […], it'll still show you everything you have turned on. It just seems not to fill that screen with *something* if there are no results.

I started wondering as well.
I toggled that switch as soon as I started running the iOS betas.
What else is it turning off?

Near the bottom of the settings pane is a small link, "About Spotlight Suggestions & Privacy".
Tapping it brings up this explanation:

> Spotlight Suggestions shows you suggestions from the web, your contacts, apps, nearby locations and media, including iTunes and the App Store &ndash; and even offers suggestions before you start typing.

<!-- As well as the above, these suggestions include Wikipedia pages, Maps results and websites. -->
If you disable Spotlight Suggestions, all of these get turned off.
News is the most obvious example of Suggestions because it's the only result that shows up on an empty search screen; all the others only appear when you start typing in a search.

I think &ndash; although I'm not certain &ndash; that it's any result that can't be looked up locally.
Results that go via the network have privacy implications, which is why these results can be turned off, and probably why they're all under the same toggle.

Below I've included a few screenshots to show the difference caused by this toggle.

<!-- summary -->

<br>

<center>
  <a href="/images/2015/cortex-enabled.PNG"><img src="/images/2015/cortex-enabled.PNG" class="two_up left"></a>
  <a href="/images/2015/cortex-disabled.PNG"><img src="/images/2015/cortex-disabled.PNG" class="two_up"></a>
</center>

**Cortex.** With Spotlight Suggestions enabled, I see the podcast in the iTunes Store, and a YouTube video.
I don't get anything when they're disabled.
(I assume that Overcast results will appear in Spotlight soon, but I think that depends on an update to the app.)

<br>

<center>
  <a href="/images/2015/vexelology-enabled.PNG"><img src="/images/2015/vexelology-enabled.PNG" class="two_up left"></a>
  <a href="/images/2015/vexelology-disabled.PNG"><img src="/images/2015/vexelology-disabled.PNG" class="two_up"></a>
</center>

**Flags are cool.** With Spotlight Suggestions enabled, I get a link to the Wikipedia page. Disabled, I just see some fallback suggestions.

<br>

<center>
  <a href="/images/2015/pizzaexpress-enabled.PNG"><img src="/images/2015/pizzaexpress-enabled.PNG" class="two_up left"></a>
  <a href="/images/2015/pizzaexpress-disabled.PNG"><img src="/images/2015/pizzaexpress-disabled.PNG" class="two_up"></a>
</center>

**Feeling peckish?** This shows the biggest disparity in results: with suggestions disabled, all I see is a count of Maps results.
Enabled, I can see star ratings from Yelp, an App Store result, a website and a Wikipedia entry (off-screen).
I can even go straight straight to driving directions.

<br>

Some of these results seem like they might be useful, but none of them can override my annoyance at headlines on an empty search screen.
I'm going to leave it turned off for now, but I would love to see a future version of iOS pull out headlines into a separate toggle.
