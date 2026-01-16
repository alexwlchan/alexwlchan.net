---
layout: post
date: 2022-04-02 08:44:29 +00:00
title: Checking lots of URLs with curl
summary: A bash script to check the HTTP status code of a bunch of URLs, for simple and portable uptime checking.
tags:
  - shell scripting
  - curl

colors:
  index_light: "#073551"
  index_dark:  "#0ad1d1"
---

I've been rejigging some stuff on the site recently -- moving the hosting, turning off my old web server, updating DNS records -- and I wanted a quick way to check I hadn't broken anything.
To help me out, I wrote a short shell script using [curl] to check a bunch of URLs on the site, and see that they were working correctly.

[curl]: https://curl.se/


## Checking a single URL

This curl command will check a single URL, and print the HTTP status code:

{% code lang="shell" %}
curl \
    --output /dev/null \
    --silent \
    --write-out "%{http_code}" \
    "https://alexwlchan.net"
{% endcode %}

You might also know this as `curl -o /dev/null -s -w "%{http_code}"`, but in scripts or teaching examples I always prefer to use the long version of flag names -- they tend to be more readable, and they're easier to look up if you don't know what they do.

We can capture the printed status code, and check if it's a 200 OK:


{% code lang="shell" names="0:STATUS_CODE" %}
STATUS_CODE=$(curl \
    --output /dev/null \
    --silent \
    --write-out "%{http_code}" \
    "https://alexwlchan.net")

if (( STATUS_CODE == 200 ))
then
  echo "Website is up!"
else
  echo "Website is down!  Expected 200, got $STATUS_CODE"
fi
{% endcode %}

The double brackets are an example of bash's *arithmetic evaluation*.
Normally bash variables are strings, but this forces bash to treat the variables as numbers.
A regular bash comparison would be fine -- `if [[ "$STATUS_CODE" = "200" ]]` -- but I find the arithmetic version a bit easier to read.



## Checking multiple URLs

I started with a text file that defines the URLs I wanted to check.
It's a pretty simple format, with newlines and #-prefixed comments to keep it organised:

```
# Some pages that definitely shouldn't break!
/
/articles/
/contact/

# A page that doesn't exist, to illustrate what errors look like
/does-not-exist/

# Examples of articles
/2022/02/two-twitter-cards/
/2021/03/inner-outer-strokes-svg/

# This is mounted in a slightly funky way using a Netlify redirect proxy
/ideas-for-inclusive-events/
```

Note that these are URL paths, rather than full URLs -- this is so I could check the same set of URLs against the live site, a local build, or a staging site like a [Netlify Deploy Preview].

[Netlify Deploy Preview]: https://docs.netlify.com/site-deploys/deploy-previews/

This is what the shell script looks like:

{% code lang="bash" names="0:BASE_URL 3:ERRORS 4:path 6:url 11:STATUS_CODE" %}
BASE_URL="${BASE_URL:-https://alexwlchan.net}"

ERRORS=0

for path in $(grep ^/ paths_to_check.txt)
do
  url="$BASE_URL$path"
  echo -n "Checking $url... "

  STATUS_CODE=$(curl \
      --output /dev/null \
      --silent \
      --write-out "%{http_code}" \
      "$url")

  if (( STATUS_CODE == 200 ))
  then
    echo "$STATUS_CODE"
  else
    echo -e "\033[0;31m$STATUS_CODE !!!\033[m"
    ERRORS=$(( ERRORS + 1 ))
  fi
done

if (( ERRORS != 0 ))
then
  echo -e "\033[0;31m!!! Errors checking URLs!\033[m"
  exit 1
fi
```
{% endcode %}
First I'm setting the base URL which will be prepended to the paths.
The `${BASE_URL:-https://alexwlchan.net}` sets a default value using shell [parameter expansion].
If I set a `BASE_URL` environment variable, that will be prepended to all the paths; if I don't, it uses the URL of my live site as a default value.

The `grep ^/` looks for lines that start with a `/`, which filters out empty lines and comments.

The `echo -n` prints the URL without a newline.
This means that when we print the status code further down in the script, the status code appears on the same line as the URL.
This is what the output looks like:

<pre><code>Checking https://alexwlchan.net/... 200
Checking https://alexwlchan.net/articles/... 200
Checking https://alexwlchan.net/contact/... 200
Checking https://alexwlchan.net/does-not-exist/... <span style="color: var(--red);">404 !!!</span>
</code></pre>

I'm printing the URL before I call curl, so that if something goes wrong I can easily see what URL was being checked at the time -- rather than guessing about what I think curl was checking.

If the status code is bad, it prints a warning for that URL and uses arithmetic expansion to increment the `ERRORS` variable.
The `\033[0;31m…\033[m` is using ANSI escape codes to print red text in my terminal, and those escape codes are enabled with `echo -e`.

In an earlier version of this script, I had it fail as soon as it found a broken URL.
I changed this to count errors in `ERRORS` so I could see every URL that was failing, rather than just the first.

[parameter expansion]: https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html



## Why curl?

There are lots of ways you could solve this problem, so why did I pick bash and curl?

I picked them because I already had them both installed, and they're installed on a *lot* of systems.
Whether it's a family member's computer or a fresh EC2 instance, I like to work with the built-in tools as much as I can.
It means I can get started immediately, and I don't have to worry about breaking somebody else's system.
If I log on to a random computer in 2022, I can be fairly sure bash and curl will be available.

My own computer is heavily customised and has a lot of extra tools installed, but I think the ability to log into a random system and do useful work is a valuable skill.
Writing this script was a good opportunity to practice.
