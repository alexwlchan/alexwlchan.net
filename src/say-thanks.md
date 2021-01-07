---
layout: page
title: How to say thanks
---

I don't get paid for the writing on this site.
I earn a generous salary from my employer, which means I can spend my free time on writing, conference speaking and open source projects.

If you've read something I wrote and want to say thanks, there are a couple of ways to do so:



## Send me a message

I love it when people reach out to tell me they enjoyed something I wrote.
If you've found something useful, used me as an example, or learnt something new -- please [send me an email][email] or [a tweet](https://twitter.com/alexwlchan) to tell me what you read, and how it was helpful.

[email]: {{ site.emails.personal | encode_mailto }}



## Give me money

If you'd rather give a monetary expression of gratitude, I have a Ko-fi page: <https://ko-fi.com/alexwlchan>, or you can send me money through PayPal: <https://paypal.me/alexwlchan>.



## Donate to charity

If you feel uncomfortable giving money to me directly, you can donate to one of the charities I support.
That list includes:

{% comment %}
  This code is meant to randomly shuffle the list, and display three charities.
  Every time the site builds, the list is rebuilt.

  I don't want this to be a long scrolling list; that would get busy and take up too much of the page.
{% endcomment %}
{% assign charities = site.data["charities"] | shuffle | slice: 0, 3 %}

<table>
{% for charity in charities %}
<tr>
  <td style="width: 100px; padding: 10px; padding-right: 1.5em; padding-bottom: 20px; height: 70px;">
    <a href="{{ charity.donate_link }}"><img alt="Logo for {{ charity.name }}" src="/images/charities/{{ charity.image }}"></a>
  </td>
  <td>{{ charity.description | smartify | render_markdown }}</td>
</tr>
{% endfor %}
</table>
