---
layout: til
title: How to get a user's email address with the Flickr&nbsp;API
summary: |
  The `flickr.profile.getProfile` API returns somebody's email address, but only if you're allowed to see it.
date: 2024-10-23 09:29:15 +01:00
tags:
  - flickr
---
Flickr members can control who can see their email address in the "Who can see what" part of the [Privacy & Permissions](https://www.flickr.com/account/privacy) settings.
The default is "nobody".

When I'm signed in and I call this API against my own account, my email address is an attribute on the `profile` element:

```xml
<profile id="199258389@N04" email="alex@alexwlchan.net" …/>
```

This attribute is omitted if I try to look up somebody else's email address and I don't have permission to see it.

[oauth]: https://www.flickr.com/services/api/auth.oauth.html
