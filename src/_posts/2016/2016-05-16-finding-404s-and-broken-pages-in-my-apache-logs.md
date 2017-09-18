---
date: 2016-05-16 21:02:00 +0000
layout: post
slug: finding-404s-in-apache-logs
summary: A Python script for finding 404 errors in my Apache web logs - and by extension,
  broken pages.
tags: python apache
title: Finding 404s and broken pages in my Apache logs
---

Sometime earlier this year, I broke the Piwik server-side analytics that I'd been using to count hits to the site.
It sat this way for about two months before anybody noticed, which I took as a sign that I didn't actually need them.
I look at them for vanity, nothing more.

Since then, I've been using Python to parse my Apache logs, an idea borrowed [from Dr. Drang][drang].
All I want is a rough view count, and if I work on the raw logs, then I can filter out a lot of noise from things like bots and referrer spam.
High-level tools like Piwik and Google Analytics make it much harder to prune your results.

My Apache logs include a list of all the 404 errors: any time that somebody (or something) has found a missing page.
This is useful information, because it tells me if I've broken something (not unlikely, see above).
Although I try to [have a helpful 404 page][404help], that's no substitute for fixing broken pages.
So I wrote a script that looks for 404 errors in my Apache logs, and prints the most commonly hit pages &ndash; then I can decide whether to fix or ignore them.

The full script is [on GitHub][github], along with some instructions.
Below I'll walk through the part that actually does the hard work.

{% highlight python linenos %}
page_tally = collections.Counter()

for line in sys.stdin:

    # Any line that isn't a 404 request is uninteresting.
    if '404' not in line:
        continue

    # Parse the line, and check it really is a 404 request; otherwise,
    # discard it.  Then get the page the user was trying to reach.
    hit = PATTERN.match(line).groupdict()
    if hit['status'] != '404':
        continue
    page = hit['request'].split()[1]

    # If it's a 404 that I know I'm not going to fix, discard it.
    if page in WONTFIX_404S:
        continue

    # If I fixed the page after this 404 came in, I'm not interested
    # in hearing about it again.
    if page in FIXED_404S:
        time, _ = hit["time"].split()
        date = datetime.strptime(time, "%d/%b/%Y:%H:%M:%S").date()
        if date <= FIXED_404S[page]:
            continue

        # But I definitely want to know about links I thought I'd
        # fixed but which are still broken.
        print('!! ' + page)
        print(line)
        print('')

    # This is a 404 request that we're interested in; go ahead and
    # add it to the counter.
    page_tally[page] += 1

for page, count in page_tally.most_common(25):
    print('%5d\t%s' % (count, page))
{% endhighlight %}

I'm passing the Apache log in to stdin, and looping over the lines.
Each line corresponds to a single hit.

On lines 6&ndash;7, I'm throwing away all the lines that don't contain the string "404".
This might let through a few lines that aren't 404 results &ndash; I'm not too fussed.
This is just a cheap heuristic to avoid (relatively) slow parsing of lots of lines that I don't care about.

On lines 11&ndash;14, I actually parse the line.
My `PATTERN` regex for parsing the Apache log format comes from [Dr. Drang's post][drang].
Now I actually can properly filter for 404 results only, and discard the rest.
The `request` parameter is usually something like `GET /about/ HTTP/1.1` &ndash; a method, a page and an HTTP version.
I only care about the page, so throw away the rest.

Like any public-facing computer, my server is crawled by bots looking for unpatched versions of WordPress and PHP.
They're looking for login pages where they can brute force credentials or exploit known vulnerabilities.
I don't have PHP or WordPress installed, so they show up as 404&nbsp;errors in my logs.

Once I'm happy that I'm not vulnerable to whatever they're trying to exploit, I add those pages to `WONTFIX_404S`.
On lines 17&ndash;18, I ignore any errors from those pages.

The point of writing this script is to find, and fix, broken pages.
Once I've fixed the page, the hits are still in the historical logs, but they're less interesting.
I'd like to know if the page is still broken in future, but I already know that it was broken in the past.

When I fix a page, I add it to `FIXED_404S`, a dictionary in which the keys are pages, and the values are the date on which I think I fixed it.
On lines 22&ndash;32, I throw away any broken pages that I've acknowledged and fixed, if they came in before the fix.
But then I highlight anything that's still broken, because it means my fix didn't work.

Any hit that hasn't been skipped by now is "interesting".
It's a 404'd page that I don't want to ignore, and that I haven't fixed in the past.
I add 1 to the tally of broken pages, and carry on.

I've been using the [Counter class][ctr] from the Python standard library to store my tally.
I could use a regular dictionary, but Counter helps clean up a little boilerplate.
In particular, I don't have to initialise a new key in the tally &ndash; it starts at a default of 0 &ndash; and at the end of the script, I can use the `most_common()` method to see the 404'd pages that are hit most often.
That helps me prioritise what pages I want to fix.

Here's a snippet from the output when I first ran the script:

```
23656    /atom.xml
14161    /robots.txt
 3199    /favicon.ico
 3075    /apple-touch-icon.png
  412    /wp-login.php
  401    /blog/2013/03/pinboard-backups/
```

Most of the actually broken or missing pages were easy to fix.
In ten&nbsp;minutes, I fixed ~90% of the 404 problems that had occurred since I turned on Apache last August.

I don't know how often I'll actually run this script.
I've fixed the most common errors; it'll be a while before I have enough logs to make it worth doing another round of fixes.
But it's useful to have in my back pocket for a rainy day.

[drang]: http://www.leancrew.com/all-this/2013/07/parsing-my-apache-logs/
[github]: https://github.com/alexwlchan/apache-utils
[404help]: /2014/09/404-pages/
[ctr]: https://docs.python.org/3.5/library/collections.html?highlight=collections.counter
