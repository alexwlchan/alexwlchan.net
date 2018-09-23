---
layout: post
title: Assume worst intent (designing against the abusive ex)
tags: pyconuk slides
summary: TBC
theme:
  card_type: summary_large_image
  image: /images/2018/worst-intent.png
---

The talk was recorded, and thanks to the magic of Tim&nbsp;Williams, you can watch it on YouTube:

{% youtube https://www.youtube.com/watch?v=XyGVRlRyT-E %}

You can read the slides and transcript on this page, or download the slides [as a PDF](/talks/assume_worst_intent.pdf).
The transcript is based on the captions on the YouTube video, with some light tweaking and editorial notes where required.

<!-- summary -->

---

{% slide assume_worst_intent 1 %}

again since you've already heard from me
before I'll skip the introduction and
gets right into the talk we're talking
this morning about online harassment and
specifically how do we build systems to
prevent it the reduce it that reduce the
risk of it I'm gonna show you some
mechanisms and practical tips some ways
that I found that are most successful in
reducing online harassment

{% slide assume_worst_intent 2 %}

but before we
start some content warnings this is a
talk about online harassment so I'm
going to talk about online harassment
I'm also gonna talk about abuse there
are mentions of things like racism
misogyny sexism suicide rape and death
threats and there are very brief
mentions of some of the other horrible
things that people do to each other on
the internet I'm a word that these are
uncomfortable subjects for some people
people in this room may have experience
and may have traumatic experiences with
these things and so while it is usually
considered poor as it get to leave a
talk midway through if anybody does feel
uncomfortable and wants to step out for
a few minutes I will absolutely not be
offended

{% slide assume_worst_intent 3 %}

so let's start off with an
example this is an app called square
cache it's a nice little mobile payments
platform it's designed to be fast easy
much more convenient than using a
banking system than using the online
banking system and you'll see what they
have is a chat feature so you can tell
somebody why you would like why you
would like money from them what are they
paying for it allows to give some
context to their transactions rather
than the 13 or so uppercase count you
get if you do it through your online
bank

{% slide assume_worst_intent 4 %}

so this all seems fine this seems
like a really useful feature this is a
thing we would like to exist in the
world except they didn't realize that
having a messaging platform opens
effective harassment and we can see here
somebody's abusive acts used that
messaging platform to send them abusive
messages for months and Square cash
never thought maybe people we should
allow people to block each other because
why would you want to block somebody
sending you money I like receiving money
you will like receiving money money
money money and to their credit when
this was posted and when this tweet went
viral they very quickly closed a
loophole but this doesn't change the
fact that four months somebody had to
put up with harassment that wasn't that
was available through their platform

{% slide assume_worst_intent 5 %}

and
this is one of the big problems with
thinking about user safety we're
thinking about harass
is that if we let it be an afterthought
it becomes expensive it's harder to
retrofit later and it often means that
our users have to learn the hard way all
of the rough edges of our platform

{% slide assume_worst_intent 6 %}

and
this is a shame because I fundamentally
believe that most developers mean well
the squash developers wants to make a
better way to send money to each other
they didn't want to build a tool for
harassment and I assume most people at
PyCon UK are pretty nice I'm assuming
you're all the same way

{% slide assume_worst_intent 7 %}

so how do we do
this how do we think about this because
it's a possibility truth is if you allow
user to user interactions you have the
possibility of harassment on your
platform ever since ever since we've had
the means of communication whether it's
talking writing sending images to each
other people have been using it to send
nasty messages to other people most
people are fundamentally nice but there
are some bad people out there and we do
have to think about them

{% slide assume_worst_intent 8 %}

so what is
unlike harassment looked like these are
some examples there's a lot of it you'll
see things like sending nasty messages
and this goes all the way from spam and
phishing through to rake threats and
death threats posting of personal
information identity theft revenge porn
and many many more things that I'm sure
you can think of that didn't fit on this
slide and now on the one hand personal
harassment isn't a new thing right it
didn't suddenly spring up in the 1980s
when we invented the internet people
being harassed long before that what
online harassment changes I think is the
scale and the scope of it because the
Internet allows me to talk to people
much further away halfway around the
world and that's a fantastic thing but
it means that I can be harassed by
somebody from a Ralph's way around the
world somebody who I've never met in
person Y might never meet in person can
still send them horrible messages
through the internet and of course the
expansion of technology the rapid
expansion of technology has enabled new
vectors of for harassment
take for example sharing intimate photos
without permission sometimes called
revenge porn so here two people and a
consensual loving relationship take
intimate photographs of each other and
share them with each other and this is
if this is a no fine thing to do between
consenting adults thirty years ago you
wouldn't have been able to do that
because
making a photograph was relatively
expensive you probably needed a large
camera you would need to go to a kept to
a specialist to a store to get the film
developed and sending photographs
required putting a stamp on an envelope
today we all have cameras in our pockets
in fact I think I have at least three
cameras standing at this podium and in
the room we probably have at least two
or 300 cameras it's much much easier to
take these photographs and it's much
much easier to share them that's
something that didn't exist that
couldn't have existed 30 years ago and
now is commonplace and as technology
continues to expand new VEX harassment
crop up so really going to any more
detail that's because I'm assuming most
of you are familiar with it

{% slide assume_worst_intent 9 %}

but one
thing I do want to stress is that this
is a thing that has an impact on people
when I was younger a lot of people used
to say about you know online bullying
and so on it's just words on the
Internet
it doesn't really matter it doesn't
affect people anybody heard that I'm
seeing yeah a few hands in the audience
and I think when I was younger a few of
us used to believe that and then one day
we came into school and we were told
that one of our friends wasn't coming
back
she'd been bullied on Facebook I was 16
she'd been bullied on Facebook and she
jumped off a bridge people stopped
saying that words on the internet didn't
matter after that but I think it was a
bit late for her so what a stress very
importantly what people say on the
Internet what have said through online
platforms that has an effect on people
it is a nasty thing it is not just words
on the Internet's not just words on a
screen

{% slide assume_worst_intent 10 %}

and I think if you're building a
platform where people interact where you
have user to user interaction it is to a
certain degree your responsibility to
think about what people are doing on
there and to think about the effects
that might have beyond your platform

{% slide assume_worst_intent 11 %}

This is all pretty nasty stuff -- who's doing it?



{% slide assume_worst_intent 12 %}

We have this popular image of a "hacker" -- a malicious person on the Internet.
This person ticks all the hacker stereotypes -- they're wearing a hoodie, they're in a darkened basement, they have green text projected on their face.

This is the sort of person we need to worry about when we're thinking about somebody stealing passwords from our database, or gaining root access to
our servers, or doing malicious things against us as a service.

But I'm talking about with harassment is much more targeted -- it's directed against a particular person.
The sort of people who do online harassment are the same as the people who do personal harassment in the physical world.



{% slide assume_worst_intent 13 %}

So let's think about who those people might be.

*   It could be an **abusive partner or an ex**.

*   It could be **family members**.

*   It could be **classmates**.
    Kids often don't have the best social skills, and will say pretty mean things.

*   **Co-workers and ex co-workers**.

*   **Friends and ex friends**.

*   **That one-date weirdo**.
    Another thing that the Internet has opened up for us -- today there are many online dating sites, and in many ways this is a wonderful thing.
    But now before you ever meet somebody, they can download your entire Facebook profile, your Twitter feed, your Instagram photos.
    They know a huge amount about you -- and if you decide that the data didn't go so well, and they disagree, they now have many more wins of finding and tracking you later.

*   **Rogue sysadmins**.
    Do you know what your sysadmins are doing with your customer data?

*   **Oppressive regimes**.
    Something we're lucky enough not to have to deal with in this country (mostly), but if you're building a global service, you may have users in environments like that.
    And there are people who'd like to come after your users, who'd like to come after their data.
    You need to be thinking about that when you build your service too.

What you'll notice about these is that none of these people are anonymous hackers who live in a basement in Russia and wear hoodies and drink bad coffee (Russia aren't lucky enough to have Brodies).



{% slide assume_worst_intent 14 %}

The pattern  we see with online harassment is the same as the pattern we see with personal harassment: **people are more likely to be hurt by people they know**.

This is very scary because a lot of the people we know are inherently more dangerous individuals, compared to anonymous faces on the Internet.

People like our family members or our friends.
They have physical access to us.
They probably know our intimate secrets
They probably know the answer to your security questions.

Just out of curiosity, put your hands up in the room if you know somebody else's phone passcode.
*[Ed. A bunch of hands went up.]*
Maybe that's two-thirds of the room?
And you're all nice people, right?
Right?
(I'm not seeing the entire audience nodding, which is a little bit concerning.)
Imagine if you were a nasty person.
If you wanted to go through somebody else's messages, go through their Facebook feed, go through their private texts -- you could do that!
You have access to do that.

Physical access makes these people quite scary, and nullifies a lot of the ways we might otherwise protect ourselves.
All the security in the world doesn't help if you have physical access to a person and their device.

And physical access can go beyond just our digital tools -- it can also come down to simple acts of physical harm.
Somebody who lives 600 miles away is going to struggle to physically hurt me, but somebody who lives in the same house as me will have very little trouble doing that.



{% slide assume_worst_intent 15 %}

This is all very upsetting.

There are horrible people in the world, they do horrible things, they might be living in the same house as you.
Maybe we should all go and hide under a tin foil blanket and never leave our room.

This would not be particularly productive.



{% slide assume_worst_intent 17 %}

the good news is that it
doesn't have to be this way there are
tools and techniques we can use to build
services to reduce the risk of
harassment we can never stop all the
nasty people in the world but we can do
better there are ways that we are always
kept platforms that are not just open to
facilitate all forms of abuse we can do
better than to
komm

{% slide assume_worst_intent 18 %}

so how can we protect our users and
restrict walkthroughs and best practice
for the rest of presentation

{% slide assume_worst_intent 19 %}

the first
thing I want to stress is that a lot of
users who aren't risk of harassment are
essentially normal users they want to
use your service for the same reason as
everyone else and that might be fun it
might be work it might be because
they're doing creative projects all
sorts of reasons same reasons it has
anybody else with you something now they
might also be using it for reasons of
looking for an escape looking to improve
their morale looking for support but a
lot of the reasons we'll along with the
rest of your users as this means that
making your service better for better
for vulnerable users users who are at
high risk of harassment can make it
better for everyone as an example of
this sorry did I hear something in the
audience right sorry I misheard
something there so um go back to this
take email spam we all probably get a
small most of us I imagines from get a
small number of emails we get a trickle
of spam if we were to turn off all a
spam filtering and just take all of the
messages that come to our inbox it would
not be overwhelming for us we could cope
with it it would be annoying but we
could deal with it
but a lot of spam filtering technology
was designed originally for people who
were just overwhelmed in spam drowning
in it thousands of messages a day they
couldn't keep up those services have
will for them but then we people who
don't really need that but would still
benefit from it we get the side benefits
of that and then same way there are lots
of ways people will use these time use
these techniques to make it better for
everyone

{% slide assume_worst_intent 20 %}

so what's the first thing you
can do first of all diversify the team
now I talked about this a lot last year
there's a video go watch it but I won't
talk about into much detail again here
the important thing to note is that we
are all individuals we all have a single
light lived experience and there are
people who are different from us who
have to worry about different things who
have to worry about different forms of
harassment
for example I'm male I do not generally
have to worry about being harassed at a
tech conference I don't have to worry
about being harassed on the bus I don't
have to worry about what might happen if
I'm sitting on the train and
slightly skeevy older dude sits down
next to me they have some basic
understanding of those things but they
don't really permeate my sphere of
consciousness in the same way they might
if I was a woman so if I'm designing
service I want to have a woman on the
team who has that lived experience and
who would instantly spawn this is
something you're doing that might be
able that might make them might make
something might be dangerous to somebody

{% slide assume_worst_intent 22 %}

let's look at an example which I imagine
many of you may have you may have used
before many who might be familiar with
git now git is a fantastic version
control tool hands up in the rooms if
you use git keep your hands up if you
have used git today but still quite a
few hands fantastic tool isn't it it was
the original blockchain sorry I meant I
said it but I said I was trying to say
nice things about it and one of the
fantastic features of git is that the
history is immutable
right so we do one-eye commits and then
that history is immutable nobody can
ever change it without fundamentally
broken it upon story and it being very
obvious this is a good thing that's a
feature yes see nothing good one of the
things get bakes into that chemistry
that is immutable that you can never
change is your name your name is
irrevocably part of the commit history
it is available forever and is publicly
browsable in the history of a git
repository can we ever think of
scenarios where somebody would change
their name if you've not read the blog
post assumptions programs make about
names really is recommended and this is
a big one there are lots of reasons
somebody might change their name they
might get married which you may notice
is something that it predominantly
happens to one gender over another
they might get divorced and they might
want to might want to get away from the
fact that they were once me that they
were once in a difficult marriage they
might be trans and want to get away from
their dead name there are lots of
reasons why somebody might want to
change their name and not have it fun
and he baked into the history of a
repository not had it permanently
available when get was originally put
together in the early 2000s I don't
think the Linux kernel team was
particularly diverse
I don't think they had many trans people
on the team because I think if they did
somebody might have looked at this and
said hey is this a problem there's a lot
of fun we're having a diverse team who
can look at something like this and tell
you about it before you ship it to
millions of users and only spot it 15
years later when it's a bit late

{% slide assume_worst_intent 20 %}

so
think about diversifying the team

{% slide assume_worst_intent 24 %}

what
we're talking about names let's talk
about name policies

{% slide assume_worst_intent 25 %}

because there is a
commonly held belief that if we ask
everyone on the Internet to use their
real name they will that will magically
make them behave because when we have
anonymous discussion that calls all the
problems right people can write anything
without impunity and they people can
write anything within people with it
with impunity and not worry about the
reputational cost and this is wrong in
both directions

{% slide assume_worst_intent 26 %}

first of all it's
perfectly possible to have very friendly
anonymous discussion this is just one
example of the thread and people are
having a very civil discussion about
making tea and coffee perfectly
reasonable six thousand comments and
they are all civil polite and
well-mannered so how did this happen is
this just an internet jam that was
hidden away protected from the world
hidden from the Sun like that I've now
expose operating that you are on a big
screen no it's because they had a really
strong and active set of moderators
people who were looking at the content
stamping down on bad behavior stamping
down on people making abusive comments

{% slide assume_worst_intent 27 %}

you can do anonymous discussion it's
just expensive for many people it's too
expensive but don't buy into the lie the
minimize the civil anonymous discussion
is possible the other side of this
though is the idea that people care
about the reputation associated with
their real name and I don't think that's
true
I think we can all think of people on a
certain website whose name might sound a
bit like a bird who write all four awful
things some of whom may be presidents of
major countries
and somehow get away with this impunity
and feel no blowback for the fact that
they are utterly utterly awful
reprehensible human beings I should make
a note that this is my personal opinion
and not the opinion of Pike on UK or my
employer there's also the problem though
that defining a real name is actually
really hard another assumption
programmers make about names because
some people have multiple names so I
have a Chinese name in my British name
that you will know me by some people

some people then have passports I don't
have an they don't have an official name
attached to it there's no name you can
prove what about organizations
corporations what exactly you calling
your real name this is a really hard
thing to define and probably not a
problem you are actually interested in
solving whatever platform you're trying
to build this is probably not in the
other thing to consider is that
connecting wallet names two identities
itself can actually be a source of
harassment we are all here because we
are in the tech industry and generally
speaking we associate our wallet name
with the name we go by online in
professional circles at these
conferences and that's because there's a
lot of benefit for us to us doing so
we're here to get job jobs potentially
do speaking opportunities it's really
useful to have your wallet name attached
to it but we can imagine communities and
discussion spaces where that might not
be the case maybe you've got a support
group for young trans people who aren't
sure about their identity are bad their
identity and are trying to talk to other
people and connect with like minds maybe
you've got a group for young LGBT folks
or people who are in abusive homes maybe
you've got a community about sex and
kink which again all perfectly
reasonable things to have on the
internet but if you start connecting
those people back to their wallet names
the names they might be known under a
law known under in the physical world
and in turn allowing people in the
physical world to connect back to them
their online identity running itself
potentially opens to the altar
harassment so the way I prefer is to go
for pseudonyms which are a good middle
ground used by a number of services

{% slide assume_worst_intent 24 %}

just
think carefully about your name policies

{% slide assume_worst_intent 29 %}

third thing moving on robust privacy
controls

{% slide assume_worst_intent 30 %}

so as a minimum you should have a quite
a ban and block malicious users both at
a platform and an individual level I
consider this table stakes for most
services we look we saw certainly a
Square crash didn't didn't do it I'm
still amazed that slack doesn't do it
and forces all that onto H H overworked
HR teams and you of course would have a
way to kick abusive users off your
platform even if you really want to be a
bastion of free speech which you
probably don't there will at some point
come somebody writing something you
probably don't want on your platform so
think about that

{% slide assume_worst_intent 31 %}

This is one of the things that Twitter actually gets right.
They have a blocking feature.
This is what it looks like if I've blocked you.



{% slide assume_worst_intent 32 %}

What you'll notice though is that *they tell you*.

It says "You are blocked from following alexwlchan and viewing alexwlchan's tweets".
Imagine you went to my Twitter profile after this talk and that's what you saw. Would that make you feel happy?
Respected?
Like you were somebody that I liked?

No.
You'd probably feel quite annoyed.
Quite upset at me.
You might decide to take that out on me, right?



{% slide assume_worst_intent 33 %}

Imagine that we were living in the same house, and you discover that I'd blocked you.
That might be its own trigger for retaliation -- so another thing you can look at things like **shadow blocking** and muting.
Allow people to block somebody without it being visible to the other person that they're blocked.
You can avoid that trigger for retaliation.

Offer granular access controls.
The default is public/private, but you can go much more you can go more granular than that.
Twitter's model is to allow posting things only to pre-approved followers, or maybe mutuals only, or down to the level of individual users.

*[Ed. Mutuals only is a feature being offered [by Pillowfort](https://twitter.com/pillowfort_io/status/1025070021993799681). I haven't tried it yet, but I like the idea.]*



{% slide assume_worst_intent 34 %}

so you look at sites like Facebook
LiveJournal dream with they offer really
granular permissions for who can see
every post and you can decide that on a
per post per person basis and this is
one of those things actually people use
for really interesting and creative
purposes aside from just not letting um
people they don't like to see their
content this is why those features that
people
that people have used in interesting
ways and this time an example of
Facebook getting it right they have some
pretty granular privacy settings they
have some pretty granular controls and
not just of what I'm writing I can
choose who can see them send me friend
requests you can see my friends lists I
changed that setting after taking this
screenshot and you should all go and
check it yourselves
who can see my future posts you also go
back and review your past posts that's
really important as well
don't make it immutable if somebody
posts something and then realizes maybe
I don't want that for a wide audience
allow them to go back in might change it
later and again

{% slide assume_worst_intent 35 %}

If you make it easier to change posting visibility, people are more comfortable.
They don't have to publish something to the entire world -- and that makes them more comfortable, and more likely to use your service.

{% slide assume_worst_intent 29 %}

{% slide assume_worst_intent 37 %}

Moving along, number 4: don't rely on technology to solve human problems.
If humans are being mean to each other, you need human moderation.



{% slide assume_worst_intent 38 %}

Because you don't have context -- you don't know everything that happens on (or off) your service.



{% slide assume_worst_intent 39 %}

Here's an example of a text I got this morning.
Someone sent me a picture of a flower -- they're thinking of me.

If it's a friend from home, and they now I've got this big talk today, that's really nice.
If it's the stalker who rang my hotel room six times last night, and left a bunch of flowers at reception, that's not so nice.
The message has a very different meaning depending on who sent it,

If that's the only two things your system can see, you don't have enough information to make a decision.
You need the additional context that goes with it; you need to know my relationship with the sender.



{% slide assume_worst_intent 40 %}

So context is important.
Give people a way to report problems, believe them, treat their reports in good faith.
Act upon them.

*[Ed. I ran out of time to mention this, but I'd point to the [Code of Conduct reporting procedure](https://2018.pyconuk.org/code-conduct/) as an example of how to collect reports of harassment.]*

Finally, look after your moderators.
Today, we've only talked about online harassment, personal harassment (it's only a 25 minute slot!).
There are lots of other awful things on the Internet: child pornography, sexual abuse, rape imagery, animal harm, torture imagery.



{% slide assume_worst_intent 41 %}

These are really awful horrific things that your moderators will have to look at and make a judgement on every time somebody reports it.
Look after them -- make sure they're supported.
Appropriate counselling, enough breaks, and so on, because even just looking at this stuff really hurts people.



{% slide assume_worst_intent 42 %}

This is a [tweet from rahaeli](https://twitter.com/rahaeli/status/1036304125418504192), who did a lot of work on the LiveJournal trust and safety team.
It's part of a larger thread -- 40% of people burnt out within three months of having to go through the cesspit of human interaction.

*[Ed. I don't remember rah's exact role at LiveJournal, but I think they might have been head of the team?  If you care about online safety and building good communities, they're a very good follow [on Twitter](https://twitter.com/rahaeli).]*



{% slide assume_worst_intent 37 %}

So human moderation is best, but look after your moderators.



{% slide assume_worst_intent 45 %}

Finally, **design with abusive personas in mind**.

We're used to designing with persona where we think about trying to help people.
How can we make this flow easier?
How can we make our service better?
How can we make this process smoother?

Think in the opposite direction: imagine somebody really awful wants to use your service.
How are they going to use it to cause harm?
How can you make their life as difficult as possible?



{% slide assume_worst_intent 46 %}

Here's a summary slide: some ways you can protect yours users better:

1.  Diversify your team
2.  Think about your name policies
3.  Robust privacy controls
4.  Human moderation
5.  Design with abusive personas in mind

These things won't catch everything, but they will catch a lot, and they will make your service better.



{% slide assume_worst_intent 47 %}

I'll leave you with this: whenever you're building something, always ask: **How could this be used to hurt someone?**
**How could an abusive ex misuse this?**

Because if you don't answer those questions, somebody else will answer them for you, and your users will get hurt in the process.

Thank you all very much.

Fin.

---

## Q&A

I didn't take audience Q&A in this session, partly for time and partly because it's a topic that gets derailed easily.
My preference is always to have conversations in the hallway track.

https://twitter.com/hannahintech
