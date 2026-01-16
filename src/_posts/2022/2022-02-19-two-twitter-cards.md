---
layout: post
date: 2022-02-19 12:45:19 +00:00
title: A tale of two Twitter cards
summary: Some recent changes I've made to fix or improve my Twitter cards.
tags:
  - twitter
  - blogging about blogging
colors:
  index_light: "#1d9bf0"
  index_dark:  "#77c8fe"
---

<style type="x-text/scss">
  #card_comparison {
    width: 700px;

    #images {
      display: grid;
      grid-template-columns: auto auto;
      grid-gap: var(--grid-gap);

      img {
        display: inline-block;
      }
    }
  }
</style>

If I had a penny for every site where I've fixed Twitter cards in the last week, I'd have two pennies.
Which isn't a lot, but it's weird that it happened twice.

Twitter [Cards] are the rich previews of URLs shown on tweets -- like a title, a description, or an image -- rather than just a bare link.
You add some meta tags to your page, and Twitter adds a card to the tweet.
But although Twitter provide instructions and [a validator], their behaviour can be confusing.
It's not always obvious why a card isn't working.

This post explains what I've been doing to fix my Twitter cards, and what I'm doing to prevent similar issues in future.
Hopefully these notes are useful to somebody else trying to debug their own Twitter cards, or quite probably my future self.

[Cards]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
[a validator]: https://cards-dev.twitter.com/validator

---

## Provide your own crops for images

One type of Twitter card is the [summary with large image][large_image], which displays a large image alongside your link.
These cards display images with a 2:1 aspect ratio, and if your image is a different aspect ratio, it gets cropped to fit.

If you let Twitter pick the crop, they pick a 2:1 rectangle from the middle of the image.
They used to use machine learning to pick the "interesting" part of the image, but apparently [it got phased out][phased_out] after accusations of bias.
This can give some unfortunate results:

<style type="x-text/scss">
  #card_comparison {
    width: 700px;

    #images {
      display: grid;
      grid-template-columns: auto auto;
      grid-gap: var(--grid-gap);

      img {
        display: inline-block;
      }
    }
  }
</style>

<figure id="card_comparison">
  <div id="images">
    {%
      picture
      filename="twitter_card_bad_crop.png"
      alt="A screenshot of a tweet linking to an article, in which the card image shows a woman's chest and the bottom half of her face."
      width="350"
    %}
    {%
      picture
      filename="twitter_card_good_crop.png"
      alt="A screenshot of the same tweet, but now the card is focused on the woman's face and shoulders."
      width="350"
    %}
  </div>
  <figcaption>
    A <a href="https://twitter.com/ExploreWellcome/status/1491038905923215361">tweet from Wellcome Collection</a>, before and after my change.
    It links to <a href="https://wellcomecollection.org/articles/Yd8L-hAAAIAWFxqa">an article</a> about women&rsquo;s experiences with autism.
  </figcaption>
</figure>

The card on the left is using a square image which was cropped by Twitter, so half of Lauren's face is cut off.
The card on the right is using a rectangular image which was cropped by a person, and now the face is visible.
The Wellcome Collection editorial team create several crops of every image, so we can use different sizes of image in different places -- we had to change our card to use the 2:1 crop, not the square crop.

This is an extreme example, but it proves a general point: crop your card images yourself, don't let Twitter crop them for you.

[large_image]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image
[phased_out]: https://www.theverge.com/2021/5/19/22444372/twitter-image-crop-racial-gender-bias-research

---

## Use ngrok to test your cards without caching

Twitter cards on my blog have been broken for a long time, and I wasn't sure why.
In particular, cards would display, but they didn't have any images attached:

{%
  picture
  filename="twitter_card_no_image.png"
  alt="Screenshot of a tweet from me, where the card image is showing a generic grey icon."
  width="350"
%}

I started by running my pages through the [Twitter Card Validator][validator].
It's a useful tool for testing cards -- you give it a URL, and it shows you what the card for that page would look like.
Unfortunately, it didn't give me any helpful errors -- it just showed me the card, sans image.

Reading [Twitter's troubleshooting documentation][troubleshooting], I wondered if it was a silent error in my meta tags, or maybe something in my `robots.txt` was blocking Twitter's crawler.
Could I rule those out?
Something from work gave me an idea to do just that.

We use a tool called [ngrok] to expose locally running web apps on the Internet.
It's useful when you want to share your work quickly: you spin up a local web server, then tell ngrok you want to publish that port.
ngrok gives you a publicly visible URL, which tunnels to your local web server, and you can send that to somebody in Slack.
When they click the URL, they connect to your local server.


{%
  picture
  filename="ngrok_screenshot.png"
  alt="Screenshot of my terminal running ngrok. It shows some information about my account, an eu.ngrok.io URL where I can access my web server, and a list of HTTP requests it's received."
  width="426"
%}

I ran my blog on a local web server, shared it through ngrok, put the public ngrok URL in the Twitter card validator… and the card worked perfectly.

This was a big discovery: I could rule out a lot of possible mistakes.
My meta tags are correct and my `robots.txt` isn't blocking Twitter's crawler, so something else is.

Because you get a different URL every time you run ngrok, it bypasses a lot of Twitter's caching.
I've had issues in the past -- even with the validator -- where I change the markup on the page, but Twitter fetches a cached version of the card, and displays the wrong thing.
I can imagine using this to test other changes to cards in the future.

[validator]: https://cards-dev.twitter.com/validator
[troubleshooting]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/troubleshooting-cards#validator
[ngrok]: https://ngrok.com/

---

## Make sure your card images are served quickly

If my page markup is correct, then Twitter is struggling to get to the page.
That points to the nginx server that hosts my blog as the culprit.
I was confused at first, because I run multiple websites from the same server, and only some of the pages were having Twitter card issues.

Then I had a glance at my server logs, which showed me the issue:

```
[17/Feb/2022:13:37:18] "GET /2022/02/safari-tabs/ HTTP/1.1" 200 5790 "-" "Twitterbot/1.0" "-"
[17/Feb/2022:13:37:19] "GET /images/profile_red.jpg HTTP/1.1" 200 31857 "-" "Twitterbot/1.0" "-"

[17/Feb/2022:13:23:58] "GET /2021/10/redacting-pdfs/ HTTP/1.1" 200 4260 "-" "Twitterbot/1.0" "-"
[17/Feb/2022:13:24:06] "GET /images/2021/redaction_cover_image.png HTTP/1.1" 200 196331 "-" "Twitterbot/1.0" "-"
```

For the first page, Twitterbot fetches the image within a second, and the card works.
For the second page, it takes about eight seconds to fetch a larger image, and the card doesn't work.
Wherever Twitterbot is located, it's taking too long to fetch the image -- and so it's not showing it in the card.

I don't know why nginx is so slow -- the second image is only a few hundred kilobytes, still small by modern web standards.
I could spend time fine-tuning my nginx config, but I don't know much about it and in 2022 it's harder and harder to justify running my own web servers.

I took this as the push to migrate my blog to [Netlify] instead.
(My web host [getting acquired][akamai] this week helped with that decision.)
It's much faster, and now Twitterbot is happy with my cards.

[Netlify]: https://www.netlify.com
[akamai]: https://www.linode.com/blog/linode/linode-and-akamai/

---

## A Jekyll plugin to keep my cards correct

I use Jekyll to build my blog, which generates static HTML files.
Before I publish changes, I always run an HTML linter, which looks for invalid markup, broken links, missing alt text, and so on.

To help me create good Twitter cards, I've added a new linter rule.
It warns me if my card image is missing, or if a large image doesn't have a 2:1 aspect ratio:

```
- _posts/2017/2017-06-07-crossness-pumping-station.md
  *  Twitter card points to a missing image
- _posts/2019/2019-11-27-my-scanning-setup.md
  *  summary_large_image Twitter card does not have a 2:1 aspect ratio
```

This rule is part of my [linting plugin][linter].
It's not published as a gem, but if you'd find it useful you can copy/paste it into your own project.

[linter]: https://github.com/alexwlchan/alexwlchan.net/blob/d681a85fd227177feff5c2d9c14e25c13a14d5b0/src/_plugins/linter.rb#L73-L170
