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

I think that's pretty much the entire audience *[Ed. I was looking at a room full of raised hands]*

If I asked you all, you all had a good reason, right?
Maybe there was a lie, there was an incident, they were mean, you had some
gossip...



{% slide suspicious-minds 8 %}

But what if I asked you to go in the other direction?
Think of somebody you really trust.

If I asked you "why do you trust them", it feels like a harder question, doesn't it?
We're often aware that we trust somebody, but it can be hard to pinpoint the moment when that happened.
How do we go from the state of "somebody we just know" to "somebody we actually trust"?





---
---
---
---
---







But trust is a nebulous concept.
What is it?

In , Charles Feltman has a definition I really like:


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

[thin_book]:



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

*[Ed. The phrase I had in mind, but which I didn't say on stage, was [decision fatigue](https://en.wikipedia.org/wiki/Decision_fatigue).]*



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



{% slide suspicious-minds 23 %}

So we know what the ingredients for trust are, and we all agree these are good traits.

We can't just "try harder" -- that's a recipe to make very little change.
When we're programming, and we want to write better software, we don't just try to write fewer bugs -- that only leads to marginal gains.
To write better software, we use new tools and processes, and building trust is just the same.



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.024.jpg"><img src="/slides/suspicious-minds/suspicious-minds.024.jpg"></a>
  <figcaption>
    Image: <a href="https://pixabay.com/en/animals-waterfowl-ducks-young-737407/">waterfowl ducks</a>, by user 422737 on Pixabay.
    CC0.
  </figcaption>
</figure>

We can start with ourselves.
Humans are natural mimics, so if you demonstrate the trustworthy behaviours you want to see in other people, you'll build trust in yourself *and* encourage others to act in a more trustworthy way.



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.025.jpg"><img src="/slides/suspicious-minds/suspicious-minds.025.jpg"></a>
  <figcaption>
    Image: <a href="https://www.pexels.com/photo/space-grey-ipad-air-with-graph-on-brown-wooden-table-187041/">iPad Air on a brown wooden table</a>, by Burak&nbsp;K on Pexels.
    CC0.
  </figcaption>
</figure>

We can monitor our levels of trust.

Although we can't give it a metric or plot a graph, we do have an innate sense of whether somebody trusts us.
When I asked you earlier to think of somebody you didn't trust, and then somebody you did, you thought of somebody almost instantly [nodding in the room] -- and you can track that.

Ask yourself -- do I trust this person?
Do I think they trust me?
You can even ask them explicitly: "do you trust me?"
And you can track the trend, and that can show you where you need to make changes, and if they're working.

In the last year, I've got into the habit of asking friends this.
"Are we good?"
"Is everything okay between us?"
"Have I done anything to upset you?"
Little check-ins that establish things are okay, and I'm not inadvertently upsetting them.
It feels awkward at first, but can be really helpful.



{% slide suspicious-minds 19 %}

Now let's look at examples of new tools and processes, applied to different parts of the trust triangle.



{% slide suspicious-minds 26 %}

Start with honesty.



{% slide suspicious-minds 27 %}

Take Airbnb as an example.
If you're a host, and somebody who wants to stay in your home says they're not a bloodthirsty axe murderer, how do you believe them?

With identity checks -- a way to verify truthfulness.
Airbnb sometimes asks for legal ID, and compares it to lists of known ne'er-do-wells -- terrorists, no-fly lists, Interpol notices, that sort of thing.

*[Ed. Legal ID isn't a system without problems.  Some people have harder time getting ID than others, which disenfranchises them from services that rely on ID like this.  It's a motivating example, not a perfect solution.]*

{% slide suspicious-minds 28 %}

Let's think about transparency.
We often have managers who "want transparency" and want to be told about possible problems -- but if we're worried about pushback or retribution, we may not be as transparent as they'd like.
It can be hard to tell somebody they've made a mistake if they control your salary, your work, your job progression.

So how do we fix that?
We have to change the incentives.

Here's a screenshot of our API just before I left for the conference.
The day before a big trip is always the best time to deploy.
Ahem.
(It's not supposed to do that.)

Now I could have come to the conference and pretended nothing was wrong -- but what my team really wants is for me to be transparent, and tell them about my mistake, so we can fix it.
And so they change the incentives -- they'll be upset with me if I try to conceal the mistake, and later find it out later (the stick), and if I fess up, I'm praised for my honesty and we get to fix the mistake (the carrot).

Transparency can't just be lip service -- the incentives have to match.



{% slide suspicious-minds 26 %}

(End of examples for honesty)



{% slide suspicious-minds 29 %}

Now examples for reliability.



{% slide suspicious-minds 30 %}

Let's pick another example from earlier: Uber.
Here's a screenshot from my trip to the venue this morning.

After the trip, I'm invited to review my driver -- and review systems like this are a great way to improve trust.
Positive reviews tell us that other people had a good experience; so we're more likely to have a good experience ourselves.
Lots of sites use this mechanism, not just Uber -- TripAdvisor, Amazon, iTunes, to name but a few.

*[Ed. Uber had [a big rebranding](https://www.fastcompany.com/90235065/uber-has-a-new-brand-again) a day or so before the conference. I'd already spent enough time photoshopping this slide, so I left the screenshot as-is.]*



{% slide suspicious-minds 31 %}

Reviews tell us that we're already being reliable -- but how do we become *more* reliable?
How to we earn/deserve those positive reviews?

As programmers, we're used to dealing with unreliable systems -- they're called "computers".
Software is inherently tricksy and unpredictable, and we have lots of tools to help us write more reliably software, some of which we'll talk about this weekend.

Notice that these are all external tools -- none of them are about me -- and the same principle applies to tools for improving our reliability in other areas.



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.032.jpg"><img src="/slides/suspicious-minds/suspicious-minds.032.jpg"></a>
  <figcaption>
    Image: <a href="https://www.pexels.com/photo/white-and-black-weekly-planner-on-gray-surface-1059383/">Black and white planner on a grey table</a>, by Bich&nbsp;Tran on Pexels.
    CC0.
  </figcaption>
</figure>

On a personal level, that means something like a personal diary or a todo list -- something to help us keep track of our promises and commitments.
Pushing it out to an external system means we're less likely to forget things, and less likely to over-commit to a promise it turns out we're unable to keep.



{% slide_captioned suspicious-minds 33 %}
  Image: [Woman holding yellow sticky note](https://www.pexels.com/photo/woman-holding-yellow-sticky-note-1391405/), by rawpixels.com on Pexels.
  CC0.
{% endslide_captioned %}

In larger teams, I think there's something to be taken from the world of [agile](https://en.wikipedia.org/wiki/Agile_software_development).
I know that's a dirty word in some quarters, but there are valuable parts for tracking reliability -- regular standup meetings, project boards, task tracking -- that let us see how much a team is committed to, and whether promises are starting to slip.



{% slide suspicious-minds 29 %}

So those are examples for reliability -- external systems that hold us to account.



{% slide suspicious-minds 34 %}

{% slide suspicious-minds 35 %}

{% slide suspicious-minds 36 %}

{% slide suspicious-minds 26 %}

{% slide suspicious-minds 37 %}

{% slide suspicious-minds 38 %}

{% slide suspicious-minds 39 %}

<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.040.jpeg"><img src="/slides/suspicious-minds/suspicious-minds.040.jpeg"></a>
  <figcaption>
    Image: <a href="https://pxhere.com/en/photo/493486">Volkswagen grille</a>, from Pxhere.
    CC0.
  </figcaption>
</figure>

{% slide suspicious-minds 41 %}



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.042.jpeg"><img src="/slides/suspicious-minds/suspicious-minds.042.jpeg"></a>
  <figcaption>
    Image: <a href="https://pxhere.com/en/photo/751319">British Airways plane against a blue sky</a>, downloaded from Pxhere.
    CC0.
  </figcaption>
</figure>

Let's look at an industry that really cares about its mistakes: aviation.

Planes are weird, right?
We all know how gravity works -- things go down.
This plane isn't going down.
What's up with that?

Despite seeming counterintuitive, planes are one of the safest ways to travel.
Last year, there were [no deaths in commercial aviation accidents](https://www.reuters.com/article/us-aviation-safety/2017-safest-year-on-record-for-commercial-passenger-air-travel-groups-idUSKBN1EQ17L).
How did they do it?



<figure class="slide">
  <a href="/slides/suspicious-minds/suspicious-minds.043.jpeg"><img src="/slides/suspicious-minds/suspicious-minds.043.jpeg"></a>
  <figcaption>
    Image: <a href="https://pxhere.com/en/photo/775521">Black and white image of a crashed plane</a>, downloaded from Pxhere.
    CC0.
  </figcaption>
</figure>

Because it's not like planes *never* crash -- they do have issues.

Here, the plane has broken an implicit promise of reliability -- it's meant to stay in the air, and it's clearly not done that.
So why do we trust planes?



{% slide suspicious-minds 44 %}

One tool



{% slide suspicious-minds 45 %}

{% slide suspicious-minds 46 %}

{% slide suspicious-minds 41 %}

(Repeat the process for rebuilding trust.)

{% slide suspicious-minds 38 %}

So that's how you recover from a mistake, and rebuild trust.

And if done well, that works in your favour!
There are studies that show if buy something from a shop, and have to return a faulty item, you're actually more likely to shop there -- even compared to somebody who never had a problem!

Remember that trust is built by small interactions -- this is another interaction that proves your reliability.
It's another data point in the risk assessment.

So think carefully about mistakes, and how you'll recover when (not if!) they happen.

{% slide suspicious-minds 19 %}

So let's recap what we've talked about today.

We've discussed the value of trust, and why it's such a critical part of effective working relationships.
It's something that permeates every aspect of our work and lives.

And we've seen the *trust triangle* – honesty, reliability, and shared values – a framework for behaviour that encourages and builds trust.
I've shown you a few examples of tools and processes to build trust; I'm sure you can think of others.

All this serves to build environments where trust can grow and thrive, which is the foundation for lots of other good things.

{% slide suspicious-minds 47 %}

If I want you to take a single thing away from this keynote, it's this: *trust is something you can actively build*.
Trust doesn't have to be something that "just happens" to you; you can and should take explicit steps to build it, and I hope I've given you some ideas how.

And on that note, I'll finish.
Thank you.

{% slide suspicious-minds 1 %}

(Closing slide)
