---
layout: post
date: 2017-10-11 22:09:25 +0000
title: Four ways to underline text in LaTeX
tags: latex typesetting
summary: I'm very picky about the way underlines look, and have spent a lot of time trying to get the perfect underline in LaTeX.
---

Because I'm old-fashioned, I still write printed documents in LaTeX, and I still think hyperlinks should be underlined.
In general, I'm glad that underlines as a form of emphasis have gone away (boldface or italics are much nicer) --- but I have yet to be convinced to drop underlines on hyperlinks.

Sometimes I have to write printed documents that contain hyperlinks, which begs the question: how do you write underlines in LaTeX?
Finding an underline I like has proven surprisingly hard --- in this post, I'll show you the different ways I've tried to underline text.

## Using the \underline command

Without installing any packages, you can just use the `\underline` command.
Here's an example:

```latex
I visited \underline{Berlin} in \underline{Germany}.
```

<style>
  .latex__example {
    max-width: 500px;
    padding-top:    8px;
    padding-bottom: 8px;
  }

  .highlight + figure {
    padding-top: 8px;
  }
</style>

and the rendered output:

<figure>
  <img src="/images/2017/example_underline.png" class="latex__example"/>
</figure>

The underline on "Berlin" is nice and tight --- but notice how the underline on "Germany" is lower than "Berlin".
That's to accommodate the descender on the "y".
(A [descender][descender] is any part of a letter that extends below the baseline of the text.
For example, "p", "y" and "j" all have descenders, but "a", "i" and "x" don't.)

The inconsistency is what I don't like about this approach.
It's fine for one-off underlines, but in a larger document, the inconsistency gets very obvious, and I don't like how it looks.

[descender]: https://en.wikipedia.org/wiki/Descender

<!-- summary -->

## The soul package

If we look beyond core LaTeX, the [soul package][soul] has a variety of methods for decorating text, including underlining, strikeouts, and letter spacing.
It provides an underline command that avoids the inconsistency.
For example:

```latex
\usepackage{soul}

I visited \ul{Berlin} in \ul{Germany}.
```

is rendered as:

<figure>
  <img src="/images/2017/example_soul.png" class="latex__example"/>
</figure>

Now, the two underlines are on the same level.
They're far down enough to avoid any descenders in the font.
But I don't like the gap under "Berlin" --- I prefer it tight against the bottom the text, as with the `\underline` command.

The soul package has a `\setuldepth` macro that allows us to adjust the height of the lines.
We pass it some text, and it draws the underlines just below the lowest character the text contains --- just enough to avoid any descenders.
So to match the spacing on "Berlin", we'd write:

```latex
\setuldepth{Berlin}
I visited \ul{Berlin} in \ul{Germany}.
```

which appears like so:

<figure>
  <img src="/images/2017/example_soul_uldepth.png" class="latex__example"/>
</figure>

Now "Berlin" is looking nicer, but the underline intersects the "y" of "Germany".
That's not great either.

[soul]: https://ctan.org/pkg/soul

## The ulem package

Like soul, the [ulem package][ulem] gives you ways to highlight text with underlines (including double and wavy underlines) and strikeouts.
For the common case, it behaves in a similar way: the default underline is drawn low enough to avoid crossing any descenders, or you can adjust the underline depth with a macro.

First, an example with the default height.

```latex
\usepackage{ulem}

I visited \uline{Berlin} in \uline{Germany}.
```

<figure>
  <img src="/images/2017/example_ulem.png" class="latex__example"/>
</figure>

Second, an example with the depth manually adjusted.

```latex
\renewcommand{\ULdepth}{1.8pt}

I visited \uline{Berlin} in \uline{Germany}.
```

<figure>
  <img src="/images/2017/example_ulem_uldepth.png" class="latex__example"/>
</figure>

But it suffers from the same problem as soul --- if you adjust the depth of the underline, it intersects with the descenders.

[ulem]: https://ctan.org/pkg/ulem

## Cutting out the descenders

What I really want is the consistent and tight underline depth in the latter soul and ulem examples, but with some gaps in the underline to accommodate descenders where appropriate.
I got inspiration for my approach from the [TeX.SX Stack Exchange][texsx]: use the [contour package][contour] to draw a white outline of the text underneath the real text, and use that to blot out bits of the underline.

Here's how you use contour to trace around a letter (in red so the effect is visible):

<!-- ```latex
\usepackage{contour}

\contourlength{1pt}

\newcommand{\mycontour}[1]{
  \contour{red}{#1}%
}

I visited \mycontour{Berlin} in \mycontour{Germany}.
``` -->

<div class="highlight"><pre><code class="language-latex" data-lang="latex"><span></span><span class="k">\usepackage</span><span class="nb">{</span>contour<span class="nb">}</span>

<span class="k">\contourlength</span><span class="nb">{</span>1pt<span class="nb">}</span>

<span class="k">\newcommand</span><span class="nb">{</span><span class="k">\mycontour</span><span class="nb">}</span>[1]<span class="nb">{</span><span class="c">%</span>
  <span class="k">\contour</span><span class="nb">{</span>red<span class="nb">}{</span>#1<span class="nb">}</span><span class="c">%</span>
<span class="nb">}</span>

I visited <span class="k">\mycontour</span><span class="nb">{</span>Berlin<span class="nb">}</span> in <span class="k">\mycontour</span><span class="nb">{</span>Germany<span class="nb">}</span>.
</code></pre></div>

<figure>
  <img src="/images/2017/example_contour.png" class="latex__example"/>
</figure>

The `\contourlength` setting defines the width of the curve --- how much extra space is added.
I usually tweak that until I get something that looks good with the font.
Then the `\contour` macro draws the supplied text, with a red contour around the letters.

Then I swap the red for white, and add the underline:

<!-- ```latex
\renewcommand{\ULdepth}{1.8pt}
\contourlength{0.8pt}

\newcommand{\myuline}[1]{
  \uline{\phantom{#1}}%
  \llap{\contour{white}{#1}}%
}

I visited \myuline{Berlin} in \myuline{Germany}.
``` -->

<div class="highlight"><pre><code class="language-latex" data-lang="latex"><span></span><span class="k">\renewcommand</span><span class="nb">{</span><span class="k">\ULdepth</span><span class="nb">}{</span>1.8pt<span class="nb">}</span>
<span class="k">\contourlength</span><span class="nb">{</span>0.8pt<span class="nb">}</span>

<span class="k">\newcommand</span><span class="nb">{</span><span class="k">\myuline</span><span class="nb">}</span>[1]<span class="nb">{</span><span class="c">%</span>
  <span class="k">\uline</span><span class="nb">{</span><span class="k">\phantom</span><span class="nb">{</span>#1<span class="nb">}}</span><span class="c">%</span>
  <span class="k">\llap</span><span class="nb">{</span><span class="k">\contour</span><span class="nb">{</span>white<span class="nb">}{</span>#1<span class="nb">}}</span><span class="c">%</span>
<span class="nb">}</span>

I visited <span class="k">\myuline</span><span class="nb">{</span>Berlin<span class="nb">}</span> in <span class="k">\myuline</span><span class="nb">{</span>Germany<span class="nb">}</span>.
</code></pre></div>

<figure>
  <img src="/images/2017/example_final.png" class="latex__example"/>
</figure>

There are two parts here: first, the `\phantom` takes up the same horizontal space as the underlined text, but doesn't actually print anything.
Putting this inside the `\uline` gives you an underline of exactly the right width for the text.

Then because you already have the horizontal offset, an `\llap` (left overlap) sits on top of it, drawing both the text and the white outline.
Because this comes second, it overrides the underline --- drawing white gaps for the descender as appropriate, for example on the "y".

I use ulem rather than soul so I can tweak the depth very precisely, mostly a case of trying different values until I find something that fits the font.
Same with the contour length, I just try it until it looks nice.

Put all together, this gives me a really nice underline.
It's drawn on a consistent level, flush against the bottom of the text, with gaps as appropriate for descenders.
If I want to tweak it further --- maybe adjust the underline thickness, or give it a different colour --- the settings in the ulem package give me plenty of scope for further refinement.

Here's one final example, a hyperlink from my CV:

<figure>
  <img src="/images/2017/underline_final.png" class="latex__example"/>
</figure>

I particularly like the "py" and "yp" in this link, which show off the effect really nicely, as well as the lower bowl on the leading "g".

The last outing for my CV was about a year ago, when I was applying for my current job.
I spent a lot of time fiddling with the underlined links before I settled on the above, because I was unsatisfied with everything else.
One of my interviewers specifically mentioned how nice my CV looked, and I tell myself it's because of the underlines.
So it might be old-fashioned to care about LaTeX and underlined links, but it might also have helped me get a job.

[contour]: https://ctan.org/pkg/contour
[texsx]: https://tex.stackexchange.com/q/36894/9668

*The code used to create the images in this post is [on GitHub][github].*

[github]: https://github.com/alexwlchan/alexwlchan.net/tree/master/examples/latex-underlines
