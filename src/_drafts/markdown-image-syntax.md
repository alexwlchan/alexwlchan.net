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
It's designed to match the Markdown [syntax for links][link_syntax].

The alt text (short for alternative text) is a description which explains the meaning and context of an image.
It's useful for several reasons, and the most well-known reason is probably accessibility.

Imagine a visually impaired user who's using a screen reader – the screen reader can read any text on a page aloud, but what does it read aloud for an image?
If the image includes alt text, that's what the screen reader can use, so the user doesn't miss out on that content.
Writing alt text makes your images more accessible, and it's an excellent habit to get into.

What I like about Markdown's image syntax is that it makes the alt text prominent, and looks wrong when you don't include it:

```
![](/path/to/img.jpg)
```

Those empty square brackets are a visual clue that something is missing.
Even if you don't know what alt text is, you might wonder what's meant to go there.

And if you do know what alt text is, this syntax makes it an explicit choice not to use it.
You know you're choosing not to write alt text -- choosing to exclude visually impaired readers -- and that subtle reminder means you're more likely to go back and add it.

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
It's not a substitute for alt text, and it's not as important – so it's de-emphasised in Markdown's syntax.
An image without a title looks complete, not as if anything's missing.
(In fact, its absence is so unobtrusive that I didn't even realise Markdown had this syntax until I started writing this post!)

Markdown could have hidden the alt text away in a similarly obscure location, where nobody would realise it was missing – but instead, alt text is a prominent part of the syntax.

Markdown's design doesn't force you to use alt text, but it provides gentle encouragement.
It reminds you that images should have alt text, and gives you an easy place to put it.
It's a subtle choice, and one I really like.

When I was writing my README, it was late and I was tired, and I almost skipping writing the alt text for my images – but Markdown reminded me that I should.
I wonder how many other people have made an image more accessible because they saw an empty pair of square brackets.

[img_syntax]: https://daringfireball.net/projects/markdown/syntax#img
[alt_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-alt
[link_syntax]: https://daringfireball.net/projects/markdown/syntax#link
[title_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#the_title_attribute