---
date: 2013-03-31 11:13:00 +0000
layout: post
summary: A script for automatically backing up bookmarks from Pinboard
tags: pinboard python
title: Automatic Pinboard backups
---

I've been using [**Pinboard**](http://pinboard.in) to store my bookmarks for nearly two years, and it's a wonderful site.

Before I joined, I kept all of my bookmarks as `.webarchive` files stored in a folder on my computer, with a hideously complicated text document holding all of my comments and tags. Pinboard has been a breath of fresh air: it's fast, simple, handles all of the archiving for me and has generally been very reliable.

Unfortunately, two years had taken their toll on my account, and the whole thing was a bit of a mess. Rather than try to restore some sense of order to an unsustainable tagging and annotation system, I decided to blow all of my bookmarks away, and start from scratch. I've exported all of my old bookmarks, and perhaps I'll add them all back as time allows. Or perhaps not.

When I exported them all, I suddenly realised how fragile my system was. Although I'm sure Pinboard keeps excellent backups, I didn't actually have a local backup of my bookmarks. I'd make a half-hearted visit to the [export page](http://pinboard.in/export/) every so often, but I didn't have it automated. This time round, I wanted to change that. So I wrote my own system for doing Pinboard backups.

<!-- summary -->

Several scripts have already been written to do this (such as [Marcelo Somers](http://behindcompanies.com/2011/12/a-guide-to-backing-up-pinboard/) and [Drew Schuster](http://nuncamind.com/blog/2011/12/31/automatic-pinboard-backup/)). I wrote my own because I wanted one written in a language that I'm familiar with (in this case, Python), and so that it provided exactly what I wanted: saving a copy of the XML&nbsp;file to my local drive.

Also, the scripts I've seen before all use username and password authentication to access the API. But about eight months ago, Pinboard introduced [API authentication tokens](http://blog.pinboard.in/2012/07/api_authentication_tokens/) that mean you don't have to do this. This seems like a better method, so I wanted to use that in my backups.

Finally, I drew inspiration from Dr. Drang's series of posts on [archiving tweets](http://www.leancrew.com/all-this/2012/07/archiving-tweets-without-ifttt/). I use a fork of his [Twitter archiving scripts](http://github.com/drdrang/archive-tweets) to back up my tweets, and my Pinboard script was modelled on the same.

So without further ado, here's the script:

{% highlight python linenos %}
import os
import pytz
from datetime import datetime

import urllib2

# Parameters.
bookmarkdir = os.environ['HOME'] + '/Dropbox/Personal/pinboard/'
pinboard_api = 'https://api.pinboard.in/v1/'
yearfmt = '%Y'
datefmt = '%m-%d'
homeTZ = pytz.timezone('GMT')
y = datetime.now(pytz.utc).strftime(yearfmt)
t = datetime.now(pytz.utc).strftime(datefmt)

# Get the user's authentication token
with open(os.environ['HOME'] + '/.pinboard-credentials') as credentials:
	for line in credentials:
		me, token = line.split(':')

if not os.path.exists(bookmarkdir + y):
	os.makedirs(bookmarkdir + y)

# Set up a new bookmarks file
bookmarkfile = open(bookmarkdir + y + '/pinboard-backup.' + t + '.xml', 'w')

# Get all the posts from Pinboard
u = urllib2.urlopen(pinboard_api + 'posts/all?auth_token=' + me + ':' + token)
bookmarkfile.write(u.read())
bookmarkfile.close()
{% endhighlight %}

The first section defines the parameters for the script: where the bookmarks are stored and the version of the Pinboard API that I'm using. The `datetime` code to get strings of the date are used later to set up the particular structure I wanted for my backups.

The second section gets my username and authentication token, which and stored in a file called `.pinboard-credentials`, that lives in my home directory. This file contains a single line, which is my API token, copied and pasted verbatim from my [Password settings](https://pinboard.in/settings/password) page:

```
alexwlchan:ABCDEFGHIJ1234567890
```

With this structure, there's no reason you couldn't then extend the script to back up multiple accounts (even if I can't think of a scenario where you'd have multiple Pinboard accounts).

Next we set up a directory for the backups. I just have a folder called `pinboard`, and I'll keep a separate folder for each year. These are created by line 22, which looks for the folder for the current year, and creates one if it doesn't already exist. Within that folder, I then name the bookmark files `pinboard-backup.%M-%d.xml`, which matches the structure I use for my IRC logs. I don't think I'll ever be saving a copy of my bookmarks more than once a day.

Finally, lines 30-33 call the Pinboard API, download a copy of all of my posts and save it to the appropriate file. It gets the authentication token which was extracted from `.pinboard-credentials` previously. Each new backup is saved to a new file. Since the files involved are so small, I didn't see the point in throwing away old backups unnecessarily.

Of course, I don't want to run this script by hand, so I used [Lingon](http://www.peterborgapps.com/lingon/) to create a Launch Agent that runs the script once a week, every Sunday morning. My laptop is usually switched on at this time, and if I miss a week, then it's not a great disaster. But this seems regular enough for me.

I also keep both the script and the archive files in Dropbox, so I could always set it to run on a different computer as well, and there shouldn't be any problems (in theory!).

![](/images/2013/pinboard_launchd.jpg)

(The "What" field is slightly truncated in the image; it ends `archive-bookmarks.py`.)

This should continue to run indefinitely and keep a copy of my bookmarks stored on my local drive. Unless I've made a mistake somewhere, I can now use Pinboard without ever having to worry about a backup.

*The script can be downloaded from [my GitHub page](http://github.com/alexwlchan/archive-pinboard).*

{% update 2013-04-01 %}
  Thanks to [Stephen H&#252;gel](https://github.com/urschrei) for tidying up some of the script; his changes have been merged with the repo at GitHub. The basic functionality is unchanged, so most of what I wrote above still stands. The GitHub repo will have the most up-to-date copy of the script.
{% endupdate %}

{% update 2013-04-02 %}
  Andrew Jones has a [much faster way of doing this](http://supersoju.com/blog/2013/04/01/pinboard-backups-in-1-line/), which does everything I did, but in a single line. I'm still glad I did this, because it was a fun morning project and I enjoyed writing it up, but other people might prefer his method.
{% endupdate %}
