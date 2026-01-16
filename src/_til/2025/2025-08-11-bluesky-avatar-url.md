---
layout: til
title: Get the avatar URL for a Bluesky user
summary: Make a request to the `app.bsky.actor.getProfile` endpoint, passing their handle as the `actor` parameter.
date: 2025-08-11 09:06:46 +01:00
tags:
  - bluesky
---
Here's an example of an unauthenticated API request using the [`app.bsky.actor.getProfile` API](https://docs.bsky.app/docs/api/app-bsky-actor-get-profile) which returns the URL of the user's avatar in the JSON response:

```console
$ curl --silent \
      --get 'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile' \
      --data 'actor=alexwlchan.bsky.social' \
      | jq .
{
  "did": "did:plc:tovvvx4o53qazoourf5u7yig",
  "handle": "alexwlchan.bsky.social",
  "displayName": "Alex Chan",
  "avatar": "https://cdn.bsky.app/img/avatar/plain/did:plc:tovvvx4o53qazoourf5u7yig/bafkreifqohcxldi2ypw74o2n2s3yohybi2n4ixbark2yshmw74kxxnoube@jpeg",
  "associated": {
    "lists": 0,
    "feedgens": 0,
    "starterPacks": 0,
    "labeler": false,
    "chat": {
      "allowIncoming": "following"
    },
    "activitySubscription": {
      "allowSubscriptions": "followers"
    }
  },
  "labels": [],
  "createdAt": "2023-07-03T19:54:00.292Z",
  "indexedAt": "2024-01-20T06:14:37.153Z",
  "followersCount": 334,
  "followsCount": 41,
  "postsCount": 205
}
```