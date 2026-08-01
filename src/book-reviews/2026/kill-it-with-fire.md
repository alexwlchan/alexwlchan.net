---
layout: book_review
date: 2026-08-01 09:28:32 +01:00

book:
  contributors:
  - name: Marianne Bellotti
  genres:
  - non-fiction
  - technology
  - software development
  isbn13: 978-1-718-50118-8
  publication_year: '2021'
  title: Kill it with Fire

review:
  date_read: '2026-07-29'
  format: paperback
  rating: 5
  summary: A thoughtful discussion of how to modernise software projects, and how to avoid needing it.

colours:
  css_light: '#094980'
  css_dark:  '#eda31e'

---

A lot of my recent work has been around building systems to last -- ideally for decades or centuries -- and so I was interested to read the perspective of somebody who has to maintain and modernise those systems.

The key themes:

*   The hardest part of a modernisation project is managing people, not technical issues.
    Most of the book is about how to keep people motivated and engaged, and how to maintain momentum once a project starts.
*   Start small and iterate from there; don't try to bit off too much at once.
    Develop your knowledge of the system; improve monitoring and resilience; build up to bigger changes.
    This is the classic “don’t do a big rewrite” advice, but with more depth and reasoning.
*   Know how your modernisation project relates to the business's goals.
    This gets you the buy-in for your project, and gives you a way to measure progress.
    (This and other ideas overlap with [*Impact-First Product Teams*][me-impact-first-product-teams].)
*   We overestimate how much we can learn from an existing system as a reference for what to do next.
    It works and it solves the problem, but we're missing the context for its design.

The book is fairly short and easy to read, with a good mix of anecdotes to add flavour.
I'd recommend for software developers working at any level of experience, with systems of any age.

---

## Notes and highlights

### Introduction

Legacy modernisation is a ubiqituous feature of working with computers, and affects organisations of all ages and sizes.
We'll all be surprised by how long our code lasts -- something can run for much longer than we expect.

Page xvi, a reminder that technology will either become old or unused:

> Simply being old is not enough to make something legacy.
> The subtext behind the phrase *legacy technology* is that it's also bad, barely functioning maybe, but legacy technology only exists if it is successful.
> Those old programs are perhaps less efficient than they were before, but technology that isn't used doesn't survive decades.

Page xx:

> We are reaching a tipping point with legacy systems.
> The generation that built the oldest of them is gradually dying off, and we are piling more and more layers of society on top of these old, largely undocumented and unmaintained computer programs.
> While I don't believe society is going to crumble at our feet over it, there's a lot of good, interesting work for people willing to jump in.

### Chapter 1: Time is a flat circle

Technology advances in cycles, not linearly.
Compare the similarities between mainframes and cloud computing.

This is inevitable, because over time, technology will optimise for one use case, and eventually the edge cases will coalesce into a viable product space for an alternative.
Moving in one direction means leaving some customers beside.

Big shifts often centre on the balance between local processing power and network bandwidth.

### Chapter 2: Cannibal code

Avoid upgrading technology simply because it's new.
But also don't hold off adopting new technology for too long -- every upgrade comes with cultural assumptions, and working through too many at once is difficult.

Advances in technology "cannablise" what came before them -- they copy patterns, ideas, and techniques from outside computing.
Often the effect of these influences is felt long after the world has moved on, but technology hasn't changed to match.

Consider the tradeoff between risk and ambiguity.
(I like this as an alternative framing to "unknown unknowns".)

We often gravitate towards full rewrites over incremental refactoring because it has "an attractive level of ambiguity" .
We're often adding new features, extending the original concept, or using novel techniques -- versus the lack of ambiguity in the original system.
Full rewrites are attract, but they're less likely to improve the system.

Familiar interfaces help speed up adoption.

Page 26 has a quote from *The UNIX-HATERS Handbook* which explains that the brevity of common Unix commands may be down to the limitations of a hardware keyboard, which have then been handed down through the ages:

> The novice Unix user is always surprised by Unix's choice of command names. No amount of training on DOS or the Mac prepares one for the majestic beauty of cryptic two-letter command names such as `cp`, `rm`, and `ls`.
>
> Those of us who used early 70s I/O devices suspect the degeneracy stems from the speed, reliability, and, most importantly, the keyboard of the ASR-33 Teletype, the common input/output device in those days. Unlike today's keyboards, where the distance keys travel is based on feedback principles, and the only force necessary is that needed to close a microswitch, keys on the Teletype (at least in memory) needed to travel over half an inch, and take the force necessary to run a small electric generator such as those found on bicyles.
> You could break your knuckles touch typing on those beasts.
>
> […]
>
> After more than two decades, what is the excuse for continuing this tradition?
> The implacable force of history, AKA existing code and books.

This reminds me of something I heard when I joined Tailscale, about [grants and ACLs][tailscale-grants-vs-acls].
ACLs are deprecated and it would be technically straightforward to upgrade all customers and remove them entirely, but there's no desire to do so.
That would invalidate years of tutorials, blog posts, and videos, and that learning material has tremendous value.

Page 32 (emphasis mine):

> Engineers tend to overestimate the value of order and neatness. **The only
thing that really matters with a computer system is its effectiveness at
performing its practical application.** Linux did not come to dominate the
operating system world because it had been artfully designed from scratch;
it scraped together ideas and implementations from a number of different
systems and focused on adding value in one key place, the kernel.

Page 32:

> The incentives that reward individual software engineers for their
uniqueness, their ability to do new things, or to do old things in innovative
ways are still present, even if the desire to publish papers in academic
journals has been supplanted by the desire to write popular blog posts. Yet
technology is more likely to be successful when it builds on common
things. These two forces are always in tension with any software project,
but legacy systems are particularly vulnerable.

Page 37:

> Figuring out when consistency adds technical value and when it is
artificial is one of the hardest decisions an engineering team must make.
Human beings are pattern-matching machines. The flip side of finding
familiar things easier is that we tend to over-optimize, giving in to artificial
consistency when better tools are available to us.

### Chapter 3: Evaluating your architecture

Three principles to keep in mind when deciding how to deal with legacy technology:

*   Modernisations should be designed around adding value, not chasing new technology
*   Familiarity can speed up adoption
*   People learn about new ideas through their networks, which may not match popularity

("Adding value" reminded me of the ideas discussed in [*Impact-First Product Teams*][me-impact-first-product-teams].)

When considering a legacy modernisation projet, ask yourself: what's the failure behind the desire to modernise?
"If it ain't broke, don't fix it" -- nobody starts one of these projects if everything is fine.

1.  **Technical debt** -- for example, a codebase that's difficult to understand or makes it hard to hire new engineers.
    This is usually caused by sub-par tradeoffs, or changes in the requirements or the tools available.

    Ask yourself: is it done this way because that's the best approach, or because it's always been done that way.

    Fixing technical debt means restoring consistency.

2.  **Performance issues.**
    Performance is relative, and only an issue if the organisation thinks something is wrong.
    If so, you have a well-defined goal for what to improve.

    Incremental improvements can compound -- if you can't find big improvements, look for ways to make 5% or 10% improvements.
    Those add up!

    Beware the quick fix to buy time to solve the underlying issue; it's easy for the organisation to forget about the problem once the immediate pain is resolved.

3.  **Stability issues** -- the app does the right thing, but it has quirks or weird behaviour.

    All systems involve a tradeoff between *coupling* (different components affect each other) and *complexity* (components are tricky to understand).
    Quoting page 48:

    > Problems that are caused by human beings failing to read something, understand something, or check something are usually improved by minimizing complexity.
    > Problems that are caused by failures in monitoring or testing are usually improved by loosening the coupling (and thereby creating places for automated testing).

    The goal isn't to minimise them both, but to balance them in the correct way.
    Can you change the ratio to mitigate problems?

When you start a legacy modernisation project, start small.
Develop your understanding of the system; improve observability and monitoring.
This will give you the deeper knowledge you need to make larger changes.

The book then compares various strategies, like a full rewrite, iterating in place, or splitting services in-place.

A good plan sets expectations and a direction -- how do you get started, learn more, and iterate towards a better system?

## Chapter 4: Why is it hard?

A successful modernisation is hard because of people problems, not technical ones.
Keeping your engineers motivated and managers engaged is the difficult part.

We overestimate the value of luck in our original decision-making, and presume too much of the original system.
We imagine we can use it as a perfect reference for how to solve the problem, but we've lost the context for those past decisions, so we can't learn as much as we think.

We underestimate and ignore "overgrowth" -- the coupling between an application and its dependencies, including the platform it runs on.
Our code almost certainly relies on specific behaviours that are different or not present in newer environments.

Beware of over-reliance on tools and automation.
There are limits to how much you can bridge gaps between technologies without human intervention.
For example, a program written in COBOL that's automatically ported to Java will still be structured like COBOL, and look unfamiliar to seasoned Java programmers.
(The book was written before the widespread use of LLMs, which change some of this, but not all of it.)

A good project manages expectations:

*   manages expectations
*   doesn't over-extend the scope or add new features
*   tries to recover the past context
*   uses tools as an augment, not a silver bullet

## Chapter 5: Building and protecting momentum

Use the same approach for modernising as for building software -- start small and iterate.
Don't assume the presence of the existing system means you understand all the requirements.

Look for measurable problems and focus on improving those.
This pushes the internal politics onto the executive who apprroved the goals, not the engineering team implementing them.
This means you can track your progress, which helps maintain motivation.

Modernisation projects don't fail because of technical issues, but loss of momentum.
Ways to preserve momentum:

*   **Fix your meeting culture.**
    Bad meetings are momentum killers.
    Here's an interesting idea from page 82:

    > With my engineers, I set the expectation that to have a productive, free-
    flowing debate, we need to be able to sort comments and issues into in-scope and out-of-scope quickly and easily as a team. I call this technique
    “true but irrelevant,” because I can typically sort meeting information into
    three buckets: things that are true, things that are false, and things that are
    true but irrelevant. Irrelevant is just a punchier way of saying out of scope.

    The goal isn't "no out of scope comments", but that they're identified and dispatched quickly.

*   **Work out how to resolve disagreements.**
    When there are disagreements, it's usually because two people are optimising for different goals.
    What are they?
    What is the team trying to achieve?

*   **Tackle scepticism early.**
    Scepticism comes from a history of failed attempts and institutional scar tissue.
    To prevent this slowing you down, front-load value to break the pattern of failure.

*   **Minimise the big decisions required.**
    Each decision adds friction and layers of approval.
    Look to ride the coattails of already-approved projects; opportunities to make decisions for compliance; seek forgiveenes rathert han permission.

    When you do have to seek approval from management, explain your value in the business's terms, not just engineering-driven goals.

If you need something to start the process, look for a (potential) crisis to create a sense of urgency.
Problems around stability and security are the two common ones.
You don't have to lie; instead, tell a compelling story about the risk.

### Chapter 6: Coming in midstream

What if a project is already mid-cycle and struggling?

*   Find responsibility gaps.
    What falls between the cracks?
*   Meetings which have large invitation lists, run long, or are scheduled at short notice are all red flags, and a sign of problems in that area.
*   Look for problems that people are running away from, or making excuses for not tackling.

Break the cycle of compounding problems; avoid the death cycle of an ineffectual project.

A common idea in modernisation projects is breaking up monoliths, as if monoliths are inherently bad -- that's not true!
Small organisations create monoliths because small organisations *are* monoliths.
Larger organisations can have the organisational structures to build a more diverse set of services.
Only break up a monolith if you need to -- fixing something that isn't broken sucks momentum and breaks trust.

All software will be rewritten eventually, and you cannot design your way out of future concerns.
Plan for it, don't avoid it.
(This was another theme in [*Impact-First Product Teams*][me-impact-first-product-teams].)

Fixing the wrong thing is a bad idea, but once you've started you must finish.
Don't leave a system in a half-migrated state, because you've just created more problems to be fixed later.

Forgotten or misunderstood resources make a system harder to reason about.
Inventory your fleet as best you can, but accept perfection is likely impossible.

Prioritise resilience over reliability -- aim for a fast resolution time, not five 9s of reliability.
This gives you more room to make big changes, because you aren't constrained by strict uptime guarantees.

Systemic issues can span many teams, like coding practices that were copied from project to project.
It can be hard to get buy-in from teams to resource fixing, especially if it's not solely their problem.
Consider declaring a "Code Yellow".
This is a practice from Google; a large incident that spans multiple teams and is the absolute priority for involved members.
They give all their time to the Code Yellow, and provide guidance to the rest of the organisation.
The goa is to get back to the point where standard team structures can absorb the work.

Too many failures can cause a crisis of confidence.
If a team doesn't believe they can deliver, they'll avoid big changes that might prove their doubts correct.
Consider using "murder boards".
These are an intense interrogation of a technical design, an exercise where the focus is *survival*.
They prove that an idea is sound, and give reassurance that if problems still occur, it's not a reflection of th team's moral character.

Useful advice for anywhere in the workplace, not just in legacy modernisation projects (page 100):

> When you can, it is always better to set up someone else for victory rather than solving the problem yourself.

I relate to this sentinment on page 105:

> I had a friend who used to say her greatest honor was hearing a system she built had to be rewritten in order to scale it. This meant she had built something that people loved and found useful to the point where they needed to scale it.

Page 128 emphasises the role of a leader:

> Legacy modernization projects do not fail because one mistake was made
or something went wrong once. They fail because the organization deploys
solutions that actually reinforce unsuccessful conditions. If you’re coming
into a project in the middle, your most important task as a leader is figuring
out where those cycles are and stopping them.

### Chapter 7: Design as destiny

Page 130 establishes an important distinction:

> Problem-*solving* versus problem-*setting* is the difference between being
*reactive* and being *responsive*.

Design conversations for the outcome you want, and turn them into a game.
For example, incentivise finding novel solutions using a piece of technology rather than shooting down other people's ideas (which is the default strategy in many discussions).

When asking follow-up questions:

*   *Why…* leads to abstract statements
*   *How…* gives practical and actionable information

Both are required!

In organisations without a defined career ladder or progression, engineers are motivated to do things that raise their personal profile, even if they're worse decisions for the system overall.

As somebody who's been through too many restructures, I was struck by this comparison on page 151:

> The reorg is the matching misused tool of the full rewrite. As the software
engineer gravitates toward throwing everything out and starting over to
project confidence and certainty, so too does the software engineers’
manager gravitate toward the reorg to fix all manner of institutional ills.

Organisation design is subject to the same pressures as technical design.
For example, engineering managers who overcomplicate their teams are like engineers who overcomplicate their code to boost their own career.
Take the same approach to broken organisations as to broken code: tackle problems incrementally, not in big reorgs.

When you want to change your organisation, and you're hiring, look for people who can cope with transitions.
"Has worked in an organisation like the one you want to be" does not mean they can help your organisation get there.

Conway's Law is often oversimplified.
Pay attention to how organisation design influences technical choices.
We don't have to be passive observers of the effect.

### Chapter 8: Breaking changes

Making changes will break things, so you need "air cover" and a sense of psychological safety for taking risk.
Look at what the organisation celebrates -- social capital is a bigger influence than monetary reward.
What do those pressures incentivise?

To preserve trust, a service that never fails isn't necessarily optimal.
Quoting page 168:

> Italian researchers Cristiano Castelfranchi and Rino Falcone have been
advancing a general model of trust in which trust degrades over time,
regardless of whether any action has been taken to violate that trust. People
take systems that are too reliable for granted. Under Castelfranchi and
Falcone’s model, maintaining trust doesn’t mean establishing a perfect
record; it means continuing to rack up observations of resilience. If a piece
of technology is so reliable it has been completely forgotten, it is not
creating those regular observations. Through no fault of the technology, the
user’s trust in it will slowly deteriorate.

Minimising breakages isn't the goal -- demonstrating resilience by recovering from outages is a more effective way to build trust.
The book calls this the *service recovery paradox*.

When trying to understand the impact of a technical project, I like the idea of Philippe Kruchten's 4+1 archiectural view:

* *Logical view* maps out how users experience a system
* *Process view* looks at what the system is doing, in what order
* *Development view* is how the software engineers see it
* *Physical view* is the hardware involved
* *Scenarios* (+1) are the use cases involved

Run failure drills, like restoring from backup or turning off an unknown service.
It's better to run these at a predetermined time with experienced engineers to hand, than wait for them to happen unexpectedly.

When communicating failure drills:

*   Don't provide too much notice, or people procrastinate and don't actually prepare
*   Follow through on the dates you set, so you don't become the boy who cried wolf

Embrace failure as part of the process.

### Chapter 9: How to finish

Software is never finished, but modernisation projects are.
You need a clear sense of "done" so everybody knows when to move on.
Sucess is not obvious!

Run post-mortems for success, because it's not as straightforward as we think.
We can learn from our successes as much as from our failures.

What's the difference between a war room and a committee?
A war room contains peers; a committee contains executives.
The goal of a war room is to shorten the lines of communication, not reinforce the existing hierarchy.

### Chapter 10: Future-proofing

The best way to avoid a legacy modernisation project is to avoid needing one.
Two types of problem affect working systems: usage changes and degradations.

Time is a frequent source of bugs, and programmers underestimate how long systems will be in use.
Problems can also occur long in advance of the due date, as page 199 explains:

> We have already seen systems fail thanks to the 2038 bug. Programs in financial institutions that must calculate out interest payments 20 or 30 years into the future act like early warning detection systems for these types of errors.

We cannot avoid deterioration or the need to migrate, and they're not signs of a broken system.
Build in graceful degradation and keep upgrades frequent to ensure they're a well-practiced process.

Automation can be helpful, but it can make it harder to resolve failures when they occur, because we've lost the knowledge of how to respond.

Consider human capacity.
Consider "wrong" systems if they're easier for a team to support.

I like the phrase used in the closing of this chapter, on page 215:

> I once had a senior executive tell me, “You’re right about the seriousness of this security vulnerability, Marianne, but we can’t stop the bus.” What he meant by this was that he didn’t want to devote resources to fixing it because he was worried it would slow down new development. He was right, but he was right only because the organization had been ignoring the problem in question for two or three years. Had they addressed it when it was discovered, they could have done so with minimum investment. Instead, the problem multiplied as engineers copied the bad code into other systems and built more things on top of it. They had a choice: slow down the bus or wait for the wheels to fall off the bus.
>
> Organizations choose to keep the bus moving as fast as possible because they can’t see all the feedback loops. Shipping new code gets attention, while technical debt accrues silently and without fanfare. It’s not the age of a system that causes it to fail, but the pressure of what  the organization has forgotten about it slowly building toward an explosion.

and the conclusion reminds us of this on page 219:

> A high-functioning organization cannot have all feedback loops open all the time. It must decide which loops have the biggest impact on operational excellence. Throughout this book, I have emphasized thinking about modernization projects not in terms of technical correctness but in terms of value add because it re-establishes the most important feedback loop: Is the technology serving the needs of its users?

[me-impact-first-product-teams]: /book-reviews/impact-first-product-teams/
[tailscale-grants-vs-acls]: https://tailscale.com/docs/reference/grants-vs-acls
