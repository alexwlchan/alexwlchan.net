---
layout: post
date: 2021-10-06 21:39:30 +0000
title: READMEs for Open Science
summary: Slides for a short talk about READMEs, why they're important, and what they should contain.
tags:
  - documentation
  - open life science
  - talks
colors:
  css_light: "#20883f"
  css_dark:  "#2fc65d"
---

Earlier today, I gave a talk for the [the Open Life Science Program][openlife] about READMEs.
I was talking about how READMEs serve as the first point of contact for a project; how they get new users interested in and excited about the project.

The cohort calls are recorded, and I'll add a link to the video.
In the meantime, you can download my slides [as a PDF][pdfslides] or read my (loosely edited) notes below.

This is my second talk for OLS -- last year I talked about how [inclusion can't be an afterthought][inclusion].

[openlife]: https://openlifesci.org/
[pdfslides]: /files/2021/ols-readme.pdf
[inclusion]: /2020/inclusion-cant-be-an-afterthought/

<style>
  .slide img {
    border: 3.5px solid #2ec65c;
  }
</style>



## References and links

References for stuff I mentioned:

-   [A thread about the origin of READMEs](https://softwareengineering.stackexchange.com/a/106090), with an example from 1974.
-   [Daniel Beck's README checklist](https://github.com/ddbeck/readme-checklist), which is what I usually use
-   Examples of READMEs I showed in screenshots:

    -   <a href="https://github.com/sczesla/PyAstronomy">sczesla/PyAstronomy</a>
    -   <a href="https://gitlab.com/acubesat/su/yeast-biology">acubesat/yeast-biology</a>
    -   [tidyverse/readxl](https://github.com/tidyverse/readxl)
    -   [numpy/numpy](https://github.com/numpy/numpy)
    -   [curl/curl](https://github.com/curl/curl)




## Slides and notes

{%
  slide
  filename="slide1.png"
  alt="Title slide. It includes my name (Alex Chan), my pronouns (they/she), and a URL pointing to these slides."
%}

Title slide.

I'm going to talk about what a README file is, why it's important for your project, and what sort of information it should contain.



{%
  slide
  filename="slide2.jpg"
  alt="Photograph of the front elevation of the Wellcome Collection building at dusk. The building is illuminated with a series of up-lighters, flooding the facade with green light. In the foreground at ground level are blurred streaks of red and yellow from the headlights and tail lights of passing vehicles. The leaves of trees to the left and right of the image frame the building and are themselves blurred as a result of the wind and long photographic exposure."
  caption="Photo by Thomas Farnetti, Wellcome Collection. Used under CC BY 4.0."
%}

I work at [Wellcome Collection][wc], a museum and library that explores the intersection of health and human experience.
If you don't know it, a museum and library is a place you'd visit to see objects and books in [The Before Times][before].

I work in the digital engagement team, and part of our remit includes [sharing what we've been doing][stacks].
We have a generous budget and we do interesting things, so all our work is [open source][gh] – anybody can read our code and see what we're doing.

[wc]: https://wellcomecollection.org/about-us
[before]: https://en.wikipedia.org/wiki/COVID-19_lockdowns
[stacks]: https://stacks.wellcomecollection.org
[gh]: https://github.com/wellcomecollection



{%
  slide
  filename="slide3.jpg"
  alt="Two vertical stacks of white paper sitting side-by-side. Between the two stacks is a gap which fades to black. A few of the pages have tabs with numbers or labels scribbled on them, but there's no clear structure."
  caption="Photo by [myrfa on Pixabay](https://pixabay.com/photos/files-paper-office-paperwork-stack-1614223/). Used under CC0."
%}

But being thrown into a new repository of code is pretty hard!

There could be hundreds or thousands of files, and if you don't know where to start it's pretty hard to wrap your head around it all.
How does it fit together?
Where should you start?
What's the point of this project?

All tricky questions to answer in a new project: the README helps get you started.



{%
  slide
  filename="slide4.png"
  alt="A black-and-white screenshot of an old Mac operating system, within an outline of a beige Macintosh computer. The screenshot shows a file browser, with a file with a newspaper icon and the name 'Read Me'."
  caption="Screenshot from James Friend’s [Mac Plus emulator](https://jamesfriend.com.au/pce-js/)."
%}

The "Read Me" as a concept has been around for a long time – this is a screenshot from [System 7][sys7], but there are examples [as far back as 1974][rm1974].

The idea is that it's the first file you'd read, to get you started.

[sys7]: https://en.wikipedia.org/wiki/System_7
[rm1974]: https://softwareengineering.stackexchange.com/a/106090



{%
  slide
  filename="slide5.jpg"
  alt="A station platform with a green cobbled edge and a black-and-white welcome mat. The welcome mat has a pattern of interspersed diamonds in different colours, and the word 'Welcome' in dark text at the centre. The green cobbled edge runs across the top of the image, and has the text 'What is a README?' overlaid in green."
  caption="Photo: Welcome mat at Tukila Station, by [SonderBruce on Flickr](https://www.flickr.com/photos/sounderbruce/16544240269). Used under CC BY-SA 2.0."
%}

A previous OLS speaker likened a README to a welcome mat, and I like that analogy.

It's meant to introduce you to a project, to get you started.
It's the first thing you'd encounter as a new user to a project.



{%
  slide
  filename="slide7.png"
  alt="Text slide. It has a title in green 'What should a README tell me?' and three bullet points: 'What is this project?' 'Who should use it?' 'How do they get started?'."
%}

There are lots of checklists and templates for READMEs, which you can find using Google.
Personally I use [Daniel Beck's checklist](https://github.com/ddbeck/readme-checklist), but there are plenty of others.
Find one that you like.

In broad strokes, a README has to answer three questions:

-   What is this project?
    What's it about, why does it exist, what problem does it solve?

    You want to explain why your project is useful, and why somebody might want to use it.
    You want to tell them if they should spend more time learning about your project, or if they should look elsewhere.

-   Who should use it?
    Who's the target audience?

    And conversely: who's not the target audience?
    Projects don't have to be for everyone, and if you can be super clear about your purpose upfront, you help people who aren't your audience as well – they can work that out quickly, and look elsewhere.

-   How do they get started?

    If this does solve their problem and they're in the target audience, how does somebody start using your project?
    This includes things like installing your code, some examples or instructions, and how to tell they've installed it correctly.

The README is a springboard to the rest of your project.
It shouldn't be your only documentation, but it should help people get started and decide if they want to spend more time with your project.



{%
  slide
  filename="slide6.png"
  alt="A slide with three grey file icons labelled 'README', 'README.txt' and 'README.md'. The slide is titled 'What is a README?'."
%}

Typically a README file is named something like `README`, `README.txt` or `README.md`.
It lives in the root of your repository.




{%
  slide
  filename="slide8.jpg"
  alt="Screenshots of repositories on GitHub and GitLab. A significant part of the area of the page is showing the README."
  caption="The landing page of [PyAstronomy](https://github.com/sczesla/PyAstronomy) (GitHub, left) and [Yeast Biology](https://gitlab.com/acubesat/su/yeast-biology) (GitLab, right)."
%}

Historically the README was the first file you'd read; today it's the first thing you'll see.

Code sharing sites like GitHub and GitLab make the README very prominent on project pages.



{%
  slide
  filename="slide7.png"
  alt="Text slide. It has a title in green 'What should a README tell me?' and three bullet points: 'What is this project?' 'Who should use it?' 'How do they get started?'."
%}

So again, three questions that should be answered by a README: what is the project?
Who should use it?
How do they get started?

You can look at checklists and templates, but I find the best way to know how to write a README is to look at examples.
What do similar projects write?
What's helpful for me?
What do I miss in READMEs that don't have it?

With that in mind, let's look at a few examples.



{%
  slide
  filename="slide9.png"
  alt="Screenshot of the README for readxl."
%}

Let's start with the README for [the readxl package](https://github.com/tidyverse/readxl).
It opens with a clear description of the project:

> The readxl package make it easy to get data out of Excel and into R.

There are a few more sentences of explanation, but this first sentence alone is great.
You can quickly decide if this is a problem you need to solve, or if this project isn't for you.

We already know what problem it solves, and who the target audience is.
If we read on, what's next?



{%
  slide
  filename="slide10.png"
  alt="Screenshot of the README for readxl, with a heading 'Installation'."
%}

Then we have a section on installation, which describes a few different ways to install readxl.

Notice that it assumes a level of familiarity with R – for example, it tells us to run `install.packages("tidyverse")`, and it trusts we'll know how to run that.
A README doesn't have to explain everything from scratch.



{%
  slide
  filename="slide11.png"
  alt="Screenshot of the README for readxl, with a heading 'Usage' and some examples."
%}

Finally, the usage section, with some runnable examples.

I love seeing examples in a README: it's a great way to get a sense of how a package works without installing it -- and then when it is installed, I can run the examples to check it's working correctly.



{%
  slide
  filename="slide12.png"
  alt="Screenshot of the numpy README."
%}

Let's look at a second example: [numpy](https://github.com/numpy/numpy).

This is a pretty popular package (the badges tell us 100M+ downloads a month), so there are lots of people who already know what it does – and the README takes a slightly different approach.
There's a one-line description, then a list of links to other documents we might find useful – the mailing list, bug tracker, documentation, and so on.

The more detailed description doesn't come until further down.



{%
  slide
  filename="slide13.png"
  alt="Screenshot of the README for curl."
%}

Finally, the README for [curl](https://github.com/curl/curl).

Again, lots of links to other pages, assuming you probably already know what curl does.
I find the description a bit dry, and I wouldn't mind having a couple of examples here, for the people who haven't yet encountered curl.


{%
  slide
  filename="slide7.png"
  alt="Text slide. It has a title in green 'What should a README tell me?' and three bullet points: 'What is this project?' 'Who should use it?' 'How do they get started?'."
%}

To repeat the three questions that should be answered by a README.
What is the project?
Who should use it?
How do they get started?

Look at READMEs you like and find useful, and try to copy their style.



{%
  slide
  filename="slide5.jpg"
  alt="A station platform with a green cobbled edge and a black-and-white welcome mat. The welcome mat has a pattern of interspersed diamonds in different colours, and the word 'Welcome' in dark text at the centre. The green cobbled edge runs across the top of the image, and has the text 'What is a README?' overlaid in green."
  caption="Photo: Welcome mat at Tukila Station, by [SonderBruce on Flickr](https://www.flickr.com/photos/sounderbruce/16544240269). Used under CC BY-SA 2.0."
%}

Remember: a README is an introduction to your project.
It's the first file a new user will read, and it helps them to decide whether to spend more time learning about your project.

You can have amazing ideas, do brilliant work, publish it for the world to read – but if nobody knows what your project does, or why it's interesting, it's not very helpful.
A README helps other people get engaged in your project, which is what you need to start spreading your ideas.



{%
  slide
  filename="slide14.png"
  alt="Wrap-up slide, with the title, my name and website address, and a link to these slides."
%}

Wrap up slide.
