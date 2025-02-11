---
layout: post
title: Creating static websites with JavaScript metadata and templating
summary:
tags:
colors:
  index_light: "#535353"
  index_dark:  "#cecece"
tags:
  - static sites
index:
  feature: true
---
Last year I wrote about [using static websites for tiny archives][static_sites].
Modern web tech is powerful, portable, and likely to remain readable for a long time.
I've been converting more and more of my local data to be stored in static websites, and I really like this approach.

[static_sites]: /2024/static-websites/

I got a lot of positive feedback on the post, but the most common reply was "can you give an example".
People wanted to see examples of the HTML and JavaScript I was using.
I deliberately omitted these examples from the original post, for a couple of reasons.

I wanted to focus on the concept, not the detail.
I was trying to persuade people that static websites are a good idea for this use cases, and I didn't want to get distracted by implementation details or code snippets.

There are lots of ways to build websites; I think that's the beauty of the web.
My own static site collection has a lot of variety -- no two sites are the same.
I want people to have their own ideas and build their own websites; not just copy what I'm doing.

Although I didn't want to provide technical detail in that post, I do have ideas about how you build this sort of site.
There's a common pattern emerging: metadata stored in JSON, rendered as HTML using JavaScript and template literals.
That's what I'm going to explain today.

This requires more technical skill than writing plain HTML, which is another reason I didn't describe it in the original post -- there are much simpler ways to get started, and I don't want anyone to be put off.
Websites should be for everyone!

I’m going to describe the key ideas, go through some more advanced features, and in a future post I'll show you a specific example of this approach.

---

## A medium viable website

Here's an absolutely tiny bookmarks website -- an HTML list of links that I edit by hand.
If you [save this to a file](/files/2025/mvp-bookmarks-page.html), you'll see a bulleted list.
This is an excellent way to get started.

```html
<h1>Bookmarks</h1>

<ul>
  <li><a href="https://estherschindler.medium.com/the-old-family-photos-project-lessons-in-creating-family-photos-that-people-want-to-keep-ea3909129943">Lessons in creating family photos that people want to keep, by Esther Schindler (2018)</a></li>
  <li><a href="https://www.theatlantic.com/technology/archive/2015/01/why-i-am-not-a-maker/384767/">Why I Am Not a Maker, by Debbie Chachra (The Atlantic, 2015)</a></li>
  <li><a href="https://meyerweb.com/eric/thoughts/2014/06/10/so-many-nevers/">So Many Nevers, by Eric Meyer (2014)</a></li>
</ul>
```

As this list gets longer, it gets a bit tedious to keep copy/pasting the HTML markup, and there's no way to sort or filter the list.
Wouldn't it be useful if we could separate the data and the presentation?

What I do for my larger collections is to define the metadata in JSON, then use JavaScript and template literals to render it on the page.
Here's an example:

```html
<script>
  const bookmarks = [
    {
      "url": "https://estherschindler.medium.com/the-old-family-photos-project-lessons-in-creating-family-photos-that-people-want-to-keep-ea3909129943",
      "title": "Lessons in creating family photos that people want to keep, by Esther Schindler (2018)"
    },
    {
      "url": "https://www.theatlantic.com/technology/archive/2015/01/why-i-am-not-a-maker/384767/",
      "title": "Why I Am Not a Maker, by Debbie Chachra (The Atlantic, 2015)"
    },
    {
      "url": "https://meyerweb.com/eric/thoughts/2014/06/10/so-many-nevers/",
      "title": "So Many Nevers, by Eric Meyer (2014)"
    }
  ];

  function Bookmark(bookmark) {
    return `
      <li>
        <a href="${bookmark.url}">${bookmark.title}</a>
      </li>
    `;
  }

  window.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#listOfBookmarks").innerHTML =
      bookmarks.map(Bookmark).join("");
  });
</script>

<h1>Bookmarks</h1>

<ul id="listOfBookmarks"></ul>
```

There's quite a lot going on, even in this short snippet:

*   The variable `bookmarks` is a [list of JSON objects][json].
    Each object has two fields for each bookmark: a URL and a title.

*   The function `Bookmark` takes a single bookmark as input, and uses a [template literal] to render it as HTML.
    This means we only have to write the `<li><a href="…">…</a></li>` markup once.

    Having a function that renders HTML is inspired by React and Next.js, where code is split into "components" that renders part of the app.
    My version is simple and only renders the HTML once -- unlike React, it won't re-render if the data changes –- which is fine for rendering a page with static data.
    It's rendered once on page load, and that's enough.

    I know there are other ways to do this, like the [`<template>` element][template_elem] and [Web Components], but template literals work fine for me, and I've never had a reason to explore more sophisticated options.

    You wouldn't do this if you had untrusted metadata -- anybody could just inject arbitrary HTML into your page -- but I'm writing all my metadata, so I trust it.

*   Then I'm listening for the [`DOMContentLoaded` event][DOMContentLoaded], which fires when the HTML page has been fully parsed.
    This means I can find the `<ul id="listOfBookmarks">` which is further down the page, and insert the rendered HTML for my list of bookmarks.
    We have to wait for this event so the `<ul>` actually exists to target.

    I'm using [`querySelector()`][querySelector] to find the element I'm looking for -- this is a newer alternative to functions like [`getElementById()`][getElementById].
    It's quite flexible, because I can target any CSS selector, and I find CSS rules easier to remember than the family of `getElementBy*` functions.
    Although it's slightly slower in benchmarks, the difference is negligible and it's easier for me to remember.

This sort of design is how a lot of my static sites start -- metadata in JSON, some React-like functions that render HTML, and an event listener that renders the whole page after it loads.

Once I have the basic site working, I add more HTML in the rendering functions, and CSS styles to make it look pretty.
This is where I can have fun, and really customise each site.
There's no rhyme or reason to this -- I just keep tweaking until I have something I'm happy with.

What else can we do?

[json]: https://www.json.org/json-en.html
[template literal]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
[template_elem]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template
[Web Components]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components
[DOMContentLoaded]: https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event
[querySelector]: https://developer.mozilla.org/en-US/docs/Web/API/Element/querySelector
[getElementById]: https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById

* Filtering
* Sorting

---

## Filtering

As the list gets longer, it's useful to have some filters so I can find things quickly.
I like using keyword tags for everything, so I could filter for items with a particular tag -- or I could add other metadata fields to filter on, like author and date.

Here's a brief sketch of the sort of interface I like to build:

{%
  picture
  filename="js_filters_sketch.png"
  width="550"
  alt="A crude sketch of a simple app. At the top is a list of three filters (tagged with animals, tagged with wtf, published in 2025) and a red 'x' to dismiss them. Below that are three items, each with a list of tags below it."
%}

I can define a series of filters, and apply them to focus on a specific subset of items.
I can combine multiple filters to refine my search further, and I can see a list of applied filters with a way to dismiss them.
I can either apply a filter from a global menu, or using controls on each item to find similar items.

I use URL query parameters to store the list of currently-applied filters, for example:

```
bookmarks.html?tag=animals&tag=wtf&publicationYear=2025
```

Any UI element that adds or removes a filter is a link, so the page URL changes -- this triggers a re-render with the new filters.

I'm taking advantage of the fact that URL query parameters are repeatable.
This is something I rarely see on other sites, but now I use it regularly -- it's a standard way to store a list of values in a URL, and there are lots of libraries that can extract the values as a list.
I don't need to come up with my own approach.

Here's a rough sketch of the code I use for filtering:

```javascript
const bookmarkFilters = [
  {
    key: 'tag',
    label: 'tagged with',
    filterFn: (bookmark, tagName) => bookmark.tags.includes(tagName),
  },
  {
    key: 'publicationYear',
    label: 'published in',
    filterFn: (bookmark, year) => bookmark.publicationYear === year,
  },
];

/*
 * Filter a list of items.
 *
 * It takes the list of items and available filters, and the
 * URL query parameters passed to the page.
 *
 * It returns a list with the items that match these filters,
 * and a list of filters that have been applied.
 */
function filterItems({ items, filters, params }) {

  // By default, all items match, and no filters are applied.
  var matchingItems = items;
  var appliedFilters = [];

  // Go through the URL query params one by one, and look to
  // see if there's a matching filter.
  for (const [key, value] of params) {
    console.debug(`Checking query parameter ${key}`);
    const matchingFilter = filters.find(f => f.key === key);

    if (typeof matchingFilter === 'undefined') {
      continue;
    }

    // There's a matching filter!  Go ahead and filter the
    // list of items to only those that match.
    console.debug(`Detected filter ${JSON.stringify(matchingFilter)}`);

    matchingItems = matchingItems.filter(
      item => matchingFilter.filterFn(item, value)
    );

    // Construct a new query string that doesn't include
    // this filter.
    const altQuery = new URLSearchParams(params);
    altQuery.delete(key, value);
    const queryIfRemoved = altQuery.toString();

    appliedFilters.push({
      type: matchingFilter.key,
      label: matchingFilter.label,
      value,
      queryIfRemoved,
    })
  }

  return { matchingItems, appliedFilters };
}
```

The `filterItems` is deliberately generic -- it takes a list of items and a list of known filters, then applies those filters to the items.
The key part of the `bookmarkFilters` array is the `filterFn` entry, which takes a bookmark and a filter value, and returns true/false depending on whether the bookmark matches the filter.
Making this generic has two benefits: it allows me to reuse this code between projects, and it makes it fairly easy to add new filter options.

It returns the list of matching items, and the list of applied filters.
The latter allows me to show that list in the UI.

Here's a quick example of how you might wire this new function into the page:

```html
<script>
  window.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);

    const { matchingItems: matchingBookmarks, appliedFilters } =
      filterItems({
        items: bookmarks,
        filters: bookmarkFilters,
        params: params,
      });

    document.querySelector("#appliedFilters").innerHTML =
      appliedFilters
        .map(f => `<li>${f.label}: ${f.value} <a href="?${f.queryIfRemoved}">(remove)</a></li>`)
        .join("");

    document.querySelector("#listOfBookmarks").innerHTML =
      matchingBookmarks.map(Bookmark).join("");
  });
</script>

<p>Applied filters:</p>
<ul id="appliedFilters"></ul>

<p>Bookmarks:</p>
<ul id="listOfBookmarks"></ul>
```

I pretty much always stick to "simple" filters that can be phrased as a boolean ("does this item match, yes/no").
I rely on my past self to provide sufficiently useful metadata that I can find stuff again later.

I've never implemented anything more like a search, where the filter logic of whether to match something is more fuzzy.

## Sorting

The next



---





---

More features you could add:
* sorting
* filtering
* pagination
put all of those inside the `window.addEventListener` block to cut down the list of entries to the specific slice you want to show rn

Noscript and errors

Bonus features:
* tests using QUnit
* manipulate JS using Python scripts, put metadata in separate file
* Playwright

Will be posting an example of a site using this pattern soon