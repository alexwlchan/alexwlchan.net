---
layout: til
date: 2024-02-05 13:44:19 +00:00
title: You need to call `resp.close()` to close the file opened by `send_file()`
tags:
  - python
---
I had a basic Flask app using `send_file()`, which I was testing with pytest:

```python
#!/usr/bin/env python3

from flask import Flask, send_file

app = Flask(__name__)


@app.route("/source.py")
def source_code():
    return send_file(__file__)


def test_can_get_source_code():
    with app.test_client() as client:
        resp = client.get("/source.py")
        assert resp.data.startswith(b"#!/usr/bin/env python3\n")
```

but when I ran this test with warnings-as-errors, I got a warning about a file not being closed:

```console
$ py.test app.py
...
E                   pytest.PytestUnraisableExceptionWarning: Exception ignored in: <_io.FileIO [closed]>
E
E                   Traceback (most recent call last):
E                     File "/.venv/lib/python3.12/site-packages/_pytest/python.py", line 193, in pytest_pyfunc_call
E                       result = testfunction(**testargs)
E                                ^^^^^^^^^^^^^^^^^^^^^^^^
E                   ResourceWarning: unclosed file <_io.BufferedReader name='app.py'>
```

I found several GitHub issues about this warning ([pallets/flask#3735](https://github.com/pallets/flask/issues/3735), [pallets/werkzeug#1785](https://github.com/pallets/werkzeug/issues/1785)).
Neither of them provide an explicit answer, but the clue is in the answer of the linked pull request ([pallets/werkzeug#2041](https://github.com/pallets/werkzeug/pull/2041)).

If I close the response when I'm done, the warning goes away:

```diff
 def test_can_get_source_code():
     with app.test_client() as client:
         resp = client.get("/source.py")
         assert resp.data.startswith(b"#!/usr/bin/env python3\n")
+        resp.close()
```
