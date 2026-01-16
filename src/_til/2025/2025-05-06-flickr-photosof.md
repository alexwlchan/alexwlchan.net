---
layout: til
title: How do I find photos of a person on Flickr?
summary: |
  `https://www.flickr.com/people/{path_identifier}/photosof`
date: 2025-05-06 10:29:43 +01:00
tags:
  - flickr
---
I'm using the [flickr.photos.people.getList API][api] to get a list of people in a given photo, and I wanted some photos to test with.
I wasn't sure how to find photos which have people tagged, but I was able to work it out.

[api]: https://www.flickr.com/services/api/flickr.photos.people.getList.html

## Photos of a single person

The example API response includes an NSID of a Flickr user who was tagged in a photo at some time in the past: `87944415@N00`.
So I visited [their profile](https://www.flickr.com/people/87944415@N00/), and at the bottom of their page is a section "Photos of Simon Batistoni".
That includes a "View all" link, and clicking it took me to:

`https://www.flickr.com/people/hitherto/photosof`

Now I know that's the URL route, I can find photos of other people.
For example, this is the (empty) list of photos that I'm tagged in:

`https://www.flickr.com/people/alexwlchan/photosof`

## Photos of multiple people

In the sidebar of that page, there's a link: "Anyone ever snapped a picture of the two of you?"
Clicking it takes me to a new URL which would show photos of me and the other person (if there were any photos tagged with me):

`https://www.flickr.com/photosof/me+hitherto`

You can put other path identifiers in here, and they'll combine as an AND query.
Here's one more example: a list of photos which tag three different people.

`https://www.flickr.com/photosof/hitherto+48857242@N00+straup`
