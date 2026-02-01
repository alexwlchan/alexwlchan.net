---
layout: post
date: 2021-09-28 19:23:39 +00:00
title: An editing toolbar for alexwlchan.net
summary: A bookmarklet that gives me a just-for-me toolbar to make changes to this site.
tags:
  - blogging about blogging
  - javascript
  - bookmarklets
---

I recently wrote a small bookmarklet that gives me an editing toolbar for this site:

{%
  picture
  filename="editing_toolbar.png"
  alt="Screenshot of my website. I have a bookmarks sidebar open in my browser, with an item 'alexwlchan.net toolbar' highlighted in green. There's an arrow from the bookmark pointing to a bar across the top of the site, which says 'Edit this page: on GitHub / in TextMate / See the local dev preview of this page.'"
  width="706"
%}

{% raw %}When I <a href="javascript:(function()%7Bvar%20sourcePath%20%3D%20document.querySelector(%22meta%5Bname%3Dpage-source-path%5D%22).attributes%5B%22content%22%5D.value%3Bif%20(document.location.href.startsWith(%22https%3A%2F%2Falexwlchan.net%2F%22))%20%7Bvar%20altEnvironment%20%3D%20%22local%20dev%20preview%22%3Bvar%20altUrl%20%3D%20document.location.href.replace(%22https%3A%2F%2Falexwlchan.net%2F%22%2C%20%22http%3A%2F%2Flocalhost%3A5757%2F%22)%3B%7D%20else%20%7Bvar%20altEnvironment%20%3D%20%22live%20version%22%3Bvar%20altUrl%20%3D%20document.location.href.replace(%22http%3A%2F%2Flocalhost%3A5757%2F%22%2C%20%22https%3A%2F%2Falexwlchan.net%2F%22)%3B%7D%2F*%20See%20https%3A%2F%2Fstackoverflow.com%2Fq%2F9038625%2F1558022%20*%2Fvar%20iOS%20%3D%20%5B'iPad%20Simulator'%2C'iPhone%20Simulator'%2C'iPod%20Simulator'%2C'iPad'%2C'iPhone'%2C'iPod'%5D.includes(navigator.platform)%20%7C%7C%20(navigator.userAgent.includes(%22Mac%22)%20%26%26%20%22ontouchend%22%20in%20document)%3Bif%20(iOS)%20%7Bdocument.querySelector(%22body%22).innerHTML%20%3D%20%60%3Carticle%20style%3D%22padding-bottom%3A%208px%3B%20padding-top%3A%208px%3B%22%3EEdit%20this%20page%3A%26nbsp%3B%3Cul%20class%3D%22dot_list%22%20style%3D%22display%3A%20inline-block%3B%20margin%3A%200%3B%22%3E%3Cli%3E%3Ca%20href%3D%22https%3A%2F%2Fgithub.com%2Falexwlchan%2Falexwlchan.net%2Fblob%2Flive%2Fsrc%2F%24%7BsourcePath%7D%22%3Eon%20GitHub%3C%2Fa%3E%3C%2Fli%3E%3C%2Ful%3E%3C%2Farticle%3E%60%20%2B%20document.querySelector(%22body%22).innerHTML%3B%7D%20else%20%7Bdocument.querySelector(%22body%22).innerHTML%20%3D%20%60%3Carticle%20style%3D%22padding-bottom%3A%208px%3B%20padding-top%3A%208px%3B%22%3EEdit%20this%20page%3A%26nbsp%3B%3Cul%20class%3D%22dot_list%22%20style%3D%22display%3A%20inline-block%3B%20margin%3A%200%3B%22%3E%3Cli%3E%3Ca%20href%3D%22https%3A%2F%2Fgithub.com%2Falexwlchan%2Falexwlchan.net%2Fblob%2Flive%2Fsrc%2F%24%7BsourcePath%7D%22%3Eon%20GitHub%3C%2Fa%3E%3C%2Fli%3E%3Cli%3E%3Ca%20href%3D%22txmt%3A%2F%2Fopen%3Furl%3Dfile%3A%2F%2F~%2Frepos%2Falexwlchan.net%2Fsrc%2F%24%7BsourcePath%7D%22%3Ein%20TextMate%3C%2Fa%3E%3C%2Fli%3E%3C%2Ful%3E%26nbsp%3B%2F%26nbsp%3BSee%20the%20%3Ca%20href%3D%22%24%7BaltUrl%7D%22%3E%24%7BaltEnvironment%7D%3C%2Fa%3E%20of%20this%20page%3C%2Farticle%3E%60%20%2B%20document.querySelector(%22body%22).innerHTML%3B%7D%7D)()">run the bookmarklet</a>, it adds a toolbar to the top of the page I'm looking at, which lets me do various useful things:{% endraw %}

*   Open the page for editing on GitHub
*   Open the page for editing in my text editor in a local checkout
*   Toggle between the local preview and live versions of the site

I can't imagine anybody else wants this particular bookmarklet, but I'll explain how it works in case anybody else wants to build something similar.

First, I added the following HTML to one of my templates:

```html
{% raw %}<meta name="page-source-path" content="{{ page.path }}">{% endraw %}
```

This is a <a href="https://jekyllrb.com/docs/variables/#page-variables">Jekyll page variable</a> that contains the path to the source code for a page.
For example, on this page this renders as:

{% raw %}
```html
<meta name="page-source-path" content="{{ page.path }}">
```
{% endraw %}

Adding it to the template means it gets baked into every page, and I can read the value with JavaScript.

Then I have some JavaScript which reads the value, and uses it to insert the appropriate blob of HTML at the top of the page:

```javascript
var sourcePath = document.querySelector("meta[name=page-source-path]").attributes["content"].value;

/* I run the site on http://localhost:5757 when working locally, so that's
 * the URL I want to switch to for the dev preview. */
if (document.location.href.startsWith("https://alexwlchan.net/")) {
  var altEnvironment = "local dev preview";
  var altUrl = document.location.href.replace("https://alexwlchan.net/", "http://localhost:5757/");
} else {
  var altEnvironment = "live version";
  var altUrl = document.location.href.replace("http://localhost:5757/", "https://alexwlchan.net/");
}

/* Are we running on iOS? I don't have a local checkout of the repo on iOS
 * and I don't run the localhost version of the site, so adding those links
 * isn't useful.  On iOS, the only link I want is to the GitHub source, so I
 * can do quick edits in the browser.
 *
 * See https://stackoverflow.com/q/9038625/1558022 */
var iOS = [
    'iPad Simulator',
    'iPhone Simulator',
    'iPod Simulator',
    'iPad',
    'iPhone',
    'iPod'
].includes(navigator.platform) || (navigator.userAgent.includes("Mac") && "ontouchend" in document);

if (iOS) {
  document.querySelector("body").innerHTML = `
    <article style="padding-bottom: 8px; padding-top: 8px;">
      Edit this page:&nbsp;
      <ul class="dot_list" style="display: inline-block; margin: 0;">
        <li><a href="https://github.com/alexwlchan/alexwlchan.net/blob/live/src/${sourcePath}">on GitHub</a></li>
      </ul>
    </article>
    ` + document.querySelector("body").innerHTML;
} else {
  /* The link to open in my text editor uses a txmt:// URL, which is the URL
   * scheme for opening files in TextMate, my editor of choice. */
  document.querySelector("body").innerHTML = `
    <article style="padding-bottom: 8px; padding-top: 8px;">
      Edit this page:&nbsp;
      <ul class="dot_list" style="display: inline-block; margin: 0;">
        <li><a href="https://github.com/alexwlchan/alexwlchan.net/blob/live/src/${sourcePath}">on GitHub</a></li>
        <li><a href="txmt://open?url=file://~/repos/alexwlchan.net/src/${sourcePath}">in TextMate</a></li>
      </ul>
      &nbsp;/&nbsp;
      See the <a href="${altUrl}">${altEnvironment}</a> of this page
    </article>
    ` + document.querySelector("body").innerHTML;
}
```

Fun fact: this is my first time using [JavaScript template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals), which are a super nice feature I wish I'd known about before.
I'm only about five years behind the cutting edge of web development!

I used [Peter Coles's bookmarklet creator](https://mrcoles.com/bookmarklet/) to turn this into my bookmarklet, and now I have an editing toolbar I can get whenever I need it.
It's been particularly useful when I want to make edits on my phone -- I can jump from a page to the source code in GitHub, make a tweak in GitHub's editor, and my [continuous deployment pipeline](/about-the-site/) will publish the updated version shortly afterwards.

I can't imagine anyone else wants this exact bookmarklet, but if you have your own static site then something like this might be useful.
