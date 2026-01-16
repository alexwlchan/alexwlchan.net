---
layout: post
date: 2022-11-06 10:39:42 +00:00
title: Saving your alt text from Twitter
summary: Twitter's archives don't include the alt text you wrote on images, but you can save a copy with their API.
tags:
  - twitter
  - digital preservation
  - accessibility
colors:
  index_light: "#235f88"
  index_dark:  "#5298c7"
---

<!-- Card from https://wellcomecollection.org/works/yghm43ap/items, public domain -->

It seems like Twitter might be circling a drain, and so a lot of people are [downloading a copy of their archive][download] in case the site goes down unexpectedly.
But large as it is, the archive doesn't contain everything:

{% tweet https://twitter.com/thingskatedid/status/1588790271940395008 %}

And since Twitter's [Accessibility Experience team have just been laid off][a11y], it seems unlikely this omission is going to be fixed any time soon.

This is particularly sad for somebody like Kate, who's put a lot of care and thought into her alt text.
It was as much a part of the tweets as the images themselves, and it would be a shame if it disappeared.
She put out a call for help, and fortunately I had some ideas.

I use a set of Python scripts to maintain an archive of my own tweets.
It's an idea I [originally got from Dr Drang][drang], which I've adapted and tweaked to suit my needs.
My scripts save the complete API response from Twitter, which includes the alt text if you pass the right parameters.

I was able to adapt that code, and write a script to [download all her alt text in a separate file][success].

In case it's useful to anybody else, here's what we did:

1.  Kate gave me a list of tweet IDs with media by looking in her Twitter archive.
    There's a file called `tweets.js`, and she extracted the IDs like so:

    ```shell
    cat tweets.js \
      | sed 's/^window.YTD.tweets.part0 = //' \
      | jq -r '.[] | select(..?|.media_url?) | .tweet.id_str' \
      | sort \
      | uniq
    ```

    Using the list of IDs from the archive is better than using the API to find IDs, because the API [to get your timeline][timeline] is limited to your most recent 3,200 tweets.

2.  I wrote a Python script that uses the v1 API [GET statuses/lookup endpoint][lookup] to walk through these IDs, and fetch the complete API response.

    I had to pass two parameters:

    *   `include_ext_alt_text=true`, which tells the API to include the alt text in the media entity in the API response
    *   `tweet_mode=extended`, which tells the API to include all the media entities

    Only the first parameter is documented, but both seem to be required.
    I believe the notion of "extended" tweets comes from when Twitter increased the character limit from 140 to 280 characters, and didn't want to break clients that expected 140 char strings in the `text` field -- but I might be misremembering.
    It's been in my scripts a very long time.

    You can make 900 requests per 15 minute window, and fetch 100 tweets per request – so you can get 90,000 tweets per window.

3.  I wrote a second script that paged through the API responses, which pulled out just the alt text -- this became the JSON file that I sent to Kate.
    Here's a quick example:

    ```json
    {
      "id": "1561561544265109504",
      "media": [
        {
          "alt_text": "Moomintroll, Snufkin and Little My, all cheering \"Happy Birthday Kate!\" with their hands in the air. Well okay Little My isn't, she is scowling but she is happy inside. They are very dotty - they are drawn with 2 by 4 grids of braille characters, in a number of colours - Moomintroll is white, Snufkin has greens and yellow clothes, with an orange feather in his hat, Little My has orange hair, a red dress and a pink bow. The colour is blocky, because each 2 by 4 braille character can on have one colour of dots. The happy birthday message is rainbow colours. The overall effect of bright coloured dots on a dark background is kind of like the Lights Alive toy from the 80s, where you pressed a tool into a black plastic grid to light up each pixel by opening a mask and letting the light through. Happy birthday!!!",
          "display_url": "pic.twitter.com/bLS5kufmZc",
          "media_url": "https://pbs.twimg.com/media/FavBZtfWAAE9qFg.png"
        }
      ]
    }
    ```

I think those are the key ideas, and here are the Python scripts that I actually ran:

<style>
  .download {
    width: 250px;
  }
</style>

{% download filename="save_tweets_by_id.py" %}
{% download filename="extract_alt_text.py" %}

If you want to do this, you'll need some credentials for the v1 API.
I wrote all my scripts before the v2 API existed, and I've yet to migrate them to the new APIs.
I'm sure you can get alt text for tweets using v2, but I have yet to try it so I don't know how that works.

[timeline]: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
[lookup]: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-lookup
[download]: https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive
[a11y]: https://twitter.com/gerardkcohen/status/1588584459779321857
[drang]: https://www.leancrew.com/all-this/2012/07/archiving-tweets-without-ifttt/
[success]: https://twitter.com/thingskatedid/status/1588980394497822720
