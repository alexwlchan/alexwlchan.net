---
layout: post
title: Markdown’s gentle encouragement towards accessible images
summary: The Markdown syntax for images reminds us that we need to write alt text.
tags: markdown accessibility
---

I was using Markdown to write a README the other night, and I noticed something rather nice about the [syntax for images][img_syntax].
This is how you define an image in Markdown:

```
![Alt text](/path/to/img.jpg)
```

You start with an exclamation mark `!`, then the [alt text description][alt_attribute] in square brackets, then the URL or path to the image in parentheses.
It's meant to mirror the Markdown [syntax for links][link_syntax], which looks very similar.

The alt text (short for alternative text) is a description which explains the meaning and context of an image.
It's useful for several reasons, and the most well-known reason is probably accessibility.

Imagine a visually impaired user who's using a screen reader – the screen reader can read any text on a page aloud, but what does it read aloud for an image?
If the image includes alt text, it can use that, so the user doesn't miss out on that content.
Writing alt text makes your images more accessible, and it's an excellent habit to get into.

What I like about Markdown's image syntax is that it makes the alt text prominent, and looks wrong when you don't include it:

```
![](/path/to/img.jpg)
```

Those empty square brackets are a visual clue that something is missing.
Even if you don't know what alt text is, you might wonder what's meant to go there.

And if you do know what alt text is and what this syntax means, you know you're choosing not to write it -- choosing to exclude visually impaired users -- and if that choice is made explicit, maybe you'll go back and fill it in.

Compare to the equivalent HTML:

```
<img src="/path/to/img.jpg">
```

This is valid HTML, but there's no alt text and nothing to suggest that anything’s missing.
Unless you already know about alt text, this looks fine.

Compare also to Markdown's syntax for [the `title` attribute][title_attribute]:

```
![Alt text](/path/to/img.jpg "Optional title")
```

The title is usually shown as a tooltip, when somebody hovers their cursor over an image.
It's not a substitute for alt text, and it's nowhere near as important – and that's reflected in the Markdown syntax.
An image without a title looks complete, not as if anything's missing.
(In fact, its absence is so unobtrusive that I didn't even realise Markdown had this syntax until I started writing this post!)

Markdown could have hidden the alt text away in a similarly obscure location, where nobody would realise it was missing – but instead, alt text is a prominent part of the syntax.

Markdown's design doesn't force you to use alt text, but it provides gentle encouragement.
The more I think about it, the more I like it.
I wonder how many people have made an image more accessible because they saw an empty pair of square brackets – I know I'm one of them.

[img_syntax]: https://daringfireball.net/projects/markdown/syntax#img
[alt_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-alt
[link_syntax]: https://daringfireball.net/projects/markdown/syntax#link
[title_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#the_title_attribute