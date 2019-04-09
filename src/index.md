---
layout: page
archive_variant: index
---

<img src="/images/profile.jpg" style="float: right; width: 250px; max-width: 50%; margin-top: 0.4em; margin-left: 1em; margin-bottom: 1em;">

## Hi, I'm Alex.

I'm a software developer at [the Wellcome Trust][wellcome] and an open-source Python developer.
At Wellcome, I'm helping build a new platform for searching and storing our digital collections.
It's taking Wellcome's assets -- books, archives, images, and more -- and presenting them through consistent, well-designed APIs.

I contribute to open source Python in my free time, including the [Hypothesis testing library][hypothesis] and the [hyper-h2 HTTP/2 stack][hyper].
I'm one of the organisers for the [PyCon&nbsp;UK][pycon] conference, and I've given a number of talks about Python (among other topics).

The site focuses on programming, with the occasional venture into accessibility, maths, bits of travel advice and Victorian engineering.
It's as a way to sharpen my skills in writing, and improve my ability to explain my ideas.
If that sounds interesting, I have an [infrequently updated blog](/blog/).

I hope you enjoy the site.

<!-- He/him. -->

[hypothesis]: https://github.com/HypothesisWorks/hypothesis-python
[wellcome]: https://en.wikipedia.org/wiki/Wellcome_Trust
[hyper]: https://github.com/python-hyper/
[pycon]: http://2018.pyconuk.org/

## Recent posts

{% assign posts = site.posts | homepage_posts %}
{% include archive_list.html %}

## Contact

You can email me at {{ site.emails.personal | mailto_link }}, or I'm [@alexwlchan](https://twitter.com/alexwlchan) on Twitter.

For anything related to Wellcome, email {{ site.emails.wellcome | mailto_link }}.
