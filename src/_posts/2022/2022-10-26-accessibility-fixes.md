---
layout: post
date: 2022-10-26 18:58:54 +00:00
title: Some small accessibility fixes
summary: Making the sites I work on sound a bit nicer for anyone who relies on screen readers.
tags:
  - accessibility
  - blogging about blogging
colors:
  css_light: "#075ba3"
  css_dark:  "#198ff5"
index:
  exclude: true
---

I've been doing a bunch of testing with VoiceOver recently, helping to [prepare the digital guides for a new exhibition at work][ips].
I like to think my site is already pretty accessible -- I put alt text on my images and I use semantic HTML -- but I did find a few rough edges to fix.
None of these were big or tricky, but I hope they make the site a bit nicer for screen reader and keyboard-only users.

[ips]: https://twitter.com/ExploreWellcome/status/1584911184242909184

---

## Skip to main content

A [skip navigation link][skipnav] allows a screen reader or keyboard-only user to jump straight to the main content.
This saves them paging through any navigation links at the top of the page.
It's invisible to sighted users, who can skip to the main content by just looking down.

Even my fairly small nav wants you to page through ten elements to get to the main content -- and now you can skip that in a single tap.

{%
  picture
  filename="IMG_1877.png"
  alt="Viewing this web page with VoiceOver in the browser. There's a dark outlined rectangle highlighting the invisible link, and the VoiceOver caption shows 'Skip to main content, in-page link'."
  width="609"
  class="screenshot"
%}

This took [less than two minutes to add][commit], and given I'd definitely heard of them before, there's no excuse for not having done this sooner.

[skipnav]: https://accessibility.oit.ncsu.edu/it-accessibility-at-nc-state/developers/accessibility-handbook/mouse-and-keyboard-events/skip-to-main-content/
[commit]: https://github.com/alexwlchan/alexwlchan.net/commit/342018fe2689412570d40cc02e33780ae7307e56

---

## Better telephone numbers

The Wellcome Collection website has quite a few phone numbers on it, and while testing I discovered that they don't scan so well.
This is read all in one go:

> plus forty-four zero two zero seven six one one two-thousand two hundred and twenty-two

This doesn't sound like how most people read phone numbers.

I found [a blog post by Joni Halabi][phone], which suggests using [an aria-label attribute][aria-label] to help screen readers.
I've added these throughout the site, and now numbers sound more natural:

> plus four four (pause) zero two zero (pause) seven six one one (pause) two two two two

This includes [a function to create the labels][function], so this behaviour can be applied to all numbers on the site (and not just the hard-coded number in the footer, where I first found this issue).

[phone]: https://jhalabi.com/blog/accessibility-phone-number-formatting
[aria-label]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label
[function]: https://github.com/wellcomecollection/wellcomecollection.org/blob/76634b1af35e8f64b7a63b52e0afd53cbeb38ff2/common/utils/telephone-numbers.ts

---

## Pronunciation hints for proper nouns

Using aria-label for phone numbers made me think of customising other text too.
There are a few places on the site where I have proper nouns which screen readers struggle with -- compound words are a particular challenge.

These are a few of the nouns where I've added alternative pronunciations.
I think they sound better, and you're more likely to understand what's being said:

<style>
  td {
    width: 25%;
  }

  table, tr {
    border-collapse: collapse;
  }

  th, td {
    padding: 5px;
  }

  td {
    vertical-align: top;
  }
</style>

<table>
  <tr style="border-top: 3px solid #075ba3; border-bottom: 3px solid #075ba3; background: rgba(7, 91, 163, 0.15);">
    <th>text</th>
    <th>default pronunciation</th>
    <th>aria-label</th>
    <th>improved pronunciation</th>
  </tr>
  <tr>
    <td>alexwlchan</td>
    <td>al-ecks-well-chun</td>
    <td>alex w l chan</td>
    <td>al-ecks-double-you-el-chan</td>
  </tr>
  <tr>
    <td>IIIF</td>
    <td>eye-eye-eye-eff</td>
    <td>triple I F</td>
    <td>triple-eye-eff</td>
  </tr>
  <tr>
    <td>urllib3</td>
    <td>err-lib-three</td>
    <td>url lib 3</td>
    <td>you-are-ell-lib-three</td>
  </tr>
  <tr>
    <td>nosetests</td>
    <td>noz-tests</td>
    <td>nose tests</td>
    <td>know-se tests</td>
  </tr>
  <tr style="border-bottom: 3px solid #075ba3;">
    <td>3&frac12;&Prime; floppy disk</td>
    <td>three and a half floppy disk</td>
    <td>three and a half inch floppy disk</td>
    <td>three and a half inch floppy disk</td>
  </tr>
</table>

These were slightly more complicated, because not all of these nouns appear in semantic elements where I can use `aria-label`.
If they're in the middle of a longer bit of text, I'd want to use `<span>`, but screen readers ignore labels on that tag.

Instead, I had to create two tags:

```html
<span class="visually-hidden">triple I F</span>  <!-- for screen readers -->
<span aria-hidden="true">IIIF</span>             <!-- for sighted users  -->
```

The CSS for the class on the first span means it will be hidden in the visual presentation of the page; the [aria-hidden attribute][hidden] on the second means it will be ignored by screen readers.

I also had to [add the text role][text_role] to parent elements, so VoiceOver on iOS would read the text as a continuous string -- rather than pausing on the proper noun.

To avoid Braille users getting the spelled-out version, I'm also setting the [aria-braillelabel attribute][braillelabel].
Unfortunately I don't have a Braille display to test with, so this is somewhat speculative.

So far I've only done this on a handful of pages, because I suspect trying to fix this automatically would create more problems than it solves – but I'm considering it, and I'll definitely try to remember to do it on new posts.

I have plenty more to learn about accessibility, and it's not something that's ever "done" – but I hope these are steps in the right direction.

[hidden]: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-hidden
[text_role]: https://tinytip.co/tips/a11y-voiceover-text-role/
[braillelabel]: https://developer.mozilla.org/en-US/docs/web/Accessibility/ARIA/Attributes/aria-braillelabel
