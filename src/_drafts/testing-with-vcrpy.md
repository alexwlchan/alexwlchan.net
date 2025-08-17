---
layout: post
title: Using vcrpy to test HTTP interactions in Python
summary:
tags:
  - python
  - software testing
index:
  feature: true
colors:
  css_light: "#ab5326"
  css_dark:  "#f49d61"
---
I write a lot of Python code that makes HTTP calls, and I like to write automated tests to verify my code is doing the right thing.
Is it making the correct request?
Is it handling the response correctly?

But I don't want my tests to make real HTTP calls every time they run.
Instead, I mock HTTP interactions with a library called [vcrpy].

With vcrpy, the first time a test runs, it makes a real HTTP call, and the request and response are recorded to a "cassette" -- a text file stored in my repo.
When I run the test again, the HTTP call is replayed from that cassette, rather than making a real network request.

I first came across this idea in [Ruby's VCR library][ruby_vcr], and vcrpy brings the concept to Python.

In this post, I'll show you how I use vcrpy in a production codebase -- not just the basics, but also how I structure and configure it so that other developers can understand and extend the tests.
I'll use the [Flickr API] as an example, but these techniques could be used with any HTTP calls.

[ruby_vcr]: https://github.com/vcr/vcr
[vcrpy]: https://vcrpy.readthedocs.io/en/latest/
[Flickr API]: https://www.flickr.com/services/developer/api/

{% table_of_contents level="h2" %}

<figure>
  {%
    picture
    filename="pexels-inspiredimages-157541.jpg"
    width="750"
  %}
  <figcaption>
    Three black <a href="https://en.wikipedia.org/wiki/Compact_Video_Cassette">compact video cassette</a> tapes.
    Photo credit: <a href="https://www.pexels.com/photo/3-black-vhs-157541/">Anthony on Pexels</a>.
  </figcaption>
</figure>



<h2 id="why_not_real_requests">Why not make real HTTP calls in tests?</h2>

There are several reasons I avoid real HTTP calls in my tests:

### It makes my tests slower

I want my tests to be fast, because then I'll run them more often and catch mistakes sooner.
An individual HTTP call might be quick, but stack up hundreds of them and tests really start to drag.

### It makes my tests less reliable

Even if my code is correct, the tests could now fail because of problems on the remote server:

*   What if I'm offline?
*   What if the server is having a temporary outage?
*   What if the server starts rate limiting me for making too many HTTP requests?

### It makes my tests more brittle

If my tests depend on the remote server having certain state, then my test suite may break or become less helpful if the state changes unexpectedly.
Sometimes this change is obvious, and sometimes it's subtle.

Here are two examples:

*   Suppose I'm testing a function that looks up photos on Flickr.

    When I'm writing the test, I pick an example photo -- the test looks up that photo, and checks it's retrieved correctly.
    Then the photo gets deleted from Flickr.
    Now my test starts failing, even though my code still works correctly for extant photos -- the fact that the example I chose has been deleted is just annoying.

*   Suppose I'm testing an edge case.
    Does my code handle photos with emoji in the title?

    When I'm writing the test, I pick an example photo, and then the photo title is changed so it no longer contains emoji.
    I could introduce a regression and never realise, because the test is no longer verifying this edge case, and it would keep passing.

### It makes my tests harder to debug

If there are more reasons why a test could fail, then it takes longer to work out if the failure was caused by my mistake, or a change on the server.

### It means passing around more secrets

A lot of my HTTP calls require secrets, like API keys or OAuth tokens.
If the tests made real HTTP calls, I'd need to copy those secrets to every environment where I'm running the tests.
That means there are more copies of the secrets floating around (e.g. developer laptops, GitHub Actions), which increases the risk of a leak.

---

for several reasons:

*   **It would make my tests much slower.**
*   **It would make my tests less reliable.**
    The tests would fail if I'm offline or if the server is having temporary issues.
*   **It would make my tests harder to debug.**
    If a test starts failing, it could be because I've introduced a bug in my code, or because
*   **It means passing around more secrets.**


This mocking happens entirely in my test suite, so I don't need to change my code to fit the tests.

Another Python implementation of this is betamax
-> only works with requests, but I use httpx
-> requires the Sessions API, so may need to update my code to fit tests

---

While I was working at the [Flickr Foundation],

filter response headers to keep cassettes readable

---

I wrote a lot of Python to call the [Flickr API].
It's a pretty standard REST API.

---

You make a GET or POST request to the Flickr API URL, passing an API key and URL query parameters.
Here's

```python
import httpx
import keyring

api_key = keyring.get_password("flickr_api", "key")

resp = httpx.get(
    "https://api.flickr.com/services/rest/",
    params={
        "api_key": api_key,
        "method": "flickr.urls.lookupUser",
        "url": "https://www.flickr.com/photos/alexwlchan/",
    }
)

print(resp.text)
# <?xml version="1.0" encoding="utf-8" ?>
# <rsp stat="ok">
# <user id="199258389@N04">
# 	<username>alexwlchan</username>
# </user>
# </rsp>
```

[Flickr Foundation]: https://www.flickr.org

---

Suppose we have code that makes HTTP calls
* e.g. Flickr API call

Want to test the code works correctly
* libraries to "record" HTTP interactions as YAML/JSON so they can be replayed later
* so we don't have to make real HTTP calls in our CI
* inspired by Ruby library of same name

Simple example:
* record single API call
* get YAML file, yay!
* but includes our secret API key, which we don't want to commit

force_decode_responses

Redacting info
* filter_headers and filter_query_params
* can remove value entirely, but I prefer to replace with redacted value – makes it easier to distinguish between "no value passed" and "value passed, but redacted"

Naming cassettes
* by default, cassette name is name of test
* if you have a lot of cassettes, can be tricky to work out what's going on
* better: pytest fixture for cassette name
* esp for parametrized tests with URLs in

Explaining how to use cassettes
* in our example, pass Flickr API key as env var
* most of the time, not an issue – when you run tests, get recorded HTTP calls and don't need to set your own Flickr API key
* suppose you record new responses -- then you need to know to set env var
* what if this isn't very common?
* solution: `before_record_response`

wrapping in a fixture
* return API client as fixture which is pre-authed and uses VCR cassette