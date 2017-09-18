---
date: 2014-08-29 22:06:00 +0000
layout: post
slug: textexpander-amazon-affiliates
tags: textexpander
title: A TextExpander snippet for Amazon affiliate links
---

Earlier this evening, Casey Liss [tweeted a link][tweet] to a post by
Stoyan Stefanov with [a bookmarklet for creating Amazon affiliate
links][book]. It's short, clean and functional. I like it, but it still
needs you to copy and paste the link into your document. I wanted to
cut out that step, by writing a TextExpander snippet that takes the URL of the frontmost browser window, and outputs an Amazon affiliate link.

<!-- summary -->

Stefan's post has a succinct explanation of the four components of an
Amazon affiliate link:

> * `http://www.amazon.com/` - self-explanatory, I think
> * `/dp/` - standing for "details product" or maybe "details page"[^1]
> * `/1847194141/` - a 10 character product code, aka ASIN code, Amazon
    Standard Identification Number
> * `?tag=affiliatecode-20` - your affiliate code, or tag

A typical Amazon link includes all of this information, but also includes
a lot of extraneous junk:

<http://www.amazon.co.uk/Special-Topics-Calamity-Physics-Marisha/dp/0141024321/ref=sr_1_1?ie=UTF8&qid=1409346826&sr=8-1&keywords=calamity+physics>

By splitting at the slashes, we can extract what we want and throw away
the rest. We can then use this to construct an affiliate URL.

I've wrapped this idea in a Python script, which I can use in TextExpander:

```python
#!/usr/bin/env python

import re
import sys

FRONT_URL      = "%snippet:;furl%"
AFFILIATE_CODE = "123-abc-456"

if re.match('[www\.]?amazon', FRONT_URL) is None:
    print FRONT_URL
    sys.exit()

components  = FRONT_URL.split('/')
amazon_site = filter(lambda x: 'amazon' in x, components)[0]
if 'dp' in FRONT_URL:
    asin_code   = components[components.index('dp') + 1]
elif 'gp' in FRONT_URL:
    idx = components.index('gp') + 1
    if components[idx + 1] == 'product':
        asin_code = components[idx + 2]
    else:
        asin_code = components[idx + 1]

aff_link = 'http://{amazon}/dp/{asin}/?tag={aff_code}'.format(
    amazon   = amazon_site,
    asin     = asin_code,
    aff_code = AFFILIATE_CODE
)

print aff_link
```

This is saved as a shell script snippet in TextExpander, and I have it
bound to the abbreviation `;az`. Of course, I replace the `AFFILIATE_CODE` with my actual affiliate code.

The `%snippet:;furl%` component gets the front URL from the running
browser, using a snippet I originally got [from Dr. Drang][drang]. Then
I put my affiliate code in at the top of the script.

Then I use a simple regex to check that it's an Amazon page. If not, I
just print the URL.

Next I split the URL at the slashes, and extract the domain name for
that particular Amazon site, and the ASIN as the next component after `/dp/`.
Older links have `/gp/product` (see footnote), so we treat those separately.
Finally, I combine these pieces into an affiliate URL, and print it out.
Then TextExpander types this link into my front document.

Now all I need to do is actually write a post that requires an Amazon
affiliate link.

[^1]: According to [Aaron Shepard][aaron], `dp` and its predecessor `gp`
are programs used on Amazon's backend to generate product pages, although
I've been unable to verify that.

[tweet]: https://twitter.com/caseyliss/status/505456285173968896
[book]:  http://www.phpied.com/short-amazon-affiliate-links-a-bookmarklet/
[aaron]: http://www.newselfpublishing.com/AmazonLinking.html
[drang]: http://www.leancrew.com/all-this/2009/07/safari-tab-urls-via-textexpander/
