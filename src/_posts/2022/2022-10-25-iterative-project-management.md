---
layout: post
date: 2022-10-25 08:07:13 +0000
title: Agile and iterative project management
summary: Notes from a talk about agile and iterative approaches to project management.
tags: talks open-life-science project-management
theme:
  color: "#20883f"
index:
  image: /images/2022/agile_ols_card.png
---

Earlier today, I gave a talk for the [the Open Life Science Program][openlife] about agile and iterative project management.
I was talking about how READMEs serve as the first point of contact for a project; how they get new users interested in and excited about the project.

The cohort calls are recorded, and I'll add a link to the video when it's posted.
In the meantime, you can download my slides [as a PDF][pdfslides], and I'll add some notes shortly.

[openlife]: https://openlifesci.org/
[pdfslides]: /files/2022/ols-6-agile.pdf



https://agilemanifesto.org
https://en.wikipedia.org/wiki/Agile_software_development
https://en.wikipedia.org/wiki/Waterfall_model

<style>
  .slide img {
    border: 3.5px solid #2ec65c;
  }

  #ols_6_agile-5 img {
    border-color: #263f83;
  }
</style>




## Slides and notes

{%
  slide_image
  :deck => "ols_6_agile", :slide => 1,
  :alt => "Title slide. It includes my name (Alex Chan), my pronouns (they/she), and a URL pointing to these slides."
%}

Title slide.

I'm going to talk about what agile and iterative project management methods are, where they come from, and why they might be good for your project.

I work at Wellcome Collection, a museum and library in London, and we do iterative project management, so I'll be drawing on examples of my own work for this talk.



{%
  slide_image
  :deck => "ols_6_agile", :slide => 2,
  :alt => "A set of green circular arrows: break down big tasks into smaller tasks, work through the smaller tasks, review/update your tasks."
%}

Agile is an approach to project management tool; it's a way of managing your tasks.
You might be doing some of it already, so I want to jump straight in.

In an iterative project, you:

1.  Break down your tasks into smaller tasks
2.  Work through the smaller tasks
3.  Review/update your tasks

Most people are already familiar with steps 1 and 2; but step 3 is super important and it's the bit people often miss.
This cycle gets us a fast feedback loop for our task management.

Stays in a cycle, like Sara was talking about earlier

​{%
  slide_image
  :deck => "ols_6_agile", :slide => 3,
  :alt => "Text slide. Building iteratively means you can react to new info or requirements, gather feedback quickly, and always be doing something important."
%}

Working in this iterative style gives you a number of benefits:

*   you can react to new info or requirements
*   gather feedback quickly
*   always be doing something important

You're not tied to a plan you made six months ago that's no longer relevant; because you're doing a regular review of your plans you can stay up-to-date.

The best example from recent years is the COVID-19 pandemic.
A lot of plans got thrown up in the air in early 2020; if you already used to an iterative approach to project management, you were better placed to adapt to changing circumstances.

{%
  slide_image
  :deck => "ols_6_agile", :slide => 2,
  :alt => "A set of green circular arrows: break down big tasks into smaller tasks, work through the smaller tasks, review/update your tasks."
%}

Repeat previous slide.

This is iterative development.

This is an idea that's come out of the software development community, and seen a massive spike in the last decade or so.
Why's there such a buzz?
To understand this, we need to understand what came before.


{%
  slide
  :deck => "ols_6_agile", :slide => 5,
  :alt => "A series of three blue boxes forming a waterfall. The first box is 'Design and requirements', the second is 'Implementation and testing', the third is 'Deployment and maintenance'."
%}
  Waterfall icon by <a href="https://thenounproject.com/icon/waterfall-3411/">Luis Prado on the Noun Project</a>.
  Used with a <a href="https://thenounproject.com/pricing/">NounPro subscription</a>.
{% endslide %}

The old approach to software development was called "waterfall", and this diagram gives an idea why.
The project gets broken down into distinct phases, and each phase blocks the next phase.

You started with all your design, requirements finding, business analysis.
That happened upfront, and produced a spec, a written document that was usually several inches thick.
You didn't do any coding until the spec was written.

Then you'd give the spec to a team of programmers, who'd write all the code, and hand off a single version of the software for distribution and deployment.

This comes from a time when computing was very different – computers were much less powerful, they weren't as numerous, and most software was distributed on plastic disks rather than over the web.
There were very slow feedback loops.

In the 21st century, software development has changed, and this model was less and less appropriate.


{%
  slide
  :deck => "ols_6_agile", :slide => 6,
  :alt => "Screenshot of a web browser showing the Agile Manifesto."
%}
  <a href="https://agilemanifesto.org">https://agilemanifesto.org</a>
{% endslide %}

In 2001, a group of developers published the "agile manifesto", which helped popularise these ideas.

This started the big push towards agile that we see today -- some of it was new ideas, some of it was a new face for existing ideas.
(Iterative methods go back way further than 2001!)



{%
  slide_image
  :deck => "ols_6_agile", :slide => 7,
  :alt => "Minimum Viable Product. The first line shows the evolution of a skateboard, to a scooter, to a pushbike, to a motorbike, to a car. The second line shows the building of a car, from the wheels, to a chassis, to a body, to a car."
%}

One of the big ideas to come out of the agile manifesto was the idea of a "minimum viable product" or "MVP".
We've talked about how you break a big task down into smaller tasks; MVP says that we should try to iterate on working versions.
Each of those smaller steps should produce useful output that we can use, react to, get feedback on.

This has obvious advantages for commercial software, but it's great for research as well – we can get feedback and review our assumptions as we go along.

This is an almost clichéd diagram when talking about MVP: the evolution of wheeled transport.
Following MVP means you go from a skateboard, to a scooter, to a pushbike, to a motorbike, to a car.
We could stop at any point and still have something useful.



{%
  slide_image
  :deck => "ols_6_agile", :slide => 8,
  :alt => "The same diagram as before, but now with offshoots from scooter to e-scooter and motorbike to cargo bike."
%}

Following MVP means we can react to new information and feedback.
Maybe we discover that people love the form factor of the scooter but want to go up hills – so rather than making a pushbike, we should make an e-scooter.
Or maybe the motorbike is a flop, and what people really wanted was a bike with more carrying capacity, so we should switch to making cargo bikes.



{%
  slide_image
  :deck => "ols_6_agile", :slide => 9,
  :alt => "The quote ‘Fail fast, fail often’, an agile proverb."
%}

This is another phrase you might have heard, which is a pithy form of the agile manifesto.
Failure is a necessary part of iteration: you learn from your mistakes.

I include this because it's a cliché, and to illustrate that waterfall and agile aren't better/worse than each other; they're appropriate in different scenarios.
They exist on a spectrum.

Making lots of mistakes on the way to success is fine if you're making a game, or a website, or an app.
It's not so good if you're designing a plane, a banking service, or a drug trial.

Iterative approaches have become very popular, but waterfall still has a place.
