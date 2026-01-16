---
layout: til
title: Use Unicode property escapes to detect emoji in JavaScript
date: 2023-09-06 23:46:15 +00:00
tags:
  - javascript
  - unicode
---
From [how to detect emoji using JavaScript](https://stackoverflow.com/a/64007175/1558022) on Stack Overflow:

> The answers might work but are terrible because they rely on unicode ranges that are unreadable and somewhat "magic" because it's not always clear where do they come from and why they work, not to mention they're not resilient to new emojis being added to the spec.
>
> Major browsers now support [unicode property escape](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Unicode_Property_Escapes) which allows for matching emojis based on their belonging in the `Emoji` unicode category: `\p{Emoji}` matches an emoji, `\P{Emoji}` matches a non-emoji.

which includes some example code:

```javascript
console.log(
  /\p{Emoji}/u.test('flowers'), // false :)
  /\p{Emoji}/u.test('flowers 🌼🌺🌸'), // true :)
  /\p{Emoji}/u.test('flowers 123'), // true :(
)
console.log(
  /\p{Extended_Pictographic}/u.test('flowers'), // false :)
  /\p{Extended_Pictographic}/u.test('flowers 🌼🌺🌸'), // true :)
  /\p{Extended_Pictographic}/u.test('flowers 123'), // false :)
)
```

But this doesn't just apply to emoji – the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions/Unicode_character_class_escape) explains you can also use this for different chunks of the Unicode spectrum, e.g. `\P{Script_Extensions=Latin}` or `\p{Letter}`.

I used this to detect emoji [as part of enhanced spam detection](https://github.com/wellcomecollection/wellcomecollection.org/pull/10181) in Wellcome Collection's catalogue search.
