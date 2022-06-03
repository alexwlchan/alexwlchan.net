---
layout: post
title: Redesigning my archive pages
summary:
tags:
---

late last night, I pushed an update to archive pages
on twitter i teaed this as a "design refresh", but it would be more accurate to call it "the first design" -- a scrolling list of text links barely counts as design

if you click the posts link in the header, looks radically different

<style>
  img {
    border: 1px solid #f0f0f0;
    border-radius: 5px;
  }

  figure.two_up {
    width: 90%;
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: 1em;
  }
</style>

<figure class="two_up">
  <img src="/images/2022/all_posts_old.png">
  <img src="/images/2022/all_posts_new.png">
</figure>

wanted to do this for a while

from brief flirtatiosn with analytics, know search + word-of-mouth are two big funnels
search is covered, word of motuh isn't

people would ask for a blog link, and I'd be vaguely embarrassed to give it to them
not because i was ashamed of the blog; but knew they couldn't find anything
nearly a decade => over 300 posts
if you don't know something is there, you won't find it

especially as many people asking aren't programmers
they assume the blog isn't for them -- and while there is a lot of prog content, plenty of non-prog in the archive
but how do you find it?

those archives are useful for me -- but I have a unique knoweldeg of my back catalogue
that list is still there for me and anyone else, but it's buried behind several clicks

i've wanted to make the archives more navigable for a while; this is a first pass at something i'll surely refine later

i've known for a while that not posts are equal
in a half-hearted measure, I put little hearts to mark my favourite posts, but this would take you to a shorter list of mystery text links
(and it was another click betweeen you and an archive)

i'd thought about writing some sort of "start here" for the site, with some sentences highlighting good posts -- but that's still a wall of text?

inspired by wellcome collection stories cards

<figure class="two_up">
  <img src="/images/2022/wellcome_collection_cards.png">
  <img src="/images/2022/books_cards.png">
</figure>

much more visually interesting!
picture + text + description

so I went and made cards for my pages, but with my own visual spin:

<img src="/images/2022/alexwlchan_cards.png" style="width: 90%;">

I had a lot of fun creating graphics for the cards -- some of them are images I already had for social media cards, others are new for this project
no consistency -- mixture of photography, line art, and diagrams

(did think I might need some placeholder red patterns or abstract art to fill the gaps, but came up with a picture for everything)

the border colour is pulled using dominant colours

it uses css grid, which i learnt about yay

at time of writing, that has 35 posts
still a lot, but substantially fewer -- and you're more likely to find *something* you're interested in

I've also redone the homepage
I added some recent posts a few years back, but still v mystery
and recency bias

every time I wrote a big post, there was a disincentive to write new stuff, because it'd push the big thing off the front page

now I have cards for the most recent three 'favourites' posts

<figure class="two_up">
  <img src="/images/2022/homepage_old.png">
  <img src="/images/2022/homepage_new.png">
</figure>

i think this is more visually appealing, and more likely to draw somebody into the blog

currently it's pulling the 3-4 most recent "favourites" posts
i can imagine at some point I might select them by hand, so there's alwyas a  mix of prog and non-prog content

also shows difference between profesh/personal site

if this was a profesh website/source of income, i'd have some analytics or metrics I was tracking, to see if this was working
but it's a hobby website, and i run it off vibes

i feel more comfortable sending people to the blog, because they're more likely to find something they want to read

it's also one of the nice things about a solo project
i enjoy working on a team, and i learn a lot from different perspectives + expertise, but here i get to just decide to do something and do it
prototype to live site in ~30 hours, most of which spent doing other things

if you want to see the new archives, go to /best-of/
might find somethign you've missed!

