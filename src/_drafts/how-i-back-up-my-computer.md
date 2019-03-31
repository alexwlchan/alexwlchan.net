---
layout: post
title: How I back up my computing devices, 2019 edition
summary:
tags:
---

About a fortnight ago, there was lots of news coverage about [Myspace losing 12 years of uploaded music][myspace].
I never had a Myspace account, so I didn't lose anything on this occasion, but it was a prompt to think about how I back up my computing devices.

A lot of my work and documents only exist on a computer.
That includes most of my photographs, all my code and prose, and many of the letters I receive (which get scanned and shredded).
It's scary to imagine losing any of that data, so I have several systems to keep it backed up and secure.

In this post, I'm going to outline my current backup process.

[myspace]: https://arstechnica.com/information-technology/2019/03/myspace-apparently-lost-12-years-worth-of-music-and-almost-no-one-noticed/

## Requirements

These are the things I think make a good backup system:

*   *Redundancy.*
    If there's a file I care about, I should have at least two copies, ideally three.

*   *No single points of failure.*
    I want to spread my copies around, so it's very difficult for them all to be deleted at once.
    This includes trying to buy hard drives from different batches (to avoid a defect in a single batch) and having offsite backups (so my house burning down doesn't destroy all my backups).

*   *Fast recovery.*
    My day job involves using a computer.
    If I have to wait hours or days to recover from a disk failure, that affects my ability to do my job.

*   *Automated backups.*
    If I have to remember to do something, it won't happen very often.
    If the computer does it automatically, it's more reliable and I'll have more up-to-date backups.



## My devices

I have three devices that have important data:

*   An always-on iMac, which is my main computer at home
*   A MacBook which I use when I'm away from home
*   An iPhone

I also have a work laptop, but I let IT manage its backups.
It has less data that I personally care about, and corporate IT policies tend to frown upon people making unauthorised copies of company data.

I also have a lot of data tied up in online accounts (Twitter, Dreamwidth, Tumblr, and so on) -- how I back up that data is a subject for a separate post.



## My setup

Because my iPhone and my laptop are both portable devices, and I take them out of the house regularly, I assume I could lose or break them at any time.
(I lost my first two phones in quick succession.)
I try not to keep important files on them for long, and instead copy the files to my iMac -- where they get backed up in multiple ways.

Here's what I do to secure my files:

*   *Full-disk encryption.*
    I've turned on [FileVault encryption][filevault] for my iMac and MacBook, so if they get lost or stolen, nobody can get to my files.

    iOS does automatic encryption of all the data on my iPhone, even if [law enforcement don't like it][ios_encrypt].

[filevault]: https://en.wikipedia.org/wiki/FileVault
[ios_encrypt]: https://www.wired.com/2014/10/golden-key/

-   *iCloud Photo Stream and iCloud Backups.*
    I pay for a 200GB iCloud storage plan, which means that I can upload any photos I take on my phone to iCloud Photo Stream, and I have an iCloud backup of my phone as well.

    My iMac downloads all the photos I store in Photo Stream, so I'm not relying on Apple's servers for a backup copy.

-   *File sync with Dropbox and GitHub.*
    When I'm actively working on something, I keep the relevant files on GitHub (if it's code) or Dropbox (if it's not).
    That's a useful short-term copy of all those files, and keeps them in sync between devices.

-   *Two full disk clones of my iMac, kept at home.*
    I have a pair of Western Digital hard drives plugged into my iMac, and I use [SuperDuper][superduper] to create bootable clones of its internal drive every 24 hours.
    One backup runs in the early morning, one in the late evening.

[superduper]: https://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html

-   *A full disk clone of my iMac, kept at the office.*
    I have a portable bus-powered Seagate hard drive, and SuperDuper creates a bootable clone of my iMac whenever it's plugged in.
    This disk usually lives in a drawer at work, thirty miles from home, so if my home and the local drives are destroyed (say, by fire or flood), I still have an easy-to-hand backup.

    Once a fortnight, I bring the drive home, plug it into the iMac, and update the clone.

    I encrypt this drive so it's not a disaster if I lose it somewhere between home and the office.

    Both this and the permanently plugged-in drives are labelled with their initial date of purchase.
    Conventional wisdom is that hard drives are reliable for about 3–4 years; the label gives me an idea of whether it's time to replace a particular drive.

-   *Remote backups with Backblaze.*
    I run [Backblaze][backblaze] to continuously make backups of both my iMac and my MacBook.

[backblaze]: https://secure.backblaze.com/r/01h8yj

The most recent addition is the portable iMac clone, kept at the office.
I realised that if my home was destroyed (say a fire or a flood), my only recovery option would be to get my files from Backblaze.
That either means doing a 600GB download (slooooow), or they can send you a physical drive with your data.
I'm hoping that a backup at the office will make it slightly easier to recover, if that ever happens.

That's my backup system.
It's not perfect, but I'm happy with it.
I don't lose sleep wondering if a hard drive is about to fail and destroy all my data.

My last drive failure was three years ago, and I didn't lose a single file.
The system is mostly unchanged since then (portable clone aside), so I'm not too worried.
