---
layout: til
title: Disable JavaScript in an `<iframe>` by setting the `sandbox` attribute
date: 2025-02-17 19:03:33 -05:00
tags:
  - javascript
---
I was loading a web page in an iframe, and I wanted to make sure it couldn't run any JavaScript.

I found the [`sandbox` attribute][sandbox] on the `<iframe>` element, which lets you control what can happen within the iframe -- for example, whether it can run scripts or control forms.
By default, you can do quite a lot of stuff inside an iframe, but setting `sandbox=""` will disable all of it.

Here's an example we can use:

```html
<iframe srcdoc="
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      document.querySelector('main').innerText = 'This iframe has JavaScript!';
    });
  </script>
    
  <noscript>This iframe doesn't have JavaScript!</noscript>

  <main></main>"></iframe>
```

And let's load this with and without the `sandbox` attribute:

<style>
  #demo {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 1em;
  }
</style>

<div id="demo">
  <figure>
    <iframe srcdoc="
      <script>
        window.addEventListener('DOMContentLoaded', function() {
          document.querySelector('main').innerText = 'This iframe has JavaScript!';
        });
      </script>
    
      <noscript>This iframe doesn't have JavaScript!</noscript>

      <main></main>"></iframe>
    <figcaption>
      <code>&lt;iframe&gt;</code>
    </figcaption>
  </figure>
  <figure>  
    <iframe sandbox="" srcdoc="
      <script>
        window.addEventListener('DOMContentLoaded', function() {
          document.querySelector('main').innerText = 'This iframe has JavaScript!';
        });
      </script>
    
      <noscript>This iframe doesn't have JavaScript!</noscript>

      <main></main>"></iframe>
    <figcaption>
      <code>&lt;iframe sandbox=""&gt;</code>
    </figcaption>
  </figure>
</div>

[sandbox]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox