---
layout: page
title: Bookmarklets
date_updated: 2024-09-25 20:29:52 +01:00
---
I love [bookmarklets](https://en.wikipedia.org/wiki/Bookmarklet).
They're a useful way to add functionality to browsers without extensions, and to me they represent the spirit of the web that encourages exploration and tinkering.
They come from a time when you could view source on any web page and see something readable, and they still work today!

These are some bookmarklets I find useful.

To add one of my bookmarklets to your own browser, drag the title link to your bookmarks bar.

<style>
  picture + details {
    margin-top: 1em;
  }
</style>

<h2><a href="javascript:(function()%7Bvar%20jsonLdElement%20%3D%20document.querySelector('script%5Btype%3D%22application%2Fld%2Bjson%22%5D')%3Bvar%20jsonLd%20%3D%20JSON.parse(jsonLdElement.innerText)%3Bvar%20datePublished%20%3D%20new%20Date(jsonLd%5B%22datePublished%22%5D)%3Bvar%20format%20%3D%20new%20Intl.DateTimeFormat(%22en-GB%22%2C%20%7Byear%3A%20%22numeric%22%2Cmonth%3A%20%22long%22%2Cday%3A%20%22numeric%22%2C%7D)%3Balert(%60This%20post%20was%20published%20on%20%24%7Bformat.format(datePublished)%7D.%60)%7D)()">Get published date of Tumblr post</a></h2>

Tumblr posts don't always say when they were published, or they show the date in a vague way like "7 years ago".
This bookmarklet pops up a dialog with the exact date a post was published.

{%
  picture
  filename="tumblr_published_date.png"
  parent="_images/bookmarklets/"
  class="screenshot"
  alt="Screenshot of a Tumblr page with a modal alert dialog on top. The modal alert reads ‘This post was published on 24 September 2024’."
  width="532"
%}

<details><summary>Source code</summary>

{% code lang="javascript" names="0:jsonLdElement 3:jsonLd 8:datePublished 11:format" %}
/* In the <head> of each Tumblr post is a block of JSON-LD (=Linked Data)
 * which has some machine-readable info about the post, e.g.
 *
 *     <script type="application/ld+json">
 *       {
 *         "@type": "SocialMediaPosting",
 *         "url": "https:\/\/example.tumblr.com\/post\/12345678\/",
 *         "datePublished": "2015-08-11T07:07:10+00:00",
 *         …
 *       }
 *     </script>
 *
 */
var jsonLdElement = document.querySelector('script[type="application/ld+json"]');
var jsonLd = JSON.parse(jsonLdElement.innerText);
var datePublished = new Date(jsonLd["datePublished"]);

/* Formats a day like "25 September 2024" */
var format = new Intl.DateTimeFormat("en-GB", {
  year: "numeric",
  month: "long",
  day: "numeric",
});

alert(`This post was published on ${format.format(datePublished)}.`);
```

{% endcode %}
</details>
