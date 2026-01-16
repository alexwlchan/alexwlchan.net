---
layout: til
title: Restricting routes to pre-approved IP addresses in Caddy
date: 2025-01-21 14:28:43 +00:00
tags:
  - caddy
---
I wanted to limit access to a WordPress login page to a pre-approved list of IP addresses, and provide instructions for anybody trying to log in.

I couldn't find any examples of this, but I did find some useful pointers in the documentation.
Here's the broad outline of what I ended up with:

```
handle /wp-login.php {
  @blocked not remote_ip 1.2.3.4 5.6.7.8

  header @blocked Content-Type "text/html"

  respond @blocked 403 {
    body <<HTML
      <html>
        <p>
          Your IP address is {http.request.remote.host}.
          You aren't allowed to log in!
          Ask Alex for help.
        </p>
      </html>
    HTML
  }

  … serve the real route
}
```

The one thing I'd love is a better way to manage the `remote_ip` list, e.g. splitting it across multiple lines or interspersing comments.
I couldn't find a way to do so, which is frustrating.
