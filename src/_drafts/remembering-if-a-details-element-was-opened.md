---
layout: post
title: Remembering if a &lt;details&gt; element was opened
summary: A JavaScript function that remembers if a &lt;details&gt; element was reopened, and keeps it open when you reload the page.
tags: javascript html
---

A rather useful HTML feature is the [&lt;details&gt; disclosure element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details).
It gives you a way to create a collapsible element without using JavaScript.
Here's an example:

<style>
  details {
    background: white;
    border: 1px solid #999;
    border-radius: 4px;
    padding: 1em;
  }

  details p:last-child {
    margin-bottom: 0;
  }
</style>

```html
<details>
  <summary>What is the HTML details element?</summary>
  <p>
    The details element represents a disclosure widget from
    which the user can obtain additional information or controls –
    <a href="https://html.spec.whatwg.org/multipage/interactive-elements.html#the-details-element">The HTML Living Standard</a>
  </p>
</details>
```

<details>
  <summary>What is the HTML details element?</summary>
  <p>The details element represents a disclosure widget from which the user can obtain additional information or controls – <a href="https://html.spec.whatwg.org/multipage/interactive-elements.html#the-details-element">The HTML Living Standard</a></p>
</details>

You can tap on the triangle to open ("disclose") the element, and to see what it contains.
You can tap the triangle again to close the element, and hide it.
It's supported in all modern browsers.

The optional `<summary>` element lets you customise the label that appears next to the disclosure triangle -- if you don't include it, your browser uses a default label.
(In my browser, that's "Details".)

People have found lots of of creative uses for &lt;details&gt; -- a native show/hide component that doesn't require JavaScript is extremely useful -- and one place I use it is to display a list of tags in [docstore](https://github.com/alexwlchan/docstore).
The list takes up a lot of space, so I don't want to show it unless I'm actively picking tags:

<img style="width: 600px; border: 1px solid #999; border-radius: 4px" src="/images/2020/docstore_details_1x.png" srcset="/images/2020/docstore_details_1x.png 1x, /images/2020/docstore_details_2x.png 2x, /images/2020/docstore_details_3x.png 3x" alt="Two details elements, with one expanded to show a cloud of links in different sizes and colours.">

Each link in the tag cloud goes to a new page -- showing documents filtered with that tag.

When you open a page, any &lt;details&gt; elements start as closed.
This slows down the process of selecting multiple tags -- I expand the tag cloud, click to the new page, expand the tag cloud again, click, and so on.
I'd rather expand it once, then click, click, click to select the tags I want.

**I want to remember if the &lt;details&gt; element has been opened, and reopen it when I load a new page.**
I've written a JavaScript function that does this.
It listens to the [toggle event](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details#Events), which fires whenever somebody opens or closes a details element, then records the state in [Window.localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
When the function runs, it also checks the current value in localStorage, and opens the details element if necessary.

Here's the code:

```javascript
// Remember the state of a <details> element.
//
// If the element is opened and the page is reloaded, the element will
// be reopened.
//
// Pass the ID of the <details> element after the page has loaded.
//
function rememberIfDetailsWasDisclosed(detailsId) {
  var localStorageKey = "detailsWasDisclosed_" + detailsId;

  var details = document.getElementById(detailsId);

  // Listen to the toggle event, which fires whenever the <details>
  // is opened or closed.  The event fires after the state has changed,
  // so looking it up will tell us the current value.
  // See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details#Events
  details.addEventListener("toggle", event => {
    if (details.open) {
      localStorage.setItem(localStorageKey, true);
    } else {
      localStorage.removeItem(localStorageKey);
    }
  });

  // If the stored value tells us the <details> was open the last time we
  // opened the page, re-open it now.
  if (localStorage.getItem(localStorageKey)) {
    details.open = true;
  }
}
```

To use this function, pass the id of the details element you want to remember.
For example:

```html
<details id="tagCloud">…</details>

<script>
  rememberIfDetailsWasDisclosed("tagCloud");
</script>
```

I've created [a small demo page](/files/2020/details_example.html) for this function.
I've been using it in docstore for a while now, and it works pretty well -- and since remembering the state of details seems like something I might want to use again in future, I'm writing it up here.
