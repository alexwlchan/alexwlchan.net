---
layout: post
title: Remembering if a &lt;details&gt; element was opened
summary:
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

You can tap on the triangle to open ("disclose") the element, and to show the text it contains.
You can tap the triangle again to close the element, and hide the text.
It's supported in all modern browsers.

The optional `<summary>` element lets you customise the label that appears next to the disclosure triangle -- if you don't include it, your browser uses a default label.
(In my browser, that's "Details".)

People have found lots of of creative uses for &lt;details&gt;; one place I use it is to display a list of tags in [docstore](https://github.com/alexwlchan/docstore).
The list takes up a lot of space, so I don't want to show it unless I'm picking tags:

<img style="width: 600px; border: 1px solid #999; border-radius: 4px" src="/images/2020/docstore_details_1x.png" srcset="/images/2020/docstore_details_1x.png 1x, /images/2020/docstore_details_2x.png 2x, /images/2020/docstore_details_3x.png 3x">

The &lt;details&gt; element is closed by default, and it closes when you reload the page.
For example, if you open the example above, then reload the page, the element will be closed again.
This is less than ideal in docstore -- I want to keep the list of tags open as I select different tags, but each tag is a link to a new page, so the &lt;details&gt; tag gets closed.

**I want to remember if the &lt;details&gt; element has been opened, and reopen it when I load a new page.**
I've written a JavaScript function to do this for me.
It listens to the [toggle event](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details#Events), which fires whenever somebody opens or closes a details element, then records the state in [Window.localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).
When the function runs, it also checks the current value in localStorage, and opens the details element if necessary:

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

  details.addEventListener("toggle", event => {
    if (details.open) {
      localStorage.setItem(localStorageKey, true);
    } else {
      localStorage.removeItem(localStorageKey);
    }
  });

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

You can see [a demo of this function](/files/2020/details_example.html).
I've been using it in docstore for a while now, and it works pretty well -- and since remembering the state of details seems like something I might want to use again in future, I'm writing it up here.
