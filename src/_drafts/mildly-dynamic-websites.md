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
✨ Splitting data and presentation
✨ Pagination, filtering and sorting
✨ User-visible errors when things go wrong
✨ And tests, if you really want them

Last year I wrote about [using static websites for tiny archives][static_sites].
The idea is that I create tiny websites to store and describe my digital collections.
HTML is flexible and lets me display data in a variety of ways; it's likely to remain readable for a long time; it lets me add more context than a folder full of files.

I'm converting more and more of my local data to be stored in static websites -- paperwork I've scanned, screenshots I've taken, and web pages I've bookmarked.
I really like this approach.

I got a lot of positive feedback on the post, but the most common reply was "can you give an example".
People wanted to see examples of the HTML and JavaScript I was using, or for me to share my source code.
I deliberately omitted any code from the original post, because I wanted to focus on the concept, not the detail.
I was trying to persuade you that static websites are a good idea for storing small archives and data sets, and I didn't want to get distracted by implementation ideas or code snippets.

There's also no single code base I could share – every site I build is different, and the code is often scrappy or poorly documented.
It would be difficult to read or understand what's going on.

However, there's clearly an appetite for that sort of explanation, so this follow-up post will discuss the "how" rather than the "why".
There's a lot of code, especially JavaScript, which I'll be explaining in small digestible snippets.
This requires more technical skill than writing plain HTML, which is another reason I didn't describe this in the original post -- there are much simpler ways to get started, and I don't want anyone to be overwhelmed or put off.

I'll go through a feature at a time, as if we were building a new static site.
I'll use bookmarks as an example, but there's nothing in this post that's specific to bookmarking.

If you'd prefer to look at complete working examples, I've made [a demo site] where you can see everything in one place.

This is a long, code-heavy post, so grab a hot drink and let's dive in!

* [Start with a hand-written HTML page](#hand-written-html) ([demo](/files/2025/static-site-demo.html?demoId=hand-written-html))
* [Reduce repetition with JavaScript templates](#template-literals) ([demo](/files/2025/static-site-demo.html?demoId=template-literals))
* [Add filtering to find specific items](#filtering) ([demo](/files/2025/static-site-demo.html?demoId=filtering))

[static_sites]: /2024/static-websites/
[a demo site]: /files/2025/static-site-demo.html

---

<h2 id="hand-written-html">Start with a hand-written HTML page</h2>

A website can be a single HTML file you edit by hand.
Open a text editor like TextEdit or Notepad, copy-paste the following text, and save it in a file named `bookmarks.html`.

```html
<h1>Bookmarks</h1>

<ul>
  <li><a href="https://estherschindler.medium.com/the-old-family-photos-project-lessons-in-creating-family-photos-that-people-want-to-keep-ea3909129943">Lessons in creating family photos that people want to keep, by Esther Schindler (2018)</a></li>
  <li><a href="https://www.theatlantic.com/technology/archive/2015/01/why-i-am-not-a-maker/384767/">Why I Am Not a Maker, by Debbie Chachra (The Atlantic, 2015)</a></li>
  <li><a href="https://meyerweb.com/eric/thoughts/2014/06/10/so-many-nevers/">So Many Nevers, by Eric Meyer (2014)</a></li>
</ul>
```

If you double-click this file to open it in your web browser, you'll see a list of three links.
(Or you can [look at my demo page](/files/2025/static-site-demo.html?demoId=hand-written-html).)

This is an excellent way to build a website.
If you stop here, you've got all the flexibility and portability of HTML, and this file will remain readable for a very long time.



<h2 id="template-literals">Reduce repetition with JavaScript templates</h2>

As you store more data, it gets a bit tedious to keep copying the HTML markup for each item.
Wouldn't it be useful if we could push it into some sort of reusable template?

When a site gets bigger, I move the metadata into [JSON][json], then I use JavaScript and template literals to render it on the page.

Let's start with a simple example of metadata in JSON.
My real data has more fields, like date saved or a list of keyword tags, but this is enough to get the idea:

```javascript
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
```

Then I have a function that renders the data for a single bookmark as HTML:

```javascript
function Bookmark(bookmark) {
  return `
    <li>
      <a href="${bookmark.url}">${bookmark.title}</a>
    </li>
  `;
}
```

Having a function that returns HTML is inspired by React and Next.js, where code is split into "components" that renders part of the app.
This function is simple and only renders the HTML once -- unlike React, it won't re-render if the data changes -- but that's okay, because my data isn't going to change.
The HTML gets rendered once on page load, and that's enough.

I'm using a [template literal] because I find it simple and readable.
It looks pretty close to the actual HTML, so I have a pretty good idea of what's going to render on the page.

Template literals are pretty risky if you're getting data from an untrusted source -- it could allow somebody to inject arbitrary HTML into your page -- but I'm writing all my metadata, so I trust it.

I know there are other ways to do this sort of thing, like constructing DOM elements directly, the [`<template>` element][template_elem], or [Web Components] -- but template literals have always been sufficient for me, and I've never had a reason to explore other options.
  
Now we have to use this function to render the bookmarks on the page.
Here's the rest of the code:

```html
<script>
  window.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#listOfBookmarks").innerHTML =
      bookmarks.map(Bookmark).join("");
  });
</script>

<h1>Bookmarks</h1>

<ul id="listOfBookmarks"></ul>
```

I'm listening for the [`DOMContentLoaded` event][DOMContentLoaded], which occurs when the HTML page has been fully parsed.
When that event occurs, it looks for `<ul id="listOfBookmarks">` in the page, and inserts the HTML for the list of bookmarks.
  
We have to wait for this event so the `<ul>` actually exists.
If we tried to run it immediately, it might run *before* the `<ul>` exists, and then it wouldn't know where to insert the HTML.

I'm using [`querySelector()`][querySelector] to find the `<ul>` I want to modify -- this is a newer alternative to functions like [`getElementById()`][getElementById].
It's quite flexible, because I can target any CSS selector, and I find CSS rules easier to remember than the family of `getElementBy*` functions.
Although it's slightly slower in benchmarks, the difference is negligible and it's easier for me to remember.

If you want to see this in action, check out [the demo page][demo_template_literals].

This sort of design is how a lot of my static sites start -- metadata in JSON, some functions that render HTML, and an event listener that renders the whole page after it loads.

Once I have the basic site working, I add more data, render more HTML, and add CSS styles to make it look pretty.
This is where I can have fun, and really customise each site.
There's no structure here -- I just keep tweaking until I have something I'm happy with.
I'm ignoring CSS because this post is long enough already, and there's a certain vintage charm to unstyled HTML.

What else can we do?

[DOMContentLoaded]: https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event
[querySelector]: https://developer.mozilla.org/en-US/docs/Web/API/Element/querySelector
[getElementById]: https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById
[json]: https://www.json.org/json-en.html
[template literal]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
[template_elem]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template
[Web Components]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components
[demo_template_literals]: /files/2025/static-site-demo.html?demoId=template-literals



<h2 id="filtering">Add filtering to find specific items</h2>

As the list gets even longer, it's useful to have some way to find specific items in the list -- I don't want to scroll the whole list every time.
I like adding keyword tags to my data, and then filtering the list for items with particular tags.
If I add other metadata fields, I could filter on those too.

Here's a brief sketch of the sort of interface I like:

{%
  picture
  filename="js_filters_sketch.png"
  width="550"
  alt="A crude sketch of a simple app. At the top is a list of three filters (tagged with animals, tagged with wtf, published in 2025) and a red 'x' to dismiss them. Below that are three items, each with a list of tags below it."
%}

I can define a series of filters, and apply them to focus on a specific subset of items.
I can combine multiple filters to refine my search further, and I can see a list of applied filters with a way to remove them, if I've filtered too far.
I can either apply a filter from a global menu, or using controls on each item to find similar items.

I use URL query parameters to store the list of currently-applied filters, for example:

```
bookmarks.html?tag=animals&tag=wtf&publicationYear=2025
```

Any UI element that adds or removes a filter is a link, so clicking it changes the URL, and triggers a complete re-render with the new filters.

When I write filtering code today, I try to make it as easy as possible to define new filters.
Every site needs a slightly different set of filters, but the overall principle is always the same: here's a long list of items, find the items that match these rules.

Let's start by expanding our data model to include a couple of new fields:

```javascript
const bookmarks = [
  {
    "url": "https://estherschindler.medium.com/the-old-family-photos-project-lessons-in-creating-family-photos-that-people-want-to-keep-ea3909129943",
    "title": "Lessons in creating family photos that people want to keep, by Esther Schindler (2018)",
    "tags": ["photography", "preservation"],
    "publicationYear": "2018"
  },
  …
];
```

Then we can define some filters we might use to narrow the list:

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
```

The `key` is the name of the filter used in the URL query parameter.
The `label` is how the filter will be described in the list of applied filters (along with the value we're filtering for).
The `filterFn` is a function that takes two arguments: a bookmark, and a filter value, and returns true/false depending on whether the bookmark matches this filter.

This list is the only place where I need to customise the filters for a particular site; the rest of the filtering code is completely generic.
This means there's only one place I need to make changes if I want to add or remove filters.

The next piece of the filtering code is a generic function that filters a list of items, and takes the list of possible filters as an argument:

```javascript
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

This function doesn't care what sort of items I'm passing, or what the actual filters are -- so I can reuse it between different sites.
It returns the list of matching items, and the list of applied filters.
The latter allows me to show that list on the page.

The final step is to wire this filtering into the page render -- we need to actually filter the list of displayed items, and show the list of applied filters.
Here's the rough code:

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
  
<h1>Bookmarks</h1>

<p>Applied filters:</p>
<ul id="appliedFilters"></ul>

<p>Bookmarks:</p>
<ul id="listOfBookmarks"></ul>
```

I usually stick to "simple" filters that can be phrased as a yes/no question.
I rely on my past self to provide sufficiently useful metadata that I can find stuff again later.

I've never implemented anything more like a search, where there are fuzzier rules about whether a particular item is a match.

If you want to see this in action, check out [the demo page](/files/2025/static-site-demo.html?demoId=hand-written-html).

---

* Filtering
* Sorting

---



## Sorting

The next feature I usually implement is sorting.
I build a little dropdown menu with all the options, and picking a new option triggers a page reload with the new sort order:

{%
  picture
  filename="js_sorting_sketch.png"
  width="537"
  alt="A crude sketch of a simple sorting interface. It's labelled “sort by” and then there’s a dropdown with four options: title (A to Z), title (Z to A), publication date (newest first), and random."
%}

As with filters, I put the sort order in a query parameter, for example:

```
bookmarks.html?sortOrder=title-a-to-z
```

Here's an example of the code I use for sorting:

```javascript
const bookmarkSortOptions = [
  {
    id: 'titleAtoZ',
    label: 'title (A to Z)',
    compareFn: (a, b) => a.title > b.title ? 1 : -1,
  },
  {
    id: 'publicationYear',
    label: 'publication year (newest first)',
    compareFn: (a, b) => a.publicationDate - b.publicationDate,
  },
];

/*
 * Sort a list of items.
 *
 * It takes the list of items and available options, and the
 * URL query parameters passed to the page.
 *
 * It returns a list with the items in sorted order, and the
 * sort order that was applied.
 */
function sortItems({ items, sortOptions, sortOrderId }) {

  // What sort order are we using?
  //
  // Look for a matching sort option, or use the default if the sort
  // order is null/unrecognised.
  const defaultSort = sortOptions[0];
  const selectedSort =
    sortOptions.find(s => s.id === sortOrderId) || defaultSort;

  console.debug(`Selected sort: ${JSON.stringify(selectedSort)}`);

  // Now apply the sort to the list of items.
  const sortedItems = items.sort(selectedSort.compareFn);

  return { sortedItems, appliedSortOrder: selectedSort };
}
```

Once again this is written in a fairly generic way -- I have a list of sort orders that I define once, and then the rest of the code can be reused between sites.
In the past I've made the mistake of not having a single source of truth for my sort orders, and then different bits of my codebase disagree on how things can be sorted.

The key is the `compareFn`, which gets passed directly to the JavaScript [`sort` function][array_sort].
I confess I never remember how this works, and I have to look it up every time: if `compareFn(a, b)` returns `1`, does that sort `a` before or after `b`?

Having them defined once makes it easy to add new sort orders, and then I have a component that renders my dropdown menu:

```javascript
/*
 * Create a dropdown control to choose the sort order.  When you pick
 * a different value, the page reloads with the new sort.
 */
function sortOrderDropdown({ sortOptions, appliedSortOrder }) {
  return `
    <select onchange="setSortOrder(this.value)">
      ${
        sortOptions
          .map(({ id, label }) => `
            <option value="${id}" ${id === appliedSortOrder.id ? 'selected' : ''}>
              ${label}
            </option>
          `)
          .join("")
      }
    </select>
  `;
}

function getSortOrder(params) {
  return params.get("sortOrder");
}

function setSortOrder(sortOrderId) {
  const params = new URLSearchParams(window.location.search);
  params.set("sortOrder", sortOrderId);
  window.location.search = params.toString();
}
```

Finally, here's how the sorting code gets wired into the app:

```html
<script>
  window.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);

    const { matchingItems: matchingBookmarks, appliedFilters } =
      filterItems(…);

    …

    const { sortedItems: sortedBookmarks, appliedSortOrder } =
      sortItems({
        items: matchingBookmarks,
        sortOptions: bookmarkSortOptions,
        sortOrderId: getSortOrder(params),
      });

    document.querySelector("#sortOrder").innerHTML +=
      sortOrderDropdown({ sortOptions: bookmarkSortOptions, appliedSortOrder });

    document.querySelector("#listOfBookmarks").innerHTML =
      sortedBookmarks.map(Bookmark).join("");
  });
</script>

<p id="sortOrder">Sort by:</p>
```

[array_sort]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort

## Pagination

Modern web browsers are very performant, and you can put thousands of elements on the page without breaking a sweat.
I've only had to add pagination in a couple of very image-heavy sites -- mostly text-based sites I just show everything, because my lists aren't that large.
(You may notice that, for example, there are no paginated lists anywhere on this site.
By writing lean HTML, I can fit all my lists on a single page.)

But on the rare occasions I want to add pagination, this doesn't require too much JavaScript.

{%
  picture
  filename="js_pagination_sketch.png"
  width="537"
  alt="A crude sketch of a simple pagination interface. The text says “Page 2 of 5”, and then there are prev/next arrow buttons."
%}

As with all the other features we've seen, I use a URL query parameter to track the current page number:

```
bookmarks.html?page=2
```

The first thing we need is a function that will select a page for us.
If we're on page N, what items should we be showing?

```javascript
/*
 * Get a page of items.
 *
 * This function will reduce the list of items to the items that should
 * be shown on this particular page.
 */
function getPageOfItems({ items, pageNumber, pageSize }) {

  // Page numbers are 1-indexed, so page 1 corresponds to
  // the indices 0…(pageSize - 1).
  const startOfPage = (pageNumber - 1) * pageSize;
  const endOfPage = pageNumber * pageSize;
  const thisPage = items.slice(startOfPage, endOfPage);

  return {
    thisPage,
    totalPages: Math.ceil(items.length / pageSize),
  };
}
```

In some of my sites, the page size is a suggestion rather than a hard rule.
If there are 27 items and the page size is 25, I think it's nicer to show all the items on one page than push a few items onto a second page which barely has anything on it.
But that might reflect my general disinclination for pagination in my static sites, and it's definitely a nice-to-have rather than a required feature.

We can also create a component that gives us some pagination controls:

```javascript
/*
 * Renders a list of pagination controls.
 *
 * This includes links to prev/next pages and the current page number.
 */
function PaginationControls({ pageNumber, totalPages, params }) {

  // If there are no pages, we don't need pagination controls.
  if (totalPages === 1) {
    return "";
  }

  // Do we need a link to the previous page?  Only if we're past page 1.
  if (pageNumber > 1) {
    const prevPageParams = new URLSearchParams(params);
    prevPageParams.set("page", prevPageParams - 1);
    prevPageLink = `<a href="?${prevPageParams.toString()}">&larr; prev</a>`;
  } else {
    prevPageLink = null;
  }

  // Do we need a link to the previous page?  Only if we're before
  // the last page.
  if (pageNumber < totalPages) {
    const nextPageParams = new URLSearchParams(params);
    nextPageParams.set("page", nextPageParams + 1);
    nextPageLink = `<a href="?${nextPageParams.toString()}">next &rarr;</a>`;
  } else {
    nextPageLink = null;
  }

  const pageText = `Page ${pageNumber} of ${totalPages}`;

  // Construct the final result.
  return [prevPageLink, pageText, nextPageLink]
    .filter(p => p !== null)
    .join(" / ");
}
```

Let's wire this into our `DOMContentLoaded` event listener, so when the page loads we'll see pagination controls and

```html
function getPageNumber() {
}

<script>
  window.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);

    const { matchingItems: matchingBookmarks, appliedFilters } =
      filterItems(…);

    const { sortedItems: sortedBookmarks, appliedSortOrder } =
      sortItems(…);

    const { thisPage: thisPageOfBookmarks, totalPages } =
      getPageOfItems({
        items: sortedBookmarks,
        pageNumber: getPageNumber(),
        pageSize: 25
      });

    document.querySelector("#paginationControls").innerHTML +=
      PaginationControls({ pageNumber: getPageNumber(), totalPages, params });

    document.querySelector("#listOfBookmarks").innerHTML =
      thisPageOfBookmarks.map(Bookmark).join("");
  });
</script>

<p id="paginationControls">Pagination controls:</p>
```

One thing that pagination makes a ltitel tricky is need to update sorting/filtering to reset to page 1

---





---

More features you could add:
* sorting
* filtering
* pagination
put all of those inside the `window.addEventListener` block to cut down the list of entries to the specific slice you want to show rn

Noscript and errors

Bonus features:
* storing in Git
* tests using QUnit/Playwright
* manipulate JS using Python scripts, put metadata in separate file
    -> why okay?

Will be posting an example of a site using this pattern soon