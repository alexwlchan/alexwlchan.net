---
layout: post
date: 2022-06-03 12:29:46 +00:00
title: Redesigning my archive pages
summary: Using coloured cards with images and descriptions to make it easier to find posts in my back catalogue.
tags:
  - blogging about blogging
colors:
  index_light: "#22201f"
  index_dark:  "#fbfafa"
index:
  exclude: true
---

Last night, I updated the archive pages for my blog.
On Twitter I teased it as a ["design refresh"][tease] but it might be more accurate to call it a "first design" -- the scrolling list of text links I had previously barely counts as a design.

[tease]: https://twitter.com/alexwlchan/status/1532029536258465795

If you click [the "posts" link in the header](/articles/), you'll see something quite different to yesterday:

<style>
  img {
    border: 3px solid #f0f0f0;
    border-radius: 8px;
  }

  figure {
    width: 90%;
  }

  figure.two_up {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: 1em;
  }

  @media screen and (max-width: 600px) {
    figure {
      width: 100%;
    }
  }

  @media screen and (max-width: 450px) {
    figure.two_up {
      grid-template-columns: auto;
    }
  }
</style>

<figure class="two_up">
  {%
    picture
    filename="all_posts_old.jpg"
    alt="A page titled 'All posts' with a list of red text links."
    width="675"
  %}
  {%
    picture
    filename="all_posts_new.jpg"
    alt="A page titled 'Posts' with various coloured tiles. Each tile has a small graphic, a post title, then a one-sentence description."
    width="675"
  %}
</figure>

I've wanted to redesign that page for a while, but I kept putting it off because it seemed hard -- once I started, it was much easier than I was expecting.



## The problem of past posts

Most people find my site from search or via word-of-mouth.
I think I'm doing pretty well for search -- a lot of my posts are about solving specific problems, and if you search for that specific problem, my posts are near the top of the results.
I have clear titles, relevant content, and my pages load quickly.
Search engines can easily find their way around my blog.
But people?
Less so.

Every so often, somebody asks for a link to my blog, and I'm vaguely embarrassed to give it to them.
It's not because I'm ashamed of the blog -- indeed, I think some of my best work is here -- it's because I know new readers don't have a good experience.
**Given only a list of text links, it was hard for anyone to find something they'd want to read.**

This especially stood out when the person asking wasn't a programmer.
They'd quickly assume it's a programming blog, and that they weren't "smart enough" to read it (yes, I've heard those exact words).
There are lots of programming posts -- but there are plenty of non-programming posts too!
They're just very difficult to find.

(The long list of links is useful for me -- but I have a unique knowledge of my back catalogue.
When I use it, I know exactly what I'm looking for.
That list is [still there](/articles/), but now it's buried a lot deeper because it's not a good starting point.)

A while back, I started marking my favourite posts in the list of links.
This was a half-hearted measure to improve discoverability, but clicking it only took you to a shorter list of text links.
I'm also not sure anybody ever realised those hearts were clickable.

{%
  picture
  filename="hearted_posts.png"
  alt="A list of text links, with small red hearts next to several of the titles."
  width="600"
%}

This is the kernel of a good idea -- I have over 300 posts, and it's unreasonable to expect anybody to choose from that many.
Giving people a shorter list of "best" posts to choose from makes that easier, but it was still difficult to choose from that list of 40-odd posts when you only had the title.

I knew this wasn't good enough, but I was struggling for ideas.

I thought about writing some sort of "start here" page for the site -- a blog post that linked to other blog posts -- but that's just replacing one wall of text with another.
I also kept putting off writing it, which doesn't bode well for anybody wanting to read it.

I also thought about new tags and categories, but that's still fiddling around the edges.
I already have tags, but they're hard to find.
I wanted a more radical change.

Then after work yesterday, I had a brainwave -- what if I used cards instead of links?
This is a pretty common design pattern on the web; here are two examples from [the Wellcome Collection website][stories] and [my book tracker][books]:

[stories]: https://wellcomecollection.org/stories/
[books]: https://books.alexwlchan.net/

<figure class="two_up">
  {%
    picture
    filename="wellcome_collection_cards.jpg"
    alt="Six cards arranged in a two-by-three grid. Each card links to a single article. Each card has a photograph or illustration, a title in a large font, and a description in smaller text. The cards have a uniform cream background."
    width="675"
  %}
  {%
    picture
    filename="books_cards.jpg"
    alt="Four cards arranged in a single column. Each card links to a book. Each card has the title of the book, the author and when I read it, the book's cover. The cards are tinted to match the book covers, e.g. the first card is green to match the book cover."
    width="675"
  %}
</figure>

These are much better than a wall of text!
The picture and description give more context about why somebody might want to read a given post, and they're much more visually interesting.
Ever since I made those cards for my book tracker, I've been jealous of how much better it looks than my main site, but I never thought to apply it here -- until yesterday.

I grabbed my laptop, and started playing around.
I quickly came up with something I liked, and which matches the style of the site:

<figure>
  {%
    picture
    filename="alexwlchan_cards.jpg"
    alt="A scrolling grid of cards, one per post. Each card has a coloured border, a picture, then a title in the same colour as the border. There's smaller text below the title that describes the post."
    width="675"
  %}
</figure>

The "posts" link in the header now goes to this list of cards, and it's only my favourite posts.
Your first impression of the blog is now these rich, colourful cards -- not a monotonous list of text links.
It's a smaller list of posts to read, and there's more information to help you choose where to go next.

{% update date="2022-06-20" %}
  I disliked this almost immediately, and I rolled it back.
  The "posts" link now goes to the "all posts" page, but the "best of" cards are more prominent, and there's a clear instruction at the top of the page directing new readers to the list of favourites.
{% endupdate %}

I had a lot of fun creating the graphics -- some of them are images I already had for social media cards, others are new for this page.
There's a mixture of photography, coloured icons, and diagrams, then I'm using [dominant_colours] to extract a tint colour for the border.
(I thought I might need some abstract art or placeholder patterns to fill in the gaps, but I got a picture for everything.)

<!-- The cards are laid out using [CSS Grid][grid], which I learnt while writing [a previous blog post][layout]. -->

At time of writing, there are 35 cards.
It's still quite a few, but substantially fewer than the "all posts" page -- and you're more likely to find something you're interested in.

[dominant_colours]: https://github.com/alexwlchan/dominant_colours
[grid]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout
[layout]: /2022/supposedly-simple-image-layout/



## Honing the homepage

As part of this design refresh, I've also updated the homepage.
A few years ago, I added a list of five recent posts to the homepage, but they were still a mystery list of text links.

I did it because sorting by post date was easy, not because it was a good idea.
Indeed, it might have been a net negative.
Every time I wrote a big post, there was a disincentive to write anything new, because it would push the link to the big post off the homepage.

Now I put in cards for some favourite posts:

<figure class="two_up">
  {%
    picture
    filename="homepage_old.jpg"
    alt="The old homepage, with a list of five links under a heading 'Recent posts'."
    width="675"
  %}
  {%
    picture
    filename="homepage_new.jpg"
    alt="The new homepage, with the list of links replaced by three cards arranged in a row."
    width="675"
  %}
</figure>

I think this is more visually appealing, and more likely to draw somebody into the blog.
It also means longer, in-depth pieces will stick around, and they won't be displaced so quickly.

Currently it's pulling the 3–4 most recent "best of" posts.
I can imagine at some point I might select them by hand, so there's always a  mix of programing and non-programming content, but that's a decision for another day.

Avid readers can still see [subscribe to the RSS feed](/atom.xml) if they want to get everything; this is meant for new readers who've never seen my blog before.



## Designing for vibes

If this was a professional website or a serious source of income, I'd have some analytics or metrics to measure this new design.
Are more people finding old posts?
Are they spending more time on the site?
Have I improved my [bounce rate]?

But this isn't a professional site, it's a hobby project where I write for fun -- and I make design decisions based on *✨&nbsp;vibes&nbsp;✨*.

I don't have any analytics, and I don't know if the redesign will improve my metrics.
I do know it'll make me more comfortable sending people to the blog, and I care about that more.

This was a fun project to work on.
I went from initial prototype to live page in a day and a half (and I spent most of that time sleeping).
I have ideas for more tweaks and changes, but already I think it's a big improvement on what was there before.

<!-- Check out the new archives at [/best-of/](/best-of/). -->
<!-- You might find something you've never read before! -->

[bounce rate]: https://en.wikipedia.org/wiki/Bounce_rate
