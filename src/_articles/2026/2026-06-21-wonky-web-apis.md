---
layout: article
date: 2026-06-21 15:29:21 +01:00
title: What can wonky APIs tell us about the web?
summary: An API with an explicitly unused parameter is a testament to the web's commitment to backward compatibility.
topic: JavaScript
---

{#
  Card image: https://www.pexels.com/photo/red-signage-on-fuel-pump-13074031/
#}

A few days ago, Misty posted something that caught my eye:

{% mastodon "https://digipres.club/@misty/116772382932474870" %}

The [`HTMLMediaElement.canPlayType` API][mdn-video-canPlayType] tells you how likely it is that a browser can play media with a given MIME type, but the response is unusual.
The word "likely" is important here, because it's not a simple yes/no answer.
The possible responses are:

*   `""` -- no, the browser can't play the media
*   `"probably"` -- the browser can probably play the media
*   `"maybe"` -- there isn't enough information to determine if the media is playable.

A ternary, probabilistic response is already a bit weird; the return values double down on the weirdness.
A clearer set of return values would be `"no"`, `"probably"` and `"unknown"`.

But when thinking of wonky web APIs, my mind went somewhere else: to [`History.pushState()`][mdn-history-pushstate] and [`replaceState()`][mdn-history-replacestate].
These APIs are for manipulating your browser history, and take an `unused` parameter which you have to pass but do absolutely nothing.

Here's the description of `pushState` from MDN (emphasis mine):

> The `pushState()` method of the [`History`][mdn-history] interface adds an entry to the browser's session history stack.
>
> Syntax:
>
> ```javascript
>     pushState(state, unused)
>     pushState(state, unused, url)
> ```
>
> Parameters:
>
> * `state` -- The `state` object is a JavaScript object which is associated with the new history entry created by `pushState()`. […]
> * `unused` -- **This parameter exists for historical reasons, and cannot be omitted; passing an empty string is safe against future changes to the method.**
> * `url` -- The new history entry's URL.

This begs the question: what historical reasons?
Why does an API supported by every major browser have a parameter that nobody uses?

The [History API][mdn-history-using] was designed for use with [single-page applications (SPAs)][mdn-single-page-applications] -- sites that only load a single page, then use JavaScript to update the contents of a page, rather than loading a new page every time something changes.
Using SPAs can make a site faster, because they only have to load the part of a page that's changed, but they also break the behaviour of the browser's "back" and "forward" buttons.

From the user's point of view, they click links and the page changes, so if they click the "back" button, they expect to go back to their previous state.

But the browser only records a single history event, when the user first loads the SPA -- all the in-page updates using JavaScript don't register as new pages.
When the user clicks the "back" button, the browser will take them to whatever page they were looking at before they opened the SPA.

Using `pushState()` and `replaceState()` allows an app to create synthetic history entries, so the "back" and "forward" buttons can step the user through the pages they've seen within the SPA.

The `pushState()` API first appeared [in a draft HTML5 spec][html5-history-pushstate] in January 2008, with three parameters:

*   The `state` object would be attached to the history event, and if the user clicked the "back" or "forward" buttons, your app would get a [`popstate` event][mdn-window-popstate] with the state value associated with the history event they'd selected.
*   The `title` parameter allowed apps to set a title for the entry saved in the browser's session history, which could be different to the title shown in the browser window.
*   The `url` parameter allowed apps to set a URL for the history entry, which could be different to the URL shown in the browser window.
    If omitted, the browser would use the current URL.

The `title` parameter was always "advisory", and in practice most browsers completely ignored the parameter, to avoid the confusion of mismatched titles in the browser UI and session history.

It soon became clear that the `title` parameter was pointless, but it was already too late to change.
Lots of sites were built as single-page applications and already using the new `pushState` and `replaceState` APIs, and breaking those sites was unacceptable.

The argument could be neither removed nor made optional.
If you removed it, you'd break sites that used the three-parameter `pushState(state, title, url)`.
If you made it optional, its position in the middle of the signature would leave browsers unable to distinguish between `pushState(state, url)` and `pushState(state, title)`.

Instead, the spec was updated to rename the parameter to `unused` and clarify it has no effect.

This wonky API reflects the challenge of designing for the web: it's difficult to design APIs without seeing how they're used on real world websites, but then it's too late to make changes in response to feedback.
The web goes to incredible lengths to preserve backward compatibility, and it's the ultimate form of "anything described as a prototype will get shipped in production".

The longevity of vanilla web technology is why I [keep using static websites][me-static-websites] for my media archives -- more than anything else in my career in tech, web technology is what lasts.

[html5-history-pushstate]: https://www.w3.org/TR/2008/WD-html5-20080122/#pushstate
[mdn-history]: https://developer.mozilla.org/en-US/docs/Web/API/History
[mdn-history-pushstate]: https://developer.mozilla.org/en-US/docs/Web/API/History/pushState
[mdn-history-replacestate]: https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState
[mdn-history-using]: https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API
[mdn-single-page-applications]: https://developer.mozilla.org/en-US/docs/Glossary/SPA
[mdn-video-canPlayType]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/canPlayType
[mdn-window-popstate]: https://developer.mozilla.org/en-US/docs/Web/API/Window/popstate_event
[me-static-websites]: /2024/static-websites/
