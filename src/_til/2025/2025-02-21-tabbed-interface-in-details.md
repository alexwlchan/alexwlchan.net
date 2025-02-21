---
layout: til
title: Creating HTML-native tabs with the `<details>` element
summary:
  If you add the `name` attribute to more than one `<details>` element, only one of them can be open at a time.
date: 2025-02-21 11:47:56 +0000
tags:
  - html:details
  - web development
---
I was reading Hacker News today, and I came across this nugget in [a comment](https://news.ycombinator.com/item?id=43119810) by Dan Fabulich:

> &gt; Where are the native HTML Tabs control?
>
> You implement tabs today (aka accordions) with \`&lt;details name=&quot;tab&quot;&gt;`. <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details#name">https://developer.mozilla.org/en-US/docs/Web/HTML/Element/de...</a> &quot;This attribute enables multiple &lt;details&gt; elements to be connected, with only one open at a time. This allows developers to easily create UI features such as accordions without scripting.&quot;
>
> You do have to write some CSS to align tabs horizontally, but it's fine.

I have to build some tabbed interfaces soon, so the idea that I could do it with plain HTML without using JavaScript is quite exciting!
I decided to do a couple of experiments.

## A basic Q&A

By default, the different `<details>` elements will arrange themselves in a vertical list, because they have `display: block;`.
This reminded me of Q&A style interfaces, where only one question can be open at a time.

Here's the code:

```html
<details name="questions">
  <summary>What is your name?</summary>
  <p>My name is Sir Lancelot of Camelot.</p>
</details>

<details name="questions">
  <summary>What is your quest?</summary>
  <p>To seek the Holy Grail.</p>
</details>

<details name="questions">
  <summary>What is your favourite colour?</summary>
  <p>Blue.</p>
</details>
```

and here's how it renders:

<blockquote>
  <details name="questions">
    <summary>What is your name?</summary>
    <p>My name is Sir Lancelot of Camelot.</p>
  </details>

  <details name="questions">
    <summary>What is your quest?</summary>
    <p>To seek the Holy Grail.</p>
  </details>

  <details name="questions">
    <summary>What is your favourite colour?</summary>
    <p>Blue.</p>
  </details>
</blockquote>

Notice that if you click to open one question, it will auto-close the previous question you had open.

(I actually dislike this style of Q&A page.
I think it's better to let readers open as many questions as they like, but this example demonstrates the feature.)

<style>
  blockquote > details:first-child {
    padding-top: var(--default-padding);
  }

  blockquote > details:not([open]):last-child {
    padding-bottom: var(--default-padding);
  }
</style>



## A basic tabbed interface

Now let's add the CSS to align the tabs horizontally.

We convert the `<details>` elements to `inline-block` so they flow on to the sme line

```css
details {
  display: inline-block;
  margin-right: 1rem;
}

details[open] summary {
  background: #007bff;
  color: white;
}

summary {
  padding: 0.5rem 1rem;
  background: #eee;
  cursor: pointer;
}

details > p {
  position: absolute;
  left:  0;
  right: 0;
}
```

<blockquote id="tabbed_interface">
  <div style="position: relative;">
    <details name="questions">
      <summary>What is your name?</summary>
      <p>My name is Sir Lancelot of Camelot.</p>
    </details>

    <details name="questions">
      <summary>What is your quest?</summary>
      <p>To seek the Holy Grail.</p>
    </details>

    <details name="questions">
      <summary>What is your favourite colour?</summary>
      <p>Blue.</p>
    </details>
  </div>
</blockquote>

<style>
  #tabbed_interface {
    details {
      display: inline-block;
      margin-right: 1rem;
    }

    details[open] summary {
      background: #007bff;
      color: white;
    }

    summary {
      padding: 0.25em 0.5em;
      background: #eee;
      cursor: pointer;
    }

    details > p {
      position: absolute;
      left:  0;
      right: 0;
    }
  }
</style>

aaa
