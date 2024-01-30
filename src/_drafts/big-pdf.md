---
layout: post
title: Making a PDF that’s larger than Germany
summary: We’re gonna need a bigger printer.
tags:
  - drawing-things
---

<style>
  :root { color-scheme: dark light; }

  @media screen and (prefers-color-scheme: light) {
    rect.pdf_component {
      fill: white;
    }

    rect.object_wrapper {
      fill: rgba(238, 238, 238, 0.85);
    }
  }

  @media screen and (prefers-color-scheme: dark) {
    rect.pdf_component {
      fill: black;
    }

    rect.object_wrapper {
      fill: rgba(61, 61, 61, 0.75);
    }
  }
</style>

{%
  inline_svg
  filename="pdf_layout.svg"
  class="dark_aware"
  alt="tbc"
  style="width: 300px;"
%}