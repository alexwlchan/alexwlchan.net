---
layout: post
date: 2022-09-10 17:04:31 +00:00
title: Finding redundant data in our Next.js props
summary: A script that helps us optimise our `__NEXT_DATA__`, which in turn helps reduce page size.
tags:
  - javascript
  - javascript:next.js
  - web development
colors:
  index_light: "#AE160E"
  index_dark:  "#f15850"
---

At work, we use the [Next.js framework][nextjs] to build our website.

For each page, we define a [getServerSideProps function][getServerSideProps], which runs on the server and returns data required to render the page.
For example, if you're reading an article, we fetch all the article data from the CMS on the server, then send it to the browser in these "props" -- this means we don't need to include a CMS client in the client-side bundle.

These props get embedded in the page as JSON, where they'll be read by the client-side code:

```html
<!DOCTYPE html>
<html lang="en" class="is-keyboard">
  <body>
    ...
    <!--
      This includes `getServerSideProps` in the `pageProps` key.
    -->
    <script id="__NEXT_DATA__" type="application/json">
    {"props":{"pageProps":{"now":"2022-09-10T11:52:10.394Z"},"__N_SSP":true},"page":"/now","query":{},"buildId":"development","runtimeConfig":{"apmConfig":{"serviceName":"content-webapp","active":true,"centralConfig":true}},"isFallback":false,"gssp":true,"customServer":true,"appGip":true,"scriptLoader":[]}
    </script>
  </body>
</html>
```

The size of these props contributes directly to the size of the HTML page, and recently we've been trying to make them more efficient.

We were sending a lot of data that we didn't need to -- for example, we'd send the full list of articles to render index pages (including the full article text), even though we only really needed the titles and images.
A couple of months ago, we started filtering out unused data inside getServerSideProps, so users get smaller, faster pages.
We've already picked off the low-hanging fruit, and further optimisations will be harder to find.

I've written [a short script] to help us out.
It scans a list of pages, then reports the size of the HTML and `__NEXT_DATA__` specifically.
Here's an example of the output:

```
https://wellcomecollection.org/ homepage
html      = 418.01 kB
next_data = 207.32 kB (50%)

https://wellcomecollection.org/stories stories
html      = 311.52 kB
next_data =  62.93 kB (20%)

https://wellcomecollection.org/articles/Yp3GthEAACIAwRi9 article
html      = 199.35 kB
next_data =  29.16 kB (14%)

https://wellcomecollection.org/ homepage
html      = 418.01 kB
next_data = 207.32 kB
```

This initial output helps us decide if it's worth spending any time reducing the size of the Next.js props.
It looks like we could improve the homepage, but the other pages are already fairly optimised.
If we wanted to make them smaller, our time might be better spent elsewhere.

If we do decide to do some optimisation, the script saves the `__NEXT_DATA__` as a pretty-printed, standalone JSON file.
This is easier to read than the minified version sent in the HTML, and we can find the parts that are worth removing.
The numbers are also useful for a before/after comparison, to measure the impact of a change.

If you use Next.js and you'd find this useful, I've [posted the script on GitHub][github].
It's not long or complicated, but it does make a repetitive task a bit quicker, and I've already used it to shave significant chunk off the site.

[nextjs]: https://nextjs.org/
[getServerSideProps]: https://nextjs.org/docs/basic-features/data-fetching/get-server-side-props
[a short script]: https://github.com/alexwlchan/nextjs-pageweight-analyser
[github]: https://github.com/alexwlchan/nextjs-pageweight-analyser
