---
date: 2014-07-11 07:43:00 +0000
layout: post
slug: latex-alpha
tags: latex wolfram-alpha
title: Getting plaintext <span class="latex">L<sup>a</sup>T<sub>e</sub>X</span> from
  Wolfram Alpha
---

Although I don't write numerical equations very often, I couldn't help but smile at [this post by Dr. Drang][drang].
Building on [a post by Eddie Smith][eddie] which shows how to use WolframAlpha to evaluate a LaTeX expression for a numerical answer, he shows off a way to automate getting the equation from BBEdit, to save a tedious copy/paste step.
Read their posts before you carry on.

Dr. Drang's script gets the LaTeX equation out of BBEdit and loads Wolfram Alpha, but you still need to click the "Copyable plaintext" link.
He ended the post as follows:

> What I’d really like is to automate the copying and pasting of the answer. Wolfram’s page structure doesn’t make that easy, but it’s something I want to explore.

I tried to parse the Wolfram Alpha page structure in the past, and it was a bit of a mess.
It's much easier to use the [Wolfram Alpha Developer API][api], which provides this very easily.
I think I can use this to get the final piece.

<!-- summary -->

If you don't already have a (free) Wolfram ID, then [signing up for one][wid] takes about a minute.
Then you can register an API key, and make queries in the form

```
http://api.wolframalpha.com/v2/query?input=\pi&appid=XXXXXX-YYYYYYYYYY
```

rather than going to the website.
This returns an XML object with your results, which saves you unpicking the page structure yourself.

The Wolfram Alpha output is divided into "pods" (which correspond roughly to the rectangles in the web output), and we can pick out the pod which gives the decimal representation of an expression.
Within this pod, the `plaintext` key gives us the text we'd get from the "Copyable plaintext" link.
That's what we want.

I've wrapped this in a script, which incorporates part of what Dr. Drang wrote:

```python
import requests
from urllib import quote_plus
import xml.etree.ElementTree as ET

appid = 'XXXXXX-YYYYYYYYYY'

def get_plaintext_query(latex):
    r = requests.get('http://api.wolframalpha.com/v2/query?input=%s&appid=%s' % (quote_plus(latex), appid))
    root = ET.fromstring(r.text.encode('utf8'))

    for pod in root:
        if pod.attrib.get('title', '') in ['Decimal approximation', 'Definite integral']:
            subpod = pod.find('subpod')
            result = subpod.find('plaintext').text

            if pod.attrib.get('title', '') == 'Definite integral':
                return result.split('~~')[1]
            else:
                return result

    if __name__ == '__main__':
        from sys import stdin
        print get_plaintext_query(stdin.read())
```

You'll need to add your own App ID in line 8.
The URL encoding is handled by `quote_plus`, taken from Dr. Drang's script, and then `ElementTree` handles the XML decoding.

It takes a few seconds to run, but it's still faster than opening a web page and doing the copy/paste yourself.

Right now it evaluates raw expressions, such as `\frac{\pi + \sqrt{3}}{\exp(2)}`, and definite integrals, such as `\int_0^5 x^2 dx`.
There may be other forms of input for which this is useful, but I couldn't think of them when I wrote this.

If we have the plaintext number in a script, then we can also do some nice formatting.
For example, if we're working with currency units, then we might want to trim all but the last two decimal places:

```pycon
>>> x = get_plaintext_query('\pi')
3.1415926535897932384626433832795028841971693993751058...
>>> y = eval(x.replace('...', ''))
>>> round(y, 2)
3.14
```

Alternatively, I remember in school being told to round to a particular number of significant figures.
Here's a quick function for rounding to significant figures:

```python
def get_sig_figs(num, n):
    div = 1
    while int(num / div) > 0: div *= 10
    return round(num / div, n) * div
```

And there are probably plenty of other things you could do with this.
But since I don't work with this sort of numerical equation on a regular basis (yet), I don't know how useful this would actually be, so I think I'll just stop there.

This script won't work every time.
Complicated expressions will probably still need a trip to Wolfram Alpha to check that it's been interpreted correctly, or if you need a different part of the output.
But for simple stuff, this should be fine.

[drang]: http://www.leancrew.com/all-this/2014/07/evaluating-latex-with-eddie-and-alpha/
[eddie]: http://www.practicallyefficient.com/home/2014/7/10/latex-alfred-wolfram
[api]: http://products.wolframalpha.com/api/
[wid]: https://developer.wolframalpha.com/portal/apisignup.html
