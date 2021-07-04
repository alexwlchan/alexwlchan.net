---
layout: post
title: A wise choice of test strings
summary:
tags:
---

A few weeks ago, somebody at HBO Max had a bad day, when a mysterious email went out to their subscribers:

{% tweet https://twitter.com/juliehubs/status/1405689243393986561 %}

As the subject line suggests and was later confirmed, this was an email [sent from their test system](https://twitter.com/HBOMaxHelp/status/1405712235108917249).

One aspect that stuck out to me: the sensible choice of test strings (the subject line and body of the email), which helped avoid a much more embarrassing situation.

It can be tempted to use fun values when testing -- nobody else will ever see them, right?
It's just a joke between you and the other developers you work with.
It's a place to insert some whimsy and playfulness that you can't do elsewhere in the codebase -- but as HBO has just learnt, something that's private today may not be private in future.

Imagine part of your codebase appeared in front of somebody who isn't a developer, and who doesn't understand the context.
How would they react to it?
These test values look pretty good: they won't cause offence, it's easy to find their origin, and they don't sound scary to non-developers.

**As a rule of thumb, I assume that every private codebase will one day become public.**
That means I try to avoid writing any code I'd feel awkward writing in public -- which includes things like rude comments, offensive variable names, or insulting commit messages.
(I've seen too many bad examples to take good test values for granted.)

This incident seemed to go pretty well for HBO: in my circles at least, people were puzzled, then sympathetic, then shared stories of their own mistakes.
If this wasn't such an inoffensive email, it's easy to imagine how it could have been much worse.

*[This post started as a thread [on Twitter](https://twitter.com/alexwlchan/status/1405760375539212289).]*
