---
layout: post
date: 2020-02-25 12:13:12 +0000
title: A remote-controlled oven is a safety nightmare
summary: We should always think about how a malicious user might misuse the things we build. What could they do with a remote-controlled oven?
category: Diversity, inclusion and accessibility

index:
  best_of: true
---

Last month, Monzo published [a blog post][monzo] about how they hire product designers.
The blog post got some attention on Twitter over the weekend, and in particular a design exercise for an app-controlled oven:

> Following a successful phone call, we’ll give you a small task to see how you respond to a real-life challenge.
>
> The brief is to design a companion app interface for an oven with no physical controls.
>
> <img src="/images/2020/monzo_oven.png" alt="A grey rectangle with the words “Monzo Oven” inscribed in faint lettering at the top">
>
> It should take about an evening or two to complete, though it’s fine to take as much time as you need to think about the problem. Most people return their tasks to us within 7-14 days.

[monzo]: https://monzo.com/blog/2019/01/17/monzo-product-designer-jobs

It's been criticised from various angles -- because it's a [take-home design exercise][exercises], because an app-controlled oven is dangerous, because hiring people who will blithely design a bad idea bodes poorly for a bank -- but I have an angle I haven't seen elsewhere.

[exercises]: https://orgdesignfordesignorgs.com/2018/05/15/design-exercises-are-a-bad-interviewing-practice/

When I saw this oven, my first thought was: *how would a terrible flatmate misuse this oven?*
This is a topic [I've written about in the past][assume_worst_intent] -- even if a product or service is bug-free, a malicious or abusive user could still use it to hurt someone.
We should always design with abusive personas in mind, and consider how the things we build might be weaponised.

[assume_worst_intent]: /2018/09/assume-worst-intent/

How could somebody nasty misuse an oven that's controlled by an app?
Before you read on, you might want to try this exercise yourself.
How many ways can *you* think of that an abusive ex or terrible flatmate might use this oven to hurt someone?
What sort of things should you consider when designing this oven?
I'll explain some of my ideas after the picture.

<figure>
  <img src="/images/2020/kitchen_fire.jpg" alt="Screenshot of a kitchen in a game world. Several units in the kitchen are on fire.">
  <figcaption>
    This scene will be familiar to anybody who&rsquo;s played <em>The Sims</em>.
  </figcaption>
</figure>

How many ideas did you think of?
How many edge cases and loopholes do we need to cover before it's safe to ship this oven?
I've written some of my ideas below, to give you a flavour of the sort of thing I thought about.
I'd be interested to hear if you thought of something I didn't -- let me know [on Twitter](https://twitter.com/alexwlchan).



## Who can control the oven?

The brief doesn't specify whether this oven is tied to a single person, or if multiple people can control it.
Since most households have more than one person, let's assume it has multi-user controls (although a single-user appliance has plenty of other problems).
How do you control who has access?

-   How do you ensure the right people can control your oven, and the wrong people can't?

-   Suppose two people give the oven conflicting instructions; which one should take precedence?
    This could be malice -- two people squabbling over dinner -- or an accident -- if one person is cooking something, and another tries to preheat the oven for their own food.

-   Do you need more granular permissions than "can control the oven"?
    For example, maybe you don't trust your children to turn the oven on, but you do want to let them turn it off in an emergency.

-   If you're a landlord who rents out your flat to long-term tenants, or an Airbnb host with short-term visitors, how do you let them cook food in the oven?

Access control is extremely hard to do well -- both the design of the permissions system, and an interface that means users can understand it and configure it for their needs.



## What happens when somebody moves out?

The people in a household change over time: a partner moves in, a flatmate moves out, somebody crashes with you while they're between places.
What happens when somebody leaves?

-   Can they still control the oven after they move out?

-   Can you block them from using the oven after they're gone?
    Conversely, could they block *you* from using it, even though you're the person who still lives there?

<!-- -   It's tempting to use physical controls as the deciding factor in access control.
    If I can get to the oven, I can pair my phone with it and I'm able to control it.
    (This is how my oven works, with physical knobs and buttons.
    If you're in my kitchen, you can turn my oven on -- but you can't do it remotely.)

    Somebody who's moved out might still visit from time to time.
    Are they allowed to control the oven when they're back? -->

-   If you're living in a rented flat, are you sure the previous tenants don't still have access to the oven?
    Do you trust the landlord has turned off their permission correctly?
    Or if you've just bought somewhere, the previous owner?

This is drilling into the complexities of multi-user access control.
Any time you have a resource that might be shared by multiple people, you need to think about how you allocate permissions, and how you update or remove permissions over time.



## What if somebody malicious can control the oven?

So far I've talked about the complexities of access control.
Now let's suppose that access control has gone wrong, and somebody malicious has control of the oven.
Maybe you have an unsavoury landlord, or an ex-flatmate you fell out with.
How could they make your life miserable?

<!-- -   They can turn off your access to the oven, so you can't cook food.
    This is plain annoying, but not especially harmful. -->

-   There are horror stories about bad landlords, who neglect or rip off their tenants.
    If the landlord is the designated "owner" of the oven, they could turn off your oven, and charge an extra fee to use it -- above and beyond the base rent.

-   Consider somebody sneaky: they never take control of the oven, so you don't realise they still have access -- they just use the app to see when the oven is turned on.
    If you're a responsible home owner and don't leave the oven running when you're out, the oven status gives them a strong indicator of when you're at home.

    If the oven is equipped with sensors that tell it what sort of food it's cooking, and that information is displayed in the app, it might even give them an idea of how many people are home -- and in particular, whether you're home alone.

-   Somebody could change the temperature of the oven while it's cooking, affecting the food inside.
    You could end up with a burnt meal -- annoying, the food is wasted, but at least it's obvious something has gone wrong.
    If they're more subtle, they could program the oven to undercook the food in a non-obvious way.
    This could be a dangerous source of food poisoning, especially if you're cooking something like meat or fish.

-   Finally, if you want to go full evil, somebody could try to damage the oven, or even start a fire in your home.
    Modern ovens have a lot of safety features, so this might be harder in practice -- but oven fires are possible, and there are definitely people who'd consider trying this.

It's nice to imagine that all of our users are lovely, wholesome people who'd never hurt anyone.
The reality is different: there are bad people in the world, and if you have a sufficiently large user base, some of your users will be bad people.
If you don't think about how they'll misuse your product or service, you'll find out when they try it in practice -- and other people will get hurt in the process.



## Conclusions

This post started as [a few tweets][thread], and as I started to write, I thought of more and more ways this could go wrong.
I hope you found it useful, and maybe it got you thinking about some failure modes you haven't considered before.

Most of us aren't building internet-connected ovens, so the specific ideas aren't immediately practical.
But the general ideas -- good access controls, dealing with malicious users, our services being used in unexpected and harmful ways -- are broadly applicable.

If you're building any sort of product or service, abusive personas need to be part of your design process.
Safety can't be an afterthought -- it's easier to head off a problem early, in the design stages, before it gets to users.
People can and will use the things we build for evil, and we need to anticipate that in advance.

[thread]: https://twitter.com/alexwlchan/status/1231869918926299136
