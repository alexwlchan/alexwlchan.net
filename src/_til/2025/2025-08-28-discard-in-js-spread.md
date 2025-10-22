---
layout: til
title: Discard a variable in a JavaScript object spread by assigning it to `_`
date: 2025-08-28 10:55:29 +0100
tags:
  - javascript
---
I had some code with [spread syntax] where some variables were being captured and used, and others were being saved into a catchall `props` variable.

There was a variable I wanted to discard -- not capture and use, and not add to `props`.
I could just capture it and not use it, but it might be flagged as an unused variable.

Here's a simple example, where I capture the `name` variable and discard `lastRoll`:

{% code lang="javascript" names="0:shape 5:name 6:lastRoll 8:diceProps" %}
const shape = {
  name:     'd20',
  sides:    20,
  color:    'red',
  lastRoll: 7,
};

const { name, lastRoll: _, ...diceProps } = shape;

console.log(name);
// 'd20'

console.log(diceProps);
// { sides: 20, color: "red" }
{% endcode %}

[spread syntax]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
