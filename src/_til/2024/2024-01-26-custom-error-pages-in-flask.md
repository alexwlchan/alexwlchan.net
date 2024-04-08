---
layout: til
date: 2024-01-26 15:58:51 +0000
title: Custom error pages in Flask
tags:
  - python
---
You can customise the error pages by adding a few instances of `app.error_handler`, for example:

```python
@app.errorhandler(404)
def not_found(e: Exception) -> str:
    return render_template("not_found.html"), 404


@app.errorhandler(500)
def internal_server_error(e: Exception) -> str:
    return render_template("internal_server_error.html"), 500
```

Some notes:

*   I was a bit concerned that the exception might get swallowed here, but it's all good – when you throw a 500 error, the underlying exception will still get logged, including the full stack trace.

*   If for some reason the 500 page fails to render correctly, Flask falls back to a generic "Internal Server Error" page.

*   I find it helpful to add a route that I can use to test the behaviour of 500 pages in the prod environment, which looks like this:

    ```python
    @app.route("/500")
    def deliberate_error() -> str:
        raise ValueError("BOOM!")
    ```
