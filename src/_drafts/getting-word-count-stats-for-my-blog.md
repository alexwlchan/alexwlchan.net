---
layout: post
title: Getting word count stats for my blog
category: Blogging about blogging
link: https://alexwlchan.net/stats/
---

For a while I've wanted to see how much I'm writing -- not for anything in particular, just idle curiosity.
Today I decided to sit down and actually plot the data.
I've got a new chart which shows me how many words I've written, on a month-by-month basis:

<img src="/images/2020/word_count_1x.png" srcset="/images/2020/word_count_1x.png 1x, /images/2020/word_count_2x.png 2x, /images/2020/word_count_3x.png 3x" alt="A vertical bar chart with a series of red bars. The vertical axis measures ‘words per month’; the horizontal axis shows time.">

You can see a live version at <https://alexwlchan.net/stats/>, which will automatically update as I write new posts.
(I took the screenshot above before I started this post, so it's already out-of-date.)

This info also tells me that I've written **~197k words** across the entire blog, which is almost as long as *Harry Potter and the Deathly Hallows*.
And while my blog isn't quite as popular, it does have several things to recommend it over JK Rowling's books:

*   There's an explicitly queer character
*   The only snake you'll encounter is a friendly Python, not a deadly Basilisk
*   I don't include [bad facts about trains](https://scifi.stackexchange.com/q/68001/3567)

If you'd like to get something like this for your own blog, the source code is on GitHub:

-   [`word_counter.rb`](https://github.com/alexwlchan/alexwlchan.net/blob/live/src/_plugins/word_counter.rb) is a custom Jekyll plugin that gets the word counts.
    It reads every post, removes blockquotes and code blocks (which I don't count as words I've written), then adds the word count of that post to the running total.

-   I'm using [Charts.js](https://www.chartjs.org/) to render the chart itself.
    You can see the config I'm using in [`stats.md`](https://raw.githubusercontent.com/alexwlchan/alexwlchan.net/live/src/stats.md).
