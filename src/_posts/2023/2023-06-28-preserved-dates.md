---
layout: post
date: 2023-06-28 16:38:25 +00:00
title: Preserving Dates during JSON serialisation with vanilla JS
summary: How to make sure you get a `Date` back when you call `JSON.parse` and `JSON.stringify`.
tags:
  - javascript
  - datetime shenanigans
colors:
  css_light: "#662c29"
  css_dark:  "#bda9a1"
---

For my sins, I've spent a lot of the last year dealing with datetime-related bugs.
One of our longest-standing issues has been around sending `Date` values via JSON – JavaScript will happily encode a `Date` value in JSON, but it gets encoded as a string, and there's no easy way to get a `Date` value back when you decode it later.

This TypeScript program illustrates the issue: we create an object that includes some `Date`s, encodes it as JSON, then decode it back into an object.
It calls a function that expects to use some `Date` values -- once before the JSON round-trip, once after.

{% code lang="typescript" names="0:ScheduledEvent 1:start 3:end 5:getDuration 6:ev 8:milliseconds 18:ev 26:jsonifiedEvent 30:parsedEvent" %}
type ScheduledEvent = {
  start: Date;
  end: Date;
}

function getDuration(ev: ScheduledEvent) {
  const milliseconds = ev.end.getTime() - ev.start.getTime();
  console.log(`The event is ${milliseconds / 1000} seconds long`);
}

const ev: ScheduledEvent = {
  start: new Date('2001-01-01T12:00:00Z'),
  end:   new Date('2001-01-01T14:00:00Z'),
}

getDuration(ev);

const jsonifiedEvent: string = JSON.stringify(ev);
const parsedEvent: ScheduledEvent = JSON.parse(jsonifiedEvent);

getDuration(parsedEvent);
{% endcode %}

This program passes type checking, but if you actually run it, you get an error:

```
[LOG]: "The event is 7200 seconds long"
[ERR]: "Executed JavaScript Failed:"
[ERR]: ev.end.getTime is not a function. (In 'ev.end.getTime()', 'ev.end.getTime' is undefined)
```

Before the JSON round-trip, the `ev.start` and `ev.end` variables are both `Date` values.
Afterward, they're both strings.

In our real code the issue is more obfuscated -- we're sending our objects via Next.js props, which does include a JSON round-trip, but we don't see it directly.

---

## Rejected approaches

We tried several ways to fix this problem before we settled on our current approach.

For a while our codebase was littered with extra calls to `new Date(…)`, making sure that every value was actually a Date before we tried to call Date methods on it.
That worked, but it was confusing -- the type system tells us this value is a `Date`, so why do we need to convert it to a `Date` again?

Later we tried writing functions to coerce the string-ified values back to `Date`.
Something like:

{% code lang="typescript" names="0:fixDatesInScheduledEvent 1:ev 12:jsonifiedEvent 16:parsedEvent 21:fixedEvent" %}
function fixDatesInScheduledEvent(ev: ScheduledEvent): ScheduledEvent {
  return {
    start: new Date(ev.start),
    end:   new Date(ev.end),
  };
}

const jsonifiedEvent: string = JSON.stringify(ev);
const parsedEvent: ScheduledEvent = JSON.parse(jsonifiedEvent);
const fixedEvent: ScheduledEvent = fixDatesInScheduledEvent(parsedEvent);
{% endcode %}

This kept all the date fixing in a single place, but for increasingly large and complex types it was tricky to be sure that we'd fixed all the `Date` values.
We'd only discover we'd forgotten to fix a field when something broke.
And it's still confusing if you look at the type system -- it's another conversion from `Date` to `Date`.

At one point I considered adding generic parameters to all our types, so we could track whether a given date value was a `Date` or a `string`:

{% code lang="typescript" names="0:ScheduledEvent 1:DateType 2:start 4:end 6:jsonifiedEvent 10:parsedEvent 15:fixedEvent" %}
type ScheduledEvent<DateType> = {
  start: DateType;
  end:   DateType;
}

const jsonifiedEvent: string = JSON.stringify(ev);
const parsedEvent: ScheduledEvent<string> = JSON.parse(jsonifiedEvent);
const fixedEvent: ScheduledEvent<Date> = fixDatesInScheduledEvent(parsedEvent);
{% endcode %}

but this would involve adding hundreds of type parameters to functions in our codebase, and spreading this JSON mess over lots more files.
I had an experimental branch, but it didn't last long.

For a while we used [superjson], a third-party library which can send Date values to and from JSON.
That worked pretty well, but we were using a tiny subset of the functionality and it caused issues with our build system.
(Specifically, we needed custom Babel config to use superjson with Next.js, and that blocked us from using the faster [SWC compiler].
We wanted those speedy compile times!)

Looking for a superjson alternative is what led to our current approach.

[superjson]: https://www.npmjs.com/package/superjson
[SWC compiler]: https://nextjs.org/docs/architecture/nextjs-compiler

---

If you look at how superjson serialises Date values, it's keeping a list of all the places in the JSON that were originally a Date:

```json
{
  "articles": [
    {
      "title": "What writing myself has revealed",
      "datePublished": "2022-12-15T10:00:01.000Z"
    },
    {
      "title": "Busting myths about turkey-baster babies",
      "datePublished": "2022-12-14T10:00:01.000Z"
    }
  ],
  "_superjson": {
    "values": {
      "articles.0.datePublished": ["Date"],
      "articles.1.datePublished": ["Date"]
    }
  }
}
```

I quite like this approach, because it encodes all the information about the Date types in the JSON itself -- you don't have to know the types which are being used on either end.
It's clear this approach could be made more flexible if you wanted to handle other types, but for us Date is plenty.

We decided to take a different route: rather than keep a list of fields that we need to de-stringify, we encode instances of `Date` as a JSON object with a `type` parameter:

```json
{
  "value": "2022-12-15T10:00:01.000Z",
  "type": "Date"
}
```

When we decode the JSON later, we can look for instances of this structure and coerce them back into the proper Date type.
I thought this might involve recursively modifying the objects, which tends to be quite fiddly – but it turns out JSON.stringify and JSON.parse already have ways to do this sort of thing.

With [JSON.stringify()][JSON.stringify], we can pass an optional *replacer* method that takes a key and a value, and replaces the value before it's encoded as JSON.
This allows us to replace any instances of `Date` with our custom object:

{% code lang="typescript" names="0:replacer 2:key 3:value" %}
const replacer = function (key: string, value: any) {
  return this[key] instanceof Date
    ? {
        value: this[key].toUTCString(),
        type: 'Date',
      }
    : this[key];
};

JSON.stringify(…, replacer);
{% endcode %}

With [JSON.parse()][JSON.parse], we can pass an optional *reviver* function that takes a key and a JSON value, and modifies the value before it's returned.
This allows us to detect our custom object, and replace any instances of it with a `Date`:

{% code lang="typescript" names="0:reviver 2:key 3:value" %}
const reviver = function (key: string, value: any) {
  if (
    value !== null &&
    typeof value === 'object' &&
    Object.keys(value).length === 2 &&
    Object.keys(value).includes('type') &&
    Object.keys(value).includes('value') &&
    value.type === 'Date'
  ) {
    return new Date(value.value);
  } else {
    return value;
  }
};

JSON.parse(…, reviver);
{% endcode %}

We use this code in our JSON encoder/decoder functions, and it's been working pretty well so far.
We get to shed a dependency and rely on vanilla JavaScript features, and it reduces the number of confusing interactions with the type system.

This is one of the JavaScript features I've been vaguely aware of for years, but never actually looked at – I'm glad to finally have a use case.

[JSON.stringify]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
[JSON.parse]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
