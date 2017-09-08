---
date_added: 2014-11-10 18:41
layout: page
minipost: true
slug: notes/custom-css-resophnotes
title: Custom CSS in ResophNotes
---

My note-taking app of choice is [nvALT][nv], but since I have to use Windows at work, I've also been using [ResophNotes][resoph], which seems to be the closest alternative you can get. I have a *lot* of notes: any error code, bugfix or useful titbit gets saved there, because trying to remember what a cryptic error message that you saw two weeks ago actually meant gets boring really fast.

Most of the time I read the plain Markdown, but for complicated notes I'll use the Markdown preview. But the preview window isn't the prettiest thing ever:

![](/images/notes/resophnotes-unstyled.png)

I was used to [customising the preview in nvALT][prev], so I wanted to do the same for ResophNotes. This turned out to be easy to do, but it wasn't entirely obvious how to do it.

<!-- summary -->

The only reference to custom CSS that I could find was this slightly cryptic [changelog][log] from August 2010:

> Add a link "resophnotes.css" in "Markdown" generated HTML file

And indeed, if you look at the HTML source of the preview page, you find that it is loading this file:

    ::html
    <link href="resophnotes.css" rel="stylesheet" type="text/css">

Initially I assumed that this was a preexisting file that I'd edit, so I was a bit confused when I couldn't find any such file. Eventually I realised that it didn't exist yet, and I found the directory where ResophNotes keeps the temporary HTML: the ".ResophNotes" directory in the home folder.

![](/images/notes/resophnotes-directory.png)

Dropping a CSS file named `resophnotes.css` there gets it applied to the Markdown preview:

![](/images/notes/resophnotes-styled.png)

Much nicer.

[prev]: http://brettterpstra.com/2013/04/06/customizing-the-nvalt-preview/

[nv]: http://brettterpstra.com/projects/nvalt/
[resoph]: http://resoph.com/ResophNotes/Welcome.html

[log]: http://resoph.com/ResophNotes/Change_Log.html
