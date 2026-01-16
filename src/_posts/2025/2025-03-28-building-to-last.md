---
layout: post
date: 2025-03-28 08:43:57 +00:00
title: "What I've Learned by Building to Last"
summary: There are patterns in what lasts; people skills matter more than technical skills; long-lasting systems cannot grow forever.
tags:
  - talks
  - digital preservation
index:
  feature: true
colors:
  css_light: "#408074"
  css_dark:  "#7CF6DF"
---
Yesterday I gave a talk at [Monki Gras 2025](https://monkigras.com/).
This year, the theme is *Sustaining Software Development Craft*, and here's the description from the conference website:

> The big question we want to explore is -- how can we keep doing the work we do, when it sustains us, provides meaning and purpose, and sometimes pays the bills? We're in a period of profound change, technically, politically, socially, economically, which has huge implications for us as practitioners, the makers and doers, but also for the culture at large.

I did a talk about the first decade of my career, which I've spent working on projects that are designed to last.

I'm pleased with my talk, and I got a lot of nice comments.
Monki Gras is always a pleasure to attend and speak at -- it's such a lovely, friendly vibe, and the organisers James Governor and Jessica West do a great job of making it a nice day.
When I left yesterday, I felt warm and fuzzy and appreciated.

I also have a front-row photo of me speaking, courtesy of my dear friend [Eriol Fox](https://erioldoesdesign.github.io).
Naturally, I chose my outfit to match my slides (and this blog post!).

{%
  picture
  filename="eriol_photo.jpg"
  width="600"
  alt="It's me! I'm standing on stage holding a microphone and looking away from the camera, talking excitedly about something to do with people skills. I have dark hair falling down my shoulders, glasses, and a dark teal dress."
%}

## Key points

How do you create something that lasts?

* You can’t predict the future, but there are patterns in what lasts
* People skills sustain a career more than technical skills
* Long-lasting systems cannot grow without bound; they need weeding

## Links/recommended reading

*   Sibyl Schaefer presented a paper [Energy, Digital Preservation, and the Climate](https://ipres2024.pubpub.org/pub/1sm257xx/release/2) at iPres 2024, which is about how digital preservation needs to change in anticipation of the climate crisis.
    This was a major inspiration for this talk.

*   Simon Willison gave a talk [Coping strategies for the serial project hoarder](https://simonwillison.net/2022/Nov/26/productivity/) at DjangoCon US in 2022, which is another inspiration for me.
    I'm not as prolific as Simon, but I do see parallels between his approach and what I remember of Metaswitch.

*   Most of the photos in the talk come from [the Flickr Commons](https://commons.flickr.org/), a collection of historical photographs from over 100 international cultural heritage organisations.

    You can learn more about the Commons, browse the photos, and see who's involved using the Commons Explorer <https://commons.flickr.org/>.
    (Which I helped to build!)

## Slides and notes

<style>
  figure {
    width: 450px;
  }
</style>

<figure>
  {%
    picture
    filename="monki-gras/slide1.jpg"
    alt="Title slide. A black-and-white photo of somebody placing a stone in a dry-stone wall, with overlaid text ‘What I've Learned by Building to Last' and my personal details."
    link_to="https://en.wikipedia.org/wiki/File:Dry_Stone_wall_building.JPG"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: dry stone wall building in South Wales.
    Taken by <a href="https://en.wikipedia.org/wiki/File:Dry_Stone_wall_building.JPG">Wikimedia Commons user TR001</a>, used under CC BY-SA 3.0.
  </figcaption>
</figure>

[Make introductory remarks; name and pronouns; mention slides on my website]

I've been a software developer for ten years, and I've spent my career working on projects that are designed to last -- first telecoms and networking, now cultural heritage -- so when I heard this year's theme "sustaining craft", I thought about creating things that last a long time.

{%
  picture
  filename="monki-gras/slide2.png"
  alt="How do you create something that lasts?"
  class="dark_aware"
  width="450"
%}

The key question I want to address in this talk is **how do you create something that lasts?**
I want to share a few thoughts I've had from working on decade- and century-scale projects.

Part of this is about how we sustain ourselves as software developers, as the individuals who create software, especially with the skill threat of AI and the shifting landscape of funding software.
I also want to go broader, and talk about how we sustain the craft, the skill, the projects.

Let's go through my career, and see what we can learn.

<figure>
  {%
    picture
    filename="monki-gras/slide3.jpg"
    alt="Black-and-white photo of women working at a telephone switchboard."
    link_to="https://www.flickr.com/photos/35740357@N03/3660047829/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: women working at a Bell System telephone switchboard.
    From the <a href="https://www.flickr.com/photos/35740357@N03/3660047829/">U.S. National Archives</a>, no known copyright restrictions.
  </figcaption>
</figure>

My first software developer job was at a company called Metaswitch.
Not a household name, they made telecoms equipment, and you'd probably have heard of their customers.
They sold equipment to carriers like AT&T, Vodafone, and O2, who'd use that equipment to sell you telephone service.

Telecoms infrastructure is designed to last a long time.
I spent most of my time at Metaswitch working with BGP, a routing protocol designed on a pair of napkins in 1989.

<figure>
  {%
    picture
    filename="monki-gras/slide4.jpg"
    alt="Scans of two napkins with handwritten sketches and notes."
    link_to="https://computerhistory.org/blog/the-two-napkin-protocol/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    BGP is sometimes known as the "two-napkin protocol", because of the two napkins on which Kirk Lougheed and Yakov Rekhter wrote the original design.
    From the <a href="https://computerhistory.org/blog/the-two-napkin-protocol/">Computer History Museum</a>.
  </figcaption>
</figure>

These are those napkins.

This design is basically still the backbone of the Internet.
A lot of the building blocks of the telephone network and the Internet are fundamentally the same today as when they were created.

I was working in a codebase that had been actively developed for most of my life, and was expected to outlast me.
This was my first job so I didn't really appreciate it at the time, but Metaswitch did a lot of stuff designed to keep that codebase going, to sustain it into the future.

Let's talk about a few of them.

<figure>
  {%
    picture
    filename="monki-gras/slide5.jpg"
    alt="Careful to adopt new technology / cautious about third-party code / comprehensive tests and safety nets."
    link_to="https://www.flickr.com/photos/sdasmarchives/35321922122/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a programmer testing electronic equipment.
    From the <a href="https://www.flickr.com/photos/sdasmarchives/35321922122/">San Diego Air & Space Museum Archives</a>, no known copyright restrictions.
  </figcaption>
</figure>

1.  **Metaswitch was very careful about adopting new technologies.**
    Most of their code was written in C, a little C++, and Rust was being adopted very slowly.
    They didn't add new technology quickly.
    Anything they add, they have to support for a long time -- so they wanted to pick technologies that weren't a flash in the pan.

    I learnt about something called ["the Lindy effect"](https://en.wikipedia.org/wiki/Lindy_effect) -- this is the idea that any technology is about halfway through its expected life.
    An open-source library that's been developed for decades?
    That'll probably be around a while longer.
    A brand new JavaScript framework?
    That's a riskier long-term bet.
    The Lindy effect is about how software that's been around a long time has already proven its staying power.

    And talking of AI specifically -- I've been waiting for things to settle.
    There's so much churn and change in this space, if I'd learnt a tool six months ago, most of that would be obsolete today.
    I don't hate AI, I love that people are trying all these new tools -- but I'm tired and I learning new things is exhausting.
    I'm waiting for things to calm down before really diving deep on these tools.

2.  **Metaswitch was very cautious about third-party code, and they didn't have much of it.**
    Again, anything they use will have to be supported for a long time -- is that third-party code, that open-source project stick around?
    They preferred to take the short-term hit of writing their own code, but then having complete control over it.

    To give you some idea of how seriously they took this: every third-party dependency had to be reviewed and vetted by lawyers before it could be added to the codebase.
    Imagine doing that for a modern Node.js project!

3.  **They had a lot of safety nets.**
    Manual and automated testing, a dedicated QA team, lots of checks and reviews.
    These were large codebases which had to be reliable.
    Long-lived systems can't afford to "move fast and break things".

This was a lot of extra work, but it meant more stability, less churn, and not much risk of outside influences breaking things.
This isn't the only way to build software -- Metaswitch is at one extreme of a spectrum -- but it did seem to work.

I think this is a lesson for building software, but also in what we choose to learn as individuals.
Focusing on software that's likely to last means less churn in our careers.
If you learn the fundamentals of the web today, that knowledge will still be useful in five years.
If you learn the JavaScript framework du jour?
Maybe less so.

How do you know what's going to last?
That's the key question!
It's difficult, but it's not impossible.

{%
  picture
  filename="monki-gras/slide6.png"
  alt="you can't predict the future, but there are patterns in what lasts"
  class="dark_aware"
  width="450"
%}

This is my first thought for you all: **you can't predict the future, but there are patterns in what lasts.**

I've given you some examples of coding practices that can help the longevity of a codebase, these are just a few.

Maybe I have rose-tinted spectacles, but I've taken the lessons from Metaswitch and brought them into my current work, and I do like them.
I'm careful about external dependencies, I write a lot of my own code, and I create lots of safety nets, and stuff doesn't tend to churn so much.
My code lasts because it isn't constantly being broken by external forces.

<figure>
  {%
    picture
    filename="monki-gras/slide7.jpg"
    alt="Black-and-white photo of a small child using a hand-saw."
    link_to="https://www.flickr.com/photos/134017397@N03/53061818113/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a child in nursery school cutting a plank of wood with a saw.
    From the <a href="https://www.flickr.com/photos/134017397@N03/53061818113/
">Community Archives of Belleville and Hastings County</a>, no known copyright restrictions.
  </figcaption>
</figure>

So that's what the smart people were doing at Metaswitch. What was I doing?

I joined Metaswitch when I was a young and twenty-something graduate, so I knew everything.
I knew software development was easy, these old fuddy-duddies were
making it all far too complicated, and I was gonna waltz in and show them how it was done.
And obviously, that happened.
*(Please imagine me reading that paragraph in a very sarcastic voice.)*

I started doing the work, and it was a lot harder than I expected -- who knew that software development was difficult?
But I was coming from a background as a solo dev
who'd only done hobby projects.
I'd never worked in a team before.
I didn't know how to say that I was struggling, to ask for help.

I kept making bold promises about what I could do, based on how quickly I thought I should be able to do the work -- but I was making promises my skills couldn't match.
I kept missing self-imposed deadlines.

You can do that once, but you can't make it a habit.

About six months before I left, my manager said to me "Alex, you have a reputation for being unreliable".

<figure>
  {%
    picture
    filename="monki-gras/slide8.jpg"
    alt="Black-and-white photo of a small boy with a startled expression."
    link_to="https://www.flickr.com/photos/nlireland/9662924724/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a boy with a pudding bowl haircut, photographed by Elinor Wiltshire, 1964.
    From the <a href="https://www.flickr.com/photos/nlireland/9662924724/
">National Library of Ireland</a>, no known copyright restrictions.
  </figcaption>
</figure>

He was right!

I had such a history of making promises that I couldn't keep, people stopped trusting me.
I didn't get to work on interesting features or the exciting projects, because nobody trusted me to deliver.
That was part of why I left that job -- I'd ploughed my reputation into the ground, and I needed to reset.

<figure>
  {%
    picture
    filename="monki-gras/slide9.jpg"
    alt="Black-and-white photo of archive stacks with somebody pushing a trolley through them."
    link_to="https://wellcomecollection.org/collections/inter-library-loans"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: the library stores at Wellcome Collection.
    Taken by <a href="https://wellcomecollection.org/collections/inter-library-loans">Thomas SG Farnetti</a> used under CC BY-NC 4.0.
  </figcaption>
</figure>

I got that reset at [Wellcome Collection](https://wellcomecollection.org), a London museum and library that some of you might know.
I was working a lot with their collections, a lot of data and metadata.

Wellcome Collection is building on long tradition of libraries and archives, which go back thousands of years.
Long-term thinking is in their DNA.

To give you one example: there's stuff in the archive that won't be made public until the turn of the century.
Everybody who works there today will be long gone, but they assume that those records will exist in some shape or form form when that time comes, and they're planning for those files to eventually be opened.
This is century-scale thinking.

<figure>
  {%
    picture
    filename="monki-gras/slide10.jpg"
    alt="Black-and-white photo of a man in a fancy hat smiling and making a thumbs-up for the camera."
    link_to="https://www.flickr.com/photos/sdasmarchives/40556490133/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Bob Hoover.
    From the <a href="https://www.flickr.com/photos/sdasmarchives/40556490133/">San Diego Air & Space Museum Archives</a>, no known copyright restrictions.
  </figcaption>
</figure>

When I started, I sat next to a guy called Chris.
(I couldn't find a good picture of him, but I feel like this photo captures his energy.)

Chris was a senior archivist.
He'd been at Wellcome Collection about twenty-five years, and there were very few people -- if anyone -- who knew more about the archive than he did.
He absolutely knew his stuff, and he could have swaggered around like he owned the place.

But he didn't.
Something I was struck by, from my very first day, was how curious and humble he was.
A bit of a rarity, if you work in software.

He was the experienced veteran of the organisation, but he cared about what other people had to say and wanted to learn from them.
Twenty-five years in, and he still wanted to learn.

He was a nice guy.
He was a pleasure to work with, and I think that's a big part of why he was able to stay in that job as long as he did.
We were all quite disappointed when he left for another job!

{%
  picture
  filename="monki-gras/slide11.png"
  alt="people skills sustain a career more than technical skills"
  class="dark_aware"
  width="450"
%}

This is my second thought for you: **people skills sustain a career more than technical ones.**
Being a pleasure to work with opens so many doors and opportunities than technical skill alone cannot.

We could do another conference just on what those people skills are, but for now I just want to give you a few examples to think about.

<figure>
  {%
    picture
    filename="monki-gras/slide12.jpg"
    alt="be a reliable and respectful teammate / listen with curiosity and intent / don’t give people unsolicited advice"
    link_to="https://www.flickr.com/photos/35740357@N03/5546316291/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Lt.(jg.) Harriet Ida Pickens and Ens. Frances Wills, first Negro Waves to be commissioned in the US Navy.
    From the <a href="https://www.flickr.com/photos/35740357@N03/5546316291/">U.S. National Archives</a>, no known copyright restrictions.
  </figcaption>
</figure>

1.  **Be a respectful and reliable teammate.**
    You want to be seen as a safe pair of hands.

    Reliability isn't about avoiding mistakes, it's about managing expectations.
    If you're consistently overpromising and underdelivering, people stop trusting you (which I learnt the hard way).
    If you want people to trust you, you have to keep your promises.

    Good teammates communicate early when things aren't going to plan, they ask for help and offer it in return.

    Good teammates respect the work that went before.
    It's tempting to dismiss it as "legacy", but somebody worked hard on it, and it was the best they knew how to do -- recognise that effort and skill, don't dismiss it.

2.  **Listen with curiosity and intent.**
    My colleague Chris had decades of experience, but he never acted like he knew everything.
    He asked thoughtful questions and genuinely wanted to learn from everyone.

    So many of us aren't really listening when we're “listening” -- we're just waiting for the next silence, where we can interject with the next thing we've already thought of.
    We aren't responding to what other people are saying.

    When we listen, we get to learn, and other people feel heard -- and that makes collaboration much smoother and more enjoyable.

3.  Finally, and this is a big one: **don't give people unsolicited advice.**

    We are very bad at this as an industry.
    We all have so many opinions and ideas, but sometimes, sharing isn't caring.

    Feedback is only useful when somebody wants to hear it -- otherwise, it feels like criticism, it feels like an attack.
    Saying "um, actually" when nobody asked for feedback isn't helpful, it just puts people on the defensive.

    Asking whether somebody wants feedback, and what sort of feedback they want, will go a long way towards it being useful.

{%
  picture
  filename="monki-gras/slide11.png"
  alt="be a reliable and respectful teammate / listen with curiosity and intent / don’t give people unsolicited advice"
  class="dark_aware"
  width="450"
%}

So again: **people skills sustain a career more than technical skills.**

There aren't many truly solo careers in software development -- we all have to work with other people -- for many of us, that's the joy of it!
If you're a nice person to work with, other people will want to work with you, to collaborate on projects, they'll offer you opportunities, it opens doors.

Your technical skills won't sustain your career if you can't work with other people.

<figure>
  {%
    picture
    filename="monki-gras/slide13.jpg"
    alt="a museum gallery where every wall is covered with pictures, no space at all on the walls"
    link_to="https://art.dblock.org/2016/08/28/the-keeper-new-museum.html"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: "The Keeper", an exhibition at the New Museum in New York.
    Taken by <a href="https://art.dblock.org/2016/08/28/the-keeper-new-museum.html">Daniel Doubrovkine</a>, used under CC BY-NC-SA 4.0.
  </figcaption>
</figure>

When I went to Wellcome Collection, it was my first time getting up-close and personal with a library and archive, and I didn't really know how they worked.
If you'd asked me, I'd have guessed they just keep … everything?
And it was gently explained to me that

*"No Alex, that's hoarding."*

*"Your overflowing yarn stash does not count as an archive."*

Big collecting institutions are actually super picky -- they have guidelines about what sort of material they collect, what's in scope, what isn't, and they'll aggressively reject anything that isn't a good match.

At Wellcome Collection, their remit was "the history of health and human experience".
You have medical papers?
Definitely interesting!
Your dad's old pile of car magazines?
Less so.

<figure>
  {%
    picture
    filename="monki-gras/slide14.jpg"
    alt="a large dumpster full of discarded books"
    link_to="https://www.flickr.com/photos/brewbooks/6132547533/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a dumpster full of books that have been discarded.
    From <a href="https://www.flickr.com/photos/brewbooks/6132547533/">brewbooks</a> on Flickr, used under CC BY-SA 2.0.
  </figcaption>
</figure>

Collecting institutions also engage in the practice of [“weeding” or “deaccessioning”](https://clairebearian.medium.com/weeding-is-fundamental-on-libraries-and-throwing-away-books-9e664aa14c00), which is removing material, pruning the collection.

For example, in lending libraries, books will be removed from the shelves if they've become old, damaged, or unpopular.
They may be donated, or sold, or just thrown away -- but whatever happens, they're gotten rid of.
That space is reclaimed for other books.

Getting rid of material is a fundamental part of professional collecting, because professionals know that storing something has an ongoing cost.
They know they can't keep everything.

<figure>
  {%
    picture
    filename="monki-gras/slide15.jpg"
    alt="black-and-white photo of a box full of printed photos"
    link_to="https://www.pexels.com/photo/old-phots-in-a-brown-box-3234896/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a box full of printed photos.
    From <a href="https://www.pexels.com/photo/old-phots-in-a-brown-box-3234896/">Miray Bostancı</a> on Pexels, used under the Pexels license.
  </figcaption>
</figure>

This is something I think about in my current job as well. I currently work at [the Flickr Foundation](https://www.flickr.org), where we're thinking about how to keep Flickr's pictures visible for 100 years.
How do we preserve social media, how do we maintain our digital legacy?

When we talk to people, one thing that comes up regularly is that almost everybody has too many photos.
Modern smartphones have made it so easy to snap, snap, snap, and we end up with enormous libraries with thousands of images, but we can't find the photos we care about.
We can't find the meaningful memories.
We're [collecting too much stuff](/2024/digital-decluttering/).

Digital photos aren't expensive to store, but we feel the cost in other ways -- the cognitive load of having to deal with so many images, of having to sift through a disorganised collection.

<figure>
  {%
    picture
    filename="monki-gras/slide16.jpg"
    alt="black-and-white photo of a wheelbarrow full of weeds"
    link_to="https://www.pexels.com/photo/a-wheelbarrow-in-a-garden-26827231/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: a wheelbarrow in a garden.
    From <a href="https://www.pexels.com/photo/a-wheelbarrow-in-a-garden-26827231/">Hans Middendorp</a> on Pexels, used under the Pexels license.
  </figcaption>
</figure>

I think there's a lesson here for the software industry.
What's the cost of all the code that we're keeping?

We construct these enormous edifices of code, but when do we turn things off?
When do we delete code?
We're more focused on new code, new ideas, new features.
I'm personally quite concerned by how much generative AI has focused on writing more code, and not on dealing with the code we already have.

Code is text, so it's cheap to store, but it still has a cost -- it's more cognitive load, more maintenance, more room for bugs and vulnerabilities.

We can keep all our software forever, but we shouldn't.

<figure>
  {%
    picture
    filename="monki-gras/slide17.jpg"
    alt="black-and-white photo of a road with a fire burning alongside it, and a car parked which is partially obscured by smoke"
    link_to="https://www.flickr.com/photos/35740357@N03/3931004271/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Open Garbage Dump on Highway 112, North of San Sebastian.
    Taken by John Vachon, 1973.
    From the <a href="https://www.flickr.com/photos/35740357@N03/3931004271/">U.S. National Archives</a> no known copyright restrictions.
  </figcaption>
</figure>

I think this is going to become a bigger issue for us.
We live in an era of abundance, where we can get more computing resources at the push of a button.
But that can't last forever.
What happens when our current assumptions about endless compute no longer hold?

*   The climate crisis -- where's all our electricity and hardware coming from?
*   The economics of AI -- who's paying for all these GPU-intensive workloads?
*   And politics -- how many of us are dependent on cloud computing based in the US?
    How many of us feel as good about that as we did three months ago?

Libraries are good at making a little go a long way, about eking out their resources, about deciding what's a good use of resources and what's waste.
Often the people who are good with money are the people who don't have much of it, and we have a lot of money.

It's easier to make decisions about what to prune and what to keep when things are going well -- it's harder to make decisions in an emergency.

{%
  picture
  filename="monki-gras/slide18.png"
  alt="long-lasting systems cannot grow without bound; they need weeding"
  class="dark_aware"
  width="450"
%}

This is my third thought for you: **long-lasting systems cannot grow without bound; they need weeding.**
It isn't sustainable to grow forever, because eventually you get overwhelmed by the weight of everything that came before.

We need to get better at writing software efficiently, at turning things off that we don't need.

It's a skill we've neglected.
We used to be really good at it -- when computers were the size of the room, programmers could eke out every last bit of performance.
We can't do that any more, but it's so important when building something to last, and I think it's a skill we'll have to re-learn soon.

<figure>
  {%
    picture
    filename="monki-gras/slide19.jpg"
    alt="black-and-white photo of two runners passing a baton between each other in a relay race"
    link_to="https://www.flickr.com/photos/32605636@N06/26774581958/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Val Weaver and Vera Askew running in a relay race, Brisbane, 1939.
    From the <a href="https://www.flickr.com/photos/32605636@N06/26774581958/">State Library of Queensland</a> no known copyright restrictions.
  </figcaption>
</figure>

Weeding is a term that comes from the preservation world, so let's stay there.

When you talk to people who work in digital preservation, we often describe it as a relay race.
There is no permanent digital media, there's no digital parchment or stone tablets -- everything we have today will be unreadable in a few decades.
We're constantly migrating from one format to another, trying to stay ahead of obsolete technology.

Software is also a bit of a relay race -- there is no “write it once and you're done”.
We're constantly upgrading, editing, improving.
And that can be frustrating, but it also means have regular opportunities to learn and improve.
We have that chance to reflect, to do things better.

<figure>
  {%
    picture
    filename="monki-gras/slide20.jpg"
    alt="black-and-white photo of a smashed computer monitor"
    link_to="https://www.flickr.com/photos/binarydreams/9599059/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Broken computer monitor found in the woods.
    By <a href="https://www.flickr.com/photos/binarydreams/9599059/">Jeff Myers</a> on Flickr, used under CC BY-NC 2.0.
  </figcaption>
</figure>

I think we do our best reflections when computers go bust.
When something goes wrong, we spring into action -- we do retrospectives, root cause analysis, we work out what went wrong and how to stop it happening again.
This is a great way to build software that lasts, to make it more resilient.
It's a period of intense reflection -- what went wrong, how do we stop it happening again?

What I've noticed is that the best systems are doing this sort of reflection all the time -- they aren't waiting for something to go wrong.
They know that prevention is better than cure, and they embody it.
They give themselves regular time to reflect, to think about what's working and what's not -- and when we do, great stuff can happen.

<figure>
  {%
    picture
    filename="monki-gras/slide21.jpg"
    alt="black-and-white photo a statue of a woman using a typewriter"
    link_to="https://www.flickr.com/photos/photobey/30099105474/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Statue of Astrid Lindgren.
    By <a href="https://www.flickr.com/photos/photobey/30099105474/">Tobias Barz</a> on Flickr, used under CC BY-ND 2.0.
  </figcaption>
</figure>

I want to give you one more example.
As a sidebar to my day job, I've been writing a blog for thirteen years.
It's the longest job -- asterisk -- I've ever had.
The indie web is still cool!

A lot of what I write, especially when I was starting, was sharing bits of code.
“Here's something I wrote, here's what it does, here's how it works and why it's cool.”
Writing about my code has been an incredible learning experience.

You might know have heard the saying “ask a developer to review 5 lines of code, she'll find 5 issues, ask her to review 500 lines and she'll say it looks good”.
When I sit back and deeply read and explain short snippets of my code, I see how to do things better.
I get better at programming.
Writing this blog has single-handedly had the biggest impact on my skill as a programmer.

<figure>
  {%
    picture
    filename="monki-gras/slide22.jpg"
    alt="black-and-white photo a statue of a sunset reflected in a sea"
    link_to="https://www.flickr.com/photos/8623220@N02/3174207141/"
    class="dark_aware"
    width="450"
  %}
  <figcaption>
    Photo: Midnight sun in Advent Bay, Spitzbergen, Norway.
    From the <a href="https://www.flickr.com/photos/8623220@N02/3174207141/">Library of Congress</a>, no known copyright restrictions.
  </figcaption>
</figure>

There are so many ways to reflect on our work, opportunities to look back and ask how we can do better -- but we have to make the most of them.
I think we are, in some ways, very lucky that our work isn't set in stone, that we do keep doing the same thing, that we have the opportunity to do better.

Writing this talk has been, in some sense, a reflection on the first decade of my career, and it's made me think about what I want the next decade to look like.

In this talk, I've tried to distill some of those things, tried to give you some of the ideas that I want to keep, that I think will help my career and my software to last.

Be careful about what you create, what you keep, and how you interact with other people.
That care, that process of reflection -- that is what creates things that last.
