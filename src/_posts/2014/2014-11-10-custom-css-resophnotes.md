---
date: 2014-11-10T18:41:00Z
layout: post
title: Custom CSS in ResophNotes
is_unlisted: true
---

My note-taking app of choice is [nvALT][nv], but since I have to use Windows at work, I've also been using [ResophNotes][resoph], which seems to be the closest alternative you can get. I have a *lot* of notes: any error code, bugfix or useful titbit gets saved there, because trying to remember what a cryptic error message that you saw two weeks ago actually meant gets boring really fast.

Most of the time I read the plain Markdown, but for complicated notes I'll use the Markdown preview. But the preview window isn't the prettiest thing ever:

{%
  picture
  filename="resophnotes-unstyled.png"
  width="835"
  alt="A window with unstyled text. The text contains headings and a few paragraphs."
%}

I was used to [customising the preview in nvALT][prev], so I wanted to do the same for ResophNotes. This turned out to be easy to do, but it wasn't entirely obvious how to do it.

The only reference to custom CSS that I could find was this slightly cryptic [changelog][log] from August 2010:

> Add a link "resophnotes.css" in "Markdown" generated HTML file

And indeed, if you look at the HTML source of the preview page, you find that it is loading this file:

    ::html
    <link href="resophnotes.css" rel="stylesheet" type="text/css">

Initially I assumed that this was a preexisting file that I'd edit, so I was a bit confused when I couldn't find any such file. Eventually I realised that it didn't exist yet, and I found the directory where ResophNotes keeps the temporary HTML: the ".ResophNotes" directory in the home folder.

{%
  picture
  filename="resophnotes-directory.png"
  width="900"
  alt="A directory in Windows Explorer: Alex Chan/.ResophNotes, with four files. resophmarkdown, resophnotes, resophnotesconfig and resophnotesdata."
%}

Dropping a CSS file named `resophnotes.css` there gets it applied to the Markdown preview:

{%
  picture
  filename="resophnotes-styled.png"
  width="835"
  alt="A window with text styled in a sans-serif font."
%}

Much nicer.

[prev]: http://brettterpstra.com/2013/04/06/customizing-the-nvalt-preview/

[nv]: http://brettterpstra.com/projects/nvalt/
[resoph]: http://resoph.com/ResophNotes/Welcome.html

[log]: http://resoph.com/ResophNotes/Change_Log.html