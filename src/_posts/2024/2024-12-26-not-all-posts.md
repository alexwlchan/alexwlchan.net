---
layout: post
date: 2024-12-26 09:54:55 +0000
title: Not all blog posts are created equal
summary: Splitting my site into "articles" and "today I learned" helped me overcome writer's block and improve my writing.
is_featured: true
colors:
  css_light: "#7b4ac8"
  css_dark:  "#bd94ff"
tags:
  - blogging about blogging
---
{% comment %}
  Card image from https://pixabay.com/photos/bluebell-green-grass-purple-flower-5095581/
{% endcomment %}

For a while now, this website has been my own personal writer's block.
I was struggling to write, even when I had good ideas; if I wrote something I liked, I was often reluctant to publish it; if somebody asked to read the site, I'd wince before giving them the link.
Something was wrong, but I couldn't put my finger on it.

At the start of this year, I finally had a breakthrough: I split my writing into two distinct categories.
"Articles" and "Today I Learned" are more than just links in my header -- they became permission to write differently.
I no longer takes a "one size fits all" approach to my writing, and instead I let different posts have different strengths.
It's made my writing better, and I'm doing more of it.
(I've published as many posts in 2024 as in the prior three years *combined*.)
This is accompanied by some visual improvements, which let me showcase my personal favourites.

I waited to write about this, because I wanted to be sure these changes weren't just a temporary fix.
Now the year is over, I can call it a success.
Let's go through what's new.

{% table_of_contents %}

---

## What do I write?

After twelve years of writing this site, I've noticed something interesting: my posts fall pretty neatly into two categories.
This wasn't a deliberate choice -- it's just emerged from the things I wanted to write.

### The first category is the problem-solvers

These are usually about programming, written when I figure something out and want to remember it for later.
They're notes to my future self, and I publish them online so other people can benefit.
I've read a lot of this sort of post written by other people, and publishing my own is a way of giving back.
If you're struggling with the same problem, these posts are golden -- and if not, you'll scroll right past.

These posts are easy to write -- they have a clear purpose and a captive audience.
If I give them a specific title, they're easy to find, and they get a lot of traffic from search engines.

### The second category is the reflections

These posts aren't about solving technical problems -- they're about exploring ideas and sharing experiences.
When I write about [Digital decluttering], [Mountaintop moments], or [Hyperfocus and hobbies], I'm trying to capture something more universal, something that isn't just for programmers.

This is some of my favourite writing, and it's where I think new readers should start.
They're much harder to write, because I don't have the easy hook of "here's your solution to keep you reading" -- but I think the extra time and effort is reflected in the quality of the final piece.

These articles aren't as popular, but I'm more proud of them.
Nobody has ever had an emotional breakthrough reading about command line arguments or Python function minutiae, but when I write about gender, or mental health, or the human experience?
Those are the posts that resonate.

[Digital decluttering]: /2024/digital-decluttering/
[Hyperfocus and hobbies]: https://wellcomecollection.org/articles/ZRrH3RIAACIAALP5

---

## What was I doing wrong?

My big mistake was trying to ignore this natural split.
This caused several problems.

### I forced unnecessary reflections into problem-solving posts

I tried to find a deeper meaning in every technical solution -- a universal truth that would appeal to readers who didn't care about the original problem.
But was this actually helping anyone?

If you have the problem and you're looking for an answer, you'll skip over my philosophical musings, just like you skip the backstory in an online recipe.
And if you don't have the problem, are you really going to read a post that's about solving that exact problem?

Lots of problem-solving posts never made it out of my drafts folder, because I couldn't find that "deeper meaning".
I was chasing an imaginary reader who wanted philosophy with their bug fixes, and letting perfectly good writing go to waste.

### I rushed my reflective pieces

Since I could write problem-solving posts quickly, I beat myself up when reflections took longer.
*"You finished that coding post in an hour, so why is this taking days?"*
It makes sense that reflections need more time -- they're more complex and nuanced, and they don't have the natural structure of a step-by-step list for solving a problem -- but I wasn't giving myself the space to do that work.

This pressure to publish quickly was self-imposed.
Nobody else was waiting, but I felt like I was taking too long.

Looking back, I can see posts that could have been improved if I'd given myself more time.

### Good reflections became roadblocks

Like many blogs, my homepage had a list of my most recent posts, and the newest post would get top billing.
After publishing something I was proud of, I didn't want to knock it off that prime spot.
I'd hold back problem-solving posts with niche appeal, because I didn't want them to displace something more meaningful.

This is completely backwards: success was making me write less, not more.
I wasn't using good feedback as motivation, I was trying to stretch it out for as long as possible.

### New readers got the wrong first impression

I can't count the number of friends who've read the site and said "Oh, it seemed too technical for me".
They came to the homepage during a streak of problem-solving posts, and assume that's all I wrote.
Many of my friends aren't programmers, so the site feels daunting and inaccessible.

I always found this disappointing, and it's why I'd wince before giving somebody the link.
I knew I had writing they'd enjoy, but it was buried by the site's design.
Worse, it left them feeling like they "weren't smart enough" to read my writing.

I want this site to be something that I'm proud to share, not something I'm embarrassed to mention.

---

## What have I changed?

The most important change is simple but powerful: I stopped ignoring the split in my writing.
I gave myself permission to write different types of post differently, and lean into the strengths of each style of writing.

I've also improved the site's design to reflect this distinction.

<style>
  h3 a, h3 a:visited {
    color: var(--tint-color);
  }
</style>

### I've split my writing into two sections: ["articles"][articles] and ["today I learned"][til] (TIL)

This replaces my old approach, which was to have a single stream of posts.
The reflections and longer pieces are articles, while the TIL section is the purest form of problem-solving -- just solutions, no fluff.

I've seen other people who write great TIL blogs (like [Simon Willison] and [Julia Evans]), but I was hesitant to copy this approach -- I wanted to take time to understand how it would work for me.
I've tried to write side blogs in the past, and they always failed because I couldn't decide what posts belonged where.

Now I know exactly what my TIL section is for: it's where I write down solutions, aimed at my future self and for people searching Google.
These posts are for people who arrive from a search, find what they need, and leave -- not for long-term fans of me or my writing.

This clarity means I can write TILs very quickly, and now I feel comfortable taking more time to work on my reflective writing.
This article was in draft for over two months -- it took me a long time to find a flow and structure that I liked, and it's improved so much from my first outline.

[articles]: /articles/
[til]: /til/
[Simon Willison]: https://simonwillison.net/2020/Apr/20/self-rewriting-readme/
[Julia Evans]: https://jvns.ca/blog/2024/11/09/new-microblog/

### I've rethought how my writing is organised: topics, not dates

I was organising by date because that's the default in my blogging software, but that's not a good fit for my writing.
Chronological ordering makes sense for journals or news sites, but nothing I write is that sort of time-sensitive.
(For more on this, I recommend Amy Hoy's article [How the blog broke the web][hoy].)

I still have dates on individual posts, but they're not the main way you browse the site.
Instead, I've created a new top-level page which is [a complete tag index][tags], and you can find the articles and TILs for each tag:

<style>
  #tag_screenshots {
    display: grid;
    grid-template-columns: 597fr 1678fr;
    grid-gap: var(--grid-gap);
  }

  #tag_screenshots picture:nth-child(1) img {
    border-top-right-radius:    0;
    border-bottom-right-radius: 0;
  }

  #tag_screenshots picture:nth-child(2) img {
    border-top-left-radius:    0;
    border-bottom-left-radius: 0;
  }
</style>

<figure class="wide_img">
  <div id="tag_screenshots">
    {%
      picture
      filename="list_of_tags.png"
      width="260"
      class="screenshot"
      alt="A page titled ‘tags’ with a list of tags. Each tag is a text link, and the number of posts is shown in parentheses after the link, for example “aws (45)”."
      style="object-fit: cover; height: 100% !important;"
    %}
    {%
      picture
      filename="tagged_with_rust.png"
      width="700"
      class="screenshot"
      alt="A page showing my posts tagged with “rust”. At the top of the page is a title and two article cards for my favourite Rust articles, and below that is a list of links -- the article title, and a short description."
      style="object-fit: cover; height: 100% !important;"
    %}
  </div>
</figure>

This matches how I read other people's sites -- I find the list of topics, open tabs for topics I care about, and then start reading.
I never look to see what somebody wrote on a specific date.

I've also added a list of my most-used tags to my homepage, giving you a quick overview of what I write about.
There's plenty of programming, but you can see the non-programming topics as well:

{%
  picture
  filename="homepage_tags.png"
  width="750"
  class="screenshot"
  alt="A paragraph titled “Here are some of the topics I write about” followed by a list of twenty or so links to key tags like “books”, “digital preservation” and “rust”."
%}

I hope this will help new visitors find something they're excited to read.

[tags]: /tags/
[hoy]: https://stackingthebricks.com/how-blogs-broke-the-web/

### I've made my favourite posts more visible
In the list of articles, these posts get special treatment -- they have a big card and a pretty picture, whereas other posts just get a text link:

<figure style="width: 444px;">
  {%
    picture
    filename="list_of_articles.png"
    width="444"
    style="max-height: calc(100vh - 2em);"
    class="screenshot"
    alt="A list of articles, with two cards at the top, then a list of four text links, then two more cards, then some more text links."
  %}
  <figcaption>
    The list is still roughly in date order, but I’m putting aesthetics above strict ordering.
    The list always starts with a couple of my favourites, and cards get grouped in a way that looks nice, even if that means the list is slightly out of order.
  </figcaption>
</figure>

This draws your eye to the posts I think are most deserving of your attention, and it was inspired by online news sites.
Their homepages aren't a collection of equal-sized links -- major international headlines get more visual weight than a minor local news story.

This is also reflected on the homepage, where I've replaced the list of recent posts with a rotating selection of my favourites:

{%
  picture
  filename="homepage_features.png"
  width="600"
  class="screenshot"
  alt="A snippet of my homepage, titled “Favourite articles” and then a 2×2 grid of cards that link to articles."
%}

Now the homepage is a better showcase of my work for new readers, and I don't have to worry about a quality post getting lost.
When I write something I'm proud of, I can give it the prominence it deserves -- it won't be buried by time.

---

## What's next?

These changes have solved my writer's block, and unlike previous attempts at a fix, this feels like a real improvement, not just a temporary boost.
I've already been writing more this year, and I expect to keep that up in 2025.
I'm also excited to write longer, more ambitious pieces -- like [Mountaintop moments], which was an idea for years before I felt confident enough to write it.

(Writing longer pieces is also why I haven't posted much in November or December.
I've been quietly working on a project that I'll write a lot more about in the new year.)

The web was promised as an infinite canvas, a space where we could build anything and we weren't confined by somebody else's rules or standards.
But in practice, we've ended up with remarkably similar sites.
Even if you escape the walled gardens of corporate social media, most blogs follow the same pattern: a collection of posts, all in one list, all ordered by date.
A lot of the quirkiness and novelty of the early web has vanished.

But this isn't inevitable, and I'm excited by the trend of "digital gardens" that I feel I'm seeing -- people trying new ways to organise their content, and resisting the siren call of the chronological timeline.
So many people are trying fun and cool ideas with their personal websites, and these changes are my pebble on that pile.

For the first time in too long, I'm excited to write this site and tell other people about it.

[Mountaintop moments]: /2024/mountaintop-moments/
