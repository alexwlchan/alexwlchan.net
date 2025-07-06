---
layout: til
title: Combine arrows in Mermaid by using an invisible node
date: 2025-07-06 09:37:21 +0100
tags:
  - mermaid
  - drawing things
---
<style>
  @media screen and (min-width: 500px) {
    .demo {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-gap: 1em;
      align-items: center;
    }
  }
</style>

I was drawing a chart with [Mermaid](https://mermaid.js.org/intro/syntax-reference.html), where several sources combine into a single destination.
Here's a quick demo:

<blockquote class="demo">
  <pre><code>flowchart LR
    SRC1[source 1]
    SRC2[source 2]
    SRC3[source 3]
    DST[destination]

    SRC1 --> DST
    SRC2 --> DST
    SRC3 --> DST</code></pre>
  {%
    inline_svg
    filename="mermaid1.svg"
    alt="Rectangle-and-arrow diagram with four rectangles. There are three ‘source’ rectangle and one ‘destination’ rectangle, with three distinct arrows from each source to the destination"
    class="dark_aware"
  %}
</blockquote>

I was slightly bothered by the way there are three completely separate arrows between the source and the destination.
Via [a comment on the Mermaid GitHub](https://github.com/mermaid-js/mermaid/issues/1712#issuecomment-1982049019), I found a [Stack Overflow answer](https://stackoverflow.com/a/71545886/1558022) by Paulo which suggests using an empty node which doesn't take up any space.

This looks more like what I want:

<blockquote class="demo">
  <pre><code>flowchart LR
  SRC1[source 1]
  SRC2[source 2]
  SRC3[source 3]
  DST[destination]

  E[ ]:::empty
  classDef empty height: 0, width: 0

  SRC1 --- E
  SRC2 --- E
  SRC3 --- E
  E --> DST</code></pre>
  {%
    inline_svg
    filename="mermaid2.svg"
    alt="Rectangle-and-arrow diagram with four rectangles. There are three ‘source’ rectangle and one ‘destination’ rectangle, with three arrows from each source that combine into a single arrow pointing to the destination"
    class="dark_aware"
  %}
</blockquote>
