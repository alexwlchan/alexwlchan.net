---
layout: post
title: (Anti) Social Media
tags: slides
---

This is a talk I gave for students on Bournemouth University's Cyber Security Management course.
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
