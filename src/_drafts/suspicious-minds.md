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

Again, something that we would have thought was quite odd a few years ago



{% slide suspicious-minds 19 %}

**This isn't an accident.**
Just because you don't trust politicians less doesn't mean that you now randomly trust strangers on the Internet.

The reason we trust these things is because people took explicit steps to make that happen -- whether that's the green padlock icon or ratings in Uber or Airbnb verification -- with all of these things, somebody did explicit work to make a system you could trust.

We can do the same.
Trust clearly isn't impossible.
There's still a lot of trust in these things, but also in the way society functions, and so we can actively build trust as well.



{% slide suspicious-minds 20 %}

So let's talk about that now.
How do you build trust?



{% slide suspicious-minds 21 %}

One exercise that is often used to build trust is this one.
Some of you might be familiar with it if you've been on a "team-building" day *[Ed. Again, finger quotes]*.

It's called [trust fall](https://en.wikipedia.org/wiki/Trust_fall).
One partner closes their eyes and falls backwards, and they know the other person is going to catch them, so they trust the other person.

(As long as you do catch them.
I did this for a small group at work on Monday, and one person said not only had they done this exercise, but their partner had dropped them.
Clearly a very effective exercise for them!)



{% slide suspicious-minds 22 %}

Trust is not built in one shot interactions.
It's also not built knowing exactly what's going to happen, and knowing that they'll catch you because if not they'll be in trouble for breaking the exercise.

---




 Trust is built
incrementally it's built over a series
of interactions small steps and remember
I said earlier that Trust is a risk
assessment when you do a risk assessment
you're looking at your past interactions
and we make a decision as to you know as
we interact with people we get a sense
of whether we can trust them and that
all fit into the risk assessment and
it's important to note as well we can
use that both those interactions are
both ways the individual person involved
so maybe and and groups as a whole so
for example I've been coming to pike on
UK for many years everybody I've met has
always been lovely charming and nice so
if I come out and meet some in you some
of you first-timers later I trust I'll
probably have the same experience I'm
John I'm judging the group I've had
interactions with the group and that
causes me to trust it now on the other
hand if I said I had a printer in the
other room and the printer just works
how many of you trust me
it doesn't so Trust is built
incrementally we have a series of
interactions and as we see trustworthy
behavior in a group in a person in a
system that's how we know that we will
be able to trust it in the future so
understand how we build it let's think
about how Trust works now some of you
might be familiar with the fire triangle
fuel heat and oxygen you need all three
to make a fire
well though please don't please don't
try that at home and if you take one of
those things away you put the fire out
and I think Trust is trust is very
similar there are three components that
you need and you need all three of them
for trust and those components are
honesty reliability and shared values so
let's break those down a little
start with honesty honestly for me
encompasses things like truthfulness do
you always say things that are true or
at least that you believe to be true
because if you lie to me how can I be
sure I won't believe you next time I
won't believe that you're telling me the
truth it's about sincerity believing
that we care about something that we
believe what we're saying and how many
of us have read a blog post from a
startup or from Google to Google Reader
team even saying we're delighted to say
that we've been acquired and therefore
the product you'll all love is going
away and we're really excited for that
as well to screw you all over
so sincerity is important as well and
finally transparency it's really
important to say bad things as well as
good things and that doesn't necessarily
mean being being mean but it does mean
giving on it you know what we would call
an honest opinion imagine for example
you've got a friend who always tells you
that you look lovely no matter what
you're wearing and then you're trying
out and trying on an outfit maybe
because you're about to go onstage for a
big presentation and you ask them how do
I look okay today and they say yeah you
look great yeah but you would say that
so it's important to be transparent
important say the bad things as well as
the good things so that's what honesty
is then we've got reliability so
reliability is about keeping your
promises if you promise you'll do
something you actually stick to that you
don't break a promise you don't promise
more than you can deliver
and it's about consistency and I think
perhaps this in this room we might
appreciate that no more than in for
example a test suite I'm sure many of us
have had to debug a flaky test a test
that sometimes passes and then it fails
but you've rerun the test and it passes
this time so it's all okay and that's
almost less useful than a test that's
just broken because then you don't know
if you could believe it when it passes
again next time and it's all similar to
a transparency thing you want it to be
consistent and finally shared values and
this is about things like having common
goals so you're a team that is all going
if you're a team you're all going in the
same direction you're all aiming for the
same thing you're not heading off in
different directions about having common
values and beliefs you all believe the
same thing and I think as well a common
understanding raise your hand if you
have been into a meeting where everybody
agreed what they were going to do and
everybody agreed a difference idea in
their head quite a few of us so it's
about that as well it's about us all
being on the same page so those are the
things you need for trust I believe
honesty reliability and shared values
and I think it's important to note that
you couldn't take one of these in
isolation take honesty for example I'm
sure you would all agree that honesty is
a very positive trait we would all like
to be considered honest people we would
all like to work with honest people but
just because somebody is honest doesn't
necessarily mean that you trust them
imagine somebody who is honest and
unreliable then we believe that they'll
tell the truth but we might not believe
them to keep their commitments and the
classic example of this is if you had a
surgeon who was honest it was honest but
incompetent
would you trust him to do a major
operation on you and I really hope for
your sake that the answer is no so
that's what we need those are the
ingredients of trust our honesty
reliability and shared values and if you
haven't or if you encourage those things
if you promote those things then you
have an environment where trust and
start to build but how do you actually
do that because it's all very once say
hey I want to be more trustworthy person
so I'm just going to try harder and
that's a recipe to get very little done
we see this I think when we're building
software if I want to write less buggy
software it's not just a case of I'm
going to try harder and magically write
better software I'm gonna make a small
game and that's not nothing but if I
want a step change we look to external
processes things like tests and code
review and documentation when we want to
write better software we put in place
new tools new processes that will change
the way we work that enable us to in to
write better software and Trust is
exactly the same so let's think about
some ways we can do that first although
something we can do with trust all
myself is being a role model being
something other people can follow humans
are naturally mimics okay we will
imitate the behavior of the people
around us we see this all the time
an example this is if you're a company
that is functioning right where one
person fudges the financial numbers not
that we could all imagine a company like
that and obviously I won't stress that
this company's entirely hypothetical and
fictional somebody fudges the financial
times and then management don't do
anything about it then just say oh yeah
that's fine we'll send that out the door
then other people learn oh that's that
you know other people start to copy them
and eventually it becomes the company
culture that hey it's fine to cook the
books it's trying to break the financial
numbers to the point you do that we copy
each other so for being a role model by
amulet by showing the behaviors that you
want to promote in the world by being
honest by being reliable by being having
those shared values and seeking there's
an that is a way to build trust another
thing you can do that I think is really
important at high level is having
monitoring have check-ins now Trust is
not a metric we can't get a KPI or put
it on a dashboard but it is a thing we
sort of have some spidey sense of when I
asked you earlier to think of somebody
you didn't trust and then somebody you
did trust I think pretty much everyone
got it almost immediately because we do
have a sense of how much we trust
somebody and is that trust declining or
is increasing and we can actually you
can ask somebody right do you trust me
and that seems it could seem awkward at
first right same suddenly hey do you
trust me do I trust and ask me ask me
yourself do you trust them but I've
started doing this a lot in my personal
relationships that in the last and thus
your so actually know if I'm
if I might with a friend and we've been
seeing each other for a while hey are we
good is everything okay am I being
overbearing is it too much that sort of
thing actually being aware of it
actively tracking it can be weights not
seeing are you doing what you need and
if not do you need to change but without
having the monitoring without having
those track ins it's hard to know that
you need to be making a change so
what'll that change look like it's not
with some examples of honesty so I
talked about Airbnb earlier but people
in your hosts invite strangers into
their home and one of the things you
probably say to them on the forum is you
were given a tick boxes I am NOT an
ax-murderer
I do not steal other people's things and
that's fine but anybody can check box on
the internet so one of the things they
do to do identity verification of this
stuff to do verification of your honesty
is they ask you for some ID you upload
your government ID they run that against
various databases say are you wanted by
the FBI Interpol are you a known
terrorist because if not maybe people
don't want you in their home so if I
actually did that's an example assistant
actively verifies honesty that doesn't
just trust the P doesn't just trust on
blind faith that people are going to do
do what they say they will another thing
you can think about is incentivizing
transparency I'm sure a lot of us have
managers who tell us that they would
love us to be transparent and tell them
when they're doing something wrong and
tell them about their mistakes and
that's a really nice thing to hear but
often it's difficult to put that into
practice because if you want to make a
complaint about it maybe someone at work
and that person is the person who also
controls your salary and benefits and
job prosper and career prospects maybe
you're going to feel uncomfortable
telling them hey actually you did this
thing that's screwed up because you're
worried about the retribution for you so
it's already was saying we want
transparency we have to actually do
think about how we're going to do it and
one way to do is change the carrot and
stick so this is an example I said
earlier that I break things this is an
example of the API at work just before I
left for the conference I heard I'd done
a production deploy about ten minutes
before getting on a train which is
always the best time to do production
deploy
and you'll see it's this is not supposed
to have here I'd made it but I'd made a
bug in what I deployed and what I could
have done would be to run out the door
and Satan I don't know I don't know I
didn't touch it it must have just broken
and I think pretty quickly somebody
would have figured out they'd have
looked at the logs and said Alex as a
production deployed from here and then
30 seconds later it went down we think
those things are connected my coworkers
are smart but instead and I could have
done that and instead and I we've had
done that I would have got in trouble
but instead I fest up I said I sort of
broke this thing accidentally let's roll
it back and then that was the
opportunity for us to have an a
discussion about well why did this
happen why did it break had we how do we
stop Alex furring up next time because
let's be honest it's mostly me
and that was a benefit to me right and
it was a benefit for both the team to
make how their Enco morosely and its
benefits for me because I feel like my
co-workers trust me and that I know I'm
not going to make the same mistake again
so there's a benefit to me being
transparent and there's a penalty for me
not being transparent which is often the
wages of the inverse of what the what
the default system would be right if we
weren't thinking about it I'd say I've
broken the API and said Alex then and
they'd say Alex you idiot fix it again
so by changing the incentives of
transparency if I'm making but you need
to think about that if you want to
promote transparency so there's some
examples of honesty let's talk next
about reliability so going going back to
one of the examples from earlier you
perhaps wouldn't trust riding in a
stranger's car but if you had lots of
people who told you know this person is
really good at letting strangers ride in
that car you might be more inclined to
do so and that's what system rating
systems do and we're almost drowning the
rating systems these days so this is an
example this is screenshot from uber I
came over this morning but also Amazon
TripAdvisor Yelp Google Maps there are
lots of ways that we crowdsource ratings
and that says that's some measure of
reliability we can decide well other
people trusted this person that was okay
before we decide to commit
but how do we actually if we are the
person who's being righted how do we
drive up that reliability how do we
write you two down so this is great if
you're already reliable how do you get
there and I think actually this is
something we as software developers are
pretty good at because we are used to
working with unreliable systems they're
called computers and we've built you
know all these different ways to to
improve the reliability of our software
to improve the reliability of the
computers we build things like testing
and code review and documentation
you all right documentation right and
other such things we've got a huge
number systems for improving the quality
of the code we write something you will
notice about these though is that none
of these come from me in from me these
are all external systems right there's a
Travis server that runs and checks micro
Biff checks moto passes test before I
check your den we require pull request
through the github user interface the
Scarlett compiler will not let me write
something doesn't fit the type system
which is why python is inherently a
better language but don't tell them I
said that we have all these external
tools we have all these external systems
that help that help us improve our
reliability and we can do the same for
the promises we make outside the outside
the text editor so on a personal level
that might be something as simple as
keeping a diary or keeping a task list
so you can see what promises you'll make
you're making so you don't forget
something or you don't over promise and
under deliver you don't promise you can
do something and not realize that you've
already promised to do three things this
week another thing I think we can look
to if we're looking at a larger group is
things like agile and I noticed some
people that's a bit of a dirty word and
you'd but you don't necessarily need to
go all in on our channel to get some of
the benefits Robert things like stand-up
meetings retrospect here's planning
meetings just so you all know what
you're doing and you all know if you've
promised to do you know a few promises
who promised to do something for
somebody else if something is slipping
if a promise isn't going to be delivered
again being really explicit about the
tracking keeping and keeping on top of
meetings like that I think there's a lot
of value in some of some of the
practices from agile in maintaining
reliability in teams
and finally let's think about some
shared values because I think shared
values we most often notice when they
diverge because shared values are often
implicit we trust that we trust that
people we believe that the people around
us are inherently reasonable people they
hold the same world rounded correct
views as we do and then one day we
discover that actually one of the people
we work for really isn't as nice as that
maybe they hold it maybe they hold view
we object to maybe they didn't
understand something maybe they had
different different belief and so the
way to get this out is to stop being
implicit about eyeshadows can actually
be explicit about them one of my
favorite lines from the zone of Python
which is a statement of explicit shared
values for Python programmers explicit
is better than implicit if we talk about
our values and we talk about the things
we care about that can be really
valuable and that's how you close those
disagreements I asked earlier if any of
you had been in meetings where everyone
agreed to do something and they had
different agreements and one what we
often do that is have meeting minutes
have a list of agreed actions that is
sent out to everyone that they can then
look at and say hey I didn't agree to do
that or this is different from my
recollection but then it gets it out at
the open rather than coming back to the
next meeting and realize you all thought
something different and one example of a
statement of shared values that we've
already talked about once this morning
is the code of conduct this is a really
explicit statement of shared of our
values as organizers and beliefs about
this event and what happens is if you're
somebody who's thinking coming to the
conference you can read this and you can
see what our values are and if you
thinks this sounds like a friendly
conference as all of you find people
clearly do then you might come to this
conference and I think this is a going
to be a good place for me to come to and
if you read this and it doesn't align
with your worldview it doesn't feel like
an event where you'd be safe you might
not you don't think you'd trust yourself
to be okay there you don't come but by
making that explicit and getting it out
of the way early we save ourselves the
houseless time to deal with somebody who
turns up who wasn't expecting it and
just to give the slightly more explicit
example this is a snippet from it PyCon
UK will not tolerate harassment if you
are somebody who shares our value of not
being harassed at calm
you can read this and know this is an
environment where we don't want that to
happen either and so hoping that gives
you some crust in us that well that
happened we would take steps enforce it
and indeed if you go and read the code
of conduct it does line steps of how we
would enforce these fair values so it's
not just lip service we are you know we
actually follow through on them so those
are some examples of how you might build
external systems external tools new
processes to build trust and I'm sure
you can all think of other ways you
might do that in your own life in your
own work in your own systems so that's
all great
it's what happened was ero we've built
some trust and how do you rebuild trust
so what about when it all goes wrong but
if you build that system honesty
reliability shared values that's all
great but it's often very fragile and
it's easy to make a mistake it all goes
wrong and suddenly you've got that loss
of trust and I'm sure we can all imagine
a time where we thought we trusted
somebody and then it turns out we didn't
and that's not that's a that's a real
gut punch because while Trust is built
in small moments it's built
incrementally Overseers interactions
it's really easy to do one thing make
one mistake and Trust evaporates
instantly anybody think of an instant
like that I think quite a few nodding
heads so when Trust is destroyed it goes
very quickly it is important to note
though a lot of people see this and then
they will add a third line and so they
will say it's gone forever that once
somebody betrays you
they've misplace your you discover your
trust in this place you never trust
somebody again and I don't necessarily
think that's true taken as an example VW
I'm sure many of you in this room may be
familiar with the VW emission scandal
about two years ago they were caught
they were caught falsifying their
emissions tests
so that they would have peered past the
EU regulations and then when they sent
their cars out on the road they would
just be spewing filthy humans and
destroying the planet and this came out
there was big fine I think several of
their engineers went to prison but it
was a huge loss of trust in VW why it
was a loss of honesty because they were
lying about what they would do
and it was a lost of the share of the
shared value of obeying the law and
looking after the planet but it's not
like VW have now vanished off the face
of the earth people still buy Volkswagen
cars they still own them they are still
allowed to operate as a business because
there was a huge amount of trust
inherent in the brand even before they
did this this bad thing so when you lose
crust it is still possible to to come
back to have some in reserve if you're
careful about it because again when you
have a loss of trust I said earlier the
builds trust you can't just try harder
in the same way if you want to rebuild
trust or fix a mistake
you can't just try hard to be more
trustworthy in future it's important to
look to actually taking explicit steps
for that so the way to do that first of
all is find the cause what what went
wrong the first step of making any
apology is knowing what you're
apologizing for second is to articulate
the issue I've given you a framework
today to identify how Trust works again
honesty reliability share values so what
was it a failure of was it a failure of
honesty was it a failure of shared
values was it an unreliable system maybe
it was all three but only when you know
which bit component failed do you know
what you've got to go and fix and
finally come up with explicit actionable
steps to resolve it don't just say I
told you no we were caught faking all
these emission scans tests but we'll
just you know try harder next time and
hopefully people will believe us they
actually put in place a stranger program
of Oak Hill we're going to do extra
tests we're going to focus more on clean
energy we're going to cancel our cars
that aren't the most emissions polluting
that sort of thing come up with explicit
steps for resolving a problem don't just
trust it's gonna work out and one
industry that does this really well I
think is the aviation industry because
flying inherently feels a bit weird we
all know how gravity works we all know
that things go down and that's not going
down flying should be this inherently
untrustworthy thing and
it's one of the safest means of
transport in fact I think it was last
year or the year before there were no
deaths in commercial aviation you could
have flown on occur on any commercial
plane that year and you would have not
and you would be at no risk of dying it
was
it's an incredibly safe industry so how
did they get there because it's not like
planes don't occasionally break but the
reason the aviation industry I think is
so trusted and so reliable is because
they take a really strong view when
there are accidents or even near
accidents and they work through to find
out where was the failure of reliability
where was the failure of trust and how
do we rebuild that and one thing I think
they do that's really nice is called the
Swiss cheese model of accident causation
some of you may be familiar with this so
if you imagine every layer of tree is an
overlapping component in your complex
system you know maybe it's an aircraft
component and where there's a hole in
the cheese that's what a problem can
occur and when they learn up in just the
right way and there's a hole all the way
through something drops through that's
when a problem occurs and what they will
do is they will try to analyze every
layer of the system every component that
could have failed find all the bugs and
fix them all at once
don't just fits to fix the last one
don't fix the surface problem fix it fix
the reason fix all the problems in the
system and to give one example of that
um this is Tenerife Airport which in
1977 was the site of the deadliest
aviation crash in history I'm sorry I
just said Aviation is really safe and
none telling about a crash but this was
years before many of you were born so
it's obviously fine what some of you so
in 1977 there were two planes one of
them was taking off one of them was look
trying to land they hit each other had
side on and that was it that was a very
horrible crack that was very nasty crash
and the reason for it was that the pilot
who was taking off thought he'd been
given clearance to take off it turns out
the tower thought he hadn't so this was
a failure of reliability on the pilot
spot the pilot promising not to cause
air accidents but also failure a shared
communication of shared values and
shared understanding the pilot and the
tower both thought they knew what go for
take off main and it turns out they both
understood completely different things
now would have been easy for the
industry at this point to say ah what a
silly pilot they made a mistake now lots
of people are dead we would fire them
for making that mistake but actually
they were killed in the accident so I
guess we're good now not only would that
be an incredibly insensitive thing to
say it would also not have I solved the
underlying problem which is that there
were discrepancies in radio
communication and so now as a whole the
aviation industry uses really standard
phraseology really standard terminology
so they know exactly what it means when
somebody says cleared for takeoff
there's no room for ambiguity and that's
something and you know that's something
I think perhaps you know often we would
benefit from one other thing the
aviation is redundant I think we should
steal for the software industry is
checklists so when planes first set off
you had to be really clever you had a
really good memory and remember you've
done all the things to make your plane
fly have I attached the propeller have I
put in petrol and I taken off the
parking brake because if you forget any
of those things you will not go very far
and eventually but as planes became more
and more complex systems it became
harder and harder to remember all those
things so they created an external
system a checklist and now you look at
the checklist to tell you everything you
need to do to fly plane taking off
checklist landing checklist seatbelt
sign checklist
engine failure checklist and they're
constantly adding new checklists for new
scenarios but it gives them a really
reliable external system for dealing
with this complex really reliable
external tool for dealing with this
complex system I want to notice well
that and I think they'll be really
useful tool for us to have I want to
notice well a lot of syndrome would like
to think that were really intelligent
and we are and that we wouldn't forget
anything which we would and therefore we
don't need checklists and this is a
common fallacy it's better people I'll
just remember a thing and another
industry that is started looking at
checklists is doctors health care and
doctors are also really really clever
people you wouldn't expect me to forget
things
and yet every time checklist are
introduced there is a meaningful and
noticeable drop in the rate of accidents
and faults in surgery and that's
probably a good thing
so checklist a great you should consider
using some so Swiss cheese model
accident causation again identifying all
the for all the layers in a fault all
the reasons why a system went wrong and
again that's my check that's my steps
for fixing a loss of trust identify what
the issue was articulate how it was a
failure of trust use the framework use
the trust triangle and come up with
explicit actionable steps to resolve it
to rebuild trust because the funny thing
is actually when we lose trust if we
rebuild it correctly we can often end up
with more trust than we started with
it's a well-studied phenomenon for
example if you go into a shop you buy a
piece of clothing the closer you get
home the clothes have got a hole in it
the shop has failed in its promise to in
its promise of consistency and its
reliability but then you go back and
they replace it free of charge so you're
a problem they resolve it you are more
likely to shop there again even compared
to somebody who didn't have a problem in
the first place because remember again
Trust is built as small interactions
they all build up incrementally and
that's what gives us the basis to trust
somebody and sometimes when a mistake
happens and you fix it and you fix it
well those are other interactions that
feed into somebody's impression of you
that feed into that layer of trust so a
mistake doesn't have to be the end of
the world as long as you don't let it be
so let's wrap up what I've shown you
today we've talked about trust I've
shown you my framework for thinking
about trust and how Trust is built
honesty reliability and shared values
have all three of those things encourage
all three of those things you have a
system where trust can merge if you lose
one of those things your problem and
I've shown you some examples of how you
can build external tools external pretty
new processes new systems to encourage
those things not just to try harder to
be more honest but actually come up with
systems of verifying and validating that
but if I want to take you to take one
thing away from the rest of it from
today the final thing I would leave you
with is this
is something you can actively build it
is not just a passive thing happens it
does just have to be something that
occurs to you that you have no control
over you can take actions to affect them
that trust you have in yourself that
other people have in you and that you
have in other people and I've shown you
my framework for dealing with using that
you might find another system that works
better for you but the important thing
is Trust is not just something that
happens to you it is something you can
do and on that note I think I'll finish
thank you all very much

[Music]
[Applause]
so just briefly because Daniele asked my
won't take questions now but I am around
all week and if I'm don't look too busy
I will be happy to answer questions
