---
layout: post
date: 2017-10-11 22:09:25 +0000
date_updated: 2018-11-13 20:54:44 +0000
summary: I'm very picky about the way underlines look, and have spent a lot of time
  trying to get the perfect underline in LaTeX.
tags:
  - latex
  - typesetting
title: Four ways to underline text in LaTeX
index:
  feature: true
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
    padding-top:    1em;
    padding-bottom: 1em;
  }

  .highlight + figure {
    padding-top: 8px;
  }
</style>

and the rendered output:

{%
  picture
  filename="example_underline.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined. The underlines are at different heights – the line below “Berlin” is close to the bottom of the letters, but the line below “Germany” has moved down to sit below the bottom of the “y”."
  width="500"
  class="latex__example"
%}

The underline on "Berlin" is nice and tight --- but notice how the underline on "Germany" is lower than "Berlin".
That's to accommodate the descender on the "y".
(A [descender][descender] is any part of a letter that extends below the baseline of the text.
For example, "p", "y" and "j" all have descenders, but "a", "i" and "x" don't.)

The inconsistency is what I don't like about this approach.
It's fine for one-off underlines, but in a larger document, the inconsistency gets very obvious, and I don't like how it looks.

[descender]: https://en.wikipedia.org/wiki/Descender

## The soul package

If we look beyond core LaTeX, the [soul package][soul] has a variety of methods for decorating text, including underlining, strikeouts, and letter spacing.
It provides an underline command that avoids the inconsistency.
For example:

```latex
\usepackage{soul}

I visited \ul{Berlin} in \ul{Germany}.
```

is rendered as:

{%
  picture
  filename="example_soul.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined. The underlines are at the same height – they’re both low enough to miss the “y” in “Germany”, which means there’s a noticeable gap between “Berlin” and its underline."
  width="500"
  class="latex__example"
%}

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

{%
  picture
  filename="example_soul_uldepth.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined. The underlines are at the same height – there’s no gap between “Berlin” and the underline, but now the underline of “Germany” clashes with the bottom of the “y”."
  width="500"
  class="latex__example"
%}

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

{%
  picture
  filename="example_ulem.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined. The underlines are at the same height – they’re both low enough to miss the “y” in “Germany”, which means there’s a noticeable gap between “Berlin” and its underline."
  width="500"
  class="latex__example"
%}

Second, an example with the depth manually adjusted.

```latex
\setlength{\ULdepth}{1.8pt}

I visited \uline{Berlin} in \uline{Germany}.
```

{%
  picture
  filename="example_ulem_uldepth.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined. The underlines are at the same height – there’s no gap between “Berlin” and the underline, but now the underline of “Germany” clashes with the bottom of the “y”."
  width="500"
  class="latex__example"
%}

But it suffers from the same problem as soul --- if you adjust the depth of the underline, it intersects with the descenders.

[ulem]: https://ctan.org/pkg/ulem

## Cutting out the descenders

What I really want is the consistent and tight underline depth in the latter soul and ulem examples, but with some gaps in the underline to accommodate descenders where appropriate.
I got inspiration for my approach from the [TeX.SX Stack Exchange][texsx]: use the [contour package][contour] to draw a white outline of the text underneath the real text, and use that to blot out bits of the underline.

Here's how you use contour to trace around a letter (in red so the effect is visible):

{% raw %}
```latex
\usepackage{contour}

\contourlength{1pt}

\newcommand{\mycontour}[1]{
  \contour{red}{#1}%
}

I visited \mycontour{Berlin} in \mycontour{Germany}.
```
{% endraw %}

{%
  picture
  filename="example_contour.png"
  alt="The phrase “I visited Berlin in Germany”, with a heavy red outline around “Berlin” and “Germany”."
  width="500"
  class="latex__example"
%}

The `\contourlength` setting defines the width of the curve --- how much extra space is added.
I usually tweak that until I get something that looks good with the font.
Then the `\contour` macro draws the supplied text, with a red contour around the letters.

Then I swap the red for white, and add the underline:

{% raw %}
```latex
\setlength{\ULdepth}{1.8pt}
\contourlength{0.8pt}

\newcommand{\myuline}[1]{
  \uline{\phantom{#1}}%
  \llap{\contour{white}{#1}}%
}

I visited \myuline{Berlin} in \myuline{Germany}.
```
{% endraw %}

{%
  picture
  filename="example_final.png"
  alt="The word “I visited Berlin in Germany”, with the words “Berlin” and “Germany” underlined."
  width="500"
  class="latex__example"
%}

There are two parts here: first, the `\phantom` takes up the same horizontal space as the underlined text, but doesn't actually print anything.
Putting this inside the `\uline` gives you an underline of exactly the right width for the text.

Then because you already have the horizontal offset, an `\llap` (left overlap) sits on top of it, drawing both the text and the white outline.
Because this comes second, it overrides the underline --- drawing white gaps for the descender as appropriate, for example on the "y".

I use ulem rather than soul so I can tweak the depth very precisely, mostly a case of trying different values until I find something that fits the font.
Same with the contour length, I just try it until it looks nice.

## Putting it all together

Here's the code I ultimately settled on:

{% raw %}
```latex
\usepackage{contour}
\usepackage{ulem}

\renewcommand{\ULdepth}{1.8pt}
\contourlength{0.8pt}

\newcommand{\myuline}[1]{%
  \uline{\phantom{#1}}%
  \llap{\contour{white}{#1}}%
}
```
{% endraw %}

This gives me a really nice underline.
It's drawn on a consistent level, flush against the bottom of the text, with gaps as appropriate for descenders.
If I want to tweak it further -- maybe adjust the underline thickness, or give it a different colour -- the settings in the ulem package give me plenty of scope for further refinement.

Here's one final example, a hyperlink from my CV:

{%
  picture
  filename="underline_final.png"
  alt="A blue link to “github.com/python-hyper/hyper-h2”, with the entire link underlined."
  width="500"
  class="latex__example"
%}

I particularly like the "py" and "yp" in this link, which show off the effect really nicely, as well as the lower bowl on the leading "g".

The last outing for my CV was about a year ago, when I was applying for my current job.
I spent a lot of time fiddling with the underlined links before I settled on the above, because I was unsatisfied with everything else.
One of my interviewers specifically mentioned how nice my CV looked, and I tell myself it's because of the underlines.
So it might be old-fashioned to care about LaTeX and underlined links, but it might also have helped me get a job.

[contour]: https://ctan.org/pkg/contour
[texsx]: https://tex.stackexchange.com/q/36894/9668

*You can [download the code](/files/2017/latex-underlines.zip) used to create the images in this post.*
