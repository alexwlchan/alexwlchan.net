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

again since you've already heard from me
before I'll skip the introduction and
gets right into the talk we're talking
this morning about online harassment and
specifically how do we build systems to
prevent it the reduce it that reduce the
risk of it I'm gonna show you some
mechanisms and practical tips some ways
that I found that are most successful in
reducing online harassment but before we
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
offended so let's start off with an
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
bank so this all seems fine this seems
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
was available through their platform and
this is one of the big problems with
thinking about user safety we're
thinking about harass
is that if we let it be an afterthought
it becomes expensive it's harder to
retrofit later and it often means that
our users have to learn the hard way all
of the rough edges of our platform and
this is a shame because I fundamentally
believe that most developers mean well
the squash developers wants to make a
better way to send money to each other
they didn't want to build a tool for
harassment and I assume most people at
PyCon UK are pretty nice I'm assuming
you're all the same way so how do we do
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
have to think about them so what is
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
of you are familiar with it but one
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
screen and I think if you're building a
platform where people interact where you
have user to user interaction it is to a
certain degree your responsibility to
think about what people are doing on
there and to think about the effects
that might have beyond your platform so
this is all pretty nasty stuff who's
doing it I think we often have this as
the popular image of a hacker a
malicious person on the Internet and we
can see they tick all the hacker
stereotypes they're wearing a hoodie
there are a darkened basement they have
green tacks projected on their face

and maybe this is the sort of person we
need to worry about when we're thinking
about somebody stealing passwords from
our database or gaining root access to
our servers or to doing Mallick doing
malicious anonymous things again against
us as a service but what I'm really
talking about with harassment is much
more targeted it's directed against a
particular person and the sort of people
who tend to do online harassment it's
the same as the people who do personal
harassment in the real world so let's
think about who those people might be it
could be an abusive partner or an ex
could be family members it could be
classmates kids often don't have the
best social skills and we'll say pretty
mean things co-workers and ex co-workers
friends and ex friends that one date
weirdo another thing that the Internet
has opened up for us
you know today today you can go online
there are many online dating sites and
in many ways this is a wonderful thing
but now before you ever meet somebody
they can download your entire Facebook
profile your Twitter feed your Instagram
photos they know a huge amount about you
and if you decide that they didn't go so
well and they want to they they disagree
they now have many one wins of finding
you and tracking you later
rogue sis admins so what are your sister
admins doing with your data
do you trust some of the people who set
up the early Facebook servers and
oppressive regimes again well that's
something we are lucky enough not to
have to deal with in this country mostly
but you might if you are building a
global service you may have users in
environments like that who would like to
come after your users who would like to
come after their data and you need to be
thinking about that when you build your
service what you will notice about these
is that none of these people are
anonymous hackers who live in it who
live in a basement in Russia and wear
hoodies and drink bad coffee Russia are
not lucky enough to have Brodie's

the pattern we see with online
harassment is the same as the pattern we
see with personal harassment people are
more likely to be caught by people they
know and this is very scary because a
lot of the people a lot of people we
know are inherently more dangerous
individuals that Anonymous faces people
on the Internet
people like our family members or our
friends they have physical access to us
they probably know our intimate secrets
they probably know the answer to your
security questions
in fact just out of curiosity put your
hands up in the room if you know
somebody else's phone passcode I'm just
a curious they would say maybe that's
two-thirds of the room right and you're
all nice people right right I'm not
seeing the entire audience nodding which
is a little bit concerning but imagine
if you were imagine if you were a nasty
person imagine if you wanted to go
through somebody else's mess just go
through their Facebook feed go through
their private texts you could do that
please don't don't try this at home but
you could do that you have access to do
that and you know that makes these
people quite scary and a lot of the ways
we might otherwise protect ourselves all
the security all the to factor in the
world doesn't help if you have physical
access to a person and their device and
of course again physical access can go
beyond just the tools that we think
about beyond digital tools it can also
come down to simple acts of physical
harm somebody who lives 600 miles away
from me is going to struggle to
physically hurt me but somebody who
lives in the same house as me is gonna
have very little trouble doing that so
this is all very upsetting there are
horrible people in the world they do
horrible things they might be living in
the same house as you so maybe we should
all go and hide under a tin foil black
under a tin foil blanket and never leave
our room this would not be particularly
productive the good news is that it
doesn't have to be this way there are
tools and techniques we can use to build
services to reduce the risk of
harassment we can never stop all the
nasty people in the world but we can do
better there are ways that we are always
kept platforms that are not just open to
facilitate all forms of abuse we can do
better than to
komm so how can we protect our users and
restrict walkthroughs and best practice
for the rest of presentation the first
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
everyone so what's the first thing you
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
years later when it's a bit late so
think about diversifying the team what
we're talking about names let's talk
about name policies because there is a
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
both directions first of all it's
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
ground used by a number of services just
think carefully about your name policies
third thing moving on robust privacy
controls
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
think about that this is one of the
things that Twitter actually gets right
they have a blocking feature this is
what it looks like
so I blocked somebody here what you'll
notice though is that they tell you that
so it says you are blocked from
following Alex WL Chan and viewing Alex
WL trans tweets and imagine you went to
my Twitter profile of this after this
talking you saw that would that make you
feel happy respected like I you were
somebody that I liked
hopefully not um you'll probably feel
you'll probably feel quite annoyed quite
upset at me and you might decide to take
that out on me right imagine that we
were living in the same house and you
discover that I block to you that might
be its own trigger for retaliation so
another thing you can look at things
like shadow blocking muting allow people
to block somebody without ever being
visible to the other person their block
avoiding that regular voice that that
possibility of retribution offer
granular access controls so the default
is public private but you can go much
more you can go more granular than that
you could have followers only so that's
the Twitter model I can only post it I
can post things that only pre-approve
followers can see maybe only Mutual's
only down to the level of individual
users so you look at sites like Facebook
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
later and again often granular access
controls it makes it if you make it
easier to change people are more
comfortable because they don't have to
publish something with the entire world
see and that's going to make them more
likely to interact up more engagement as
people like to say number four rushing
on don't belong technology to solve
human problems so you need human
moderation because you don't have
context you don't know everything
happens on or off your service here's an
example of a text I got this morning
someone sent me a picture of a flower
they're thinking of me as a friend from
home and they now I've got this big talk
today that's really nice if it's the if
it's the stalker who rang my hotel room
six times last night and left me a bunch
of flowers at reception that's perhaps
not so nice but if that's the only two
things your moderators can see your
machine can see it doesn't know how to
make decision based on that you need
that you need the additional context
that goes with it
so context is important give people a
way to report problems and believe them
treat problems in good faith and finally
look after your moderators and this is
an important one as well
we've talked mostly today about I'm
talking mostly stay back from online
harassment personal harassment there are
lots of other awful things on the
Internet child pornography sexual abuse
rape imagery to an animal harm torture
imagery and these are really awful
horrific things that your moderators
will have to look at every time somebody
reports it and says hey maybe this is a
bad thing that you don't want to be
allowing allowing on your platform look
after them make sure let's ported
canceled hat breaks and so on because
looking at this stuff really hurts
people and briefly this is a tweet from
rah who was the LiveJournal trust and
safety 40% of people burnt out within
three months of having to go through the
cesspit of human interaction seeking
moderation is best
and finally design with abusive personas
in mind we're used to designing with
persona with personas where we think
about trying to help people how can I
make this flow easier for them make my
service better for them think in the
opposite direction imagine somebody
really awful wants to use my service how
are they going to use it to cause harm
and how can I make their life as
difficult as possible
so there's a summary slide some ways you
can protect now users make you better
diversify your team think about your
name policies robust privacy controls
human moderation design with abusive
personas in mind like I said these
things will not catch everything but
they will catch a lot and they'll make
up an and they will make your service
better and I'll leave you with this
always when you're building something
ask how could this be used to hurt
someone how could an abusive ex misuse
this because if you don't answer those
questions somebody else will answer them
for you and your users will get hurt in
the process thank you all very much

[Applause]
thank you Alex I'm sure and we more than
welcome to talk about it afterwards as
well we don't have any time for
questions I'm afraid we'll see you in
five minutes
