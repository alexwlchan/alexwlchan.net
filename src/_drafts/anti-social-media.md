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

You can read the slides and (lightly edited) notes on this page, or download the slides [as a PDF](/slides/anti_social_media/anti_social_media_slides.pdf).

<em><strong>Content warning:</strong> this talk includes discussion of online harassment, misogyny, racism, suicide, domestic abuse, police violence, sexual violence and assault, rape threats and death threats.</em>

[pycon]: /2017/11/privilege-inclusion/

<!-- summary -->

---

### A note of thanks

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
    TODO PUT AN IMAGE CREDIT HERE
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


{% slide anti_social_media 6 %}

TODO INSERT LINK TO TWEET

Well... yes and no.

In its original form, the Square Cash developers never thought to add a block feature.
After all, who'd want to turn down money?
But that left the messaging feature open for abuse -- for example, as this tweet explains, you could send anybody a message by sending them small amounts.

TODO DID SQUARE FIX IT?


{% slide anti_social_media 7 %}

The Square Cash developers aren't evil.
They set out to build a better payment platform, not a tool of harassment -- but somebody twisted what they'd built.

I think this is true of most people: they mean well, and don't want to build services to enable harassment.
Unfortunately, there are bad people in the world, and they exploit services for malicious ends.


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

TODO ANOTHER SLIDE ABOUT CONSEQUENCES


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
    TODO PUT AN IMAGE CREDIT HERE
    https://en.wikipedia.org/wiki/Rainbow_flag_(LGBT_movement)#/media/File:Rainbow_flag_and_blue_skies.jpg
  </figcaption>
</figure>

For example, outing somebody who's LGBTQ+ without their consent.

If a gay person is outed in a conservative community, or a trans person is exposed to their bigoted coworkers, that puts them at very direct risk of harm.


<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.021.png"><img src="/slides/anti_social_media/anti_social_media.021.png"></a>
  <figcaption>
    TODO PUT AN IMAGE CREDIT HERE
    https://www.pexels.com/photo/gray-house-with-fireplace-surrounded-by-grass-under-white-and-gray-cloudy-sky-731082/
  </figcaption>
</figure>

Another is a practice called [doxing][doxing], which is posting somebody's personally identifiable information -- their address, phone number, place of work.
Or if somebody is quite guarded, going after their friends and family -- who might be less careful about what they share.

Again, you can see how this puts somebody at risk.

[doxing]: https://en.wikipedia.org/wiki/Doxing



<figure class="slide">
  <a href="/slides/anti_social_media/anti_social_media.022.png"><img src="/slides/anti_social_media/anti_social_media.022.png"></a>
  <figcaption>
    TODO PUT AN IMAGE CREDIT HERE
    https://commons.wikimedia.org/wiki/File:U.S._%26_Romanian_Forces_Conduct_Bilateral_Training_150225-M-XZ244-306.jpg
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
    TODO PUT AN IMAGE CREDIT HERE
    https://www.pexels.com/photo/bed-bedroom-blue-brown-172872/
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
    TODO PUT AN IMAGE CREDIT HERE
    https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/2001_Audi_RS4_B5_Avant_-_Flickr_-_The_Car_Spy_%283%29.jpg/1280px-2001_Audi_RS4_B5_Avant_-_Flickr_-_The_Car_Spy_%283%29.jpg
  </figcaption>
</figure>


{% slide anti_social_media 27 %}

(Recap slide of forms of online harassment.)

In many areas, law enforcement are struggling to keep up -- things like cyberbullying or revenge porn didn't really exist a few years back, and laws are still being updated to reflect that these things are very, very bad.
And often, police don't really have the tools or bandwidth to investigate these crimes -- there's just too much for them to manage.


{% slide anti_social_media 28 %}


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


{% slide anti_social_media 34 %}

TODO ADD A PHOTO CREDIT

When these factors overlap, it gets even worse.

This is Diane Abbott, who was the first black woman MP in the UK.
She's one of 177 women MPs (at time of speaking TODO check this), but she receives more online abuse than most of them, and it's not hard to guess why.

Source: https://www.amnesty.org.uk/online-violence-women-mps

TODO proper credit


{% slide anti_social_media 36 %}


{% slide anti_social_media 37 %}


{% slide anti_social_media 38 %}


{% slide anti_social_media 39 %}


{% slide anti_social_media 42 %}


{% slide anti_social_media 43 %}


{% slide anti_social_media 44 %}


{% slide anti_social_media 45 %}


{% slide anti_social_media 46 %}


{% slide anti_social_media 47 %}


{% slide anti_social_media 48 %}


{% slide anti_social_media 49 %}


{% slide anti_social_media 51 %}


{% slide anti_social_media 52 %}


{% slide anti_social_media 54 %}


{% slide anti_social_media 55 %}


{% slide anti_social_media 56 %}


{% slide anti_social_media 57 %}


{% slide anti_social_media 59 %}


{% slide anti_social_media 61 %}


{% slide anti_social_media 62 %}


{% slide anti_social_media 63 %}


{% slide anti_social_media 64 %}

TODO: IMAGE CREDIT


{% slide anti_social_media 66 %}


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

TODO private/public is easy

what about more granular


{% slide anti_social_media 73 %}

Here's an example of the granular controls [exposed by Facebook](https://www.facebook.com/settings?tab=privacy).

More than just "who can see my posts", they have tools like:

-   Editing privacy settings on past posts.
-   How visible on my friends list?
    This is useful if I have friends who keep changing their handles to evade detection.
-   Who can find me, and how?
    Which affects the chance of drive-by bullying.


{% slide anti_social_media 75 %}


{% slide anti_social_media 76 %}


{% slide anti_social_media 79 %}


{% slide anti_social_media 80 %}


{% slide anti_social_media 81 %}


{% slide anti_social_media 82 %}

TODO PHOTO CREDIT

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


{% slide anti_social_media 89 %}

(Link to slides, thank everybody who helped.)

TODO Add Gail to thanks slide
