---
layout: til
title: Group nodes in a Mermaid flowchart by putting them in a subgraph
date: 2025-07-06 19:54:31 +0100
tags:
  - mermaid
  - drawing things
---
I was drawing a flowchart with [Mermaid][mermaid], and I wanted to draw a box around several items to group them together.

I found a suggestion by [Stack Overflow user KZiovas][so] to use a subgraph.
Here's an example:

```
flowchart LR
  subgraph sources["my sources"]

    SRC1[source 1]
    SRC2[source 2]
    SRC3[source 3]
  end
  DST[destination]

  SRC1 --> DST
  SRC2 --> DST
  SRC3 --> DST
```

and here's what the rendered graph looks like:

{%
  inline_svg
  filename="mermaid_subgraphs.svg"
  class="mermaid dark_aware"
%}

[mermaid]: https://mermaid.js.org/intro/syntax-reference.html
[so]: https://stackoverflow.com/a/77439747/1558022
