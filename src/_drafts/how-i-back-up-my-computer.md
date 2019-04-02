---
layout: post
title: How I back up my computing devices, 2019 edition
summary:
tags:
---

About a fortnight ago, there was lots of news coverage about [Myspace losing 12 years of uploaded music][myspace].
I never had a Myspace account, so I didn't lose anything on this occasion, but it was a prompt to think about how I back up my computing devices.

A lot of my work and documents only exist on a computer.
That includes most of my personal photographs, all my code and prose, and many of the letters I receive (physical copies of which get scanned and shredded).
It's scary to imagine losing any of that data, so I have a number of systems to keep it backed up and secure.

In this post, I'm going to outline my current backup process.

[myspace]: https://arstechnica.com/information-technology/2019/03/myspace-apparently-lost-12-years-worth-of-music-and-almost-no-one-noticed/

## Requirements

These are the things I think make a good backup system:

*   *Redundancy.*
    If there's a file I care about, I should have at least two copies, ideally three.
    Two is one, one is none.

*   *No single points of failure.*
    I want to spread my copies around, so it's very difficult for them all to be deleted at once.
    That includes:

    -   Buying hard drives from different batches (to avoid a defect in a single batch)
    -   Offsite backups (so my house burning down wouldn't destroy all my backups)
    -   Using different software for different backups (so a bug in one product isn't catastrophic)

*   *Fast recovery.*
    My day job involves using a computer.
    If I have to wait hours or days to recover from a disk failure, that affects my ability to do my job.

*   *Automated backups.*
    If I have to remember to do something, it won't happen very often.
    If I can get the computer to perform my backups automatically, they'll be more reliable and I'll have more up-to-date backups.



## My devices

I have three devices that have important data:

*   An always-on iMac, which is my main computer at home
*   A MacBook which I use when I'm away from home
*   An iPhone

I also have a work laptop, but I let IT manage its backups.
It has less data that I personally care about, and corporate IT policies tend to frown upon people making unauthorised copies of company data.

I also have a lot of data tied up in online accounts (Twitter, Dreamwidth, Tumblr, and so on), and I try to keep separate copies of that.
How I back up that data is a subject for a separate post.



## My setup

Because my iPhone and my laptop are both portable devices, and I take them out of the house regularly, I assume I could lose or break them at any time.
(Many years ago, I lost my first two phones in quick succession.)
I try not to keep important files on them for long, and instead copy the files to my iMac -- where they get backed up in multiple ways.

Here's what I do to secure my files:

### Full-disk encryption

My scanned documents have a lot of personal information, including my bank details, home address, and healthcare records.
I don't want that to be readily available if my phone or laptop get stolen, so I do full-disk encryption on both of them.

On my iMac and MacBook, I've turned on [FileVault encryption][filevault].
On my iPhone, I'm using the encryption provided by iOS.

[filevault]: https://en.wikipedia.org/wiki/FileVault

### iCloud Photo Stream and iCloud Backups

Any photos I take on my iPhone are automatically uploaded to iCloud Photo Stream, and I have an iCloud backup of the entire phone.
My iMac downloads the original, full-resolution file for every photo I store in Photo Stream, so I'm not relying on Apple's servers.
Because the iMac is always running, I get an extra copy very quickly.

When I'm using a camera with an SD card, I transfer photos off the SD card to my phone, and upload those to iCloud Photo Stream as well.

I'm paying for a 200GB iCloud storage plan (£2.49/month), which is easily enough for my needs.

### File sync with Dropbox and GitHub

When I'm actively working on something, I keep the relevant files on GitHub (if it's code) or Dropbox (if it's not).
That's a useful short-term copy of all those files, and keeps them in sync between devices.

### Two full disk clones of my iMac, kept at home

I have a pair of Western Digital hard drives plugged into my iMac, and I use [SuperDuper][superduper] to create bootable clones of its internal drive every 24 hours.
One backup runs in the early morning before I start work, one in the late evening when I'm in bed.

I space out the backups to reduce the average time since the last backup, and to give me more time to spot if SuperDuper is having issues before it affects both drives.

The drives are permanently mounted; ideally I'd only mount them when SuperDuper is creating a clone.

Both these drives are encrypted with FileVault.
They never leave my desk, but it means I don't have to worry about a burglar getting my personal data.

[superduper]: https://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html

### A full disk clone of my iMac, kept at the office

I have a portable bus-powered Seagate hard drive, and SuperDuper creates a bootable clone of my iMac whenever it's plugged in.
This disk usually lives in a drawer at work, thirty miles from home, so if my home and the local drives are destroyed (say, by fire or flood), I still have an easy-to-hand backup.

Once a fortnight, I bring the drive home, plug it into the iMac, and update the clone.

I encrypt this drive so it's not a disaster if I lose it somewhere between home and the office.

Both this and the permanently plugged-in drives are labelled with their initial date of purchase.
Conventional wisdom is that hard drives are reliable for about 3–4 years; the label gives me an idea of whether it's time to replace a particular drive.

### Remote backups with Backblaze

I run [Backblaze][backblaze] to continuously make backups of both my iMac and my MacBook.

This is a last resort.
Restoring my entire disk from Backblaze would be slow or expensive, but it means that even if all my physical drives are destroyed, I have an offsite copy of my data.

But it's handy at other times -- if I'm on my laptop and I realise I need a file that's only on my iMac, I can restore a single file from Backblaze.
It's a good way to shuffle files around in a pinch.

[backblaze]: https://secure.backblaze.com/r/01h8yj



## Keeping it up-to-date

The most recent addition to this setup is the portable iMac clone.

When I was moving house last year, I was moving my iMac and all my backup drives in the same car.
If I'd had an accident, all my backups would disappear at once, and I'd be stuck downloading 600GB of files from Backblaze.
The extra drive was a small cost, but makes it much easier to restore if that worst-case scenario ever happens.

At some point I'll replace the other drives plugged into my iMac -- they're both three years old, and approaching the end of their reliable lives.
The current pair are both desktop hard drives, with dedicated power supplies.
I'll probably replace them with bus-powered, portable drives, to tidy up my desk.

I don't have any local backups of my laptop, and I'm not planning to change that.
The only files I keep on there are things I'm actively working on, which also go in Dropbox and GitHub.

So that's my backup system.
It's not perfect, but I'm happy with it.
My last drive failure was three years ago, and I didn't lose a single file.
I don't lose sleep wondering if a hard drive is about to fail and lose all my data.

If you already have a backup system in place, use the Myspace disaster as a prompt to review it.
Are there gaps?
Single points of failure?
Could it be improved or made more resilient?

And if you don't have a backup system, please get one!
Data loss is miserable, and your hard drive is going to fail -- it's a matter of when, not if.
