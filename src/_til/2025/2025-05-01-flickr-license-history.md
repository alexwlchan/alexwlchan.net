---
layout: til
title: How does Flickr's getLicenseHistory handle photos with no license changes?
date: 2025-05-01 11:32:47 +0100
tags:
  - flickr
---
I'm using the Flickr's [getLicenseHistory API][api], which returns the license history for a photo.

The example response shows a photo with two license changes: from all rights reserved to CC BY 2.0, and back again.
Both of them are accompanied by a `date_change` timestamp:

```xml
<rsp stat="ok">
  <license_history date_change="1295918034" old_license="All Rights Reserved" old_license_url="" new_license="Attribution License" new_license_url="https://creativecommons.org/licenses/by/2.0/" />
  <license_history date_change="1598990519" old_license="Attribution License" old_license_url="https://creativecommons.org/licenses/by/2.0/" new_license="All Rights Reserved" new_license_url="" />
</rsp>
```

The API also includes a note about photos with no license changes:

> If no changes have been made to the license, it returns the original license as old_license (and an empty new_license).

I wanted to understand what this would look like in practice, so I did some experiments with one of my photos.

[api]: https://www.flickr.com/services/api/flickr.photos.licenses.getLicenseHistory.html

## When a photo has no license changes

This is the API repsonse for a photo with no license changes:

```xml
<rsp stat="ok">
  <license_history
    date_change="1733215279"
    old_license="All Rights Reserved" old_license_url="https://www.flickrhelp.com/hc/en-us/articles/10710266545556-Using-Flickr-images-shared-by-other-members"
    new_license="" new_license_url=""
  />
</rsp>
```

The timestamp `1733215279` is the date I uploaded the photo to Flickr, because that's when I set the initial license.

This is the API response after I updated the license for the first time:

```xml
<rsp stat="ok">
  <license_history
    date_change="1746095208"
    old_license="All Rights Reserved" old_license_url="https://www.flickrhelp.com/hc/en-us/articles/10710266545556-Using-Flickr-images-shared-by-other-members"
    new_license="Attribution License" new_license_url="https://creativecommons.org/licenses/by/2.0/"
  />
</rsp>
```

The new timestamp `1746095208` is the date I updated the license -- the timestamp of the original photo has now vanished from this response.
