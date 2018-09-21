---
layout: post
title: Building trust in an age of suspicious minds
summary: Notes and slides from my PyCon UK 2018 keynote. In a world where people are less and less trusting, hwo can we take steps to make ourselves more trustable?
tags: pyconuk slides
---

This is a talk I gave on Saturday as the opening keynote of [PyCon UK 2018][pyconuk].

I was already planning to do a talk about online harassment, and Daniele *[Ed. Procida, the conference director]* encouraged me to expand the idea, and turn it into a talk about positive behaviour.
This is my abstract:

> In 2018, trust is at a low.
> Over the past several decades, trust has declined – fewer and fewer people trust each other, and the reputation of big institutions (government, media, politicians, even non-profits) is in tatters.
>
> What happened?
>
> In this talk, I’ll explain how the design of certain systems have been exploited for abuse, and this has corroded our trust – and conversely, how we can build environments that encourage and sustain good behaviour.

The talk was recorded, and thanks to the wizardry of Tim&nbsp;Williams, it's already been posted on YouTube:

{% youtube https://www.youtube.com/watch?v=B3XxPnbehqQ %}

You can read the slides and notes on this page, or download the slides [as a PDF](/talks/suspicious-minds.pdf).

<!--
Note:
This doesn't include everything I said, but I hope it's a useful starting point.
-->

[pyconuk]: https://2018.pyconuk.org/

<!-- summary -->

The transcript is based on the YouTube video, with editorial notes and fix-ups as appropriate.

I prepped this talk at fairly short notice, and it wasn't as polished as I'd like.
There's a lot of um'ing and ah'ing.
If I end up doing this talk again, I'd love to go back and get some more practice.

---

*[Ed. I was introduced by Daniele Procida, the conference director.]*

{% slide_captioned suspicious-minds 1 %}
  Based on the cover art [of the Elvis single](https://en.wikipedia.org/wiki/Suspicious_Minds#/media/File:Elvis_presley_suspiciousminds.jpg).
{% endslide_captioned %}

Thanks for that introduction.
As Daniele said, my name is Alex, I'm a software developer at [the Wellcome Trust](https://wellcome.ac.uk/) in London, and I help organise this conference.
It's a pleasure to be opening this year's conference, and I really hope you all have a great time.

The reason I was asked to do this talk is that I spent my time thinking about a lot of ways that systems can be exploited for harassment, abuse, and to do nasty things.
(Which is a polite way of saying I'm good at breaking stuff, so the fact we've made the projector work on the first try is a huge achievement.
If nothing else goes well this morning, I'll take that.)

By thinking about how things can be exploited and broken, you often come to them with a very defensive mindset.
You're thinking about damage control -- how do I limit the potential of harm?

Daniele challenged me to flip that on its head.
Could you go the other way, and not just design a system that prevents bad behaviour, but actually *encourages* good behaviour?
I started thinking about good behavior, how you build that, how you encourage that, and what I started thinking about was *trust*.



{% slide suspicious-minds 2 %}

Trust is really important.
It underpins all of our working relationships -- whether that's with other people, with our tools, with our users (the people we're building systems for).

If we feel like we trust somebody, we feel like we can rely on them, we can cooperate with them, we can believe they will actually do what they say they will.
It gives us a sense of security.
It means we're not looking over our shoulder, looking for the next mistake or betrayal, trying to work out what's going to go wrong.

So we're going to talk about trust today, because it's a foundation of good working relationships, and the other positive behaviours that they foster.



{% slide suspicious-minds 3 %}

But trust is kind of a nebulous thing, isn't it?

We sort of know when we trust somebody, we know when we don't -- I think it's helpful to start by having a definition of trust.

Charles Feltman has written a book called [*The Thin Book of Trust*](https://www.thinbook.com/the-thin-book-of-trust/) that has a definition I really like:

> Trust is choosing to risk making something you value vulnerable to another person's actions.

So let's break down that definition.



{% slide suspicious-minds 4 %}

Trust is **choosing to risk** -- it's a risk assessment.
We look at our past experiences with somebody, and we decide if we want to take the risk.
If we trust somebody, we probably do want to take that risk; and if we don't trust them, then we don't.



{% slide suspicious-minds 5 %}

And it's taking **something you value** -- and we value all sorts of things.
Money, happiness, fulfillment, not being fired from our jobs, not being booed off a stage in front of 400 people.



{% slide suspicious-minds 6 %}

And finally, we're **making it vulnerable**.
We're giving up some control over the thing we care about.

In the software industry, we often think about vulnerability as a really bad thing, because we think about it in the context of security vulnerabilities.
It's a hack, it's got to be patched and closed off immediately, and that's right -- but vulnerability is also really important.

If you have vulnerability, you have the opportunity to progress, opportunity for growth.
You need vulnerability to be able to grow, and it's a really important part of trust.



{% slide suspicious-minds 3 %}

So that's the definition of trust we're going to use today.



{% slide suspicious-minds 7 %}

We're usually pretty good at articulating when we **don't** trust somebody.

Hands up in the audience: who has ever thought "I just don't trust them"?

I think that's pretty much the entire audience. *[Ed. I was looking at a room full of raised hands.]*

If I asked you all, you all had a good reason, right?
Maybe there was a lie, there was an incident, they were mean, you had some
gossip...



{% slide suspicious-minds 8 %}

But what if I asked you to go in the other direction?
Think of somebody you really trust.

If I asked you "why do you trust them", it feels like a harder question, doesn't it?
We're often aware that we trust somebody, but it can be hard to pinpoint the moment when that happened.
How do we go from the state of "somebody we just know" to "somebody we actually trust"?



{% slide suspicious-minds 9 %}

Because trust isn't something you can tell somebody to do, you can't ask for it, and as much as Facebook's marketing marketing team would love, you can't buy
it!

That's not great, is it?
If trust is such an important thing, we shouldn't just be passive participants.
That's what I want to look at today.
I want to look at how we take an active role in the formation of trust.
How do we actively build trust for ourselves?



{% slide suspicious-minds 10 %}

So what's the state of trust in 2018, a year of only happiness and rainbows?
How much do we trust in each?



{% slide_captioned suspicious-minds 11 %}
  Image: [Easter Fire](https://pixabay.com/en/easter-fire-brand-heat-firelight-1439323/), by claus-heinrichcarstens on Pixabay.
  CC0.
{% endslide_captioned %}

If we go on Twitter, in the six minutes that I've been speaking, there have probably been about six years worth of news.
It feels like the world is on fire (sometimes literally), and the unfortunate thing is it seems like that often isn't any trust.

Studies consistently show that trust in each other -- trust in individuals -- is declining.
And trust in big institutions -- businesses, governments, nonprofits, the media -- we're not trusting those institutions as much either.
Those are places that we might have once looked to for trust and guidance.

You wouldn't inspect the credentials of every journalist in a newspaper; you'd trust the newspaper would do that for you.
You trust they'd so some fact checking.
And we now longer trust that they will do that.



{% slide suspicious-minds 12 %}

So how did we get here?

I think it was caused by three major trends in the last 10--15 years:

1. Major world events
2. The downsides of globalisation
3. Social media

So let's go through them in turn.



{% slide suspicious-minds 13 %}

**Some significant events.**

If you look at the last twenty years, there have been several major turning points where we stopped trusting people.

*   The first was the [September 11th attacks in 2001](https://en.wikipedia.org/wiki/September_11_attacks) and the subsequent response by the governments of the world.
*   Then the [faulty rationale](https://en.wikipedia.org/wiki/September_Dossier) for the war in Iraq.
    "45 minutes to deployment of weapons of mass destruction."
*   The [2008 financial collapse](https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%932008), which we're still seeing the fallout of ten years later.
*   In this country (and I'm very jealous of our overseas attendees) is the [Brexit referendum](https://en.wikipedia.org/wiki/United_Kingdom_European_Union_membership_referendum,_2016) and all the following "negotiations". *[Ed. Yes, I used finger quotes.]*

All of these things these events leave people feeling angry, feeling bitter, feeling divided, suspicious, sceptical.
Those are a really poor recipe for trust.
When we have all these heated emotions, it's not surprising that we
don't trust some of these big institutions as much.

One thing that's interesting as well -- I think we might be in the middle of another seismic trust event.
For years, there have been a trickle of stories about bad things happening at tech companies -- probably companies that some of us work at.
Privacy violations at Facebook, location tracking at Google, safety violations at Uber -- and it feels to me like that trickle is starting to become a flood.
Every week I look at the headlines, and I see some other bad thing that's happening another tech company

I do wonder if we'll look back in a couple of years, and see 2018 as the point where trust in tech started to falter.
Maybe one day we could be aspire to be as trusted as bankers.
*[Ed. The audience laughed, but I'm serious.]*

Those are some of the major world events that have already happened, and that we need to be worrying about.



{% slide suspicious-minds 14 %}

Second let's talk about **the downsides of globalisation**.

On the one hand, globalisation is wonderful.
It's made the world a smaller, more interconnected place.
It's the reason we have such a diverse group of attendees here today.

But it's not without its downsides, and a lot of the time those benefits aren't evenly distributed.
Too many people, too many workers, too many families feel like they're bearing all the brunt of globalisation, and they're not feeling any of the benefits.

That could be in things like automation and job losses (which again, the tech industry is sort of responsible for).
Or things like open borders, mass movement of people, the changing of cultures.
People are afraid -- they're worried about their economic security, their job prospects -- and they lash out.
This manifests itself in things like nationalism and xenophobia, and older audience members might remember a time when those were considered fringe political movements.
Happier days.



{% slide suspicious-minds 15 %}

With the advent of **social media**, a lot of those fringe movements have become mainstream.

We're seeing now the true effect of having a firehose of unfiltered information and outrage piped directly to a screen in our pockets.
Social media stirs up anger, it provokes hate, it spreads lies.

When I was younger, there was a quote my grandfather loved: *"A lie can get halfway around the world before the truth has got its boots on.*
Not only has the Internet made the lie go a lot faster, it's also completely mangled that quote.
If you type that quote into Google, you will find at least 15 different people who it's attributed to, and that cannot possibly be right!

One aspect of this is "fake news".
It's become a bit of a catch phrase the last year or so as a catch-all term for "everything that Donald Trump doesn't like" but there is---

(I started saying "legitimate fake news", which is surely an oxymoron.
Let's try that again.)

There is "news" that is really fake.
You can go on the Internet now, you can find a website that looks like a legitimate news source with not sentences that contain words that you think are facts -- and it's entirely wrong.

This makes it much harder now to determine true from false when we're reading the news.
Not only that, social media has eroded our ability to do so, by presenting us with a firehose.
It's a denial-of-service attack on our ability to make trust decisions, because there's just so much stuff we have to deal with.



{% slide suspicious-minds 12 %}

So these are the three things that have led to an erosion of trust:

1.  Major world events
2.  The downsides of globalisation
3.  The advent and spread of social media

These three trends all build on each other.
They accelerate each other, and perhaps it's not so surprising that we don't trust each other as much as we used to.

But it's not like trust is gone entirely.
We can still be very trusting people -- let's look at a few examples.



{% slide suspicious-minds 16 %}

First: **online banking**.

If you paid for your own ticket for the conference, you'll have seen a screen that looked a bit like this, and you all happily put in your credit card details and clicked the pay button.
(At least, it seems like you did, because you're all here.)
And we gave you a ticket.

You put in your credit card details, and you trusted that we were going to send that to a credit card provider and use it to pay for your ticket -- and we weren't going to use it to buy Bitcoins, we weren't going to send it to a server in Russia, it wouldn't be sent to my personal Gmail.

We trust that we can put our banking details into website into the Internet, and it's going to work.
If you think about it, that's a really recent thing.
Not so many years ago, that would have been a very unusual thing to do, and yet today we just take it granted.



{% slide_captioned suspicious-minds 17 %}
  I'm sure this driver is just making sure she's crossing the road safely.
  What an upstanding fine citizen!
{% endslide_captioned %}

Another example: **ride-sharing**.

When I was younger, I was taught ["stranger danger"](https://en.wikipedia.org/wiki/Stranger_danger).
You don't give out your personal details on the Internet; you don't get into other people's cars; you don't give out your location.
And now it's routine for people to give out their personal
details on the Internet… to a stranger… to
invite them to their location… so that we can get in their car.

And then we pay them for it.

And many people even trust this more than they trust traditional black cabs or public transport.
This book isn't that old -- this is another weird inversion of trust.



{% slide suspicious-minds 18 %}

The final one: **Airbnb**.

How many of you are staying tonight not in a licensed hotel chain, not a registered B&B, not in Mrs. Potts but you've gone to a stranger's home?
*[Ed. [Mrs. Potts](http://www.mrspottsbackpackers.co.uk/) is a Cardiff hostel that's fairly popular among PyCon UK attendees. I saw a few hands in the audience.]*

You've picked a random stranger on the Internet, and said, "Yes, I will stay in your home, and I trust that you will not steal my things or turn out to be a bloodthirsty axe murderer or kidnap me so that I never seen again."

And likewise, your hosts -- they've invited you, a suspicious programmer type
going to "PyCon".
They trust that you're going to come into their home and sleep there and you won't steal their things, you won't ransack their home, and that it's safe to invite an (almost literally) revolving door of strangers into their home.

Again, something that we would have thought was quite odd a few years ago.
