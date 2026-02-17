---
layout: topic
title: Digital preservation
---

Digital preservation is about protecting digital information to ensure it's available for a long time into the future.
Libraries and archives have old manuscripts and papers from centuries ago; digital preservation is about trying to give digital media a similar lifespan.

I've always been a digital packrat, saving fanfiction as a teenager when it became clear I couldn't rely on my favourite websites to stay up.

I formalised those ideas when I went to work for [Wellcome Collection](https://wellcomecollection.org) and [the Flickr Foundation](https://www.flickr.org/), where I helped to build services to store digital collections.

Sub-topics:

<ul>
  {%- for c in get_topic_by_name(page.title).children | sort(attribute="name") -%}
  <li>
    <a href="{{ c.href }}">{{ c.name }}</a>
  </li>
  {%- endfor -%}
</ul>
