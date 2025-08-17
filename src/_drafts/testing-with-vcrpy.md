---
layout: post
title: Using vcrpy to test HTTP interactions in Python
summary: How I record HTTP requests to get fast, reliable, and consistent tests, and the patterns I use in a production codebase.
tags:
  - python
  - software testing
index:
  feature: true
colors:
  css_light: "#ab5326"
  css_dark:  "#f49d61"
---
Testing code that makes HTTP requests can be difficult.
Real requests are slow, flaky, and hard to control.
That's why I use a Python library called [vcrpy], which does a one-off recording of real HTTP interactions, then replays them during future tests.

These recordings are saved to a "cassette" -- a plaintext file that I keep alongside my tests and my code.
The cassette ensures that all my tests get consistent HTTP responses, which makes them faster and more reliable, especially in CI.
I only have to make one real network request, and then I can run my tests locally and offline.

In this post, I'll show you how I use vcrpy in a production codebase -- not just the basics, but also the patterns, pitfalls, and fixtures that make it work for a real team.

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



<h2 id="why_not_real_requests">Why not make real HTTP requests in tests?</h2>

There are several reasons why I avoid real HTTP requests in my tests:

### It makes my tests slower

I want my tests to be fast, because then I'll run them more often and catch mistakes sooner.
An individual HTTP call might be quick, but stack up hundreds of them and tests really start to drag.

### It makes my tests less reliable

Even if my code is correct, my tests could fail because of problems on the remote server.
What if I'm offline?
What if the server is having a temporary outage?
What if the server starts rate limiting me for making too many HTTP requests?

### It makes my tests more brittle

If my tests depend on the server having certain state, then the server state could change and break or degrade my test suite.

Sometimes this change is obvious.
For example, suppose I'm testing a function to fetch photos from Flickr, and then the photo I'm using in my test gets deleted.
My code works correctly for photos that still exist, but now my test starts failing.

Sometimes this change is more subtle.
Suppose I've written a regression test for an edge case, and then the server state changes, so the example I'm checking is no longer an instance of the edge case.
I could break the code and never realise, because the test would keep passing.
My test suite would become less effective.

### It means passing around more secrets

A lot of my HTTP calls require secrets, like API keys or OAuth tokens.
If the tests made real HTTP calls, I'd need to copy those secrets to every environment where I'm running the tests.
That increases the risk of the secret getting leaked.

### It makes my tests harder to debug

If there are more reasons why a test could fail, then it takes longer to work out if the failure was caused by my mistake, or a change on the server.

### Recording and replaying HTTP requests solves these problems

If my test suite is returning consistent responses for HTTP calls, and those responses are defined within the test suite itself, then my tests get faster and more reliable.
I'm not making real network calls, I'm not dependent on the behaviour of a server, and I don't need real secrets to run the tests.

There are a variety of ways to define this sort of test mock; I like to record real responses because it ensures I'm getting a high-fidelity mock, and it makes it fairly easy to add new tests.

---

## Why do you like vcrpy?

I know two Python libraries that record real HTTP responses: [vcrpy] and [betamax], both based on [a Ruby library called vcr][vcr.rb].
I've used all three, they behave in a similar way, and they work well.

I prefer vcrpy for Python because it supports a [wide variety of HTTP libraries][compatibility], whereas betamax only works with [requests].
I currently use a mixture of [httpx] and [urllib3], and it's convenient to test them both with the same library and test helpers.

I also like that vcrpy works without needing any changes to the code I'm testing.
I can write HTTP code as I normally would, then I add a vcrpy decorator in my test and the responses get recorded.
I don't like test frameworks that require me to rewrite my code to fit -- the tests should follow the code, not the other way round.

[vcrpy]: https://vcrpy.readthedocs.io/
[betamax]: https://github.com/betamaxpy/betamax
[vcr.rb]: https://github.com/vcr/vcr
[requests]: https://requests.readthedocs.io/en/latest/
[httpx]: https://github.com/encode/httpx
[urllib3]: https://urllib3.readthedocs.io/en/stable/
[compatibility]: https://vcrpy.readthedocs.io/en/latest/installation.html#compatibility

---

## A basic example of using vcrpy

Here's a test that uses vcrpy to fetch `www.example.com`, and look for some text in the response.
I use `vcr.use_cassette` as a context manager around the code that makes an HTTP request:

```python
import httpx
import vcr


def test_example_domain():
    with vcr.use_cassette("fixtures/vcr_cassettes/test_example_domain.yml"):
        resp = httpx.get("https://www.example.com/")
        assert "<h1>Example Domain</h1>" in resp.text
```

Alternatively, you can use `vcr.use_cassette` as a decorator:

```python
@vcr.use_cassette("fixtures/vcr_cassettes/test_example_domain.yml")
def test_example_domain():
    resp = httpx.get("https://www.example.com/")
    assert "<h1>Example Domain</h1>" in resp.text
```

With the decorator, you can also omit the path to the cassette file, and vcrpy will name the cassette file after the function:

```python
@vcr.use_cassette()
def test_example_domain():
    resp = httpx.get("https://www.example.com/")
    assert "<h1>Example Domain</h1>" in resp.text
```

When I run this test using pytest (`python3 -m pytest test_example.py`), vcrpy will check if the cassette file exists.
If the file is missing, it makes a real HTTP call and saves it to the file.
If the file exists, it replays the previously-recorded HTTP call.

By default, the cassette is a YAML file.
Here's what it looks like: [test_example_domain.yml](/files/2025/test_example_domain.yml).

If a test makes more than one HTTP request, vcrpy records all of them in the same cassette file.



---

## Using vcrpy in production

### Keeping secrets out of my cassettes

The cassette files contain the complete HTTP request and response, which includes the URL, form data, and HTTP headers.
If I'm testing an API that requires auth, the HTTP request could include secrets like an API key or OAuth token.
I don't want to save those secrets in the cassette file!

Fortunately, vcrpy can [filter sensitive data][filters] before it's saved to the cassette file -- HTTP headers, URL query parameters, or form data.

Here's an example where I'm using `filter_query_parameters` to redact an API key.
I'm replacing the real value with the placeholder `REDACTED_API_KEY`.

```python
import os

import httpx
import vcr


def test_flickr_api():
    with vcr.use_cassette(
        "fixtures/vcr_cassettes/test_flickr_api.yml",
        filter_query_parameters=[("api_key", "REDACTED_API_KEY")],
    ):
        api_key = os.environ.get("FLICKR_API_KEY", "API_KEY")

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

When I run this test the first time, I need to pass an env var `FLICKR_API_KEY`.
This makes a real request and records a cassette, but with my redacted value.
When I run the test again, I don't need to pass the env var, but the test will still pass.

You can see the complete YAML file in [test_flickr_api.yml](/files/2025/test_flickr_api.yml).
Notice how the `api_key` query parameter has been redacted in the recorded request:

```yaml
interactions:
- request:
    …
    uri: https://api.flickr.com/services/rest/?api_key=REDACTED_API_KEY&method=flickr.urls.lookupUser&url=https%3A%2F%2Fwww.flickr.com%2Fphotos%2Falexwlchan%2F
    …
```

You can also tell vcrpy to omit the sensitive field entirely, but I like to insert a placeholder value.
It's useful for debugging later -- you can see that a value was replaced, and easily search for the code that's doing the redaction.

[filters]: https://vcrpy.readthedocs.io/en/latest/advanced.html#filter-sensitive-data-from-the-request

### Improving the human readability of cassettes

If you look at the first two cassette files, you'll notice that the response body is stored as base64-encoded binary data:

```yaml
response:
  body:
    string: !!binary |
      H4sIAAAAAAAAAH1UTXPbIBC9+1ds1UsyIyQnaRqPLWn6mWkPaQ9pDz0SsbKYCFAByfZ08t+7Qo4j
      N5makYFdeLvvsZC9Eqb0uxah9qopZtljh1wUM6Bf5qVvsPi85aptED4ZxaXO0tE6G5co9BzKmluH
      Po86X7FFBGkxcdbetwx/d7LPo49Ge9SeDWEjKMdZHnnc+nQIvzpAvYSkucI86iVuWmP9ZP9GCl/n
```

That's because `example.com` and `api.flickr.com` both [gzip compress][gzip] their responses, and vcrpy is preserving that compression.
But gzip compression is handled by the HTTP libraries -- my code never needs to worry about compression; it just gets the uncompressed response.

Where possible, I prefer to store responses in their uncompressed form.
It makes the cassettes easier to read, and you can see if secrets are included in the saved response data.
I also find it useful to read cassettes as an example of what an API response looks like -- and in particular, what it looked like when I wrote the test.
Cassettes have helped me spot undocumented changes in APIs.

Here's an example where I'm using [`decode_compressed_response=True`][decode_compressed_response] to remove the gzip compression in the cassette:

```python
def test_example_domain_with_decode():
    with vcr.use_cassette(
        "fixtures/vcr_cassettes/test_example_domain_with_decode.yml",
        decode_compressed_response=True,
    ):
        resp = httpx.get("https://www.example.com/")
        assert "<h1>Example Domain</h1>" in resp.text
```

You can see the complete cassette file in [test_example_domain_with_decode.yml](/files/2025/test_example_domain_with_decode.yml).
Notice the response body now contains an HTML string:

```yaml
response:
  body:
    string: "<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n
      \   <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-type\" content=\"text/html;
      charset=utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width,
```

[gzip]: https://developer.mozilla.org/en-US/docs/Glossary/gzip_compression
[decode_compressed_response]: https://vcrpy.readthedocs.io/en/latest/advanced.html#decode-compressed-response

### Naming my cassettes to make sense later

If you write a lot of tests that use vcrpy, you'll end up with a fixtures directory that's full of cassettes.
I like cassette names to match my test functions, so they're easy to match up later.

I could specify a cassette name explicitly in every test, but that's extra work and prone to error.
Alternatively, I could use the decorator and use the automatic cassette name -- but vcrpy uses the name of the test function, which may not distinguish between tests.
In particular, I often group tests into classes, or use [parametrized tests] to run the same test with different values.

Consider the following example:

```python
import httpx
import pytest
import vcr


class TestExampleDotCom:
    def test_status_code(self):
        resp = httpx.get("https://example.com")
        assert resp.status_code == 200


@vcr.use_cassette()
@pytest.mark.parametrize(
    "url, status_code",
    [
        ("https://httpbin.org/status/200", 200),
        ("https://httpbin.org/status/404", 404),
        ("https://httpbin.org/status/500", 500),
    ],
)
def test_status_code(url, status_code):
    resp = httpx.get(url)
    assert resp.status_code == status_code
```

This is four different tests, but vcrpy's automatic cassette name is the same for each of them: `test_status_code`.
The tests will fail if you try to run them -- vcrpy will record a cassette for the first test that runs, then try to replay that cassette for the second test.
The second test makes a different HTTP request, so vcrpy will throw an error because it can't find a matching request.

Here's what I do instead: I have a pytest fixture to choose cassette names, which includes the name of the test class (if any) and the ID of the parametrized test case.
Because I sometimes use URLs in parametrized tests, I also check the test case ID doesn't include slashes or colons -- I don't want those in my filenames!

Here's the decorator:

```python
@pytest.fixture
def cassette_name(request: pytest.FixtureRequest) -> str:
    """
    Returns the filename of a VCR cassette to use in tests.

    The name can be made up of (up to) three parts:

    -   the name of the test class
    -   the name of the test function
    -   the ID of the test case in @pytest.mark.parametrize

    """
    name = request.node.name

    # This is to catch cases where e.g. I try to include a complete
    # HTTP URL in a cassette name, which creates messy folders in
    # the fixtures directory.
    if ":" in name or "/" in name:
        raise ValueError(
            "Illegal characters in VCR cassette name - "
            "please set a test ID with pytest.param(…, id='…')"
        )

    if request.cls is not None:
        return f"{request.cls.__name__}.{name}.yml"
    else:
        return f"{name}.yml"
```

Here's my test rewritten to use that new decorator:

```python
class TestExampleDotCom:
    def test_status_code(self, cassette_name):
        with vcr.use_cassette(cassette_name):
            resp = httpx.get("https://example.com")
            assert resp.status_code == 200


@vcr.use_cassette()
@pytest.mark.parametrize(
    "url, status_code",
    [
        pytest.param("https://httpbin.org/status/200", 200, id="ok"),
        pytest.param("https://httpbin.org/status/404", 404, id="not_found"),
        pytest.param("https://httpbin.org/status/500", 500, id="server_error"),
    ],
)
def test_status_code(url, status_code, cassette_name):
    with vcr.use_cassette(cassette_name):
        resp = httpx.get(url)
        assert resp.status_code == status_code
```

The four tests now get distinct cassette filenames:

*   `TestExampleDotCom.test_status_code`
*   `test_status_code[ok]`
*   `test_status_code[not_found]`
*   `test_status_code[server_error]`

[parametrized tests]: https://nedbatchelder.com/blog/202508/starting_with_pytests_parametrize.html

### Explaining how to use cassettes with helpful errors

Most of the time, you don't need to worry about how vcrpy works.
If you're running an existing test, then vcrpy is just a fancy test mock that happens to be reading its data from a YAML file.
You don't need to worry about the implementation details.

However, if you're writing a new test, you need to record new cassettes.
This can involve some non-obvious setup, especially if you've never done it before.

Let's revisit an earlier example:

```python
def test_flickr_api():
    with vcr.use_cassette(
        "fixtures/vcr_cassettes/test_flickr_api.yml",
        filter_query_parameters=[("api_key", "REDACTED_API_KEY")],
    ):
        api_key = os.environ.get("FLICKR_API_KEY", "API_KEY")

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

If you run this test without passing a `FLICKR_API_KEY` environment variable, it will call the real Flickr API with the placeholder API key.
Unsurprisingly, the Flickr API will return an error response, and your test will fail:

```xml
<?xml version="1.0" encoding="utf-8" ?>
<rsp stat="fail">
  <err code="100" msg="Invalid API Key (Key has invalid format)" />
</rsp>
```

Worse still, vcrpy will record this error in the cassette file.
Even if you work out you need to re-run the test with the env var, it will keep failing as it replays the recorded error.

Can we make this better?
In this scenario, what I'd prefer is:

1.  The test fails if you don't pass an env var
2.  The error explains how to run the test properly
3.  vcrpy doesn't save a cassette file

I worked out how to get this nicer error handling.
vcrpy has a [`before_record_response` hook][before_record_response], that allows you to modify a response before writing it to the cassette file.
You could use this to redact secrets from responses, but I realised you could also use it to validate the response -- and if you throw an exception, it prevents vcrpy from writing a cassette.

Here's a hook I wrote, which checks if a vcrpy response is a Flickr API error telling us that we passed an invalid API key, and throws an exception if so:

```python
def check_for_invalid_api_key(response):
    """
    Before we record a new response to a cassette, check if it's
    a Flickr API response telling us we're missing an API key -- that
    means we didn't set up the test correctly.

    If so, give the developer an instruction explaining what to do next.
    """
    try:
        body: bytes = response["body"]["string"]
    except KeyError:
        body = response["content"]

    is_error_response = (
        b'<err code="100" msg="Invalid API Key (Key has invalid format)" />' in body
    )

    if is_error_response:
        raise RuntimeError(
            "You tried to record a new call to the Flickr API, \n"
            "but the tests don't have an API key.\n"
            "\n"
            "Pass an API key as an env var FLICKR_API_KEY=ae84…,\n"
            "and re-run the test.\n"
        )

    return response
```

We can call this hook in our `vcr.use_cassette` call:

```python
def test_flickr_api(cassette_name):
    with vcr.use_cassette(
        cassette_name,
        filter_query_parameters=[("api_key", "REDACTED_API_KEY")],
        decode_compressed_response=True,
        before_record_response=check_for_invalid_api_key,
    ):
        ...
```

Now, if you try to record a Flickr API call and don't set the API key, you'll get a helpful error explaining how to re-run the test correctly.

[before_record_response]: https://vcrpy.readthedocs.io/en/latest/advanced.html#custom-response-filtering

### Wrapping everything in a fixture for convenience

This is all useful, but it's a lot of boilerplate to add to every test.
To make everything cleaner, I wrap vcrpy in a [pytest fixture] that returns an HTTP client I can use in my tests.
This fixture allows me to configure vcrpy, and also do any other setup I need on the HTTP client -- for example, adding authentication params or HTTP headers.

Here's an example of such a fixture in a [library for using the Flickr API][flickr-photos-api]:

```python
@pytest.fixture
def flickr_api(cassette_name):
    with vcr.use_cassette(
        cassette_name,
        filter_query_parameters=[("api_key", "REDACTED_API_KEY")],
        decode_compressed_response=True,
        before_record_response=check_for_invalid_api_key,
    ):
        client = httpx.Client(
            params={"api_key": os.environ.get("FLICKR_API_KEY", "API_KEY")},
            headers={
                # Close the connection as soon as the API returns a
                # response, to fix pytest warnings about unclosed sockets.
                "Connection": "Close",
            },
        )

        yield client
```

This makes individual tests much shorter and simpler:

```python
def test_flickr_api_without_boilerplate(flickr_api):
    resp = flickr_api.get(
        "https://api.flickr.com/services/rest/",
        params={
            "method": "flickr.urls.lookupUser",
            "url": "https://www.flickr.com/photos/alexwlchan/",
        },
    )

    assert '<user id="199258389@N04">' in resp.text
```

When somebody reads this test, they don't need to think about the authentication or or mocking; they can just see the API call that we're making.

[pytest fixture]: https://docs.pytest.org/en/6.2.x/fixture.html
[flickr-photos-api]: https://github.com/Flickr-Foundation/flickr-photos-api

---

## When I don't vcrpy

Although vcrpy is useful, there are times when I prefer to test my HTTP code in a different way.
Here are a few examples.

### If I'm testing error handling

If I'm testing my error handling code -- errors like timeouts, connection failures, or 5xx errors -- it's difficult to record a real response.
Even if I could find a reliable error case today, it might be fixed tomorrow, which makes it difficult to reproduce if I ever need to re-record a cassette.

When I test error handling, I prefer a pure-Python mock where I can see exactly what error conditions I'm creating.

### If I'm fetching lots of binary files

If my HTTP code is downloading images and video, storing them in a vcrpy cassette is pretty inefficient -- they have to be encoded as base64.
This makes the cassettes large and inefficient, the extra decoding step slows my test down, and the files are hard to inspect.

When I'm testing with binary files, I store them as standalone files in my `fixtures` directory (e.g. in `tests/fixtures/images`), and I write my own mock to read the file from disk.
I can easily inspect or modify the fixture data, and I don't have the overhead of using cassettes.

### If I'm testing future or hypothetical changes in an API

A vcrpy cassette locks in the current behaviour.
But suppose I know about an upcoming change, or I want to check my code would handle an unusual response -- I can't capture that in a vcrpy cassette, because the server isn't returning responses like that (yet).

In those cases, I either construct a vcrpy cassette with the desired response by hand, or I use a code-based mock to return my unusual response.

---

## Summary

Using vcrpy has allowed me to write more thorough tests, and it does all the hard work of intercepting HTTP calls and serialising them to disk.
It gives me high-fidelity snapshots of HTTP responses, allowing me to mock HTTP calls and avoid network requests in my tests.
This makes my tests faster, consistent, and reliable.

Here's a quick reminder of what I do to run vcrpy in production:

*   I use `filter_query_parameters` and `filter_headers` to keep secrets out of cassette files
*   I set `decode_compressed_response=True` to make cassettes more readable
*   I name cassettes after the test function they're associated with
*   I throw errors if an HTTP client isn't set up correctly when you try to record a cassette
*   I wrap everything in a fixture, to keep individual tests simpler

If you make HTTP calls from your tests, I really recommend it: <https://vcrpy.readthedocs.io/en/latest/>
