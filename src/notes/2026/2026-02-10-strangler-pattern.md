---
layout: note
title: The "strangler" pattern is named after a tree, not an act of violence
summary: It's named after the strangler fig tree, which wraps itself a host tree and gradually kills them.
date: 2026-02-10 20:20:26 +00:00
topic: The world around us
---
In software development, the [strangler pattern][wiki-strangler-pattern] is an approach to upgrading old code.
You create a wrapper around old code, and gradually modify the wrapper to divert calls to your new code, until there's nothing left that's calling the old code.

I've never loved the name, because the word "strangler" conjures up some pretty violent imagery.
That's not a great vibe in an industry that's historically been pretty hostile towards women.
But today I read the Wikipedia article, and I learnt that it's actually a named for a type of tree.

Martin Fowler first compared software development with the strangler fig tree in 2004; here's a quote from [an updated version of his blog post][fowler]:

> During a vacation in the rain forests of Queensland in 2001, we saw some [strangler figs][wiki-strangler-fig]. These are vines that germinate in a nook of a tree. As it grows, it draws nutrients from the host tree until it reaches the ground to grow roots and the canopy to get sunlight. It can then become self-sustaining, and its original host tree may die leaving the fig as an echo of its shape.
>
> This gradual process of replacing the host tree struck me as a striking analogy to the way I saw colleagues doing modernization of legacy software systems. A couple of years later I posted a brief blog post about this metaphor. While I've not used the term in my writing since then, it caught attention anyway, and the term “Strangler Fig” is now often used to describe a gradual approach to legacy modernization.

At some point the word "fig" got lost, and for many years I only heard it as "strangler pattern".
I like this version more!

I can think of two other terms in software development which have oft-surprising etymologies.
Python is named after [Monty Python][python-monty], but everybody leans on snake imagery.
Rust is named after [a type of fungus][rust-fungus], and I'm not sure anybody would guess that if they didn't already know.

It's a bit unfortunate that "strangler fig" is often shortened to something that sounds more violent, and I'm glad to know the true origin.

[wiki-strangler-pattern]: https://en.wikipedia.org/wiki/Strangler_pattern
[wiki-strangler-fig]: https://en.wikipedia.org/wiki/Strangler_fig
[fowler]: https://martinfowler.com/bliki/StranglerFigApplication.html
[python-monty]: https://docs.python.org/3/faq/general.html#why-is-it-called-python
[rust-fungus]: https://www.reddit.com/r/rust/comments/27jvdt/internet_archaeology_the_definitive_endall_source/
