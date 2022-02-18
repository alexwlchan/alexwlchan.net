---
layout: post
title: A tale of two Twitter cards
summary: Some recent changes I've made to fix or improve my Twitter cards.
tags: twitter
theme:
  card_type: summary_large_image
  image: /images/2022/twitter_cards.png
---

If I had a penny for every Twitter card I've fixed in the last week, I'd have two pennies.
Which isn't a lot, but it's weird that it happened twice.

Twitter [Cards] are the rich previews of URLs shown on tweets, like a title, a description, or an image, rather than just a bare link.
You add some meta tags to your page, and Twitter adds a card to the page.
But they're a bit of a mystery box -- although Twitter provide instructions and [a validator], they don't always behave like you'd expect.
Cards work or they don't, and I can't always work out why.

Hopefully these notes are useful to somebody else trying to debug their Twitter cards, or quite probably my future self.

[Cards]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
[a validator]: https://cards-dev.twitter.com/validator



## Provide your own crops for images

One type of Twitter card is the [summary with large image][large_image], which displays a large image alongside your link.
These cards display images with a 2:1 aspect ratio, and if your image is a different aspect ratio, it gets cropped to fit.

I think Twitter is just picking the 2:1 rectangle in the centre of the image.
They used to have a machine learning tool that tried to guess what the "interesting" part of an image was, but apparently [it got phased out][phased_out] after accusations of bias.

However it works, if you let Twitter pick the crop, you can get some suboptimal results:

<figure style="width: calc(80% + 5px)">
  <img src="/images/2022/twitter_card_bad_crop.png" style="width: calc(50% - 10px); display: inline-block; margin-right: 5px;" alt="A screenshot of a tweet linking to an article, in which the card image shows a woman's chest and the bottom half of her face.">
  <img src="/images/2022/twitter_card_good_crop.png" style="width: calc(50% - 10px); display: inline-block; margin-left: 5px; float: right;" alt="A screenshot of the same tweet, but now the card is focused on the woman's face and shoulders.">
  <figcaption>
    A <a href="https://twitter.com/ExploreWellcome/status/1491038905923215361">tweet from Wellcome Collection</a>, before and after my change.
  </figcaption>
</figure>

The card on the left is using a square image which was cropped automatically, so half of Lauren's face is cut off.
The card on the right is using a rectangular image which was cropped by a person, and now the face is visible.
The Wellcome Collection editorial team create several crops of every image, so we can use different sizes of image in different places -- we had to change our card to use the 2:1 crop, not the square crop.

(There's a sad irony that this card was for an article about [how women's experiences of autism are erased][erased], and the automatic crop ended up erasing a Black woman's face.)

This is an extreme example, but it proves a general point: crop your card images yourself; don't let Twitter crop them for you.

[large_image]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image
[phased_out]: https://www.theverge.com/2021/5/19/22444372/twitter-image-crop-racial-gender-bias-research
[erased]: https://wellcomecollection.org/articles/Yd8L-hAAAIAWFxqa



## Use ngrok to test your cards without caching

Twitter cards on my blog have been broken for a while, and I'm not sure why.
In particular, cards would display, but they didn't have any images attached:

<img src="/images/2022/twitter_card_no_image.png" style="width: 40%" alt="Screenshot of a tweet from me, where the card image is showing a generic grey icon.">

I started by running my pages through the [Twitter Card Validator][validator].
It's a useful tool for testing cards -- you give it a URL, and it shows you what the card for that page would look like.
Unfortunately, it didn't give me any helpful errors -- it just showed me the card, sans image.

Reading [Twitter's troubleshooting documentation][troubleshooting], I wondered if it was a silent error in my meta tags, or maybe something in my `robots.txt` was blocking Twitter's crawler.
Could I rule those out?
Something from work gave me an idea to do just that.

We use a tool called [ngrok] to expose locally running web apps on the Internet.
It's useful when you want to share your work quickly: you spin up a local web server, then tell ngrok you want to publish that port.
ngrok gives you a publicly visible URL, which you can send to somebody in Slack.
When they click that URL, they get connected to your local server, with the changes you've just made.

<img src="/images/2022/ngrok_screenshot_2x.png" style="width: 426px;" srcset="/images/2022/ngrok_screenshot_2x.png 2x, /images/2022/ngrok_screenshot_1x.png 1x" alt="Screenshot of my terminal running ngrok. It shows some information about my account, an eu.ngrok.io URL where I can access my web server, and a list of HTTP requests it's received.">

So I ran my blog on a local web server, shared it through ngrok, put the public ngrok URL in the Twitter card validator… and the card worked perfectly.

This was a big discovery: I could rule out a lot of possible mistakes.
My meta tags are correct and my `robots.txt` isn't blocking Twitter's crawler, so something else is.

[validator]: https://cards-dev.twitter.com/validator
[troubleshooting]: https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/troubleshooting-cards#validator
[ngrok]: https://ngrok.com/



## Make sure your card images are served quickly

If my page markup is correct, it points to the nginx server that hosts my blog as the culprit.
That was confusing at first, because I run multiple websites from the same server, and only some of the pages were having Twitter card issues.

I had a glance at my server logs for two different pages, and this seems to show the issue:

```
[17/Feb/2022:13:37:18] "GET /2022/02/safari-tabs/ HTTP/1.1" 200 5790 "-" "Twitterbot/1.0" "-"
[17/Feb/2022:13:37:19] "GET /images/profile_red_square.jpg HTTP/1.1" 200 31857 "-" "Twitterbot/1.0" "-"

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
