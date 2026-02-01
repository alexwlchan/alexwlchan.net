---
layout: post
date: 2024-05-14 14:39:11 +00:00
title: What comes after AWS?
summary: |
  Whatever displaces public cloud as the default model for large-scale computing has to be more than “AWS, but 3% better”.
tags:
  - aws
colors:
  index_dark:  "#80a737"
  index_light: "#3c5a32"
card_attribution: https://www.pexels.com/photo/green-forest-2739664/
---

James Governor posed some interesting questions yesterday:

{% tweet "https://twitter.com/monkchips/status/1790018203478876243" %}

I started writing a reply, but it was too long for Twitter, so I'm posting it here.

Whatever displaces AWS (and similar public clouds) as a dominant force in computing has to be significantly better in some key area.
It's not enough to offer a marginal improvement -- "like AWS but 3% better" isn't going to win anyone over.
You need some major advantage that provides the activation energy to justify the expense of switching away from AWS.

This is why we see lots of stories of migrations between on-prem and public cloud, but not as many between different clouds.
There are major differences between on-prem and public cloud, and one of those differences might offer an advantage that justifies the cost of moving (in either direction).
But the big public clouds are similar enough that there are less advantages to switching between them.

So what might be the big improvement that draws people away from AWS?
Here are some guesses:

### Turnkey solutions for common problems

AWS has [a *lot* of services](https://aws.amazon.com/products/).
That flexibility is great, but it comes with challenges.

It's not always obvious which service is best for a given task, and a lot of common use cases require combining core primitives in architecture diagrams that resemble [Rube Goldberg machines].
These complex setups put a lot of responsibility on the developer to get everything right, and open the door to subtle bugs.
For example, setting up your IAM permissions so services can talk to each other is quite fiddly, and it's tempting to write a blanket "allow all" policy and be done with it.

I think there's an opportunity for higher-level services that streamline this experience.
Combine these core primitives and present a nicer interface for common use cases -- static sites, web apps, data pipelines.
Developers give up some flexibility, but in return they get a simpler workflow, better guard rails, and the peace of mind that they haven't left a ticking time bomb somewhere in their config.

I already see some services in this area -- Vercel, Glitch, and Netlify spring to mind -- and I'm sure there more.
They won't replace all use of AWS, and they're not trying to, but I think they can carve off big chunks if they're lucky.

[Rube Goldberg machines]: https://en.wikipedia.org/wiki/Rube_Goldberg_machine

### Closer to the Edge

There are lots of advantages to running your code close to users -- as in, geographically close.
At some point all our devices are powerful enough that the network speed is the bottleneck for an app, and over long enough distances geographic latency becomes an issue.

AWS is still very tied to the "region" model -- your code runs in data centres in a specific geographic location.
A lot of requests still need to be routed back to that location before they can be handled, even if that's halfway round the world.
It's non-trivial to run your app across multiple regions.

There are a few AWS services that have a global presence, like CloudFront and CloudFront Functions, but there are other platforms that run in the edge by default, not tied to specific locations.
If this becomes more important, I think AWS might struggle to catch up compared to newer players.

I wrote those three paragraphs in January 2022, long before the current wave of generative AI and Large Language Models arrived.
At the time I thought there might be applications that would benefit from running in an edge network, but I wasn't sure what they were.
I wonder if AI and LLMs will be those applications -- they're definitely trying to be as fast as possible.

I haven't followed the field closely, but it feels like LLM latency is still defined by the speed of the model rather than the network connection.
Even if you're running a model locally, you're still waiting multiple seconds for results.
How long will that last?
How long before models are fast enough that there's a perceptible benefit to running them close to your users?

### More presence in the Global South

Like a lot of the tech industry, AWS is very US-centric.
There are [more AWS regions on the west coast of the USA](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) than in all of South America and Africa.
But there are a lot of users and developers in the rest of the world, and it feels like they're underserved by a tech industry which is based in the Global North.
(Which assumes, for example, reliable access to cutting-edge hardware and high-bandwidth Internet connections as standard.)

I wonder what infrastructure that envisions the Global South as your primary users would look like.
What if Silicon Valley isn't the centre of your universe?
Is it just the same AWS, but at a lower latitude?
Or are there meaningful differences in how you build services for people who live in that part of the world?

(This is only a vague thought because I'm not an expert on politics, socioeconomics, or the tech industry in the Global South.
I don't know what might happen here, but I suspect it's not nothing.)

### A Free Tier that's actually free

There are plenty of horror stories about devs who set up an account on the so-called "Free Tier", and then receive a life-ruining bill.
Even if AWS forgives those charges, it has a chilling effect and deters people from trying the platform.
(I don't have a personal AWS account for precisely this reason.)

The free tier isn't about making money -- it's about cultivating a community of users who are experienced and comfortable with your platform.
When those users later have money to spend, you hope they'll pick you as the thing they already know.
But that can't happen if they're scared off before they can try the free tier.

Making a better free tier is a long-term play for a competitor, and risky -- you have to survive long enough for your free tier users to become paying customers.
But I think it could work, and you could win some business by speaking to people who aren't CTOs yet, but will be in a couple of years.

### Better bills for big business

Individual users want to get the most bang for their buck; companies have different priorities.
They want something that's predictable, which can fit in their accounting spreadsheets.

It's really hard to predict your AWS bill, because it follows a "pay-as-you-go" model and you can use different amounts each month.
At my last job, we'd routinely see a 5–10% change in our month-to-month bill.
That wasn't a big issue for us, but it could be an issue for somebody trying to do plan tight budgets or estimate future spending.

Even when you get the bill, it can be hard to understand where the money is going.
There are consultancies whose sole purpose is helping companies understand the cryptic crossword that is an AWS billing statement.

Predictable and comprehensible billing feels like it would be appealing to a lot of businesses.
I don't think it'd be the sole reason to switch to a competitor, but it would sweeten the deal.

### The power of politics

Public sentiment towards big tech companies is changing, and not in a positive way.
I can imagine new legislation that would hamstring AWS and other big public clouds, and drive a shift towards a larger set of small clouds, for example:

*   Concerns about the environmental impact of large data centres might lead to restrictions on their construction or expansion.
*   Antitrust or anti-monopoly lawsuits might force AWS to make changes which make their product worse, and leave an opening for a competitor.
*   More data locality laws that force companies to keep data inside national boundaries could lock AWS out of certain contracts, and drive business towards smaller, local clouds.

I don't know how likely any of these are, but they seem more plausible now than they did, say, five years ago.
I can imagine a future where AWS comes under more political scrutiny.

### Or maybe something completely different

Take all this with a pinch of salt.
I'm no expert, and this is light-hearted speculation rather than in-depth analysis.

When a company comes along that displaces AWS, it could do all of these, or none of them.
There are plenty of other strategies that smarter people than me have thought of.

I do think it's "when", not "if".
We may think of AWS as an institution now, but one day it will be relegated to the likes of IBM and Oracle -- tech companies that still exist, but with a fraction of the power and influence they had at their zenith.
The bigger a company gets, the more work it takes to change direction -- and eventually a smaller, more agile competitor will replace you.

At a previous job I was designing a digital archive that was stored in AWS, and that archive is expected to last decades, if not centuries.
That's why I was thinking about the long-term future of AWS -- that archive probably will outlast public cloud as a dominant model, and we designed the archive to make it easy to exit when that day comes.
This article has sat in my drafts for years, and I'm glad James's tweet finally prompted me to finish it.

I don't think AWS is going away any time soon, and if you're not an Amazon executive you probably don't need to think about it.
We should all be more concerned with our own longevity, not AWS.
