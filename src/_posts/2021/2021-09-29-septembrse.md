---
layout: post
date: 2021-09-29 20:23:05 +00:00
title: "SeptembRSE: Missing narratives in discussions around diversity and inclusion"
tags:
  - talks
  - inclusion
---

Yesterday I was part of a panel on [missing narratives around diversity inclusion][panel_link] as part of SeptembRSE, a conference for Research Software Engineers.
It was a pleasure to be invited, and I learnt a lot listening to the other panellists.

There are [notes from the session][notes] and a [video recording].
This post has my notes, based on a rough transcript, plus my responses to two questions from the Q&A that didn't fit into the time.

This post is only lightly edited, because I wanted to finish it while the event was fresh in my mind.

[panel_link]: https://septembrse.github.io/#/event/L1001
[notes]: https://pad.sfconservancy.org/p/missing-narrative-rse-panel-2021
[video recording]: https://www.youtube.com/watch?v=tpxCWCTSZUc&t=2014s

## Redefining merit, and the inequality of free time

These are the prompts we were given:

1. How did someone center and advocate for intersectionality marginalised voices, and how did that make a positive impact?
2. When did someone redefine merit and how did that make a positive impact?

Here's what I said:

I was thinking about this question of defining merit, and I started thinking about an aspect of merit that we often see in the software industry: workaholism.
The idea that you should work, work, work.
Somebody who works all the hours in the day somehow better than somebody who doesn't.

Think about the flipside: if you're able to work, work, work, what that probably means you have a lot of free time.

Some people have more free time than others.
t's a function of other aspects of your life – how much free time you have, how much free time you can devote to work.
For example, somebody who has a well-paid 9 to 5 job, they might have a lot of free time – versus somebody who's working two or three jobs and struggling to make ends meet.

The amount of free time you have is already an inequity.
That gets even worse if your free time becomes a lever to gain certain advantages, like promotion, compensation, or opportunities.

This is something we've always tried to be aware of on my team – that the amount of free time somebody has can have an impact on their opportunities.

We've tried ensure people don't use their free time to gain an unfair advantage at work.
We do software development.
It's not the sort of work where putting in more hours is going to benefit you as an individual or an organisation.
We don't want to incentivise overwork, so we don't pay overtime.
We don't schedule it, we don't pay for it.

You can choose to work outside office hours, but you won't be financially compensated for that.
And anything you do in that time can't be considered when it comes to things like annual reviews, performance ratings, bonus season.
We try to measure those based on what you do in those core hours, not what you do in your free time.

There's a variety of reasons you don't want people doing overtime, this is just one of them.
We don't want people using their free time to get opportunities at work that other people might not able to access.

Then the last 18 months happened.
This has exposed the inequity and inequality of free time even more, because some people have seen more draws on their time than others.

Suppose you're a parent or having caring responsibilities, and that was something that was previously handled for you during work hours -- now that's your problem.
You had young kids going to school, you came into the office, did a day's work, went home and collected the kids from school.
Now you're having to supervise your children at the same time as trying to work.

(And we know this disproportionately affects women.
Raising children isn't equally distributed across genders.)

Some people on our team just can't do the same number of hours as they could when we were in the office.
How do we make sure that the number of hours they can work doesn't have a disproportionate effect, and doesn't affect their access to opportunities, promotion, and compensation?

We try to handle it in two ways.

First, we've tried to adjust our expectations of somebody's output.
If you were doing an eight hour day before, now you're doing a four hour day, that's okay.
We acknowledge that caring, parenting, and so on – those are important things.
We only expect you to do the hours you can manage, and we're not going to harangue or harass you to make up the hours.
We know you're doing the best you can and we try to adjust our expectations accordingly.

But this introduces a new risk that someone's going to be marginalised on the team because we're expecting less of them.

We've been careful to make sure we continue to centre people, regardless of their hours – in leadership roles, in technical roles.
We continue to give them opportunities to drive things forward on the team, and we respect their primacy in those projects.

Somebody might have young kids, maybe they can't always do a full day, but they're still the project lead.
Even if somebody else is putting in more hours, grinding away for longer, they're still the project lead.
They're the key decision-maker, they report on the project at the all-hands meeting, they decide what's happening next.
They're still the project lead.

We want to make sure that just because you're working less hours doesn't mean we don't stop counting you as a member of the team.

Those are a few examples of how we're trying to make sure that your free time, the number of hours you can work doesn't affect your opportunities and promotion, and that free time doesn't become a wedge for more marginalisation.

## Q&A: Programming in non-English languages

This was a question in the Q&A:

> Most programming languages use English keywords.
> Is this a barrier for non-native English speakers?
> Does this need to be balanced against ease of sharing?

Yanina and Rowland talked about the barrier and cost of learning to program in English if it's not your first language; I wanted to add a couple of other thoughts.

The questioner asked about programming languages, but this issue goes much wider -- it's also the tooling that goes around software development.

Tooling is hardware and input devices, including keyboards.
You can use a QWERTY keyboard with a remapped layout or try to find a non-QWERTY keyboard, but they're both points of friction.

Tooling is also the software that help us write software: our text editor, IDE, debugger.
If those tools or their documentation are only available in English, they're unusable for people who don't speak it.

This can create a "rich get richer" scenario.
For example, I was recently doing some profiling work, following instructions from a blog post written in English.
I was able to fix several inefficiencies, so my code runs faster and cheaper.
This has lots of obvious knock-on benefits which aren't available to somebody who can't read that blog post.

Of course, I wouldn't be able to read that blog post if it had been written in Spanish instead of English – but programming content is heavily weighted towards English.

This gets 10x harder if you use a language that isn't left-to-right; tooling support for right-to-left languages is notoriously bad.
For example, if I put Arabic in my text editor, text selection stops working.
For more on Arabic and computers, I recommend [Rami Ismail's XOXO talk](https://www.youtube.com/watch?v=X1ynZm1wI18).

Trying to write software when you speak English is a thousand papercuts.

## Q&A: The accessibility of virtual conferences

Another question in the Q&A:

> Q: Do you think virtual conferences have helped or hinder people being allowed more opportunities?

I've written previously about my [ideas for inclusive events](https://alexwlchan.net/ideas-for-inclusive-events/), so I have thoughts on this.
Briefly:

I think virtual conferences are a mixed bag: they're not uniformly better or worse.
They extend opportunities to some people, but make them harder for others.

For example: travel.
Being able to participate virtually is great for some people, because they don't have to travel.
Travelling is tricky for a variety of reasons, including cost, time, and visas – more people can participate if they don't have to travel.
But you can only participate virtually if you have a reliable Internet connection, which isn't a given.

I think virtual conferences are going to improve at inclusion and accessibility.
Virtual conferences are still fairly new for a lot of organisers, and it takes time to find the best practices.
Compare to in-person events, which have been running for decades – many more opportunities to get feedback, improve, repeat.
