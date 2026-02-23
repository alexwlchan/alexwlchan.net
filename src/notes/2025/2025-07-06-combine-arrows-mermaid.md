---
layout: note
title: Combine arrows in Mermaid by using an invisible node
date: 2025-07-06 09:37:21 +01:00
topic: Drawing things
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
  
  .nodeLabel p {
    font-size: 16px;
  }
</style>

I was drawing a chart with [Mermaid](https://mermaid.js.org/intro/syntax-reference.html), where several sources combine into a single destination.
Here's a quick demo:

<blockquote class="demo">
  <pre><code>flowchart LR
    <span class="n">SRC1</span>[source 1]
    <span class="n">SRC2</span>[source 2]
    <span class="n">SRC3</span>[source 3]
    <span class="n">DST</span>[destination]

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
  <span class="n">SRC1</span>[source 1]
  <span class="n">SRC2</span>[source 2]
  <span class="n">SRC3</span>[source 3]
  <span class="n">DST</span>[destination]

  <span class="n">E</span>[ ]:::empty
  classDef <span class="n">empty</span> height: 0, width: 0

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
