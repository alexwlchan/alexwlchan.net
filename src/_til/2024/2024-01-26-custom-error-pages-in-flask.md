---
layout: til
date: 2024-01-26 15:58:51 +00:00
date_updated: 2024-08-07 10:51:48 +01:00
title: Custom error pages in Flask
summary:
  You can use `app.error_handler` to add custom responses for HTTP status codes, so the errors match the look and feel of the rest of the site.
tags:
  - python
---
You can customise the error pages by adding a few instances of `app.error_handler`, for example:

```python
@app.errorhandler(404)
def not_found(e: Exception) -> str:
    return "Not found!", 404


@app.errorhandler(500)
def internal_server_error(e: Exception) -> str:
    return "Internal server error!", 500
```

If it can't render a custom error page, it will throw a 500 error.
If it can't render the custom 500 Internal Server Error page, it will return Flask's generic 500 Internal Server Error page.

## A custom route for 500 errors

I find it helpful to add a route that I can use to test the behaviour of 500 pages in the prod environment, which looks like this:

```python
@app.route("/500/")
def deliberate_error() -> str:
    raise ValueError("BOOM!")
```

## Including tests

Here's a complete program to illustrate this pattern, including tests for the two custom error pages:

```python
from flask import Flask

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e: Exception) -> str:
    return "Not found!", 404


@app.errorhandler(500)
def internal_server_error(e: Exception) -> str:
    return "Internal server error!", 500


@app.route("/500/")
def deliberate_error() -> str:
    raise ValueError("BOOM!")


def test_custom_404_page():
    # This creates a test instance of the Flask app, as described
    # in the Flask docs on testing.
    # See https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures
    app.config["TESTING"] = True

    with app.test_client() as client:
        resp = client.get("/404/")

        assert resp.status_code == 404
        assert b"Not found!" in resp.data


def test_custom_500_page():
    # This is similar to the test instance above, but we disable
    # TESTING -- this means that Flask will render the error page
    # as it would be shown to a real user, not the Werkzeug error
    # page shown for local development/debugging.
    app.config["TESTING"] = False

    with app.test_client() as client:
        resp = client.get("/500/")

        assert resp.status_code == 500
        assert b"Internal server error!" in resp.data
```
