---
layout: note
title: Don't nest a `<Script>` in a `<Head>` with Next.js
summary: If you do, the rendered page won't include the script anywhere.
date: 2025-09-14 11:01:26 +01:00
topic: JavaScript
---
I was working on a Next.js app, and I got a warning in my local dev console:

> Do not add `<script>` tags using `next/head` (see `<script>` tag with `src="https://example.com/example.js"`). Use `next/script` instead.
See more info here: <https://nextjs.org/docs/messages/no-script-tags-in-head-component>

This is a rough approximation of the code I was using (although I've been unable to reproduce this warning in a minimal example):

```tsx {"names":{"1":"Head","2":"ExamplePage","3":"Head","4":"title","7":"title","8":"script","9":"src","10":"Head","11":"h1","14":"h1"}}
import Head from 'next/head';

export default function ExamplePage() {
  return (
    <>
      <Head>
        <title>Hello world</title>
        {/* works fine, but gives a warning */}
        <script src="https://example.com/my-script.js"/>
      </Head>

      <h1>Hello world!</h1>
    </>
  );
}
```

I was tempted to just swap out `<script>` for the `next/script` component:

```tsx {"names":{"1":"Head","2":"ExamplePage","3":"Head","4":"title","7":"title","8":"script","9":"src","10":"Head","11":"h1","14":"h1"}}
import Head from 'next/head';

export default function ExamplePage() {
  return (
    <>
      <Head>
        <title>Hello world</title>
        {/* works fine, but gives a warning */}
        <script src="https://example.com/my-script.js"/>
      </Head>

      <h1>Hello world!</h1>
    </>
  );
}
```