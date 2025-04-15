---
layout: post
date: 2025-04-15 21:23:24 +0000
title: Localising the `<time>` with JavaScript
summary:
  I'm using the `<time>` element and some JavaScript to display timestamps as human-readable, localised timestamps. Something like `Tue, 15 Apr 2025 at 20:45 BST` is easier to read than `2025-04-15T19:45:00Z`.
tags:
  - javascript
  - datetime shenanigans
---
I've been writing some internal dashboards recently, and one hard part is displaying timestamps.
Our server does everything in UTC, but the team is split across four different timezones, so the server timestamps aren't always easy to read. 

For most people, it's harder to understand a UTC timestamp than a timestamp in your local timezone. 
Did that event happen just now, an hour ago, or much further back? 
Was that at the beginning of your working day?
Or at the end?

Then I remembered that I tried to solve this [five years ago] at a previous job. I wrote a JavaScript snippet that converts UTC timestamps into human-friendly text.
It displays times in your local time zone, and adds a short suffix if the time happened recently.
For example:

> today @ 12:00 BST (1 hour ago) <br/>
> yesterday @ 11:00 CST <br/>
> Fri, 22 May 2020 @ 10:00 PST

In my old project, I was using writing timestamps in a `<div>` and I had to opt into the human-readable text for every date on the page. 
It worked, but it was a bit fiddly.

Doing it again, I thought of a more elegant solution.

HTML has [a `<time>` element][time_element] for expressing datetimes, which is a more meaningful wrapper than a `<div>`.
When I render the dashboard on the server, I don't know the user's timezone, so I include the UTC timestamp in the page like so:
  
```html
<time datetime="2025-04-15 19:45:00Z">
  Tue, 15 Apr 2025 at 19:45 UTC
</time>
```

I put a machine-readable date and time string with a timezone offset string in the [`datetime` attribute][datetime_attribute], and then a more human-readable string in the text of the element.

Then I add this JavaScript snippet to the page:

```javascript
window.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("time").forEach(function(timeElem) {
    
    // Set the `title` attribute to the original text, so a user
    // can hover over a timestamp to see the UTC time.
    timeElem.setAttribute("title", timeElem.innerText);

    // Replace the display text with a human-friendly date string
    // which is localised to the user's timezone.
    timeElem.innerText = getHumanFriendlyDateString(
      timeElem.getAttribute("datetime")
    );
  })
});
```

This updates any `<time>` element on the page to use a human friendly date string, which is localised to the user's timezone.
For example, I'm in the UK so that becomes:

```html
<time datetime="2025-04-15 19:45:00Z" title="Tue, 15 Apr 2025 at 19:45 UTC">
  Tue, 15 Apr 2025 at 20:45 BST
</time>
```

In my experience, these timestamps are easier and more intuitive for people to read. 

I always include a timezone string (e.g. BST, EST, PDT) so it's obvious that I'm showing a localised timestamp.
If you really need the UTC timestamp, it's in the `title` attribute, so you can see it by hovering over it.
(Sorry, mouseless users, but I don't think any of my team are browsing our dashboards from their phone or tablet.)

If the JavaScript doesn't load, you see the plain old UTC timestamp.
It's not ideal, but the page still loads and you can see all the information -- this behaviour is an [enhancement], not an essential.

To me, this is the unfulfilled promise of the `<time>` element.
In my fantasy world, web page authors would write the time in a machine-readable format, and browsers would show it in a way that makes sense for the reader.
They'd take into account their language, locale, and time zone. 

I understand why that hasn't happened -- it's much easier said than done.
You need so much context to know what's the "right" thing to do when dealing with datetimes, and guessing without that context is at the heart of many datetime bugs.
These sort of human-friendly, localised timestamps are very handy sometimes, and a complete mess at other times.

In my staff-only dashboards, I have that context.
I know what these timestamps mean, who's going to be reading them, and I think they're a helpful addition that makes the data easier to read. 
  
[five years ago]: /2020/human-friendly-dates-in-javascript/
[time_element]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/time
[datetime_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/time#datetime
[enhancement]: https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement
