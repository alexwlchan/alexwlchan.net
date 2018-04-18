---
layout: post
title: (Anti) Social Media
tags: slides
---

This is a talk I gave today for students on Bournemouth University's Cyber Security Management course.
It's loosely inspired by a talk about [privilege and inclusion][pycon] I gave at PyCon UK last year, focusing on a specific area -- online harassment.

The idea is to discuss harassment, and how the design of online services can increase (or decrease) the risk to users.
A common mantra is *"imagine how an abusive ex will use your service"* -- this talk is the expanded version of that.

Here's a brief outline:

*   What does online harassment look like?
    With specific examples: harassment, bullying, doxing, threats, and so on.
    Not everyone faces harassment to the same degree (or at all!), so I wanted to illustrate the sort of risks a user might face.

*   Threat models: why some groups are more at risk, and the sort of people we should worry about.
    The abusive ex is an important risk to consider, but who else?

*   What are some possible good practices?
    How can service operators reduce the risk to their users?
    Reviewing some common suggestions -- things like blocking, shadow bans, restricting anonymity -- what works and what doesn't.

The aim isn't to be a comprehensive resource, but to get students thinking about these risks.
Harassment is a constantly moving target, and it's better to anticipate them before they happen.

You can read the slides and notes on this page, or download the slides [as a PDF](/slides/anti_social_media/anti_social_media_slides.pdf).
The notes are my lightly edited thoughts about what I was going to say with each slide -- but they may not be exactly what I said on the day!

(Caveat: I didn't quite finish writing up all the notes before the lecture.
The PDF slides are the most up-to-date, and I'll try to go back and update the inline notes soon.)

<em><strong>Content warning:</strong> this talk includes discussion of online harassment, misogyny, racism, suicide, domestic abuse, police violence, sexual violence and assault, rape threats and death threats.</em>

[pycon]: /2017/11/privilege-inclusion/

<!-- summary -->

<!-----

### A note of thanks

Thanks to [Gail Ollis](https://staffprofiles.bournemouth.ac.uk/display/gollis), who invited me to Bournemouth to give the talk.

The ideas in this talk are influenced by a number of people -->

---

{% slide anti_social_media 1 %}

(Introductory slide.
Mention that slides/notes will be available after the talk.)


{% slide anti_social_media 2 %}

Harassment can be a difficult topic.
**This talk comes with a number of content warnings**, including discussion of:

*   Online harassment
*   Misogyny
*   Racism
*   Suicide
*   Domestic abuse
*   Police violence
*   Sexual violence and assault
*   Rape and death threats

If somebody wants to step out for a few minutes (or you want to stop reading), I won't be upset.
Please look after yourselves!


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.004.png"><img src="/slides/anti_social_media/anti_social_media.004.png" alt="An illustration of a blank cheque book"></a>
  <figcaption>
    Image credit: A cheque book.
    Made by <a href="https://www.flickr.com/photos/easy-pics/8138517266/">The Clear Communication People</a>, used under CC BY-NC-ND.
  </figcaption>
</figure>

A [tweet from a friend][drmaciver] got me thinking about cheques recently, and ways to pay.
The Internet has changed finance -- today, we have all sorts of ways to send money to each other.
Besides cash and cheques, we have online banking, PayPal, micropayment services, and so on...

[drmaciver]: https://twitter.com/DRMacIver/status/981267514738003968


{% slide anti_social_media 5 %}

Here's an example of one such app: [Square Cash][square].

People can send money to each other with an app on their phones, and they can send messages to discuss the payments.
The money is transferred near instantly, much faster than if you're using paper, and the conversation forms a useful audit trail.
This is much better, right?

[square]: https://en.wikipedia.org/wiki/Square_Cash


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.006.png"><img src="/slides/anti_social_media/anti_social_media.006.png" alt="An illustration of a blank cheque book"></a>
  <figcaption>
    Tweet by <a href="https://twitter.com/TweetAnnaMarie/status/789957313649967104">Anna Marie Clifton</a>.
    Retrieved 18 April 2018.
  </figcaption>
</figure>

Well... yes and no.

In its original form, the Square Cash developers never thought to add a block feature.
After all, who'd want to turn down money?
But that left the messaging feature open for abuse -- for example, as this tweet explains, you could send anybody a message by sending them small amounts.

(Shortly after this tweet, Square Cash [did add a way](https://twitter.com/rsa/status/790592489799331841) to block users.
Instructions are [on their help site](https://squareup.com/help/us/en/article/5144-cash-app-security).)


{% slide anti_social_media 7 %}

The Square Cash developers aren't evil.
They set out to build a better payment platform, not a tool of harassment -- but somebody twisted what they'd built.

I think this is true of most people: they mean well, and don't want to build services to enable harassment.
Unfortunately, there are bad people in the world, and they exploit services to do nasty things.


{% slide anti_social_media 8 %}

A lot of time, discussion of security focuses on technical measures -- stuff to protect a service from bad actors.
Things like passwords, two-factor authentication, encryption.

But what if that all works?

Who protects users from other users on our service?


{% slide anti_social_media 9 %}

The sad truth is, if you allow any sort of user-to-user interaction on a service, it will probably be exploited for harassment.
People will find ways to hurt other people, because people are terrible.


{% slide anti_social_media 10 %}

So what does this sort of harassment look like?


{% slide anti_social_media 11 %}

In its simplest form, it means nasty messages.
Give people a free text box to send to each other, and some people will use it to write something unpleasant.

Two forms most of us are familiar with are [spam][spam] and [phishing][phishing].
We've all had emails from Nigerian princes or suspicious medical companies, and phishing attacks happen a-plenty.

[spam]: https://en.wikipedia.org/wiki/Spamming
[phishing]: https://en.wikipedia.org/wiki/Phishing


{% slide anti_social_media 12 %}

Here's an example of a recent attempt that nearly fooled me.

I'd been complaining about Virgin Media on Twitter, and somebody slipped into my DMs to talk about the problem.
I was taken in, and it wasn't until they asked for credit card details that I realised something was up -- but not before I'd explained my problem, and given them my account number.

Notice the extra "a1" in the handle?
I totally missed that.

So spam and phishing are common annoyances.
They're a problem in volume, but otherwise not too bad.
Let's think about messages that cause more direct harm.


{% slide anti_social_media 13 %}

Let's talk about more direct nasty messages.
Specific, harmful language designed to upset or distress somebody.
This is particularly common among kids, who consistently use the Internet to be terrible to each other (aka [cyberbullying][cyberbullying]).

[cyberbullying]: https://en.wikipedia.org/wiki/Cyberbullying


{% slide anti_social_media 14 %}

This isn't limited to a few bad eggs -- it happens a lot.
In 2016, 37% of children survey said they "often" experienced some form of online bullying.

Like all bullying, this has a documented, detrimental effect on mental health.
It can lead to anxiety, depression, self-harm, and so on -- it's not just something to "shrug off".
It can take years to recover from this stuff -- for children and adults.

[Source: Ditch the Label's [Annual Bullying Survey 2016][survey].
On p14, there's a graph *"How frequently did you experience cyberbullying?"*, and I summed the responses between *"often"* and *"constantly"*.
Retrieved 16 April 2018.]

[survey]: https://www.ditchthelabel.org/annual-bullying-survey-2016/


{% slide anti_social_media 15 %}

And unfortunately, some people don't get a chance to recover.
It's not unheard of for cyberbullying to lead to suicide among young people.

Examples:

-   [*Ryan Halligan loses his life to Taunts, Rumors and Cyber Bullying*][halligan], NoBullying.com.
    Retrieved 16 April 2018.

-   [*Candlelight vigil held in honor of Megan Meier*][meier], sccworlds.com.
    Retrieved 16 April 2018.

-   [*Holly Grogan, 15, leapt to her death ‘after abuse from Facebook bullies’*][grogan], by Steve Bird.
    The Times.
    Retrieved 16 April 2018.

That last one hits particularly hard for me, because Holly was in the year below me at school.

Harassment isn't something everyone can (or should) brush off.
This slide isn't for shock value -- it's to emphasise that harassment can have real, lasting consequences for the people involved.

[halligan]: https://nobullying.com/ryan-halligan/
[meier]: https://web.archive.org/web/20081222014832/http://www.sccworlds.com/worlds/index_files/dardenne_prairie/meierwalk.htm
[grogan]: https://www.thetimes.co.uk/article/holly-grogan-15-leapt-to-her-death-after-abuse-from-facebook-bullies-gl22hgwwzps


{% slide anti_social_media 16 %}

Some more examples of the sort of deliberately harmful messages people send:

Hate speech, which targets an entire group instead of an individual.

If a service allows sending images as well as text, people try to build distressing images to send to people.
This could be something violent, threatening, or unsolicited pornographic content.
None of which are pleasant to get in your inbox.


{% slide anti_social_media 17 %}

An example of what that imagery might look like: your head photoshopped into images or mutilation or sexual violence.
This is the sort of horrible, brutal stuff that people do to each other.

[Source: [*The Cops Don't Care About Violent Online Threats. What Do We Do Now?*][jezebel], by Anna Merlan.
Jezebel.
Retrieved 16 April 2018.]

[jezebel]: https://jezebel.com/the-cops-dont-care-about-violent-online-threats-what-d-1682577343


{% slide anti_social_media 18 %}

It can go all the way up to rape and death threats.
And if you get one of these, you have to decide: is this credible?
Do I report it?
Do I need to take evasive action?
Even if the threat never comes to pass, that's incredibly draining for the target.

So that's just some of the nasty messages people might send each other.

[An early edition of this talk included some screenshots from Anita Sarkeesian's post [*One Week of Harassment on Twitter*][oneweek], but when I did a test run of the talk, the mood was already so sombre I decided to skip the slide.]

[oneweek]: https://femfreq.tumblr.com/post/109319269825/one-week-of-harassment-on-twitter


{% slide anti_social_media 19 %}

So what else?

Posting personal information is another common form of harassment.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.020.png"><img src="/slides/anti_social_media/anti_social_media.020.png"></a>
  <figcaption>
    Image: Rainbow flag and blue skies, by <a href="https://commons.wikimedia.org/wiki/File:Rainbow_flag_and_blue_skies.jpg">Ludovic Berton</a>.
    Used under CC BY.
  </figcaption>
</figure>

For example, outing somebody who's LGBTQ+ without their consent.

If a gay person is outed in a conservative community, or a trans person is exposed to their bigoted coworkers, that puts them at very direct risk of harm.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.021.png"><img src="/slides/anti_social_media/anti_social_media.021.png"></a>
  <figcaption>
    Image: Grey house with fireplace, by <a href="https://www.pexels.com/photo/gray-house-with-fireplace-surrounded-by-grass-under-white-and-gray-cloudy-sky-731082/">Sebastian Soerensen</a>.
    Used under CC0.
  </figcaption>
</figure>

Another is a practice called [doxing][doxing], which is posting somebody's personally identifiable information -- their address, phone number, place of work.
Or if somebody is quite guarded, going after their friends and family -- who might be less careful about what they share.

Again, you can see how this puts somebody at risk.

[doxing]: https://en.wikipedia.org/wiki/Doxing



<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.022.png"><img src="/slides/anti_social_media/anti_social_media.022.png"></a>
  <figcaption>
    Image: US & Romanian forces conduct bilateral training, by <a href="https://commons.wikimedia.org/wiki/File:U.S._%26_Romanian_Forces_Conduct_Bilateral_Training_150225-M-XZ244-306.jpg">Sgt. Esdras Ruano</a>.
    Public domain.
  </figcaption>
</figure>

And a final odious form of this technique is [SWATing][swating].
After somebody's address has been leaked online, another person makes a phone call to the police and calls in a fake threat -- bomb hoax, hostage situation, home shooting -- which gets armed police send to their house.
Unaware of what's happened, you wake up at 2am to police with guns at your front door.

This is more common in the US.

[swating]: https://en.wikipedia.org/wiki/Swatting


{% slide anti_social_media 23 %}

This is extremely distressing for the victims, and wastes time and money for the police.
In a few unfortunate cases, it also leads to injury or death when the police get a bit too trigger-happy.

Examples:

-   [*Destiny developer startled awake by police, sheriff's helicopter after faked 911 call*](https://www.polygon.com/2014/11/7/7172827/destiny-swatting), by Brian Crecent.
    Polygon.
    Retrieved 17 April 2018.

-   [*Prank call sends close to 20 police officers to Southwest Portland home*](http://www.oregonlive.com/portland/index.ssf/2015/01/prank_call_sends_several_polic.html), by Casey Parks.
    The Oregonian.
    Retrieved 17 April 2018.

-   [*Gamer who made "swatting" call over video game dispute now facing manslaughter charges*](https://www.vox.com/policy-and-politics/2018/1/13/16888710/barris-swatting-death-charges), by Emily Stewart.
    Vox.
    Retrieved 17 April 2018.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.025.png"><img src="/slides/anti_social_media/anti_social_media.025.png"></a>
  <figcaption>
    Image: bedroom in blue and brown, by <a href="https://www.pexels.com/photo/bed-bedroom-blue-brown-172872/">Digital Buggu</a>.
    Used under CC0.
  </figcaption>
</figure>

I particularly dislike this next one -- sharing intimate photos without consent, or so-called "revenge porn".
This is relatively new.
In the past, taking a photograph was a complicated process that required specialist equipment, but now it's easy to take and share a photo.

So, couples take intimate photos and send them to each other.
All well and good, until they break up, and somebody decides to post those photos on the Internet.
It's an intrusion of privacy for their ex, and incredibly distressing to have those images leaked.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.026.png"><img src="/slides/anti_social_media/anti_social_media.026.png"></a>
  <figcaption>
    Image: rear seats of an Audi RS4, by <a href="https://commons.wikimedia.org/wiki/File:Audi_B5_RS4_Avant_-_Flickr_-_The_Car_Spy_(6).jpg">The Car Spy</a>.
    Used under CC BY.
  </figcaption>
</figure>

We need to be worried about child grooming.

When I was younger, we were all warned "stranger danger!  Don't get into the back of strange cars."
Now, children can be groomed or targeted from hundreds of miles away
Services need to think about how they protect children.

{% slide anti_social_media 27 %}

(Recap slide of forms of online harassment.)

In many areas, law enforcement are struggling to keep up -- things like cyberbullying or revenge porn didn't really exist a few years back, and laws are still being updated to reflect that these things are very, very bad.
And often, police don't really have the tools or bandwidth to investigate these crimes -- there's just too much for them to manage.

And this stuff changes all the time -- people are constantly finding new ways to harass, intimidate, hurt people.
If we're going to protect people, we need to anticipate new attacks before they happen.

One way to do that is threat modelling -- who's doing this, and why?
Getting inside their head can help us imagine what they might do next.
We'll cover that in the next section.


{% slide anti_social_media 28 %}

Notes on why harassment is bad -- it can escalate, we've seen examples of how it has consequences in the physical world, and it's just unpleasant to watch.


{% slide anti_social_media 31 %}

Okay, so nasty stuff happens on the Internet.

But who is it happening to?


{% slide anti_social_media 32 %}

Who is at risk?

In theory, anybody can be the target for online harassment -- and we've probably all had the mild stuff, like spam or phishing.
But this probably isn't a very useful question, so let's instead ask a different question.


{% slide anti_social_media 33 %}

Who is at *increased* risk?

Minority groups tend to come in for disproportionate levels of abuse and harassment in the physical world, and it's perhaps not surprising that the same patterns play out online.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.034.png"><img src="/slides/anti_social_media/anti_social_media.034.png"></a>
  <figcaption>
    Image: Official portrait of Diane Abbott MP, from the <a href="https://beta.parliament.uk/media/S3bGSTqn">UK Parliament website</a>.
    Used under CC BY.
  </figcaption>
</figure>

When these factors overlap, it gets even worse.

This is Diane Abbott, who was the first black woman MP in the UK.
She's one of 195 women MPs (at time of speaking), but she receives more online abuse than most of them, and it's not hard to guess why.

[Source: [*Black and Asian women MPs abused more online*](https://www.amnesty.org.uk/online-violence-women-mps). Amnesty International. Retrieved 18 April 2018.]

So that's who might be at risk.
But who's doing all this harassment?
Who might our hypothetical user be worried about?


{% slide anti_social_media 36 %}

Let's talk about threat models.


{% slide anti_social_media 37 %}

These are the sort of people you might be worried about -- an abusive partner or ex, your friends, a weirdo you went on one date with and never saw again.
These are the sort of people who commonly feature in reports of online harassment.


{% slide anti_social_media 38 %}

You'll notice that almost all of them are people that our user *knows*.
They're not the anonymous "trolls" we often talk about -- these are people we think we know.
Sadly, people are very likely to be hurt by people they know, but we often overlook them as a threat model because nobody needs to worry about their friends, right?


{% slide anti_social_media 39 %}

TOOD Are these state sup to date?

So let's break these examples down into different groups.


{% slide anti_social_media 42 %}

The first, most potent threat model: an abusive, current close contact.
Somebody who knows you very well.


{% slide anti_social_media 43 %}

I start with this model because it's the most important one.
These are the really scary people -- they have physical access to their user, and maybe their devices.
This puts the user at immediate risk.
And all the encryption and security in the world won't help someone if their abusive partner knows their phone password.


{% slide anti_social_media 44 %}

You also need to think about estranged contacts, who can be almost as scary.
They might not have physical access any more, but they still know most of your secrets -- mother's maiden name, first pet, town you grew up in -- so a lot of security questions are bunk.

And for somebody jaded, no form of revenge is too petty.

<!-- TODO msising a slide here -->


{% slide anti_social_media 45 %}

You need to consider not just individuals, but groups of people.
Herd mentality is a problem too!


{% slide anti_social_media 46 %}

And somebody who's indiscriminately targeted by bullies -- they've not done anything specifically wrong, but they were in the wrong time or place.

This raises questions of discoverability -- how easy is it to find other users on your service?
How easy is it for somebody to hide themselves from view?


{% slide anti_social_media 47 %}

And suppose one of your sysadmins or moderators takes a dislike to one of your users.
They have plenty of tools at their disposal -- they could steal personal information, go after friends, make a user's life very unpleasant.
How do you limit their destructive power?


{% slide anti_social_media 48 %}

(Recap slide of major threat models.)


{% slide anti_social_media 49 %}

<!-- TODO FINISH -->


{% slide anti_social_media 51 %}

<!-- TODO FINISH -->


{% slide anti_social_media 52 %}

Let's end on a more positive note: how can we build a service that minimises the risks of harassment?


{% slide anti_social_media 54 %}

So let's suppose we have a high-risk user.
Why do they want to use your service?

Mostly the same reasons as everybody else.
They *might* have additional reasons, but in general you can treat them as normal users.


{% slide anti_social_media 55 %}

A rising tide lifts all boats.

Make your service safer for high-risk users helps everybody -- all your users can benefit from improved safety/privacy/security.


{% slide anti_social_media 56 %}

So how might we make a service better?

Let's examine some approaches that are often suggested.


{% slide anti_social_media 57 %}

People sometimes say "if you don't like it, don't be on the Internet".

In 2018, this isn't practical advice -- many of us need the Internet for things like work, social life, finding a job.
It's impractical for people to stay offline, and severely disadvantages them if they do.


{% slide anti_social_media 59 %}

Some people/services take the attitude that users should just ignore harassment.

I think this is a morally dubious position ("I won't take steps to protect users on my service"), but okay.
We've already seen how harassment is more than just nasty comments, and can have physical-world consequences, but okay.

Consider also: what about the friends they have on your service?
They're not just giving up your service -- they're no longer able to talk to friends who they only talk to there.
(This is why leaving Facebook is so tricky for some people.)

And suppose they take your advice, and do leave.
If enough people do that, their friends might take note, and follow suit -- even if they're not being directly harassed themselves.
Suddenly you have a stampeding herd heading for the door.


{% slide anti_social_media 61 %}

Not everyone is tech savvy.

For users, this means they shouldn't need to be technical experts to be safe/comfortable online.
PGP, VPNs, Tor -- these are all useful tools, but they shouldn't be required knowledge to get by online.

For attackers, this means it's worth providing *some* protection, even if it isn't perfect.
Maybe you can't implement end-to-end encryption or protect against nation state actors, but you can probably stop somebody's nosy relative.
It's often said that [perfect is the enemy of good](https://en.wikipedia.org/wiki/Perfect_is_the_enemy_of_good), and that applies here.


{% slide anti_social_media 62 %}

You should think about what data you need to collect.

Any data you collect could be stolen, leaked, or inadvertently exposed -- but you can't lose data you don't have!
What's the minimal set of information you need to ask for, and then just ask for that.
Not every service needs a full set of personal details, contact info, and credit card numbers.

(GDPR makes this even more necessary.)


{% slide anti_social_media 63 %}

When you're building new features, think about ways they might be abused.
How could it be used in ways you don't expect?
And can you build it with safety in mind?


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.064.png"><img src="/slides/anti_social_media/anti_social_media.064.png"></a>
  <figcaption>
    Image: a marketing screenshot from <em>Journey</em>, by <a href="http://thatgamecompany.com/journey/">thatgamecompany</a>.
  </figcaption>
</figure>

An example: many multiplayer games have peer-to-peer interactions.
Everyone plays in a shared world, and they can talk to their fellow players.

But in *Journey*, players can't just send arbitrary text to other people


{% slide anti_social_media 66 %}

Have a way to ban or block malicious users -- this is the example from the opening.

You should have rules for what's acceptable on the platform, and be ready to enforce those, booting people out if they don't play nice.
And for individual users, give them a way to block other users -- they're under no obligation to talk to everybody.

I consider individual and platform-level blocking to be table stakes for online services.
Unfortunately not everybody does this (hi Slack), which can lead to uncomfortable experiences for their users.


{% slide anti_social_media 67 %}

This is what it looks like if you're blocked on Twitter.
You can't send the person a message, or see any of their tweets.


{% slide anti_social_media 68 %}

But notice -- the page is very explicit about this.
*"You are blocked."*

In some scenarios, just the act of blocking might put somebody at risk -- suppose somebody blocks their abusive partner just before an escape.
That itself could be a trigger for retaliation.


{% slide anti_social_media 70 %}

Another useful technique is [shadow banning](https://en.wikipedia.org/wiki/Shadow_banning).
You block or ban a user, but hide that fact from them.
They keep screaming into the void, but nobody else has to see what they're saying.

The idea is that eventually, they'll leave on their own because nobody's talking to them -- but without instigating any direct retaliation.


{% slide anti_social_media 72 %}

And really, banning and blocking are just parts of a much larger puzzle.

Give your users sophisticated privacy controls.
These are harder to implement, but add a lot of value.

<!-- TODO private/public is easy

what about more granular -->


{% slide anti_social_media 73 %}

Here's an example of the granular controls [exposed by Facebook](https://www.facebook.com/settings?tab=privacy).

More than just "who can see my posts", they have tools like:

-   Editing privacy settings on past posts.
-   How visible on my friends list?
    This is useful if I have friends who keep changing their handles to evade detection.
-   Who can find me, and how?
    Which affects the chance of drive-by bullying.


{% slide anti_social_media 75 %}

Let's change tack and talk about a different tactic some people suggest.

Anonymity is the source of all problems on the web, right?
Because you're not posting under your real name, people feel like they can say anything they like.

This isn't entirely true -- it's possible to have discussions where everybody involved is entirely anonymous, but it needs a lot of moderation and care.

And what is a real name, exactly?
Is it my driving license (which not everybody has)?
My passport (ditto)?
My birth certificate (even though lots of people change their name after birth)?
And how do you enforce that -- do people upload photos of their passports (see previous slide about limiting what you collect)?
And so on.

[The topic of "what is a name" could be a talk unto itself.
Patrick McKenzie's post [*Falsehoods programmers believe about names*](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/) is a good starting point, although a lot of the useful information from the comments is missing in the current version of the post.]

Let's suppose we have some real names -- we could be creating more risk.
On some sites, connecting a user to their physical world name could put them at risk -- dating sites, or kink communities.
So you may be inviting more harassment, or just driving users away.


{% slide anti_social_media 76 %}

An example from a thread with thousands of anonymous comments, but mostly civil discourse -- this one about coffee, typically a topic of much contention online!

Source: [*Skills For Someone Else*](https://fail-fandomanon.dreamwidth.org/187889.html?thread=1023582705#cmt1023582705), fail_fandomanon.
Retrieved 18 April 2018.


{% slide anti_social_media 79 %}

If you don't want to put in the moderation for true anonymity, pseudonyms are a good middle ground.
You get the accountability and reputation of a persistent name, but without trying to define what somebody's "real" name actually is.


{% slide anti_social_media 80 %}

Believe users if they save they have a problem.
All of our lived experiences is incomplete -- we don't know what it's like to be somebody of a different gender, or race, or sexual orientation.
So if they say there's a problem, be ready to believe them!

Your service may be big and large, and there are corners of it you don't see.
Even people with the same life experience as you may use your site differently.

And remember that it can be hard to report something, so don't penalise somebody who reports in good faith -- for example, don't sue somebody who reports a security bug.


{% slide anti_social_media 81 %}

Humans talking to other humans is a human problem, and automated systems will really struggle to solve it -- use humans instead!
For resolving a dispute between people, the best solution is to hire (and look after) human moderators.
This is expensive, but necessary.

It helps if your moderation team speak the same language as your users, ideally natively or at least fluently.
Language has subtle context that's hard to infer if you're not a fluent speaker, or using automated translation software.

Further reading:

*   [*Is queer a slur? Twitter seems to think so*](https://www.pinknews.co.uk/2018/03/19/is-queer-a-slur-twitter-thinks-so/), by Jess Glass.
    Pink News.
    Retrieved 18 April 2018.
*   [*The Scunthorpe Problem*](https://en.wikipedia.org/wiki/Scunthorpe_problem), Wikipedia.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.082.png"><img src="/slides/anti_social_media/anti_social_media.082.png"></a>
  <figcaption>
    Image: a yellow rose, by <a href="https://www.pexels.com/photo/beautiful-bloom-blooming-blossom-133472/">Anthony</a>.
    Used under CC0.
  </figcaption>
</figure>

Here's an example where it's impossible to infer context: somebody's sent me a text saying *"Thinking of you!"*.

This could be from my partner: they know I have a big talk today, they're sending me luck, that's really sweet.
Or it could be that creep who won't stop texting me, and rang my hotel room four times last night.
But most services don't have enough information to tell that difference.


{% slide anti_social_media 84 %}

And finally -- design with abusive personas in mind.
Repeating what we've said already: you should think about how an abusive ex will use your service.

We spend a lot of time thinking about design personas for our ideal user.
How can we make the service as elegant as easy as possible?
Let's take a negative slant as well.
For somebody who wants to do harm, how can I make their life as difficult and frustrating as possible?


{% slide anti_social_media 85 %}

(Recap slide of good practices.)


{% slide anti_social_media 86 %}


{% slide anti_social_media 87 %}


{% slide anti_social_media 88 %}

Closing thoughts.

When you build something, you have to ask: *How could this be used to hurt someone?*
For a more specific version: *How could an abusive ex use this?*

If you don't answer this question, it will be answered for you -- and somebody else will be hurt in the process.


{% slide anti_social_media 89 %}

(Link to slides, thank everybody who helped.)
