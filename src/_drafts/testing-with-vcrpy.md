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

[ruby_vcr]: https://github.com/vcr/vcr
[vcrpy]: https://vcrpy.readthedocs.io/en/latest/

{% table_of_contents %}

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

There are several reasons why I avoid real HTTP calls in my tests:

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

### Mocking solves all of these problems

If my test suite is returning consistent responses for HTTP calls, and those responses are defined within the test suite itself, then my tests get faster and more reliable.
I'm not making real network calls, I'm not dependent on the behaviour of a server, and I don't need real secrets to run the tests.

There are a variety of ways to define this sort of test mock; I like to record real responses because it ensures I'm getting a high-fidelity mock, and it makes it easier to add new mocks.

---

## Why do you like vcrpy?

I know two Python libraries that record real HTTP responses: [vcrpy] and [betamax].
They behave in a similar way, I've used both and they work well.

I use vcrpy because it supports a [wide variety of HTTP libraries][compatibility], whereas betamax only works with requests.
I currently use a mixture of httpx and urllib3, and it's convenient to be able to test them both with the same library.

I like the flexibility of vcrpy.
It has a lot of options and hooks for configuring what it records, and I'll show you the ones I use below.

I also like that it works without needing any changes to the code I'm testing.
I can write HTTP code as I normally would, then I add a vcrpy decorator in my test and the responses get recorded.
I don't like test frameworks that require me to rewrite my code to fit -- the tests should follow the code, not the other way round.

[vcrpy]: https://vcrpy.readthedocs.io/
[betamax]: https://github.com/betamaxpy/betamax
[compatibility]: https://vcrpy.readthedocs.io/en/latest/installation.html#compatibility

---

## A basic example of using vcrpy

Here's a test that uses vcrpy to fetch `www.example.com`, and look for some text in the response:

```python
import httpx
import vcr


@vcr.use_cassette("fixtures/vcr_cassettes/test_example_domain.yml")
def test_example_domain():
    resp = httpx.get("https://www.example.com/")
    assert "<h1>Example Domain</h1>" in resp.text
```

The `use_cassette()` decorator tells vcrpy to record any HTTP requests in the specified YAML file.

When I run this test using pytest (`python3 -m pytest test_example.py`), vcrpy will check if that YAML file exists.
If the file is missing, it makes a real HTTP call and saves it to the file.
If the file exists, it replays the HTTP call from the YAML file.
You can see what the YAML file looks like here: [test_example_domain.yml](/files/2025/test_example_domain.yml).

If your test makes more than one HTTP call, vcrpy records all of the requests and responses in the same YAML file.



## Keeping secrets out of my cassettes

The cassette files contain the complete HTTP request and response, which includes the URL, form data, and HTTP headers.
They're a text file that I check into my repo, alongside my code and tests.

If I'm testing an API that requires authentication, the HTTP request could include secrets like an API key or OAuth token.
I don't want to save those secrets in the cassette file!

Fortunately, vcrpy can [filter sensitive data][filters] from the cassette file.
In particular, you can redact HTTP headers, the URL query parameters, or form data.

Here's an example of a test where I'm using `filter_query_parameters` to remove an API key from the query parameters.

```python
import httpx
import keyring
import vcr


@vcr.use_cassette(
    "fixtures/vcr_cassettes/test_flickr_api.yml",
    filter_query_parameters=[("api_key", "REDACTED_API_KEY")],
)
def test_flickr_api():
    api_key = keyring.get_password("flickr_api", "key")

    resp = httpx.get(
        "https://api.flickr.com/services/rest/",
        params={
            "api_key": api_key,
            "method": "flickr.urls.lookupUser",
            "url": "https://www.flickr.com/photos/alexwlchan/",
        },
    )

    assert '<user id="199258389@N04">' in resp.text
```

You can see the complete YAML file in [test_flickr_api.yml](/files/2025/test_flickr_api.yml).
Notice how the `api_key` query parameter has been replaced with `REDACTED_API_KEY` in the recorded request:

```yaml
interactions:
- request:
    …
    uri: https://api.flickr.com/services/rest/?api_key=REDACTED_API_KEY&method=flickr.urls.lookupUser&url=https%3A%2F%2Fwww.flickr.com%2Fphotos%2Falexwlchan%2F
    …
```

When you filter out sensitive information, you can choose to just omit it, or replace it with a new value -- in general, I prefer the latter.
This makes it clearer that a value was passed, and it was redacted -- rather than never being passed at all.
if a developer is unsure of what's going on, the replacement value gives them something they can search for in the rest of the codebase.

[filters]: https://vcrpy.readthedocs.io/en/latest/advanced.html#filter-sensitive-data-from-the-request

## Improving the human readability of cassettes

If you look at the first two responses, you'll notice that the response body is a chunk of base64-encoded binary data:

```yaml
response:
  body:
    string: !!binary |
      H4sIAAAAAAAAAH1UTXPbIBC9+1ds1UsyIyQnaRqPLWn6mWkPaQ9pDz0SsbKYCFAByfZ08t+7Qo4j
      N5makYFdeLvvsZC9Eqb0uxah9qopZtljh1wUM6Bf5qVvsPi85aptED4ZxaXO0tE6G5co9BzKmluH
      Po86X7FFBGkxcdbetwx/d7LPo49Ge9SeDWEjKMdZHnnc+nQIvzpAvYSkucI86iVuWmP9ZP9GCl/n
```

This is because the `example.com` and `api.flickr.com` servers are both [gzip compressing][gzip] their responses, is, and vcrpy is preserving that compression.
But gzip compression is handled by the HTTP libraries I use libraries -- my code never needs to worry about compression; it just gets the uncompressed response.

Where possible, I prefer to store responses in their uncompressed form.
It makes the cassettes easier to read if somebody is looking for an example of a server response, and you can see if secrets are included in the saved response data.

Here's an example where we pass the [`decode_compressed_response` parameter][decode_compressed_response], which tells vcrpy to decompress responses before saving them to the cassette.

```python
import httpx
import vcr


@vcr.use_cassette(
    "fixtures/vcr_cassettes/test_example_domain_with_decode.yml",
    decode_compressed_response=True,
)
def test_example_domain_with_decode():
    resp = httpx.get("https://www.example.com/")
    assert "<h1>Example Domain</h1>" in resp.text
```

You can see the complete YAML file in [test_example_domain_with_decode.yml](/files/2025/test_example_domain_with_decode.yml).
Notice how the response body now contains an HTML string:

```yaml
response:
  body:
    string: "<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n
      \   <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-type\" content=\"text/html;
      charset=utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width,
```

[gzip]: https://developer.mozilla.org/en-US/docs/Glossary/gzip_compression
[decode_compressed_response]: https://vcrpy.readthedocs.io/en/latest/advanced.html#decode-compressed-response

---

What if you make a different request?

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