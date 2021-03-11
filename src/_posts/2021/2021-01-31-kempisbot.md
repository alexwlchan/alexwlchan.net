---
layout: post
date: 2021-01-31 12:25:06 +0000
title: How KempisBot works
summary: How I reincarnated a fifteenth-century monk and taught him to use Twitter.
tags: python twitter
index:
  best_of: true
---

A couple of weeks ago, I got a message from my friend Jay, asking if I'd help him build a Twitter bot to tweet [*The Imitation of Christ*](https://en.wikipedia.org/wiki/The_Imitation_of_Christ) as a long Twitter thread:

<img src="/images/2021/messages_from_jay.png" style="width: 418px;" alt="Screenshot of some Twitter DMs from Jay that read: ‘Alex.... I came up with a stupid idea and even created the account, but I literally have no idea what to do now...? I googled stuff and all the tech words are unintelligble because I do not speak that language’. Do you want to join in this idiotic scheme? I can sort out the text if you can sort out the tech.">

At this point, I'd never heard of *The Imitation of Christ*, or its author Thomas à Kempis, nor did I have any idea of its theological significance.
I'm not religious, but I am ridiculous -- and ridiculous ideas are often the most fun -- so I agreed to help.

Jay has written [his own blog post](https://jayhulme.com/blog/kempisbot) about how he came up with this idea, and why this book is important for Christians.
I recommend reading that if you want to understand the "why" of the project; here I'm going to explain the "how".

The bot posts a snippet from the book once every four hours, and [you can follow it at @KempisBot](https://twitter.com/kempisbot).
It's been running for about a fortnight, and already there are lots of discussions around the tweets.
I'm learning from the theology, and now I want to share some of the "tech magic".

I know plenty of KempisBot's followers aren't software developers, so I'm not going to go into the level of detail I usually do in my programming posts.
The goal of this post is to explain the key ideas I used to write this bot, not provide a detailed walkthrough of the code.

(If you are a developer, you can [download my code](/files/2021/kempisbot.py).)



{% separator "scripture.svg" %}



**The first thing we need is the text -- what should the bot tweet?**

Jay got a translation of the book from Project Gutenberg, and the translation he chose is a shade over 60,000 words (or 330,000 characters).
Seasoned tweeters will know that's more than you can fit in a single tweet, so we need to break the book into tweet-sized pieces.

You could try to do this programatically, but the results probably wouldn't be very good.
In some cases, a sentence works well as a standalone tweet:

{% tweet "https://twitter.com/KempisBot/status/1355552988199325696" %}

In others, it makes more sense to put adjacent sentences together:

{% tweet "https://twitter.com/KempisBot/status/1355611529325015041" %}

It's non-trivial for a computer to even recognise sentences, let alone decide which ones belong in the same tweet.
(This is the topic of an entire field, called [*natural language processing*](https://en.wikipedia.org/wiki/Natural_language_processing).)

Thankfully, Jay had volunteered to "sort out the text", and he went through the book and identified the individual tweets.
I asked him to insert three dashes (`---`) between each tweet, and then send me the finished file.
Here's the beginning of that file, which became the first three tweets:

> ‘The Imitation of Christ’, by Thomas à Kempis
>
> \-\-\-
>
> THE FIRST BOOK: Admonitions Profitable For The Spiritual Life
>
> \-\-\-
>
> CHAPTER I: Of the imitation of Christ, and of contempt of the world and all its vanities

There are lots of ways to store a list of text; I picked this because it made life simple for Jay.
He was able to do this entirely in a Google Doc, without learning any special software or syntax.

Those dashes don't appear anywhere in the real text, so the code that runs the bot can look for them to decide where one tweet stops and the next tweet starts.
It can step through this list, one-by-one, and work its way through the entire book.



{% separator "scripture.svg" %}



**Once we know what we want to tweet, we need to post it on Twitter.**

If you want to post a tweet, you open the Twitter app or the Twitter website, you type some text into a box, and you tap the button labelled "Tweet".
If you do this sequence of actions, Twitter will post your tweet and show it on twitter.com.
These type-and-tap actions are easy for humans, but tricky for computers, so computers have a different sequence of actions they can use to post tweets.

Computer programs can talk to each other by passing special messages.
This is called an *Application Programming Interface*, or *API*.
If a program sends the right sequence of messages, Twitter will post a tweet and show it on twitter.com.

If a program wants to post a tweet, it sends the Twitter API a message saying "please post this text as a new tweet".
Twitter's API will read the message, and reply to say "Yes, I posted that", "No, I didn't", or maybe "I didn't understand what you were saying".
In turn, the program can read the reply, and decide what to do next.

When KempisBot has worked out what part of the book wants to tweet, it sends a message to the Twitter API asking for that to be posted as a tweet.
If the Twitter API replies "Yes, I posted that", it marks that part as done, and prepares to tweet the next part.

I'm grossly oversimplifying, but I hope this gets across the general gist.
Computers can talk to each other by passing around special messages.



{% separator "scripture.svg" %}



**To thread or not to thread: that was never a question.**

We did consider writing the entire book as one, long Twitter thread, but we quickly decided not to.
This book is over 2000 tweets long, and threads that are more than a hundred tweets or so start getting very slow or unresponsive.

When you look at a tweet in a long thread, your computer pre-emptively loads other tweets in the thread.
This means you can scripture to read more of the the thread, and you don't have to keep waiting for new tweets to load.
If there are too many tweets, your computer just grinds to a halt.

But even if it was technologically possible, I'm still not sure we'd have threaded the tweets.
You can read all the tweets by scriptureing through the KempisBot timeline, and part of the appeal is that a lot of the tweets work as standalone thoughts.
They don't need to be threaded to make sense.



{% separator "scripture.svg" %}



**Once we can post a single tweet, we want to post on a schedule.**

I have a computer which is always turned on, and on that computer I run a program called [*cron*](https://en.wikipedia.org/wiki/Cron).
If I tell you the name is from the same root as "chronological" or "chronicle" (albeit [misspelled](https://www.quora.com/What-is-the-etymology-of-cron/answer/Kah-Seng-Tay)), you might be able to guess what it does -- cron is a program for running other programs, and to run them at particular times.
For example, it could run a program every minute, or twice an hour, or at 2pm every Friday.

I have cron set up to run my "post tweet" program every four hours, so six times a day -- the book is 2170 tweets long, and this means the whole book will take 362 days, just shy of a year.

The first few tweets came out quite quickly -- cron is notoriously fiddly to set up, and I made a few mistakes when I was setting up the bot.
Fingers crossed, it's all working now!



{% separator "scripture.svg" %}



This is only one way to build a Twitter bot, and I did it this way because it's very similar to other programs I've written.
There are plenty of other ways you could do something like this, none any better than the other -- it works, and that's good enough.

I hope this post has given you a bit more insight into how a Twitter bot works, especially if you don't know much about programming.
Not everyone is going to be a programmer, and that's fine -- but programming shouldn't be something seen as scary or inaccessible.
Our work is something to be shared and enjoyed, not something to lock away in an ivory tower.

If you'd like to ask me questions, I'm on Twitter at [@alexwlchan](https://twitter.com/alexwlchan).

If you'd like to follow along with the theology, join us at [@KempisBot](https://twitter.com/KempisBot).
