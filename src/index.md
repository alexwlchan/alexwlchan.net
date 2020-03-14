---
layout: page
archive_variant: index
---

<style>
  img.profile {
    float: right;
    width: 250px;
    max-width: 50%;
    margin-top: 0.4em;
    margin-left: 1em;
    margin-bottom: 1em;
  }

  .archive__date {
    padding-right: 4px;
  }
</style>

<img src="/images/profile.jpg" class="profile" alt="A picture of a person set against the sky.">

## Hi, I'm Alex.

I'm a software developer at [the Wellcome Trust][wellcome].
I'm helping to build a platform for searching and storing our digital collections.
It's taking Wellcome's assets -- books, archives, images, and more -- and presenting them through consistent, well-designed APIs.

I have a fairly active online presence -- I [tweet a lot](https://twitter.com/alexwlchan), and [my blog](/all-posts/) is a place where I share longer ideas that don't fit into a tweet.
You can read my posts on the web, or subscribe to them [as an RSS feed](/atom.xml).

The blog is a place for me to hone my writing skills, and write about anything I find interesting -- there's plenty of programming, but a lot of other stuff as well.
Past topics include [accessibility](/2019/01/monki-gras-the-curb-cut-effect/), [braille](/2019/07/ten-braille-facts/), [Chinese dictionaries](/2019/06/reading-a-chinese-dictionary/), and [Welsh waterfalls](/2018/11/aberdulais-waterfall/).

Sometimes I give talks at meetups or conferences, and I have a list of slides/videos from [my past talks](/talks/).

I've also written about my [ideas for running inclusive and accessible events](https://alexwlchan.net/ideas-for-inclusive-events/).

I'm trans, genderfluid, and my pronouns vary.
If you don't know me, "they/them" is a safe default.

I hope you enjoy the site.

[wellcome]: https://en.wikipedia.org/wiki/Wellcome_Trust

## Recent posts

{% assign posts = site.posts | homepage_posts %}
{% include archive_list.html %}

## Contact

You can email me at {{ site.emails.personal | create_mailto_link }}, or I'm [@alexwlchan](https://twitter.com/alexwlchan) on Twitter.

For anything related to Wellcome, email {{ site.emails.wellcome | create_mailto_link }}.

If you enjoy what I write, perhaps [say thanks](/say-thanks/)?
