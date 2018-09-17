---
layout: post
title: Building trust in an age of suspicious minds
summary: Notes and slides from my PyCon UK 2018 keynote. In a world where people are less and less trusting, hwo can we take steps to make ourselves more trustable?
tags: pyconuk slides
theme:
  color: 109A19
  touch_icon: 109A19
---

This is a talk I gave this morning as the opening keynote of [PyCon UK 2018][pyconuk].

I was already planning to do a talk about online harassment, and Daniele (the conference director) encouraged me to expand the idea, and turn it into a talk about positive behaviour.
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

These are the notes of what I intended to say, but there was a lot of ad libbing.
I've tried to update them as best I can for what I actually said, but inevitably it's not a word-for-word transcription.

I prepped this talk at fairly short notice, and it wasn't as polished as I'd like.
There's a lot of um'ing and ah'ing.
If I end up doing this talk again, I'd love to go back and get some more practice.

---

<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.001.jpg"><img src="/slides/suspicious-minds/suspicious-minds.001.jpg"></a>
  <figcaption>
    Based on the cover art <a href="https://en.wikipedia.org/wiki/Suspicious_Minds#/media/File:Elvis_presley_suspiciousminds.jpg">of the Elvis single</a>.
    I was introduced to the song in the 2002 Disney film <a href="https://en.wikipedia.org/wiki/Lilo_%26_Stitch"><em>Lilo & Stitch</em></a>, which is the best Disney film by far.
    Don't @ me.
  </figcaption>
</figure>

(Introductory slide)

Hi, I'm Alex.

I'm a software developer at [the Wellcome Trust][wellcome] and one of the conference organisers.
It's a privilege to open this year's conference, and I hope you all have a great few days.

I spend my time thinking about how to exploit systems -- find bugs, loopholes, opportunities for harassment and bad behaviour.
(This is a polite way of saying I break things.)
And in turn, I think about how to design systems defensively, to prevent bad behaviour.

The defensive mindset leads to one of damage control, of "least bad" solutions -- for this talk, Daniele [the conference director] challenged me to flip this on its head.
Could I design a system to encourage *good* behaviour?
And I started thinking about good behaviour, and specifically about *trust*.

[wellcome]: https://wellcome.ac.uk/



{% slide suspicious-minds 2 %}

Trust is really important.

It underpins all effective working relationships -- with people, with tools, with systems.

If we have trust, we feel like we can rely on somebody, we can cooperate with them, we can believe them.
It permeates every aspect of our work and our lives -- our friends, our co-workers, our tools.
It gives us a sense of security, and means we're not looking over our shoulder for mistakes.



{% slide suspicious-minds 3 %}

But trust is a nebulous concept.
What is it?

In [*The Thin Book of Trust*][thin_book], Charles Feltman has a definition I really like:

> Trust is choosing to risk making something you value vulnerable to another person's actions.

Let's break down that definition:

*   **Choosing to risk.**
    Trust is a risk assement.
    We think about our past experience and decide if we want to take a particular risk.

*   **Something we value.**
    There are lots of things we might care about -- happiness, fulfilment, quality of work, not being booed off a stage in front of 300 people.

*   **Making it vulnerable.**
    We're giving up some control -- letting somebody else have responsibility.
    In tech, we usually think of vulnerabilities in the context of security, where they're bad and should be eliminated -- but vulnerability can also lead to growth, to progress.

And trust is multi-dimensional -- we trust different people with different things.
I might trust Alice to borrow a book, but not a loan.
I might trust Bob to borrow a loan, but not look after my cat.
And I might trust Carol to look after my cat, but not to borrow a book.

That's the definition of trust we'll be using today.

[thin_book]: https://www.thinbook.com/the-thin-book-of-trust/



{% slide suspicious-minds 4 %}

We're usually pretty good at articulating why we *don't* trust somebody.

Have you ever said *"I just don't trust that person"*?
Raise your hand.
[Nearly everybody in the room had their hand up.]

And if I asked, you'd probably have a good reason -- maybe there was some dishonesty, there were mean, made a mistake.
Maybe you heard some gossip.
There was some incident that made you distrust them.



{% slide suspicious-minds 5 %}

But what if I asked you in the other direction.
Think of somebody you really trust, and ask yourself: why do you trust them?

That feels like a harder question.

*   It isn't something you can tell somebody to do
*   You can't just ask for it
*   For all the Facebook marketing team would love, you can't buy it

We're vaguely aware that we trust certain people, but we're not sure why.
It's hard to say when we crossed a line from "acquaintance" to "person I trust" -- and that's not great.
If trust is so important, why aren't we better at articulating it, and knowing why it occurs?

That's what this talk is about -- how to stop being a passive participant in trust.



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.006.jpg"><img src="/slides/suspicious-minds/suspicious-minds.006.jpg"></a>
  <figcaption>
    Image: <a href="https://pixabay.com/en/easter-fire-brand-heat-firelight-1439323/">Easter Fire</a>, by claus-heinrichcarstens on Pixabay.
    CC0.
  </figcaption>
</figure>

So what's the state of trust in 2018?

It often seems like there isn't any!
If you look at the news or on Twitter, it seems like the world is on fire -- sometimes literally.

Studies show declining levels of trust -- we trust each other less and less.
And that includes big institutions -- business, governments, the media, non-profits -- places we used to look to for trust and guidance.



{% slide suspicious-minds 7 %}

How did we get here?
Why is trust in tatters?

I think it's caused by three major trends:

1.  Major events since the turn of the century
2.  The downsides of globalisation
3.  The advent of social media

Let's go through those in turn:



{% slide suspicious-minds 8 %}

**Major world events.**
There are several events that have shaken our trust in institutions:

<ul>
  <li>
    The <a href="https://en.wikipedia.org/wiki/September_11_attacks">9/11 attacks</a>, and the responses from governments around the world
  </li>
  <li>
    The wars in Iraq and Afghanistan, and the <a href="https://en.wikipedia.org/wiki/September_Dossier">questionable rationale</a> for doing so
  </li>
  <li>
    The 2008 <a href="https://en.wikipedia.org/wiki/Global_financial_crisis_in_September_2008">financial collapse</a>, and the ongoing fallout
  </li>
  <li>
    Closer to home, the <a href="https://en.wikipedia.org/wiki/Brexit">Brexit referendum</a> and subsequent “negotiations” [yes, I used air quotes]
  </li>
</ul>

All these things leave people feeling angry, bitter, divided, suspicious -- all a poor environment for building trust.

And I wonder if we're in the middle of another seismic trust event.
For years there's been a trickle of new stories about bad behaviour at tech companies -- privacy violations at Facebook, location tracking at Google, safety violations at Uber -- and it feels like maybe the trickle is becoming a flood.
I'm not sure yet, but I wonder if trust in the tech industry is faltering.
(Maybe one day the tech industry could aspire to be as trusted as bankers!)



{% slide suspicious-minds 9 %}

**The downsides of globalisation.**
Globalisation has undoubtedly advanced the human condition.
The world is smaller and more interconnected than ever before -- PyCon UK attends a wide range of attendees, the laptop I'm using has components from a dozen different countries.

But it's not without its downsides -- and the benefits aren't evenly distributing.
Too many people/workers/families feel they're bearing the brunt of globalisation, and not reaping the rewards.
It could be automation and job losses.
Or open borders, the mass movement of people, the changing of cultures.
People are worried about their economic security, scared for their job prospects.

This leads people to lash out, and to turn to xenophobia and nationalism -- which were once considered fringe movements.



{% slide suspicious-minds 10 %}

**The advent of social media** has taken these movements mainstream.
We're seeing the effects of having a firehose of unfiltered information and outrage, piped directly into our pockets.
It stirs up anger, it provokes hate, it spreads lies.

My grandfather had a phrase he liked when he was younger -- "a lie can be halfway round the world before the truth has its boots on" -- and social media has only made it faster.
(And even that quote is corrupted!
When trying to find the original author, Google suggested at least 15 different people.)

We all joke about fake news being anything that Trump doesn't like, but it's a legitimate concern.
[I tried to say "legitimate fake news", which feels like an oxymoron.]
You can go online and look at what seems like a genuine news website, with sentences which you think contain facts, which is entirely false.
The media is no longer a good indicator of what's true.

I think this serves as a sort of [denial-of-service attack](https://en.wikipedia.org/wiki/Denial-of-service_attack) on our ability to make judgements.
We're so overwhelmed with news and stories to evaluate, it's hard to make any judgements at all.

[The phrase I had in mind, but which I didn't say on stage, was [decision fatigue](https://en.wikipedia.org/wiki/Decision_fatigue).]



{% slide suspicious-minds 7 %}

All these three things build on each other, and accelerate each other.
It leads to an erosion of trust -- and it starts to make sense why people don't trust each other any more.

But in other ways, we're more trusting than ever -- let's look at some examples.



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.011.png"><img src="/slides/suspicious-minds/suspicious-minds.011.png"></a>
  <figcaption>
    A screenshot of the PyCon UK payments screen.
  </figcaption>
</figure>

If you paid for your own ticket, you went through this payment screen.
(Or at least, I hope you did, as you're all here!)
And you put in your credit card details, and you just trusted that was okay.
You could put them into a website, and they'd be sent to our credit card provider, and not a shady Russian server or my personal Gmail.

This is a really recent phenomenon -- online payments are brand new, relatively speaking.
And now we take them for granted, and forget they're a thing we had to get used to.



{% slide suspicious-minds 12 %}

Another example: ridesharing.
When I was younger, I was taught ["stranger danger"](https://en.wikipedia.org/wiki/Stranger_danger).
Don't give out your details to strangers, don't give out your location, don't get into other people's cars.

Today, it's considered routine to give out your details to a stranger, invite them to your location, and get into their car.

And pay them for it.

This is a really weird inversion.
And not only to people trust it, some people trust services like Uber and Lyft *more* than traditional taxi services or public transport.



{% slide suspicious-minds 13 %}

Or take Airbnb.

How many people aren't sleeping tonight in a hotel chain, or a licensed B&B, or Mrs&nbsp;Potts [the recommended conference hostel], but in a stranger's home?
You picked a stranger off the Internet, decided you'd sleep in their home, and you think it's unlikely you'll be murdered, have your belongings stolen, or be harassed while you sleep.

And in turn, your hosts have invited you -- a stranger to them -- to sleep in their home, and are trusting that you're not a terrorist or a murderer.
(Even worse: a programmer!)



{% slide suspicious-minds 14 %}

What do these examples have in common?

None of them happened by accident.
Declining trust in politicians doesn't mean we magically trust strangers more.
People deliberately built these systems to be trusted -- things like the green padlock, ratings in Uber, verification in Uber -- and we can do the same.

That's what we'll talk about to today -- how to build systems that build trust.



{% slide suspicious-minds 15 %}

So how do we build trust?



{% slide suspicious-minds 16 %}

How many of us have been on a "team-building" day [air quotes] and done the [trust fall](https://en.wikipedia.org/wiki/Trust_fall) exercise?
One partner closes their eyes and falls backwards, and the other partner will catch them before they hit the floor.
This supposedly builds trust.

(I gave a preview of this talk to some work colleagues earlier in the week, and one person had done this exercise and been dropped!
Err…)



{% slide suspicious-minds 17 %}

But lasting trust isn't a one-shot deal.
It's built over a series of interactions, and it's important not to mistake one-off events as trust builders.



{% slide suspicious-minds 18 %}

Trust is built incrementally.

As we interact with people, we get a sense of whether we trust them -- it all feeds into our risk assessment.

And we use this to judge groups/collectives, not just individual.
If our interactions with a group are good, we're more likely to trust another member of the group that we've never met.

For example, I've met lots of PyCon UK attendees, and they're all lovely.
If I meet a new person later, I expect that they'll probably be nice -- even though I've never met them before.
Whereas if I said to you all "I have a printer in the back room, and it just works, trust me!" -- nobody would believe me.



{% slide suspicious-minds 19 %}

To understand how we build it, let's think about how trust works.

Some of you might be familiar with [the fire triangle](https://en.wikipedia.org/wiki/Fire_triangle).
Oxygen, Fuel, Heat.
You need all three to make fire, and you put out fire by taking one of them away.

In the same way, trust is made of a series of interconnected factors, including

*   honesty
*   reliability
*   shared values

Let's go through them in turn.



{% slide suspicious-minds 20 %}

Honesty is about things like:

*   truthfulness -- if you lie to me, I don't believe what you say, and I won't believe what you say next time

*   sincerity -- do you care about what you're saying?

*   transparency -- do you say bad things as well as good things?

    If you only ever talk about good things, that's not so useful.
    Imagine a friend who always tells you that you look nice, no matter what you're wearing.
    If you've got a new outfit that you're a bit unsure of, you ask their opinion, and they say "you look great!", how much do you believe them?



{% slide suspicious-minds 21 %}

Reliability is about whether you keep your promises -- do you do what you say you'll do?

And it's about consistency.
As developers, we know this from our test suites -- a test that's flaky or intermittent is worse than no test at all, because even when it's passing we doubt its results.



{% slide suspicious-minds 22 %}

Shared values is about having:

*   common goals -- so we're all aiming for the same thing, rather than pulling in different directions

*   common values and beliefs -- do we all care about the same things?

*   common understanding -- how often have we been in a meeting, and everybody's agreed what the outcomes and actions are, and they've all agreed something different?



{% slide suspicious-minds 19 %}

So that's the trust triangle.

When you have an environment that encourages those three things -- honesty, reliability, shared values -- you have an environment where trust can form.

And again, you need all three of them -- you can't isolate one and still have trust.
Take honesty.
This is definitely a positive trait -- we'd all like to be thought of as honest, and work with honest people -- but would we trust somebody who was honest but unreliable?
We'd believe what they'll say, but not that they'll kepe their commitments.
The classic example: would you trust an honest but incompetent surgeon to perform surgery on you?
