These are some tests for the behaviour of the live website.
They check things like:

*   Are pages being served properly?
*   Are images being served properly?
*   If a page has been redirected, are you sent to the right place?
*   If I've removed a page, does it get the correct HTTP [410 Gone](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/410) response?
*   Are my HTTPS certificates renewing correctly?
*   Am I setting the right HTTP headers on responses? (e.g. for caching)

These tests can be run manually, or they run on a regular schedule in GitHub Actions.

## Running the tests

```console
$ ruby run_all_tests.rb
```

(No dependencies; I was using Ruby 3.3 when I wrote the first set of tests.)
