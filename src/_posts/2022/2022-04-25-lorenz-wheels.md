---
layout: post
date: 2022-04-25 21:10:40 +00:00
title: Illustrating the cipher wheels of a Lorenz machine
summary: Some old code I wrote to draw cam-accurate illustrations of cipher wheels.
tags:
  - drawing things
  - latex
  - history
link: https://github.com/alexwlchan/lorenz-wheels
colors:
  index_light: "#423f3a"
  index_dark:  "#a9a69a"
---

Yesterday I found a set of old illustrations I'd made for the wheels of a [Lorenz cipher machine], which was a machine used by the German Army during World War II.

The machine had twelve wheels, which were combined to form a 5-bit key.
Each wheel had a number of switches around its rim (called "cams"), which could be set in an "on" or "off" position.
Here's a close-up photo of two of the wheels:

<figure style="width: 303px">
  {%
    picture
    filename="lorenz_cams.jpg"
    width="303"
    alt="A close-up photo of two metal wheels. The wheels have numbers running around the rim, and next to each number is a small metal switch."
  %}
  <figcaption>
    Photo by TedColes <a href="https://commons.wikimedia.org/wiki/File:Lorenz_Cams.jpg">on Wikimedia Commons</a>, used under CC BY-SA 4.0.
  </figcaption>
</figure>

Each wheel had a different number of switches, and those numbers were [coprime][coprime] (they had no common factors).
Between the switch settings and the starting positions of the wheels, this meant there were a dizzying number of possible setups -- and the Germans believed this made it an unbreakable cipher.
They trusted it with their most important messages.

Unfortunately for them, an operator made a mistake, and this let British codebreaker [Bill Tutte] find a weakness in the cipher.
He helped Bletchey Park develop a system to read these top secret messages.
His analysis grouped the wheels into three sets, based on how they were used in the machine: psi/ψ, chi/χ, and mu/μ.

I made some illustrations that show the wheels as coloured circles, with tick marks to represent the number of switches:

<style>
  .grid {
    display: grid;
    grid-template-columns: calc(32% - 4px) calc(32% - 4px) calc(32% - 4px);
    grid-gap: 18px;
    margin-bottom: 0.5em;
  }

  figure {
    max-width: 520px;
  }
</style>

<figure>
  <div class="grid">
    <img src="/images/2022/wheels-1.png" alt="A blue wheel with the label psi-2.">
    <img src="/images/2022/wheels-10.png" alt="A red wheel with the label mu-1.">
    <img src="/images/2022/wheels-8.png" alt="A green wheel with the label chi-4.">
  </div>
  <figcaption>
    The <em>ψ</em><sub>2</sub> wheel has 47&nbsp;cams,
    the <em>μ</em><sub>1</sub> wheel has 37&nbsp;cams,
    and the <em>χ</em><sub>4</sub> wheel has 26&nbsp;cams.
  </figcaption>
</figure>

I meant to use them in a presentation about Lorenz and the British break of the cipher, but it never happened.
They languished on a disk for years, until I found them yesterday.

They're drawn using polar coordinates in [TikZ], a graphics library for LaTeX.
I've put the code and instructions for compiling the diagrams in [a GitHub repository][repo], in case you'd like to draw similar diagrams yourself.

Alternatively, if you want to read more about the Lorenz cipher, there are some pages written by [the late Tony Sale][tony_sale] that explain how the cipher works, and how it was cracked.
He also talks about Colossus, a codebreaking computer used to read Lorenz messages, which was kept secret for nearly thirty years after the war -- and which he helped to rebuild in the early 2000s.

[Bill Tutte]: https://en.wikipedia.org/wiki/W._T._Tutte
[Lorenz cipher machine]: https://en.wikipedia.org/wiki/Lorenz_cipher
[TikZ]: https://tikz.dev/
[coprime]: https://en.wikipedia.org/wiki/Coprime_integers
[repo]: https://github.com/alexwlchan/lorenz-wheels
[tony_sale]: https://www.codesandciphers.co.uk/virtualbp/fish/fishindex.htm
