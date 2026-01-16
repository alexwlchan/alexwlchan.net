---
layout: post
date: 2022-08-01 08:21:03 +00:00
title: A surprise smattering of stardom
summary: My last post was surprisingly popular; a few reflections on the experience.
tags:
  - blogging about blogging
colors:
  index_light: "#ff6602"
  index_dark:  "#fe6600"
---

My previous post [about taking more screenshots][screenshots] has resonated with a lot of people.
It got thousands of impressions on Twitter, and at one point it was #2 on the Hacker News homepage:

<figure style="width: 562px;">
  {%
    picture
    filename="hn_screenshot.png"
    alt="A screenshot of the Hacker News homepage, with my post in the second slot from the top. The top slot is a link to a Vi Hart video about hexaflexagons."
    class="screenshot"
    width="562"
  %}
  <figcaption>
    I’m a big fan of Vi Hart, so having my posts be considered on a par with their videos is a huge compliment.
  </figcaption>
</figure>

I was a bit surprised: most of my posts are only read by a handful of people.
In hindsight, I can see why this post had broad appeal, but when I was writing I thought it would get a similar reception to my other posts.
This isn't the first time one of my posts has become popular, but it still feels unusual.

Whenever a post escapes my small corner of the Internet, I brace myself for negativity and cynicism, but this experience was broadly positive.
Most of the comments I saw were constructive and thoughtful, and many people shared stories of their own projects they'd preserved through screenshots.

It was also relatively stress-free.
These are a few notes on what it was like to be (briefly) popular.

[screenshots]: /2022/screenshots/

---

## Not having analytics: good

I don't have any analytics on this blog.
I don't know how many people read the post.

At various times I've used Google Analytics, self-hosted Piwik, and parsing server-side logs, but right now I don't know anything about my visitors.
No hit counts, no metrics, no dashboards, nothing.
I wouldn't do anything with those numbers, so I don't collect them.

This was probably a good thing: if I had a hit counter, I know I'd have been obsessively refreshing it for the dopamine hit.
That would have ruined my day for very little gain.
Instead, I got to enjoy a relaxing walk through London and mostly ignore the post's popularity.

---

## Hosting on Netlify: good

A couple of months ago, I switched this blog from a single [VPS] to [Netlify].

There were several reasons for the switch, and performance was one of them.
The VPS was quite slow to serve pages, and it struggled when lots of people were trying to get to the site.
(For small values of "lots"; I don't think I'd configured nginx properly.)

If I was still using my VPS, I think the site would have been ["hugged to death"][hug].
Netlify handled it fine; as far as I know the site stayed up all weekend.
I never worried about the site going down, or felt the need to monitor it.

That's what good infrastructure should be: reliable enough that I never need to care.

[VPS]: https://en.wikipedia.org/wiki/Virtual_private_server
[Netlify]: https://www.netlify.com
[hug]: https://en.wikipedia.org/wiki/Slashdot_effect

---

## Static HTML and CSS: good

I build this site the "old-fashioned" way: I have static HTML pages, with a smidgen of CSS and images for decoration.
This undoubtedly helped the site stay up: there was no central server or shared resource to fall over.

---

## The cost of serving my post: sad

I published the post on Saturday; on Sunday I woke up to an email from Netlify:

> Your bandwidth usage on your team (alexwlchan) has reached 50% of the current allowance in your billing cycle from July 17 to August 17.
>
> If bandwidth usage goes over the allowance before the end of the billing cycle, we’ll add an **extra bandwidth pack for $55**, increasing your allowance by **100GB** for the current billing cycle.

This came in around 4am; by the time I read it, I was at 97%. Eek.

I was on the Netlify Starter plan, which is free and comes with 100GB of bandwidth per month.
Normally I use a fraction of that; this post burnt through it in a day.

I temporarily upgraded to the Netlify Pro plan, which gets me 1TB of bandwidth for $19 per month.
It gave me time to think, and to decide how to fix it properly.

**I lost money because my post got popular.**
I don't get any income from the site, and normally I'm okay with that, but this was a bit of a weird realisation.
I'll be fine, it's just strange.

I could stick a free CDN like Cloudflare in front of the site, which would cost much less.
I've resisted this in the past because it felt unnecessary, but I might have to revisit that.
If I'm going to do it, I should do it before another post gets popular -- trying to insert a CDN during a spike feels like a recipe for outages.

---

## Forgetting to optimise my images: bad

I did a bit of digging, and realised I'd forgotten to optimise the image in the post.
It was 4× wider than it needed to be, and using 1.5MB of bandwidth per page load.
Oops.

I replaced the image with a smaller version, and I added alternative resolutions with the [`srcset` attribute][srcset].
That reduced the image to a much more manageable 147KB, and my bandwidth usage has dropped off (though it's hard to tell if that's the new images or less people visiting the post).

Normally I'm pretty good about keeping page weight down, and I'm proud of that.
(One person even commented about how fast it felt!)
The rest of the post is just 39KB, which is *tiny* by modern web standards.
I got unlucky that I forgot to optimise the images on this occasion.

This made my bandwidth problem worse, but even without the image I might have blown my cap.

[srcset]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-srcset

---

## Preparing for next time: maybe?

I don't know if there will be a next time; I'm terrible at predicting which posts will be popular.
It could be next week, or it could be never.

Designing my blog to handle "viral" traffic has always felt like a premature optimisation (air quotes because this was still very small by Internet standards) -- but the unexpected Netlify bandwidth bill has me rethinking that.
I don't want to wake up, discover a post went properly viral while I was asleep, and realise I'm facing hundreds of dollars in bandwidth usage fees.

I'll probably set up Cloudflare when I have some time, to give me peace of mind.

Otherwise, I'm not planning to change much.
I'll keep posting as I always have, and be pleasantly surprised if anything else catches the Internet's eye.
