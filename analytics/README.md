# analytics

This is a simple analytics app based on [Flask][flask].
The original code was written [by Charles Leifer][leifer], and lightly tweaked/configured for my setup.

In every page, there's a link to a tiny snippet of JavaScript:

    https://alexwlchan.net/analytics/a.js

If you fetch and run this JavaScript, you download a one-pixel tracking with the URL embedded as a query parameter:

    https://alexwlchan.net/analytics/a.gif?url=https://example.org

This gets saved in a SQLite database, which I can query with the reporting script to get basic site statistics.

[leifer]: http://charlesleifer.com/blog/saturday-morning-hacks-building-an-analytics-app-with-flask/
[flask]: http://flask.pocoo.org/

## Why not just use Google Analytics?

I have very simple wants.
I'd like to know how many people are looking at the site, and which pages they're looking at.
(And I don't even *need* that information, it's just a curiosity.)

Google Analytics records far more data than I need.
It's a very sophisticated tool, and I don't need that level of power or flexibility.
I'm also wary of adding unnecessary third-party tracking to the site -- this is just a more sophisticated version of grepping my nginx logs.

And because the data is in my own database, I can slice it however I like.
I have the full power of Python available, whereas GA requires me to use Google's web interface, which I've never fully understood.

Minimalist, homebrew software FTW.
